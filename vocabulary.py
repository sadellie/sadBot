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
Bot's vocabulary
"""

# This the list of trigger-words (in russian language, but may be easily modified to support multiple languages)
# r_ for response
# v_ for vengeance...

# BOT THINGS (start/help/keyboard etc.)
v_start = {"начать", "start"}
v_keyboard_show = {'покажи кнопки', 'включи кнопки', 'покажи клавиатуру', 'включи клавиатуру'}
v_keyboard_hide = {'убери кнопки', 'выключи кнопки', 'убери клавиатуру', 'выключи клавиатуру'}
r_keyboard = "Готово"
v_tutorial = {'как работает бот', 'как пользоваться ботом', 'доступные команды', 'команды бота', 'обучение',
              'что делает бот'}
r_tutorial = "Основные возможности бота. Вся документация доступна по ссылке: https://vk.com/@sadb0t-commands"
v_alive = {'бот работает?', 'бот жив?', 'бот упал', 'аптайм'}
v_trigger = {'sadbot', 'тупой бот', 'хороший бот'}

# REGISTER
v_register = '/группа'
r_no_register = 'Вы не состоите ни в одной из групп'
r_register_success = "👌 Теперь вы в группе {g}\nОтправьте «Обучение», если нужна помощь"
r_register_fail = "🙅 Данной группы нет в базе"
r_register_help = 'Ку 👋🏼 \nДля регистрации отправьте\n«/группа [Название группы]»'
# GROUPS
v_groups_list = {'какие есть группы?'}

# IMPORTANT
v_important = '/важно'
r_important_template = "⚠ @everyone {m} \nПоставьте плюс о прочтении (не работает с ПК):"
r_important_dead_payload = "Я ребутнулся, ничем не могу помочь"

# WEEK
v_current_week = {'какая сейчас неделя', 'сейчас верхняя', 'сейчас нижняя', 'неделя?'}

# CLASSES (FOR A DAY)
v_classes_today = {'расписание на сегодня', 'расписание сегодня', 'пары сегодня', 'сегодняшние пары'}
v_classes_tomorrow = {'расписание на завтра', 'расписание завтра', 'пары завтра', 'какие пары завтра'}

# CLASS (ONLY ONE)
v_class_now = {'какая сейчас пара', 'что у нас сейчас', 'текущая пара', 'пара сейчас', 'где у нас'}
v_class_next = {'какая дальше пара', 'что у нас потом', 'следующая пара', 'пара потом'}

# TEACHER
v_teacher_find = '/препод'
v_teacher_find_help = {'как искать?'}
r_teacher_find_help = "💁🏼‍♂️ Пример: \n '/препод Предмета'"
v_teacher_add = '/добавь'
v_teacher_add_help = {'как добавить?'}
r_teacher_add_help = "💁🏼‍♂️ Пример: \n '/добавь Имя=Предмет'"
v_teacher_delete = '/удали'
v_teacher_delete_help = {'как удалить?'}
r_teacher_delete_help = "💁🏼‍♂️ Пример: \n '/удали Предмет'"
