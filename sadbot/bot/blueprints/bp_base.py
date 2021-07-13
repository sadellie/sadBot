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

"""Basic Blueprint"""

import asyncio
import logging
import random
import time
import aiohttp

from vkbottle import BaseMiddleware
from vkbottle.bot import Blueprint, Message
from vkbottle.dispatch.handlers import FromFuncHandler
from vkbottle.dispatch.rules.bot import ChatActionRule, AttachmentTypeRule
from vkbottle.tools.dev_tools.mini_types.bot import MessageMin
from vkbottle_types.objects import MessagesMessageAttachment

from bot.base import db, club_id, stats, dd
from bot.base_vocabulary import *
from bot.classes_vocabulary import *
from bot.exams_vocabulary import *
from bot.teachers_vocabulary import *
from bot.user_functions import (OnlyRegistered, BannedRule, OnlyAdmin,
                                get_all_groups_formatted, register_user, get_group_by_user, get_user, UserClass,
                                GroupClass)
from bot.utils.utils import get_uptime, record_stats, load_sad_replies, update_schedule, update_name
from bot.utils.vk_elements import kbrd, no_kbrd, crsl

bp = Blueprint()


class LogsAndStats(BaseMiddleware):
    """Middleware for logging and stats"""
    async def post(self,
                   event,
                   view,
                   handle_responses,
                   handlers: list):
        if isinstance(event, MessageMin) and handlers:
            if event.text and isinstance(handlers[0], FromFuncHandler):
                name = handlers[0].handler.__name__
                logging.info(f'{event.from_id}[{event.peer_id}] - {name} - {event.text}')
                stats.mincr()  # Group joins included and other events


bp.labeler.vbml_ignore_case = True
bp.labeler.message_view.register_middleware(LogsAndStats())

ban_rule = BannedRule()
reg_rule = OnlyRegistered()
random_replies = load_sad_replies(db)

all_commands = r_commands.format('\n'.join(i.replace('<!>', '')
                                           for i in [*v_start, *v_groups_list, v_req,
                                                     v_group_my, v_register, '/upd', v_group_rename,
                                                     v_keyboard_toggle, v_tutorial, v_commands, v_alive, v_trigger,
                                                     v_classes_today, v_classes_tomorrow, v_class_now, v_class_next,
                                                     v_current_week, v_class_timetable,
                                                     *v_teacher_add, *v_teacher_delete, *v_teacher_find,
                                                     *v_exam_add, *v_exam_delete, v_closest_exam,
                                                     v_closest_exam_with_limit,
                                                     v_kill, v_run_script]
                                           ),
                                 r_link)


async def run_me(p: str, m: Message):
    a = await asyncio.create_subprocess_shell(p, stdout=asyncio.subprocess.PIPE)
    await a.wait()
    stdout, stderr = await a.communicate()
    await m.answer(stdout.decode() if stdout else stderr.decode())


@bp.on.message(ChatActionRule("chat_invite_user"))
async def react_join(a: Message):
    """
    React to bot being added to chat
    """
    if a.action.member_id == club_id:
        await a.answer(r_register_help)
        stats.jincr()


@bp.on.message(ban_rule, lev=v_start)
async def start_bot(ans: Message):
    """
    First interaction with bot ("Start" or "Начать")
    """
    await ans.answer(r_register_help)


@bp.on.message(ban_rule, text=v_groups_list)
async def send_list_of_groups(ans: Message):
    """
    Send list of groups available
    """
    await ans.answer(r_groups_list.format(get_all_groups_formatted()))


@bp.on.message(ban_rule, text=v_register)
async def send_register_result(ans: Message, group_name):
    """
    Register in database
    """
    e = register_user(ans.peer_id, group_name)
    r = [r_register_success, kbrd] if e else [r_register_fail, None]
    await ans.answer(r[0].format(e), keyboard=r[1])


@bp.on.message(ban_rule, text=v_group_my)
async def send_my_group(ans: Message):
    """Sends your group"""
    g = await get_group_by_user(ans.peer_id)
    await ans.answer(r_group_my_template.format(g.name) if g else r_group_my_none)


