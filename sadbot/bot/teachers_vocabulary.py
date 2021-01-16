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
This the list of trigger-words for everything related to 'teachers search' feature
"""

# TEACHER FIND
v_teacher_find = ['/препод найти <find_req>', '/препод найди <find_req>']
r_teacher_find_success = '🔍 Результаты поиска:\n{}'
r_teacher_find_fail = '🤷🏼‍♂️ Я не знаю кто преподаёт {}.' \
                      '\n\nКоманда для добавления: «/препод добавить [Имя=Предмет]»'
r_teacher_find_symbols = '❗ Недостаточно символов (минимум 3)'

# TEACHER ADD
v_teacher_add = ['/препод добавь <add_req>', '/препод добавить <add_req>']
r_teacher_add_help = '💁🏼‍♂️ Пример:\n/добавь Имя=Предмет'
r_teacher_add_success = '👍 {} преподаёт {}, понял'

# TEACHER DELETE
v_teacher_delete = ['/препод удали <del_req:int>', '/препод удалить <del_req:int>']
r_teacher_delete_help = '💁🏼‍♂️ Пример:\n/препод удалить Имя=Предмет'
r_teacher_delete_success = '🗑️ Готово, теперь его никто не найдёт...'
r_teacher_delete_fail = '🤷🏼‍♂️ Не нашёл такого [ошибки в запросе?]'
r_teacher_delete_zero_fail = '❗ Удалено 0 записей [что-то сломалось]'
r_teacher_delete_permission_fail = '🤷🏼‍♂️Не ты добавлял, сорян'
