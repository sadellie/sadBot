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
Bot's vocabulary for exams feature
This the list of trigger-words (in russian language, but may be easily modified to support multiple languages)
r_ for response
"""

# EXAMS
v_closest_exam = '<!>/экзамен'
v_closest_exam_with_limit = '<!>/экзамен <limit:int>'
r_closest_exam = '📝 [{} {} в {}]\n{}. {}'
r_closest_exam_list = 'Список экзаменов:'
r_closest_exam_empty = '👍 Экзаменов больше нет'
r_closest_exam_limit_warning = '❗ Максимум 10 экзаменов'

# EXAM ADD
v_exam_add = ['<!>/экзамен добавить <add_req>', '<!>/экзамен добавь <add_req>']
r_exam_add_success = '👍 Экзамен добавлен'
r_exam_add_fail_not_reg = '❗ Not registered'
r_exam_add_fail_params = '❗ Недостаточно параметров. [Пример: 31-12-2077 23:59=Название]'
r_exam_add_fail_name = '❗ Название не может быть длиннее 55 символов. (Дано {})'
r_exam_add_fail_date = '❗ Неправильная дата. [Пример: 31-12-2077 23:59=Название]'

# EXAM DELETE
v_exam_delete = ['<!>/экзамен удалить <del_req:int>', '<!>/экзамен удали <del_req:int>']
r_exam_delete_success = '🗑️ Экзамен удалён'
r_exam_delete_fail = '❗ Экзамен не был удалён. [Был добавлен другим пользователем или неправильный id]'

r_months = [
    'Янв.',
    'Фев.',
    'Мар.',
    'Апр.',
    'Мая',
    'Июн.',
    'Июл.',
    'Авг.',
    'Сен.',
    'Окт.',
    'Ноя.',
    'Дек.'
]
