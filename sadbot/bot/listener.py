#    Copyright 2021 Elshan Agaev
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
Event Listener
"""
import datetime
import logging
import logging.config
import random
import sys
import configparser
import asyncio

from vkbottle import GroupEventType, GroupTypes

from bot.utils import element_builders as eb
from bot import classes, teachers, exams
from bot.base_vocabulary import *
from bot.classes_vocabulary import *
from bot.teachers_vocabulary import *
from bot.user_functions import *
from bot.utils.utils import get_uptime, connect_to_database, load_sad_replies, record_stats

start_time = datetime.datetime.now()  # storing time when bot has started working. Used for stats

cp = configparser.ConfigParser()
cf = cp.read(sys.path[0] + '/config.ini', encoding='utf-8')  # Read config file
sad_bot = Bot(cp['DEFAULT']['Token'])  # Passing token from config file
sad_bot.labeler.vbml_ignore_case = True  # bot will ignore case in messages

conn = connect_to_database(sys.path[0] + cp['DEFAULT']['DatabaseName'])  # Establishing connection to database
sad_replies = load_sad_replies(conn)  # Caching random replies so we don't need to load them everytime
im: ImportantMessagesCollection = ImportantMessagesCollection()  # Object to store 'important messages'
loop: asyncio.AbstractEventLoop  # Main loop

logging.config.fileConfig(cp, disable_existing_loggers=False)  # setting up logging


@sad_bot.on.message(lev=v_start)
async def start_bot(ans: Message):
    """
    First interaction with bot ("Start" or "Начать")
    """
    logging.info(f'{ans.from_id}[{ans.peer_id}]')
    await ans.answer(r_register_help, keyboard=eb.no_kbrd)


@sad_bot.on.message(text=v_groups_list)
async def send_list_of_groups(ans: Message):
    """
    Send list of groups available
    """
    logging.info(f'{ans.from_id}[{ans.peer_id}]')
    await ans.answer(get_all_groups_formatted(conn))


@sad_bot.on.message(text=v_register)
async def send_register_result(ans: Message, group_name):
    """
    Register in database
    """
    logging.info(f'{ans.from_id}[{ans.peer_id}] tried to register in {group_name}')
    # FIX Send keyboard only when registered successfully
    r = [r_register_success, eb.kbrd] if register_user(conn, ans.peer_id, group_name) else [r_register_fail, eb.no_kbrd]
    await ans.answer(r[0].format(group_name), keyboard=r[1])


@sad_bot.on.message(OnlyRegistered(conn), text=v_keyboard_toggle)
async def send_keyboard(ans: Message, toggle):
    """
    Show/Hide keyboard
    """
    logging.info(f'{ans.from_id}[{ans.peer_id}] toggled "{toggle}"')
    if toggle == 'выкл':
        await ans.answer(r_keyboard, keyboard=eb.no_kbrd)
    elif toggle == 'вкл':
        await ans.answer(r_keyboard, keyboard=eb.kbrd)
    else:
        await ans.answer(r_keyboard_help)


@sad_bot.on.message(OnlyRegistered(conn), text=v_tutorial)
async def send_tutorial(ans: Message):
    """
    Send carousel with tutorial
    """
    logging.info(f'{ans.from_id}[{ans.peer_id}]')
    await ans.answer(r_tutorial, template=eb.crsl)


@sad_bot.on.message(OnlyRegistered(conn), text=v_alive)
async def send_uptime(ans: Message):
    """
    Send uptime
    """
    logging.info(f'{ans.from_id}[{ans.peer_id}]')
    await ans.answer(f"Uptime: {get_uptime(start_time)}")


@sad_bot.on.message(OnlyRegistered(conn), text=v_trigger)
async def send_random_reply(ans: Message):
    """
    Send random reply
    """
    logging.info(f'{ans.from_id}[{ans.peer_id}]')
    r: dict = random.choice(sad_replies)
    user = await sad_bot.api.users.get(user_ids=[ans.from_id])
    await ans.answer(
        message=r['replyText'].format(u_fn=user[0].first_name),
        attachment=r['replyAtt'],
        sticker_id=r['replySticker']
    )


@sad_bot.on.message(OnlyRegistered(conn), text=v_classes_today)
async def send_classes_today(ans: Message):
    """
    Send today classes
    """
    logging.info(f'{ans.from_id}[{ans.peer_id}]')
    await ans.answer(
        classes.get_classes(conn.cursor(), get_user(conn.cursor(), ans.peer_id).group_peer_id, as_list=False))


@sad_bot.on.message(OnlyRegistered(conn), text=v_classes_tomorrow)
async def send_classes_tomorrow(ans: Message):
    """
    Send tomorrow classes
    """
    logging.info(f'{ans.from_id}[{ans.peer_id}]')
    await ans.answer(
        classes.get_classes(conn.cursor(), get_user(conn.cursor(), ans.peer_id).group_peer_id, 1, as_list=False))


@sad_bot.on.message(OnlyRegistered(conn), text=v_classes_offset)
async def send_classes_tomorrow(ans: Message, offset: int):
    """
    Send classes with offset
    """
    logging.info(f'{ans.from_id}[{ans.peer_id}] OFFSET {offset}')
    await ans.answer(
        classes.get_classes(conn.cursor(),
                            get_user(conn.cursor(), ans.peer_id).group_peer_id, offset, as_list=False))


@sad_bot.on.message(OnlyRegistered(conn), text=v_class_now)
async def send_class_now(ans: Message):
    """
    Send current class
    """
    logging.info(f'{ans.from_id}[{ans.peer_id}]')
    await ans.answer(classes.get_class(conn.cursor(), get_user(conn.cursor(), ans.peer_id).group_peer_id))


@sad_bot.on.message(OnlyRegistered(conn), text=v_class_next)
async def send_class_next(ans: Message):
    """
    Send next class
    """
    logging.info(f'{ans.from_id}[{ans.peer_id}]')
    await ans.answer(classes.get_class(conn.cursor(), get_user(conn.cursor(), ans.peer_id).group_peer_id, 1))


@sad_bot.on.message(OnlyRegistered(conn), text=v_current_week)
async def send_current_week(ans: Message):
    """
    Send current week
    """
    logging.info(f'{ans.from_id}[{ans.peer_id}]')
    await ans.answer(classes.get_cur_week_text())


@sad_bot.on.message(OnlyRegistered(conn), text=v_class_timetable)
async def send_timing(ans: Message):
    """
    Send timing
    """
    logging.info(f'{ans.from_id}[{ans.peer_id}]')
    await ans.answer(classes.time_to_next(conn.cursor(), get_user(conn.cursor(), ans.peer_id).group_peer_id))


@sad_bot.on.message(OnlyRegistered(conn), text=v_teacher_add)
async def send_teacher_add(ans: Message, add_req):
    """
    Add teacher
    """
    logging.info(f'{ans.from_id}[{ans.peer_id}] ADDS {add_req}')
    await ans.answer(teachers.add_teacher(conn, add_req, ans.from_id))


@sad_bot.on.message(OnlyRegistered(conn), text=v_teacher_find)
async def send_teacher_find(ans: Message, find_req):
    """
    Find teacher
    """
    logging.info(f'{ans.from_id}[{ans.peer_id}] FINDS {find_req}')
    await ans.answer(teachers.find_teacher(conn.cursor(), find_req))


@sad_bot.on.message(OnlyRegistered(conn), text=v_teacher_delete)
async def send_teacher_delete(ans: Message, del_req):
    """
    Delete teacher
    """
    logging.info(f'{ans.from_id}[{ans.peer_id}] DELETES {del_req}')
    await ans.answer(teachers.delete_teacher(conn, del_req, ans.from_id))


@sad_bot.on.message(OnlyRegistered(conn), text=v_closest_exam)
async def send_exam_closest(ans: Message):
    """
    Closest exam
    """
    logging.info(f'{ans.from_id}[{ans.peer_id}]')
    await ans.answer(exams.get_next_exam(
        group=get_user(conn.cursor(), ans.peer_id).group_peer_id,
        limit=1,
        cur=conn.cursor()
    ))


@sad_bot.on.message(OnlyRegistered(conn), text=v_closest_exam_with_limit)
async def send_exam_closest_with_limit(ans: Message, limit):
    """
    Closest exam
    """
    logging.info(f'{ans.from_id}[{ans.peer_id}] {limit}')
    await ans.answer(exams.get_next_exam(
        group=get_user(conn.cursor(), ans.peer_id).group_peer_id,
        limit=limit,
        cur=conn.cursor()
    ))


@sad_bot.on.chat_message(OnlyRegistered(conn), text=v_important)
async def send_important_message(ans: Message, imp_message: str = None):
    """
    Send important message
    """
    logging.info(f'{ans.from_id}[{ans.peer_id}] MESSAGE {imp_message}')
    res = im.add_new_important_message(peer_id=ans.peer_id, text=imp_message)
    await ans.answer(res[0], keyboard=res[1])


@sad_bot.on.message(OnlyAdmin(conn), text='/stop')
async def stop_bot(ans: Message):
    """
    Stop bot, record stats to database and finally close connection to database
    """
    global loop
    logging.info(f'{ans.from_id}[{ans.peer_id}]')
    await asyncio.gather(ans.answer('done'),
                         record_stats(conn, (datetime.datetime.now() - start_time).seconds))
    conn.close()
    loop.stop()


async def decider(ans: GroupTypes.MessageEvent):
    """
    Reacts to events by checking payloads

    :param ans:
    """
    payload = ans.object.payload
    event_data = None
    group_uid = get_user(conn.cursor(), ans.object.peer_id).group_peer_id
    peer_id = ans.object.peer_id

    logging.info(f'{ans.object.user_id}[{peer_id}] PAYLOAD {payload}')

    if payload == eb.bt_cl_td.payload:
        await sad_bot.api.messages.send(
            message=classes.get_classes(conn.cursor(), group_uid, as_list=False),
            peer_id=peer_id,
            random_id=get_random()
        )
    elif payload == eb.bt_cl_tmrw.payload:
        await sad_bot.api.messages.send(
            message=classes.get_classes(conn.cursor(), group_uid, 1, False),
            peer_id=peer_id,
            random_id=get_random()
        )
    elif payload == eb.bt_cl_now.payload:
        event_data = await eb.sb_builder(classes.get_class(conn.cursor(), group_uid))
    elif payload == eb.bt_cl_next.payload:
        event_data = await eb.sb_builder(classes.get_class(conn.cursor(), group_uid, 1))
    elif payload == eb.bt_week.payload:
        event_data = await eb.sb_builder(classes.get_cur_week_text())
    elif payload == eb.bt_timetable.payload:
        event_data = await eb.sb_builder(classes.time_to_next(conn.cursor(), group_uid))
    elif payload == eb.bt_exam.payload:
        event_data = await eb.sb_builder(exams.get_next_exam(group_uid, 1, conn.cursor()))
    elif peer_id in im.all:
        if payload['bt_id'] == im.all[peer_id].payload:
            event_data = await eb.sb_builder(
                await im.imp(
                    sad_bot,
                    ans.object.user_id,
                    peer_id,
                    ans.object.conversation_message_id
                )
            )
        else:
            event_data = await eb.sb_builder(r_important_not_last)

    await sad_bot.api.messages.send_message_event_answer(ans.object.event_id, ans.object.user_id, peer_id, event_data)


@sad_bot.on.raw_event(GroupEventType.MESSAGE_EVENT, dataclass=GroupTypes.MessageEvent)
async def handle_message_event(event: GroupTypes.MessageEvent):
    """
    Callback buttons listener
    """
    await decider(event)


def start_listening():
    """
    Start listening to events. Will work non-stop
    """
    # We need our own loop to have full control and be able to stop bot (check stop_bot function)
    global loop
    loop = asyncio.get_event_loop()
    loop.create_task(sad_bot.run_polling())
    loop.run_forever()
