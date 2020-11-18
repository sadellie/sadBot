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
This the list of trigger-words for everything related to 'schedule' feature
r_ for response
v_ for vendetta...
"""

# WEEK
v_current_week = '<!>/неделя'

# CLASSES (FOR A DAY)
v_classes_today = '<!>/сегодня'

v_classes_tomorrow = '<!>/завтра'

# CLASS (ONLY ONE)
v_class_now = '<!>/сейчас'

v_class_next = '<!>/далее'

# TIMETABLE
v_class_timetable = '<!>/звонок'

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