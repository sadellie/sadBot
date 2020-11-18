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
Everything related to teachers
"""
import logging
from sqlite3 import Cursor, Connection

from sadbot.teachers_vocabulary import r_teacher_delete_help, r_teacher_add_help, r_teacher_find_fail


def add_teacher(db: Connection, req: str, user_id: int):
    """
    Add teacher to database
    
    :param user_id: User id, who is adding
    :param db: Database
    :param req: Request. For example, пример: '/добавь Имя Препода=Предмет'
    :return: Result
    """
    if req.lower() == "имя=предмет":
        return "🤬 Чел, ты... [Имя=Предмет это лишь пример]"
    # We create list, where 0 is Teacher, and 1 is Class
    try:
        req = req.split("=")
        req = (req[0], req[1], req[1].lower(), user_id)  # Teacher, Class, Tags(same as class by default)
    except IndexError:
        return r_teacher_add_help
    sql = '''INSERT INTO teachers (teacherName, teacherClass, teacherClassSearchable, userId) VALUES (?, ?, ?, ?)'''
    db.cursor().execute(sql, req)
    db.commit()
    return req[0] + " преподаёт " + req[1] + ", понял"


def delete_teacher(db: Connection, req: str, user_id: int):
    """
    Delete teacher from database

    :param db: Database
    :param req: Request, class name
    :param user_id: User id
    :return: Result (success or fail)
    """
    try:
        teacher_name = req.split('=')[0]
        teacher_class = req.split('=')[1]
    except IndexError:
        return r_teacher_delete_help

    cur = db.cursor()
    # First we check if this user has added this class
    req_to_find = (teacher_class, teacher_name)
    sql_to_find = "SELECT userId FROM teachers WHERE teacherClass == ? AND teacherName == ?"
    find = cur.execute(sql_to_find, req_to_find).fetchall()
    if len(find) > 0:
        # Now we need to work only with records only by this user
        users = []  # List of user who has added records with requested parametrs
        for i in find:
            users.append(int(i['userId']))
        if user_id in users:  # User is in list
            req_to_delete = (teacher_class, teacher_name, user_id)
            sql = "DELETE FROM teachers WHERE teacherClass == ? AND teacherName == ? AND userId == ?"
            if cur.execute(sql, req_to_delete).rowcount > 0:
                db.commit()
                return "Готово, теперь его никто не найдёт..."
            else:
                logging.error('Deleted 0 records. Request: %s', req)
                return "Удалено 0 записей [что-то сломалось]"
        else:  # User wants to delete existing other users' record
            return "Не ты добавлял, сорян"
    else:
        # No records of class with this name at all
        return "Не нашёл такого [ошибки в запросе?]"


def find_teacher(cur: Cursor, req: str):
    """
    Find teacher

    :param req: Request
    :param cur: Cursor
    :return: Search result as string
    """
    if len(req) < 3:
        return "Маловато символов"

    req_f = f"%{req.lower()}%"
    qwe = (req_f,)
    sql = "SELECT * FROM teachers WHERE teacherClassSearchable LIKE ?"
    cur.execute(sql, qwe)
    res = cur.fetchall()
    out = ""
    for counter, i in enumerate(res[:5]):  # We take only first 5 results
        out += f"{counter + 1}. {i['teacherName']}\n({i['teacherClass']})\n"
    if not out:
        return r_teacher_find_fail.format(req)
    return "🔍 Результаты поиска: " + out

