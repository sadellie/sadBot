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
Here is everything related to classes/schedule
"""
import calendar
from random import choice
import datetime
import sqlite3
from .classes_vocabulary import *


def get_classes_sql(cur: sqlite3.Cursor,
                    wd: str,
                    p: int):
    """
    SQL function to get classes for a specified day.

    :param cur: Cursor
    :param wd: Day of the week (for example: friday2)
    :param p: Group uid
    :return: All 6 classes
    """
    return cur.execute(f"SELECT {wd} FROM 'group{p}'").fetchall()


def get_cur_week(day: datetime,
                 i=0):
    """
    Get current week id. Special value to work with database

    :param day: Date
    :param i: Special value, used to get week of the next week...
    :return: Strings! 1 for first week, 2 for the second one
    """

    if i != 0:
        day = day + datetime.timedelta(days=1)
    week_number = day.isocalendar()[1]
    if week_number % 2 == 0:
        # First week (bottom week in RU)
        return '2'
    else:
        # Second week (upper week in RU)
        return '1'


def get_cur_week_text():
    """
    Ger current week as text

    :return: Name of the week
    """
    return week_a if get_cur_week(datetime.datetime.today()) == '1' else week_b


def get_classes(cur: sqlite3.Cursor,
                p: int,
                modifier: int = 0,
                as_list: bool = True,
                custom_day: list = None):
    """
    Get classes

    :param cur: Database cursor
    :param p:  Group unique identifier in database
    :param modifier: Days offset. For example, "Tomorrow classes" will require this value to be 1
    :param as_list: If False will return string
    :param custom_day: Used for tests. Will overwrite today's date
    :return: List of classes by default, formatted string if not
    """
    today = datetime.datetime.today()
    if custom_day is not None:
        today = today.replace(day=custom_day[0], month=custom_day[1], year=custom_day[2])

    try:
        # Adding offset to get classes. For tomorrow, for example, it will be 1
        today = today + datetime.timedelta(days=modifier)
    except OverflowError:
        return r_classes_offset_error

    # Name of the weekday in db, i.e. "friday2"
    cur_weekday = calendar.day_name[today.weekday()].lower() + get_cur_week(today, modifier)

    # Name of the weekday
    out = []  # List of classes
    for i in get_classes_sql(cur, cur_weekday, p):
        class_name = str(i[cur_weekday])
        if class_name == 'None':
            class_name = r_classes_placeholder
        out += [class_name]

    if not as_list:  # Transform our list into string with formatting
        out_str = r_classes_template.format(r_weekdays_template[today.weekday()])
        for x, z in enumerate(out):
            out_str += f"{x + 1}. {z}\n"
        return out_str
    return out


def get_class(cur: sqlite3.Cursor,
              p: int,
              modifier=0,
              custom_day: list = None,
              custom_time: list = None):
    """
    Get class

    :param cur: Cursor
    :param p: Group id in database
    :param modifier: Offset, if 1, will return next class
    :param custom_day: Used for tests. Will overwrite today's date. List of day, month, year
    :param custom_time: Used for tests. Will overwrite current time
    :return: Name of the class
    """
    # Decide whether ot not to use custom set time (for testing purposes)
    now = datetime.datetime.now().replace(
        hour=custom_time[0],
        minute=custom_time[1]
    ) if custom_time else datetime.datetime.now()  # Change current time to custom

    # Loading timing
    timing = cur.execute(f"SELECT groupTimeTable FROM group{p}").fetchall()
    for class_number, i in enumerate(timing):
        one_time = i['groupTimeTable'].split('-')  # [9:00, 10:20]
        for index, x in enumerate(one_time):
            x = x.split(':')
            if now < now.replace(hour=int(x[0]), minute=int(x[1])):
                # Check if current class is the last one, but user asks for the next one
                if class_number + modifier >= len(timing):
                    return r_class_last

                # *book emoji* Пара 5:
                # History (в 15:00)
                return r_class_template.format(
                    e=choice(['📒', '📕', '📗', '📘', '📙']),  # Every call will have random book emoji
                    n=str(class_number + 1 + modifier),
                    c=get_classes(cur, p, custom_day=custom_day)[class_number + modifier],
                    t=timing[class_number + modifier]['groupTimeTable'].split('-')[0]  # Getting class start time
                )
    return r_class_no_more


def time_to_next(cur: sqlite3.Cursor,
                 g: int,
                 custom_time: list = None):
    """
    When is the next class(timing)?

    :param cur: Cursor
    :param g: Group id in database
    :param custom_time: Used for tests. Will overwrite current time, H:M
    :return: Formatted string with minutes till next class
    """
    # Decide whether ot not to use custom set time (for testing purposes)
    now = datetime.datetime.now().replace(
        hour=custom_time[0],
        minute=custom_time[1]
    ) if custom_time else datetime.datetime.now()

    timing = cur.execute(f"SELECT groupTimeTable FROM group{g}").fetchall()
    for class_number, i in enumerate(timing):
        one_time = i['groupTimeTable'].split('-')  # [9:00, 10:20]
        for x in one_time:
            x = x.split(':')
            check = now.replace(hour=int(x[0]), minute=int(x[1]))
            if now < check:
                d = (check - now).seconds // 60  # Time to next class in seconds
                h = d // 60  # Hours
                m = d - h * 60  # Minutes
                r = r_class_timetable_template

                if h > 0:
                    r += f' {h} ч.'
                if m > 0:
                    r += f' {m} мин.'
                return r
    return r_class_no_more