@bp.on.message(reg_rule, text=v_keyboard_toggle)
async def send_keyboard(ans: Message, toggle):
    """
    Show/Hide keyboard
    """
    if toggle == 'выкл':
        await ans.answer(r_keyboard_success, keyboard=no_kbrd)
    elif toggle == 'вкл':
        await ans.answer(r_keyboard_success, keyboard=kbrd)
    else:
        await ans.answer(r_keyboard_help)


@bp.on.message(ban_rule, text=v_tutorial)
async def send_tutorial(ans: Message):
    """
    Send carousel with tutorial
    """
    await ans.answer(r_tutorial, template=crsl)


@bp.on.message(text=v_commands)
async def send_commands(ans: Message):
    """
    Send all available commands
    """
    await ans.answer(all_commands)


@bp.on.message(reg_rule, text=v_alive)
async def send_uptime(ans: Message):
    """
    Send uptime
    """
    await ans.answer(r_alive.format(
        get_uptime(stats.start_time),
        stats.u,
        stats.m + 1 + stats.j + stats.c,
        stats.m + 1,
        stats.c,
        stats.j,
        round(time.time() - ans.date + stats.offset_time, 2)
    ))


@bp.on.message(reg_rule, text=v_trigger)
async def send_random_reply(ans: Message):
    """
    Send random reply
    """
    r: dict = random.choice(random_replies)
    await ans.answer(
        message=r['replyText'],
        attachment=r['replyAtt'],
        sticker_id=r['replySticker']
    )


@bp.on.message(OnlyAdmin(), text=v_kill)
async def stop_bot(ans: Message):
    """
    Stop bot, record stats to database and finally close connection to database
    """
    await asyncio.gather(ans.answer('done'),
                         record_stats(db,
                                      stats))
    db.close()
    bp.loop.stop()


@bp.on.message(OnlyAdmin(), text=v_run_script)
async def run_scripts(ans: Message, path):
    """Run custom script"""
    # Since this operation may take a while, we create a task, so we can continue listening to event
    bp.loop.create_task(run_me(path, ans))


@bp.on.message(ban_rule, text=v_req)
async def register_req(ans: Message):
    m = ans.attachments[0].doc.url if ans.attachments else ''
    await bp.api.messages.send(user_id=41163756,
                               random_id=0,
                               message=f'{ans.text} {m}')

    await ans.answer('🤖 Переслал ваше сообщение админу.')


@bp.on.message((reg_rule, AttachmentTypeRule('doc')), text='/upd')
async def updater(ans: Message):
    """Command to update a schedule"""
    u: UserClass = await get_user(ans.peer_id)
    g: GroupClass = await get_group_by_user(ans.peer_id)
    att = ans.attachments[0]

    if u.user_id == g.admin_id:
        if att.doc.ext == 'xls':
            async with aiohttp.ClientSession() as session:
                d = await session.get(att.doc.url)
                p = dd + f'/group{u.group_peer_id}.' + att.doc.ext
                f = open(p, 'wb')
                c = await d.content.read()
                f.write(c)
                f.close()
                try:
                    r = update_schedule(db, p, g.group_id)  # None means that there are no errors, OK
                except Exception as e:
                    logging.error(e)
                    await ans.answer(r_sch_fail)
                await ans.answer(
                    r_sch_fail.format(r) if r else r_sch_success.format(g.name))
        else:
            await ans.answer(r_not_xls)
    else:
        await ans.answer(r_sch_access.format(g.name))


@bp.on.message(reg_rule, text=v_group_rename)
async def updater(ans: Message, name: str):
    """Command to update a schedule"""
    u: UserClass = await get_user(ans.peer_id)
    g: GroupClass = await get_group_by_user(ans.peer_id)

    if u.user_id == g.admin_id:
        update_name(db, g.group_id, name)
        await ans.answer(r_group_rename_success)
    else:
        await ans.answer(r_sch_access.format(g.name))
