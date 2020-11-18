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
Here is everything related to classes/schedule
"""
import calendar  # IDE bug (?) shows ImportError but runs normally
from random import choice
import datetime
import sqlite3
from sadbot.classes_vocabulary import r_weekdays_template


def get_classes_sql(cur: sqlite3.Cursor, wd: str, p: int):
    """
    SQL function to get classes for a specified day.
    
    :param cur: Cursor
    :param wd: Day of the week (for example: friday2)
    :param p: Group uid
    :return: All 6 classes
    """

    sql = f"SELECT {wd} FROM 'group{p}'"
    cur.execute(sql)
    r = cur.fetchall()
    return r


def get_cur_week(day, i=0):
    """
    Get current week
    
    :param day: Date
    :param i: Special value, used to get week of the next week...
    :return: 1 for first week, 2 for the second one
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
    if get_cur_week(datetime.datetime.today()) == 1:
        return "📅 Нижняя неделя"
    else:
        return "📅 Верхняя неделя"


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
    :return: List of classes (if as_list is default)
    """
    today = datetime.datetime.today()
    if custom_day is not None:
        today = today.replace(
            day=custom_day[0],
            month=custom_day[1],
            year=custom_day[2]
        )
    today = today + datetime.timedelta(days=modifier)
    cur_weekday = calendar.day_name[today.weekday()].lower() + get_cur_week(today, modifier)  # Number of the weekday
    cur_weekday_name = r_weekdays_template[today.weekday()]  # Name of the weekday

    # Classes as list
    if as_list:
        out = []
        for i in get_classes_sql(cur, cur_weekday, p):
            class_name = str(i[cur_weekday])
            if class_name == 'None':
                class_name = "Нет пары"
            out += ["\n" + class_name]
    else:
        # Classes as string
        out = f"📅 Пары {cur_weekday_name}:"  # Example: 'Пары в среду:'
        for count, i in enumerate(get_classes_sql(cur, cur_weekday, p)):
            # noinspection PyTypeChecker
            class_name = str(i[cur_weekday])
            if class_name == 'None':
                class_name = "Нет пары"
            out += f"\n{count + 1}. {class_name}"
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
    :param custom_day: Used for tests. Will overwrite today's date
    :param custom_time: Used for tests. Will overwrite current time
    :return: Name of the class
    """
    # Loading timing
    timing = cur.execute(
        f"SELECT groupTimeTable FROM group{p}"
    ).fetchall()

    now = datetime.datetime.now().replace(
        hour=custom_time[0],
        minute=custom_time[1]
    ) if custom_time else datetime.datetime.now()

    for class_number, i in enumerate(timing):
        one_time = i['groupTimeTable'].split('-')  # [9:00, 10:20]
        for x in one_time:
            x = x.split(':')
            if now < now.replace(
                    hour=int(x[0]),
                    minute=int(x[1])
            ):
                if class_number + modifier >= len(timing):
                    return '❌ Сейчас последняя пара, дальше ничего нет'

                return "{e} Пара {n}: {c}".format(
                    e=choice(['📒', '📕', '📗', '📘', '📙']),
                    n=str(class_number + 1 + modifier),
                    c=str(
                        get_classes(
                            cur=cur,
                            p=p,
                            custom_day=custom_day
                        )[class_number + modifier]
                    )
                )
    return "❌ Больше пар нет"


def time_to_next(cur: sqlite3.Cursor, g: int, custom_time: list = None):
    """
    When is the next class(timing)?

    :param cur: Cursor
    :param g: Group id in database
    :param custom_time: Used for tests. Will overwrite current time
    :return: Formatted string with minutes till next class
    """
    timing = cur.execute(f"SELECT groupTimeTable FROM group{g}").fetchall()

    now = datetime.datetime.now().replace(
        hour=custom_time[0],
        minute=custom_time[1]
    ) if custom_time else datetime.datetime.now()

    for class_number, i in enumerate(timing):
        one_time = i['groupTimeTable'].split('-')  # [9:00, 10:20]
        for x in one_time:
            x = x.split(':')
            check = now.replace(
                hour=int(x[0]),
                minute=int(x[1])
            )
            if now < check:
                return "Звонок через {m} мин.".format(m=(check - now).seconds // 60)
    return "❌ Больше пар нет"
