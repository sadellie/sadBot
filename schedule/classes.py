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
# Here is everything related to classes/schedule
"""
import calendar
from random import choice
import datetime
import sqlite3


def get_classes_sql(cur: sqlite3.Cursor, wd: str, p: str):
    """
    SQL function to get classes for a specified day.
    
    :param cur: Cursor
    :param wd: Day of the week (for example: friday2)
    :param p: Group uid
    :return: All 6 classes
    """
    try:
        cur.execute("SELECT classId, " + wd + " FROM '" + p + "'")
        r = cur.fetchall()
        return r
    except Exception as e:
        print(e)
        return "Error while getting classes"


#
def get_cur_week(i=0):
    """
    Get current week
    
    :param i: Special value, used to get week of the next week...
    :return: 1 for first week, 2 for the second one
    """
    td = datetime.date.today()
    if i != 0:
        td = td + datetime.timedelta(days=1)
    week_number = td.isocalendar()[1]
    if week_number % 2 == 0:
        # First week (bottom week in RU)
        return 2
    else:
        # Second week (upper week in RU)
        return 1


def get_cur_week_text():
    """
    Ger current week as text
    
    :return: Name of the week
    """
    if get_cur_week() == 1:
        return "📅 Нижняя неделя"
    else:
        return "📅 Верхняя неделя"


#
def get_classes(cur: sqlite3.Cursor, p: str, modifier=0, as_list=True):
    """
    Get classes
    
    :param cur: Database cursor
    :param p:  Peer_id
    :param modifier: 1, if we need to get classes from the next week
    :param as_list: If False will return string
    :return: List of classes (if as_list is default)
    """
    today = datetime.datetime.today()
    if modifier != 0:
        today = today + datetime.timedelta(days=1)
    cur_weekday = calendar.day_name[today.weekday()].lower() + str(get_cur_week(modifier))
    try:
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
            out = "📅 Пары:"
            for count, i in enumerate(get_classes_sql(cur, cur_weekday, p)):
                # noinspection PyTypeChecker
                class_name = str(i[cur_weekday])
                if class_name == 'None':
                    class_name = "Нет пары"
                out += "\n{n}. {c}".format(n=str(count + 1),
                                           c=class_name)
    except Exception as e:
        # Couldn't find database'
        print(str(e))
        return "--------"  # Very ugly fix of a bug, which appears only during debug
    return out


def get_class(cur: sqlite3.Cursor, p: str, i=0):
    """
    Get class

    :param cur: Cursor
    :param p: Peer_id
    :param i: Offset, if 1, will return next class
    :return: Name of the class
    """
    # Loading timing
    timing = cur.execute("SELECT groupTiming FROm groups WHERE groupId = ?", (p,)).fetchone()['groupTiming'].split(";")

    now = datetime.datetime.now()
    for index, t in enumerate(timing):
        t = t.split(":")
        if now <= now.replace(hour=int(t[0]), minute=int(t[1])):
            cur_cn = index
            # Need next class (last class number or less)
            if i != 0 and cur_cn < len(timing):
                cur_cn += 1
            # Need next class, but there is nothing left
            elif i != 0:
                return "❌ Сейчас последняя пара, дальше ничего нет"
            return "{e} Пара {n}: {c}".format(e=choice(['📒', '📕', '📗', '📘', '📙']),
                                              n=str(cur_cn + 1),
                                              c=str(get_classes(cur, p)[cur_cn]))

    return "Больше пар нет"

