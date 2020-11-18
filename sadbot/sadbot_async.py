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
Event Listener
"""
import datetime
import logging
import random

import vbml
from vkbottle import GroupEventType, GroupTypes

import config
import utils.element_builders as eb
from sadbot import classes, teachers
from sadbot.base_vocabulary import *
from sadbot.classes_vocabulary import *
from sadbot.teachers_vocabulary import *
from sadbot.user_functions import *
from utils.utils import get_uptime, connect_to_database, load_sad_replies

sad_bot = Bot(config.token)
sad_bot.labeler.vbml_ignore_case = True
logging.basicConfig(level=logging.DEBUG)
start_time = datetime.datetime.now()

conn = connect_to_database()
sad_replies = load_sad_replies(conn)
im: ImportantMessagesCollection = ImportantMessagesCollection()
patcher = vbml.Patcher()


# class MyRule:
#     def __init__(self):
#


@sad_bot.on.message(text=v_start)
async def start_bot(ans: Message):
    """
    First interaction with bot ("Start" or "Начать")
    """
    await ans.answer(r_register_help, keyboard=eb.no_kbrd)


@sad_bot.on.message(text=v_groups_list)
async def send_list_of_groups(ans: Message):
    """
    Send list of groups available
    """
    await ans.answer(get_all_groups_formatted(conn))


@sad_bot.on.message(text=v_register)
async def send_register_result(ans: Message, group_name):
    """
    Register in database
    """
    await ans.answer(register_user(conn, ans.peer_id, group_name))


@sad_bot.on.message(OnlyRegistered(conn), text=v_keyboard_toggle)
async def send_keyboard(ans: Message, toggle):
    """
    Show/Hide keyboard
    """

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
    await ans.answer(r_tutorial, template=eb.crsl)


@sad_bot.on.message(OnlyRegistered(conn), text=v_alive)
async def send_uptime(ans: Message):
    """
    Send uptime
    """
    await ans.answer(f"Uptime: {get_uptime(start_time)}")


@sad_bot.on.message(OnlyRegistered(conn), text=v_trigger)
async def send_random_reply(ans: Message):
    """
    Send random reply
    """
    r: dict = random.choice(sad_replies)
    await ans.answer(
        message=r['replyText'].format(u_fn='TODO'),
        attachment=r['replyAtt'],
        sticker_id=r['replySticker']
    )


@sad_bot.on.message(OnlyRegistered(conn), text=v_classes_today)
async def send_classes_today(ans: Message):
    """
    Send today classes
    """
    await ans.answer(
        classes.get_classes(conn.cursor(), get_user(conn.cursor(), ans.from_id).group_peer_id, as_list=False))


@sad_bot.on.message(OnlyRegistered(conn), text=v_classes_tomorrow)
async def send_classes_tomorrow(ans: Message):
    """
    Send tomorrow classes
    """
    await ans.answer(
        classes.get_classes(conn.cursor(), get_user(conn.cursor(), ans.from_id).group_peer_id, 1, as_list=False))


@sad_bot.on.message(OnlyRegistered(conn), text=v_classes_today)
async def send_class_now(ans: Message):
    """
    Send current class
    """
    await ans.answer(classes.get_class(conn.cursor(), get_user(conn.cursor(), ans.from_id).group_peer_id))


@sad_bot.on.message(OnlyRegistered(conn), text=v_class_now)
async def send_class_now(ans: Message):
    """
    Send current class
    """
    await ans.answer(classes.get_class(conn.cursor(), get_user(conn.cursor(), ans.from_id).group_peer_id))


@sad_bot.on.message(OnlyRegistered(conn), text=v_class_next)
async def send_class_next(ans: Message):
    """
    Send next class
    """
    await ans.answer(classes.get_class(conn.cursor(), get_user(conn.cursor(), ans.from_id).group_peer_id, 1))


@sad_bot.on.message(OnlyRegistered(conn), text=v_current_week)
async def send_current_week(ans: Message):
    """
    Send current week
    """
    await ans.answer(classes.get_cur_week_text())


@sad_bot.on.message(OnlyRegistered(conn), text=v_class_timetable)
async def send_timing(ans: Message):
    """
    Send timing
    """
    await ans.answer(classes.time_to_next(conn.cursor(), get_user(conn.cursor(), ans.from_id).group_peer_id))


@sad_bot.on.message(OnlyRegistered(conn), text=v_teacher_add)
async def send_teacher_add(ans: Message, add_req):
    """
    Add teacher
    """
    await ans.answer(teachers.add_teacher(conn, add_req, ans.from_id))


@sad_bot.on.message(OnlyRegistered(conn), text=v_teacher_find)
async def send_teacher_find(ans: Message, find_req):
    """
    Find teacher
    """
    await ans.answer(teachers.find_teacher(conn.cursor(), find_req))


@sad_bot.on.message(OnlyRegistered(conn), text=v_teacher_delete)
async def send_teacher_delete(ans: Message, del_req):
    """
    Delete teacher
    """
    await ans.answer(teachers.delete_teacher(conn, del_req, ans.from_id))


@sad_bot.on.chat_message(OnlyRegistered(conn), text=v_important)
async def send_important_message(ans: Message, imp_message: str = None):
    """
    Send important message
    """
    res = im.add_new_important_message(peer_id=ans.peer_id, text=imp_message)
    await ans.answer(res[0], keyboard=res[1])


async def decider(ans: GroupTypes.MessageEvent):
    """
    Reacts to events by checking payloads

    :param ans:
    """
    payload = ans.object.payload
    event_data = None
    group_uid = get_user(conn.cursor(), ans.object.user_id).group_peer_id
    peer_id = ans.object.peer_id
    print(payload)
    print(eb.bt_week.payload)

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
    elif peer_id in im.all:
        if payload == im.all[peer_id].payload:
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

    await sad_bot.api.messages.send_message_event_answer(
        ans.object.event_id,
        ans.object.user_id,
        peer_id,
        event_data
    )


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
    sad_bot.run_forever()
