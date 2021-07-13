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

"""Blueprint for keyboard"""

import logging

from vkbottle.bot import Blueprint
from vkbottle_types.events import GroupEventType, MessageEvent

from bot import classes, exams
from bot.base import stats
from bot.user_functions import get_user
from bot.utils.vk_elements import (bt_cl_td, bt_cl_tmrw,
                                   bt_cl_now, bt_cl_next,
                                   bt_week, bt_timetable, bt_exam,
                                   sb_builder)

bp = Blueprint()


# KEYBOARD
@bp.on.raw_event(GroupEventType.MESSAGE_EVENT, MessageEvent)
async def react(m: MessageEvent):
    """
    Reacts to callback buttons
    """
    logging.info(f'{m.object.user_id}[{m.object.peer_id}] PAYLOAD {m.object.payload}')
    pl = m.object.payload
    p_id = m.object.peer_id
    e = None  # Event data
    u = await get_user(p_id)  # Cannot be None since user gets keyboard after being added to local database
    g = None
    if u is None:
        e = await sb_builder('❗ Зарегистрируйтесь.\nКоманда со списком групп: /группы')
        await bp.api.messages.send_message_event_answer(m.object.event_id, m.object.user_id,
                                                    m.object.peer_id, e)
        stats.cincr()
        return
    elif u.is_banned:
        return
    g = u.group_peer_id  # Just to make things shorter
    if pl == bt_cl_td.payload:
        await bp.api.messages.send(
            peer_id=m.object.peer_id,
            message=classes.get_classes(g, as_list=False),
            random_id=0)  # Random ID can be 0 for bots
    elif pl == bt_cl_tmrw.payload:
        await bp.api.messages.send(
            peer_id=m.object.peer_id,
            message=classes.get_classes(g, 1, as_list=False),
            random_id=0)
    elif pl == bt_cl_now.payload:
        e = await sb_builder(classes.get_class(g))
    elif pl == bt_cl_next.payload:
        e = await sb_builder(classes.get_class(g, 1))
    elif pl == bt_week.payload:
        e = await sb_builder(classes.get_cur_week_text())
    elif pl == bt_timetable.payload:
        e = await sb_builder(classes.time_to_next(g))
    elif pl == bt_exam.payload:
        e = await sb_builder(await exams.get_next_exam(m.object.peer_id, 1))
    await bp.api.messages.send_message_event_answer(m.object.event_id, m.object.user_id,
                                                    m.object.peer_id, e)
    stats.cincr()
