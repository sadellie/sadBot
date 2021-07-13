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
r_keyboard_success = '👍 Готово'
r_keyboard_help = 'Для вкл/выкл клавиатуры отправьте «/кнопки вкл» или «/кнопки выкл»'

v_tutorial = '/помощь'
r_link = 'https://vk.com/@sadb0t-help'
r_tutorial = f'Основные возможности бота. Вся документация доступна по ссылке: {r_link}'

v_req = '/вопрос<!>'

v_commands = '<!>/команды'
r_commands = '🤖 Команды:{}\n\nПодробнее тут: {}'

v_alive = '/ping'
r_alive = '📊 Статистика\n' \
          'Бот работает уже: {}\n' \
          'Пользователей: {}\n' \
          'Обработано действий: {}\n' \
          '-Сообщений: {}\n' \
          '-Нажатий на кнопки: {}\n' \
          '-Добавлений в чаты: {}\n' \
          'Время ответа (прим.): {}'
v_trigger = '/sadbot'
v_kill = '/kill'

v_run_script = '/run <path>'

# REGISTER
v_register = '/группа <group_name:int>'
r_register_success = "👌 Теперь вы в группе {}\nОтправьте «/помощь», если нужна помощь"
r_register_fail = '🙅 Данной группы нет в базе. Спроси меня: «/список»'
r_register_help = 'Привет 👋🏼 \n' \
                  'Для регистрации нужно выбрать группу из списка. Отправь команду:\n' \
                  '/группы\n\n' \
                  'Если нужна помощь, то отправь:\n' \
                  '/помощь'

# GROUPS
v_group_my = '/группа'
r_group_my_template = '🎓 Вы в группе {}'
r_group_my_none = '❌ Вы не состоите ни в одной из групп. Список групп: «/список»'
v_groups_list = ['/группы', '/список']
r_groups_list = '🎓 Список доступных групп:\n{}\n\nДля регистрации отправьте:\n/группа [id группы]'
v_group_rename = '/переим <name>'
r_group_rename_success = '👌 Переименовано!'

# SCHEDULE UPDATE
v_sch_update = '/обновить'
r_sch_success = '👌 Расписание для {} успешно обновлено'
r_sch_fail = '❌ Что-то пошло не так:\n{}'
r_sch_access = '❌ Вы не являетесь старостой {}'
r_not_xls = '❌ Файл должен быть в формате .xls'
