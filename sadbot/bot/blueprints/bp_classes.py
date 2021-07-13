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

"""Blueprint for classes"""

import logging

from vkbottle.bot import Blueprint, Message

from bot import classes
from bot.classes_vocabulary import *
from bot.user_functions import OnlyRegistered, get_user

bp = Blueprint()
bp.labeler.auto_rules.append(OnlyRegistered())
bp.labeler.vbml_ignore_case = True


# TEXT MESSAGES
@bp.on.message(text=v_classes_today)
async def send_classes_today(ans: Message):
    """
    Send today classes
    """
    await ans.answer(
        classes.get_classes((await get_user(ans.peer_id)).group_peer_id, as_list=False))


@bp.on.message(text=v_classes_tomorrow)
async def send_classes_tomorrow(ans: Message):
    """
    Send tomorrow classes
    """
    await ans.answer(
        classes.get_classes((await get_user(ans.peer_id)).group_peer_id, 1,
                            as_list=False))


@bp.on.message(text=v_classes_offset)
async def send_classes_tomorrow(ans: Message, offset: int):
    """
    Send classes with offset
    """
    await ans.answer(
        classes.get_classes((await get_user(ans.peer_id)).group_peer_id, offset, as_list=False))


@bp.on.message(text=v_class_now)
async def send_class_now(ans: Message):
    """
    Send current class
    """
    await ans.answer(classes.get_class((await get_user(ans.peer_id)).group_peer_id))


@bp.on.message(text=v_class_next)
async def send_class_next(ans: Message):
    """
    Send next class
    """
    await ans.answer(classes.get_class((await get_user(ans.peer_id)).group_peer_id, 1))


@bp.on.message(text=v_current_week)
async def send_current_week(ans: Message):
    """
    Send current week
    """
    await ans.answer(classes.get_cur_week_text())


@bp.on.message(text=v_class_timetable)
async def send_timing(ans: Message):
    """
    Send timing
    """
    await ans.answer(classes.time_to_next((await get_user(ans.peer_id)).group_peer_id))
