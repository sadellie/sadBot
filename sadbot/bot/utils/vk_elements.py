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

"""VK Elements"""

import json

from vkbottle import Keyboard, Callback, KeyboardButtonColor,  TemplateElement, template_gen

from bot.base_vocabulary import r_link
from bot.classes_vocabulary import *
from bot.exams_vocabulary import *

bt_cl_td = Callback(label=v_classes_today[3:], payload={'bt_id': 'today'})
bt_cl_tmrw = Callback(label=v_classes_tomorrow[3:], payload={'bt_id': 'tomorrow'})
bt_cl_now = Callback(label=v_class_now[3:], payload={'bt_id': 'now'})
bt_cl_next = Callback(label=v_class_next[3:], payload={'bt_id': 'next'})
bt_week = Callback(label=v_current_week[3:], payload={'bt_id': 'week'})
bt_timetable = Callback(label=v_class_timetable[3:], payload={'bt_id': 'timetable'})
bt_exam = Callback(label=v_closest_exam[3:], payload={'bt_id': 'exam'})

kbrd = (
    Keyboard()
    .add(bt_cl_td).add(bt_cl_tmrw)
    .row()
    .add(bt_cl_now, color=KeyboardButtonColor.PRIMARY).add(bt_cl_next, color=KeyboardButtonColor.PRIMARY)
    .row()
    .add(bt_week).add(bt_timetable).add(bt_exam)
)

no_kbrd = Keyboard()


crsl = template_gen(
    TemplateElement(
        photo_id='-174398795_457239105',
        title='Расписание',
        description='Команды',
        buttons=Keyboard().add(bt_cl_td).add(bt_cl_tmrw).get_json(),
        action={'type': 'open_link', 'link': r_link}
    ),
    TemplateElement(
        photo_id='-174398795_457239106',
        title='Пары',
        description='Команды',
        buttons=Keyboard().add(bt_cl_now).add(bt_cl_next).get_json(),
        action={'type': 'open_link', 'link': r_link}
    ),
    TemplateElement(
        photo_id='-174398795_457239107',
        title='Дополнительно',
        description='Команды',
        buttons=Keyboard().add(bt_week).add(bt_timetable).get_json(),
        action={'type': 'open_link', 'link': r_link}
    )
)


async def sb_builder(text: str):
    """
    Snackbar builder

    :param text: Snackbar text
    :return: Ready to use Snackbar (already converted)
    """
    sb = {
        'type': 'show_snackbar',
        'text': text[:90]  # 90 is the max amount of symbols allowed in Snackbar
    }
    return str(json.dumps(sb, ensure_ascii=False))
