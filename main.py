#    Copyright 2020 Elshan Agaev
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

"""
Main file. Run this thingy and bot will be alive.
Don't forget to configure config.py file.
Arguments:
    --full will enable additional functions, but they are buggy not necessary
"""
import datetime
import random
import sqlite3
import sys

from os.path import dirname
from vk_api.bot_longpoll import VkBotEventType

from vocabulary import *
from schedule import classes
from vk_methods import *
import element_builders as eb
import teachers
import user_functions as uf

# TODO Stats
# Path to this file (main.py). Used by different functions so they know where to read/write files
directory = dirname(__file__)

# Arguments passed
arguments = sys.argv
print(arguments)
full_mode = False  # Full mode == more functions available (not necessary at all)
if "--full" in arguments:
    print("Full mode")
    full_mode = True
    from schedule import pandasfunctions as pf, checker
    from image_generator import imgen
else:
    print("Lite mdoe")


# Carousel
carousel = eb.carousel
# Uptime
start_time = datetime.datetime.now()
e_counter = 0


def get_uptime():
    """
    Get current uptime

    :return: Formatted string DD:HH:MM:SS (for example, 13:20:17:25)
    """
    current_time = datetime.datetime.now()
    uptime: datetime.timedelta = current_time - start_time
    days = uptime.days
    hours = uptime.seconds // 3600
    minutes = uptime.seconds // 60 % 60
    seconds = uptime.seconds % 60
    return "{d:02}:{h:02}:{m:02}:{s:02}".format(d=days, h=hours, m=minutes, s=seconds)


# Database setup
def custom_factory(cursor, row):
    """
    Custom factory, makes working with database operations results easier

    :param cursor: Database Cursor
    :param row: Row, idk...
    :return: Dictionary
    """
    cf = {}
    for i, x in enumerate(cursor.description):
        cf[x[0]] = row[i]
    return cf


conn = sqlite3.connect(directory + '/databases/sadBot2.sqlite')
conn.row_factory = custom_factory
cur = conn.cursor()

# Админы и старосты, int для сравнения в функции
v_admins = uf.get_user(cur, only_admin_ids=True)
sad_replies = cur.execute("SELECT * FROM sad_replies").fetchall()

print("Admins: " + str(v_admins))

imp_r_pl = {}  # IMPORTANT PAYLOAD
imp_m = {}  # IMPORTANT MESSAGE TEXT
imp_u = {}  # IMPORTANT USERS WHO CLICKED THE BUTTON


def imp(user_id, peer_id, message_id):
    """
    IMPORTANT function. Reacts to button clicks.

    :param user_id: User_id (who clicked)
    :param peer_id: Chat peer_id (where it was clicked)
    :param message_id: Message_id (which message was clicked and will be edited)
    :return: Result
    """
    global imp_r_pl, imp_m, imp_u
    p_str = str(peer_id)
    if user_id in imp_u[p_str]:  # Check if user has already clicked the button
        return "Ты уже нажимал, хватит 😡"
    else:  # User has never clicked this button
        u_info = get_user_info(user_id)  # Info about user

        # Adding user name to the end of the message
        message_local = imp_m[p_str] + "\n" + u_info['first_name'] + " " + u_info['last_name'][0] + "."
        imp_m.update({p_str: message_local})  # Updating latest version of the edited message
        users_local = imp_u[p_str] + [user_id]
        imp_u.update({p_str: users_local})  # Updating list of users who clicked the button

        # Finally we can edit the message
        vk.messages.edit(
            peer_id=peer_id,
            message=message_local,
            conversation_message_id=message_id,
            keyboard=eb.json_converter(eb.kb_imp_builder(imp_r_pl[p_str])))
        return "Принято 👍"


# FIXME Broken for some reason
def update_schedule(priv_att, priv_peer):
    """
    Update schedule in database

    :param priv_att: attachment_id of file that will be used (Excel-file)
    :param priv_peer: Chat peer (where to send the result of this operation)
    """
    admin: uf.UserClass = uf.get_user(cur, str(priv_peer))
    result: str = ""  # Message that will be sent
    if len(priv_att) > 0:  # Checking for attachments
        att = priv_att[0]  # Picking first attachment
        if att['type'] == 'doc':  # Checking for file attachment file (must be doc, not photo or something else)
            url = att['doc']['url']  # It's document, getting download url
            check = checker.check_sheet(url, str(admin.group_peer_id) + ".xlsx")  # Checking downloaded file
            if check == "OK RESULT":
                try:  # File is OK, now let's try to update schedule
                    pf.add_table(
                        table_name=admin.group_peer_id,
                        file=requests.get(url),
                        db=conn)  # FIXME Throws exception here. File path problem?
                    result = "Расписание обновлено, ошибок не выявлено"  # Good ending
                except Exception as add_table_error:
                    result = "main.py Ошибка при добавлении файла " + str(add_table_error)  # Bad ending
                    print(result)
            else:  # File has is not correct
                result = check
    send_message(result)  # Sending result to user


