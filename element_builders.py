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
VK Chat elements (buttons, keyboard, carousel and others)
"""
import json
import random

link = "https://vk.com/@sadb0t-commands"


class VkButton:
    """
    Button in chat
    """

    def __init__(self, label: str, b_type: str = "text", payload: str = "", color: str = "default"):
        self.label = label
        self.payload = payload
        self.type = b_type
        self.color = color


bt_cl_td = VkButton(label="Пары сегодня",
                    payload="bt01",
                    b_type="callback")
bt_cl_tmrw = VkButton(label="Пары завтра",
                      payload="bt02",
                      b_type="callback")
bt_cl_now = VkButton(label="Пара сейчас",
                     payload="bt03",
                     b_type="callback",
                     color="primary")
bt_cl_next = VkButton(label="Следующая пара",
                      payload="bt04",
                      b_type="callback",
                      color="primary")
bt_week = VkButton(label="Неделя?",
                   payload="bt05",
                   b_type="callback")
bt_search_tutorial = VkButton(label="Как искать?",
                              payload="bt06",
                              b_type="callback")
bt_kb = VkButton(label="Кнопки бота")
bt_plus = ["+++"]


def ac_link_builder():
    """
    Build action to open link

    :return: Formatted action
    """
    return {
        "type": "open_link",
        "link": link}


def bt_builder(button: VkButton):
    """
    Build one button

    :param button: Button
    :return: Formatted button
    """
    return {"action": {"type": button.type,
                       "label": button.label,
                       "payload": pl_builder(button.payload)
                       },
            "color": button.color
            }


def pl_builder(pld: str):
    """ Payload builder

    :param pld: Payload
    :return: Formatted payload
    """
    return {'bt_id': pld}


def el_builder(photo_id: str, title: str, button_1: VkButton, button_2: VkButton):
    """
    Carousel builder

    :param photo_id: photo_id (will be on top and clickable)
    :param title: Title of the element
    :param button_1: First button
    :param button_2: Second button
    :return: Ready to use one carousel element
    """
    return {
        'photo_id': photo_id,
        'title': title,
        'description': "Команды",
        'action': ac_link_builder(),
        'buttons': [
            # First button
            bt_builder(button_1),
            # Second button
            bt_builder(button_2)]}


def json_converter(s):
    """
    Very important converter. Important for all elements

    :param s: Any element
    :return: Converted ready to sent element
    """
    s = json.dumps(s, ensure_ascii=False).encode('utf-8')
    s = str(s.decode('utf-8'))
    return s


# Элементы карусели
elements = [
    # 1. РАСПИСАНИЕ
    el_builder(photo_id="-174398795_457239105",
               title="Расписание",
               button_1=bt_cl_td,
               button_2=bt_cl_tmrw),
    # 2. ПАРЫ
    el_builder(photo_id="-174398795_457239106",
               title="Пары",
               button_1=VkButton(label="Пара сейчас",
                                 payload="bt03",
                                 b_type="callback"),
               button_2=VkButton(label="Следующая пара",
                                 payload="bt04",
                                 b_type="callback")),
    # 3. Дополнительные команды
    el_builder(photo_id="-174398795_457239107",
               title="Дополнительно",
               button_1=bt_search_tutorial,
               button_2=bt_kb)]

# КАРУСЕЛЬ
carousel = json_converter({'type': "carousel", 'elements': elements})


def kb_builder():
    """
    Keyboard builder

    :return: Keyboard
    """
    return {
        "one_time": False,
        "inline": False,
        "buttons": [
            # LVL 1 Расписание
            [
                bt_builder(bt_cl_td),
                bt_builder(bt_cl_tmrw)
            ],
            # LVL 2 Пара сейчас
            [
                bt_builder(bt_cl_now)
            ],
            # LVL 3 Следующая пара
            [
                bt_builder(bt_cl_next)
            ],
            # LVL 4 Подсказки
            [
                bt_builder(bt_search_tutorial),
                bt_builder(bt_week)
            ]
        ]
    }


kb = json_converter(kb_builder())  # Keyboard
no_kb = json_converter({"buttons": [], "one_time": True})  # Empty keyboard to remove it from chat
kb_enabled = False


def toggle_keyboard():
    """
    Show/hide keyboard. Never used...

    :return: Keyboard or empty keyboard(removes keyboard from chat)
    """
    global kb_enabled
    print("kb_enabled " + str(kb_enabled))
    if not kb_enabled:
        kb_enabled = True
        return kb
    else:
        kb_enabled = False
        return no_kb


def kb_imp_builder(r_pl: str):
    """
    Build inline keyboard with callback buttons

    :param r_pl: Payload, randomised for different chats
    :return: Keyboard
    """
    return {
        "one_time": False,
        "inline": True,
        "buttons": [
            # LVL 1
            [
                bt_builder(
                    VkButton(
                        label=random.choice(bt_plus),
                        payload=r_pl,
                        b_type="callback",
                        color="positive"
                    )
                )
            ]
        ]
    }


def sb_builder(text: str):
    """
    Snackbar builder

    :param text: Snackbar text
    :return: Ready to use Snackbar (already converted)
    """
    sb = {
        "type": "show_snackbar",
        "text": text[:90]  # 90 is the max of symbols allowed in Snackbar
    }
    return json_converter(sb)
