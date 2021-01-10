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
VK Chat elements (buttons, keyboard, carousel and others)
"""
import json
import random
from typing import List
from ..classes_vocabulary import (v_classes_today,
                                  v_classes_tomorrow,
                                  v_class_now,
                                  v_class_next,
                                  v_current_week,
                                  v_class_timetable,
                                  v_closest_exam)

link = "https://vk.com/@sadb0t-commands"


class VkButton:
    """
    Button in chat class
    """

    def __init__(self, label: str, color="default", payload: str = None):
        if payload is not None:
            b_type = "callback"
        else:
            b_type = "text"
        self.label = label
        self.color = color
        self.b_type = b_type
        self.payload = {'bt_id': payload}


bt_cl_td = VkButton(label=v_classes_today[3:], payload='today')
bt_cl_tmrw = VkButton(label=v_classes_tomorrow[3:], payload='tomorrow')
bt_cl_now = VkButton(label=v_class_now[3:], payload='now', color='primary')
bt_cl_next = VkButton(label=v_class_next[3:], payload='next', color='primary')
bt_week = VkButton(label=v_current_week[3:], payload='week')
bt_timetable = VkButton(label=v_class_timetable[3:], payload='timetable')
bt_exam = VkButton(label=v_closest_exam[3:], payload='exam')
bt_kb = VkButton(label='Кнопки бота')
bt_plus = [
    '+++',
    'わかった',
    'gut',
    'bonum',
    'хорошо...',
    'океюшки',
    'Pay respect',
    'ну ладно'
]


def json_cnv(s):
    """
    Very important converter for all elements

    :param s: Any element
    :return: Converted, ready to sent element
    """
    return str(json.dumps(s, ensure_ascii=False))


def add_button(button: VkButton):
    """
    Build one button

    :param button: VkButton
    :return: Formatted button
    """
    return {
        'action': {
            'type': button.b_type,
            'label': button.label,
            'payload': button.payload},
        'color': button.color}


def add_element(photo_id: str, title: str, buttons: List[dict]):
    """
    Build one carousel element

    :param photo_id: photo_id
    :param title: Element title
    :param buttons: List of buttons
    :return: Formatted element
    """
    return {
        'photo_id': photo_id,
        'title': title,
        'description': 'Команды',
        'action': {
            'type': 'open_link',
            'link': link},
        'buttons': buttons}


def kb_imp_builder(r_pl: str):
    """
    Build inline keyboard with callback buttons

    :param r_pl: Payload, randomised for different chats
    :return: Keyboard
    """
    return json_cnv(
        {
            'one_time': False,
            'inline': True,
            'buttons': [
                # LVL 1
                [
                    add_button(
                        VkButton(
                            label=random.choice(bt_plus),
                            payload=r_pl,
                            color='positive'
                        )
                    )
                ]
            ]
        }
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
    return json_cnv(sb)


crsl = json_cnv(
    {
        'type': 'carousel',
        'elements': [
            # PAGE 1 SCHEDULE
            add_element(
                '-174398795_457239105',
                'Расписание',
                [
                    add_button(bt_cl_td),
                    add_button(bt_cl_tmrw)
                ]
            ),
            # PAGE 2 CLASSES
            add_element(
                '-174398795_457239106',
                'Пары',
                [
                    add_button(bt_cl_now),
                    add_button(bt_cl_next)
                ]
            ),
            # PAGE 3 ADDITIONAL
            add_element(
                '-174398795_457239107',
                'Дополнительно',
                [
                    add_button(bt_timetable),
                    add_button(bt_week)
                ]
            ),
        ]
    }
)

no_kbrd = json_cnv(
    {'buttons': [],
     'one_time': True}
)  # Empty keyboard to remove it from chat

kbrd = json_cnv(
    {
        'one_time': False,
        'inline': False,
        'buttons': [
            # LVL 1
            [
                add_button(bt_cl_td),
                add_button(bt_cl_tmrw)
            ],
            # LVL 2
            [
                add_button(bt_cl_now),
                add_button(bt_cl_next)
            ],
            # LVL 3
            [
                add_button(bt_week),
                add_button(bt_timetable),
                add_button(bt_exam)
            ]
        ]
    }
)
