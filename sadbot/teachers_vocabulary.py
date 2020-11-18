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
This the list of trigger-words for everything related to 'teachers search' feature
"""
v_teacher_find = '/препод <find_req>'
r_teacher_find_help = '💁🏼‍♂️ Пример:\n/препод Предмет'
r_teacher_find_fail = '🤷🏼‍♂️ Я не знаю кто преподаёт {}.' \
                      '\n\nКоманда для добавления: «/добавь Имя=Предмет»'

v_teacher_add = '/добавь <add_req>'
v_teacher_add_help = {'как добавить'}
r_teacher_add_help = '💁🏼‍♂️ Пример:\n/добавь Имя=Предмет'

v_teacher_delete = '/удали <del_req>'
v_teacher_delete_help = {'как удалить'}
r_teacher_delete_help = '💁🏼‍♂️ Пример:\n/удали Имя=Предмет'