def main_chat_listener(event):
    """
    React to user messages (group and private chats)

    :param event: Event in chat (MESSAGE_NEW)
    """
    global imp_r_pl, imp_m, imp_u

    u_id = event.message.from_id  # User id
    text_unf = event.message.text  # Unformatted text of the message
    text = text_unf.lower()  # Lowered message so 'in' function will work
    chat_peer = str(event.message.peer_id)  # Chat peer_id

    # First interaction with bot ("Start" or "Начать")
    if text in v_start:
        send_message(
            peer_id=chat_peer,
            message=r_register_help,
            keyboard=eb.no_kb)

    # Send list of groups available
    if text == v_groups_list:
        all_group_names = uf.get_all_groups(cur)[1]
        message = ""
        for index, group in enumerate(all_group_names):
            message = message + str(index + 1) + "." + " " + group + "\n"
        send_message(peer_id=chat_peer, message=message)

    # Updating schedule. Never used, but works correctly
    # Checking for admin privileges
    # if priv_chat_text == "/обновить":
    #     if str(priv_chat_peer) in v_admins and full_mode:
    #         update_schedule(priv_att, priv_chat_peer)
    #     else:
    #         send_message(
    #             peer_id=priv_chat_peer,
    #             message="Бот работает в light режиме, обновление/добавление расписаний отключено"
    #         )

    if text_unf[0:7] == v_register:
        group_name = text_unf[8:]
        all_groups = uf.get_all_groups(cur)
        all_group_names = all_groups[1]
        all_group_ids = all_groups[0]
        if group_name in all_group_names:
            index = all_group_names.index(group_name)
            uf.register_user(
                db=conn,
                cur=cur,
                user_id=str(chat_peer),
                group_uid=all_group_ids[index],
                group_name=group_name
            )
            send_message(chat_peer, r_register_success.format(g=group_name), keyboard=eb.kb)
        else:
            send_message(chat_peer, r_register_fail)

    user: uf.UserClass = uf.get_user(cur, chat_peer)
    if user is None:  # None means user is not in database, exit function
        return None
    else:
        group_uid = str(user.group_peer_id)

    # Removing mention from message text
    if text[0:23] == config.mention:
        text = text[24:]

    # FIXME Not working / Waiting for VK API update
    # if text == "+++":
    #     print("Нажали на +++")
    #     imp(u_id, group_uid, m_id)

    # Show keyboard
    if text in v_keyboard_show:
        send_message(
            peer_id=chat_peer,
            message=r_keyboard,
            keyboard=eb.kb)

    # Hide Keyboard
    elif text in v_keyboard_hide:
        send_message(
            peer_id=chat_peer,
            message=r_keyboard,
            keyboard=eb.no_kb)

    # Send carousel with tutorial
    elif any(i in text for i in v_tutorial):
        send_message(
            peer_id=chat_peer,
            message=r_tutorial,
            template=carousel)

    # Send uptime and error counter
    elif any(i in text for i in v_alive):
        uptime = get_uptime()
        if full_mode:
            photo = imgen.generate_photo(
                t1="Current uptime:",
                t2=uptime,
                filename=chat_peer
            )
            send_message(
                peer_id=chat_peer,
                attachments=save_photo_to_vk(photo)
            )
        else:
            send_message(chat_peer, "Uptime: " + str(uptime) + "\n" + "errors: " + str(e_counter))
    # Send random reply
    elif any(i in text for i in v_trigger):
        r = random.choice(sad_replies)
        rt = r['replyText'].format(u_fn=get_user_info(str(u_id))['first_name'])
        ra = r['replyAtt']
        rs = r['replySticker']
        send_message(chat_peer, rt, attachments=ra, sticker_id=rs)

    # Send today classes
    elif any(i in text for i in v_classes_today):
        print("uid" + str(group_uid))
        send_message(chat_peer, classes.get_classes(cur, group_uid, as_list=False))

    # Send tomorrow classes
    elif any(i in text for i in v_classes_tomorrow):
        send_message(chat_peer, classes.get_classes(cur, group_uid, 1, as_list=False))

    # Send current class
    elif any(i in text for i in v_class_now):
        print("uid" + str(group_uid))
        send_message(chat_peer, classes.get_class(cur, group_uid))

    # Send next class
    elif any(i in text for i in v_class_next):
        send_message(chat_peer, classes.get_class(cur, group_uid, 1))

    # Add teacher
    elif text[0:7] == v_teacher_add:
        send_message(
            peer_id=chat_peer,
            message=teachers.add_teacher(
                cur=cur,
                db=conn,
                req=text_unf,
                user_id=user.user_id)
        )

    # Delete teacher
    elif text[0:6] == v_teacher_delete:
        send_message(chat_peer, teachers.delete_teacher(cur, conn, text_unf, user.user_id))

    # Find teacher
    elif text[0:7] == v_teacher_find:
        send_message(chat_peer, teachers.find_teacher(cur, text_unf))

    # Send find teacher help
    elif text in v_teacher_find_help:
        send_message(chat_peer, r_teacher_find_help)

    # Send add teacher help
    elif text in v_teacher_add_help:
        send_message(chat_peer, r_teacher_add_help)

    # Send delete teacher help
    elif text in v_teacher_delete_help:
        send_message(chat_peer, r_teacher_delete_help)

    # Send current week
    elif any(i in text for i in v_current_week):
        send_message(chat_peer, classes.get_cur_week_text())

    # Send important message
    elif text[0:6] == v_important and int(user.user_id) > 2000000000:
        print("text is " + text)
        message = r_important_template.format(m=text_unf[7:])
        print(message)
        r_pl = str(get_random())
        users = []

        imp_m.update({chat_peer: message})
        imp_r_pl.update({chat_peer: str(r_pl)})
        imp_u.update({chat_peer: users})

        send_message(
            peer_id=chat_peer,
            message=imp_m[chat_peer],
            keyboard=eb.json_converter(
                eb.kb_imp_builder(
                    r_pl)))

        print(imp_m)
        print(imp_u)
        print(imp_r_pl)


