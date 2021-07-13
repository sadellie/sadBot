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

"""Blueprint for teachers"""

import logging

from vkbottle.bot import Blueprint, Message

from bot import teachers
from bot.user_functions import OnlyRegistered
from bot.teachers_vocabulary import *

bp = Blueprint()
bp.labeler.auto_rules.append(OnlyRegistered())
bp.labeler.vbml_ignore_case = True


@bp.on.message(text=v_teacher_add)
async def send_teacher_add(ans: Message, add_req):
    """
    Add teacher
    """
    await ans.answer(teachers.add_teacher(add_req, ans.from_id))


@bp.on.message(text=v_teacher_find)
async def send_teacher_find(ans: Message, find_req):
    """
    Find teacher
    """
    await ans.answer(teachers.find_teacher(find_req))


@bp.on.message(text=v_teacher_delete)
async def send_teacher_delete(ans: Message, del_req):
    """
    Delete teacher
    """
    await ans.answer(teachers.delete_teacher(del_req, ans.from_id))
