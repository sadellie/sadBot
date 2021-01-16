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
Bot's vocabulary
This the list of trigger-words (in russian language, but may be easily modified to support multiple languages)
r_ for response
v_ for vendetta...
"""

# BOT THINGS (start/help/keyboard etc.)
v_start = [
    'начать',
    'start'
]

v_keyboard_toggle = '/кнопки <toggle>'
r_keyboard_success = 'Готово'
r_keyboard_help = 'Для вкл/выкл клавиатуры отправьте «/кнопки вкл» или «/кнопки выкл»'

v_tutorial = '<!>/помощь'
r_tutorial = 'Основные возможности бота. Вся документация доступна по ссылке: https://vk.com/@sadb0t-commands'

v_commands = '<!>/команды'
r_commands = 'Команды:'

v_alive = '/ping'
v_trigger = ['/sadbot', 'sadbot']
v_kill = '/kill'

v_run_script = '/run <path>'

# REGISTER
v_register = '/группа <group_name>'
r_register_success = "👌 Теперь вы в группе {}\nОтправьте «/помощь», если нужна помощь"
r_register_fail = '🙅 Данной группы ({}) нет в базе. Спроси меня: «/список»'
r_register_help = 'Ку 👋🏼 \nДля регистрации отправьте\n«/группа [Название группы]»'

# GROUPS
v_groups_list = '<!>/список'

# IMPORTANT
v_important = '/важно <imp_message>'
r_important_template = '⚠ @everyone {m} \nПоставьте плюс о прочтении (не работает с ПК):'
r_important_dead_payload = '⭕ Ничем не могу помочь'
r_important_not_last = '❗ Ставить плюсы можно только к последнему объявлению'
r_important_ok = 'Принято 👍'
r_important_not_ok = 'Одного раза достаточно, {} 😡'