def payload_listener(event):
    """
    Payload listener for callback-buttons

    :param event: Event (button click)
    """
    global imp_r_pl, imp_m, imp_u
    bt_id = event.object.payload['bt_id']  # Payload of the clicked button
    group_uid = event.object.peer_id  # Group id
    chat_peer = group_uid  # Peer_id
    try:
        group_uid = str(uf.get_user(cur, group_uid).group_peer_id)
    except:
        # User is not registered, but smh got keyboard
        return None

    user_id = event.object.user_id  # User id
    event_id = event.object.event_id  # Event id
    message_id = event.object.conversation_message_id  # Message id
    ed = "0"  # Text for Snackbar

    print(bt_id)

    if bt_id == eb.bt_cl_td.payload:  # Today classes
        send_message(chat_peer, classes.get_classes(cur, group_uid, as_list=False))

    elif bt_id == eb.bt_cl_tmrw.payload:  # Tomorrow classes
        send_message(chat_peer, classes.get_classes(cur, group_uid, 1, as_list=False))

    elif bt_id == eb.bt_cl_now.payload:  # Current class
        ed = eb.sb_builder(classes.get_class(cur, group_uid))

    elif bt_id == eb.bt_cl_next.payload:  # Next class
        ed = eb.sb_builder(classes.get_class(cur, group_uid, 1))

    elif bt_id == eb.bt_search_tutorial.payload:  # Find teacher help
        ed = eb.sb_builder(r_teacher_find_help)

    elif bt_id == eb.bt_week.payload:  # Current week
        ed = eb.sb_builder(classes.get_cur_week_text())
    else:
        try:  # IMPORTANT.
            if bt_id == imp_r_pl[str(chat_peer)]:  # Green inline button (in important message)
                ed = eb.sb_builder(imp(user_id=user_id, peer_id=chat_peer, message_id=message_id))
        except:
            ed = eb.sb_builder(r_important_dead_payload)
            pass

    vk.messages.sendMessageEventAnswer(
        peer_id=chat_peer,
        user_id=user_id,
        event_id=event_id,
        # ed will be 0 just to stop spinning animation
        # TODO event_data is optional, don't use 0 as workaround
        event_data=ed)


def start_listening():
    """
    Listening to ALL events

    Слушает события и реагирует на них
    """
    print("Started listening:")
    for event in longpoll.listen():
        # print(event)
        # print("STARTED AT" + str(event.type) + " " +  str(datetime.datetime.now()))

        # Listening to callback buttons
        if event.type == "message_event":
            payload_listener(event)

        # Chat message
        elif event.type == VkBotEventType.MESSAGE_NEW:
            main_chat_listener(event)

        # print("ENDED AT " + str(datetime.datetime.now()))


if __name__ == "__main__":
    while True:
        try:
            print("LOOP")
            start_listening()
        except Exception as exception:
            e_counter += 1
            print("EXCEPTION!!!")
            print(datetime.datetime.now())
            print(exception)
            time.sleep(65)
