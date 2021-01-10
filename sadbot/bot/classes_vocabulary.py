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
This the list of trigger-words for everything related to 'schedule' feature
r_ for response
v_ for vendetta...
"""

# WEEK
v_current_week = '<!>/неделя'
week_a = "📅 Нижняя неделя"
week_b = "📅 Верхняя неделя"

# CLASSES (FOR A DAY)
v_classes_today = '<!>/сегодня'
v_classes_tomorrow = '<!>/завтра'
v_classes_offset = '/пары <offset:int>'
r_classes_placeholder = 'Нет пары'
r_classes_template = '📅 Пары {}\n'
r_classes_offset_error = '❌ Слишком большое число'

# CLASS (ONLY ONE)
v_class_now = '<!>/сейчас'
v_class_next = '<!>/далее'
r_class_template = '{e} Пара {n} (в {t}):\n{c}'
r_class_last = '❌ Сейчас последняя пара, дальше ничего нет'
r_class_no_more = '❌ Больше пар нет'

# TIMETABLE
v_class_timetable = '<!>/звонок'
r_class_timetable_template = '⏰ Звонок через'

# EXAMS
v_closest_exam = '<!>/экзамен'
v_closest_exam_with_limit = '<!>/экзамен <limit:int>'

# WEEKDAYS. used for replies
r_weekdays_template = [
    'в понедельник',
    'во вторник',
    'в среду',
    'в четверг',
    'в пятницу',
    'в субботу',
    'в воскресенье'
]
