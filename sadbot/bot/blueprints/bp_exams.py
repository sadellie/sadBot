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

"""Blueprint for exams"""

import logging

from vkbottle.bot import Blueprint, Message

from bot import exams
from bot.exams_vocabulary import *
from bot.user_functions import OnlyRegistered

bp = Blueprint()
bp.labeler.auto_rules.append(OnlyRegistered())
bp.labeler.vbml_ignore_case = True


@bp.on.message(text=v_closest_exam)
async def send_exam_closest(ans: Message):
    """
    Closest exam
    """
    await ans.answer(await exams.get_next_exam(ans.peer_id, 1))


@bp.on.message(text=v_closest_exam_with_limit)
async def send_exam_closest_with_limit(ans: Message, limit):
    """
    Closest exam
    """
    await ans.answer(await exams.get_next_exam(ans.peer_id, limit))


@bp.on.message(text=v_exam_add)
async def send_exam_add(ans: Message, add_req):
    """
    Add exam
    """
    await ans.answer(await exams.add_exam(add_req, ans.peer_id))


@bp.on.message(text=v_exam_delete)
async def send_exam_delete(ans: Message, del_req):
    """
    Delete exam
    """
    await ans.answer(await exams.delete_exam(del_req, ans.peer_id))
