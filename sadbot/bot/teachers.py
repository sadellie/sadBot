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
Everything related to teachers
"""
import logging
from sqlite3 import Cursor, Connection

from bot.teachers_vocabulary import *


def add_teacher(db: Connection, req: str, user_id: int):
    """
    Add teacher to database
    
    :param user_id: User id, who is adding
    :param db: Database
    :param req: Request
    :return: Result
    """
    if req.lower() == "имя=предмет":
        return "🤬 Чел, ты... [Имя=Предмет это лишь пример]"
    # We create list, where 0 is Teacher, and 1 is Class
    try:
        req = req.split("=")
        req = (req[0], req[1], req[1].lower(), user_id)  # Teacher, Class, Searchable(we search in this column), User
    except IndexError:
        return r_teacher_add_help
    sql = "INSERT INTO teachers (teacherName, teacherClass, teacherClassSearchable, userId) VALUES (?, ?, ?, ?)"
    db.cursor().execute(sql, req)
    db.commit()
    return r_teacher_add_success.format(req[0], req[1])


def delete_teacher(db: Connection, req: int, user_id: int):
    """
    Delete teacher from database

    :param db: Database
    :param req: Request, class name
    :param user_id: User id
    :return: Result (success or fail)
    """
    sql = db.cursor().execute("DELETE FROM teachers WHERE teacherId = ? AND userId = ?", (req, user_id)).rowcount
    db.commit()
    return r_teacher_delete_success if (sql != 0) else r_teacher_delete_fail  # Not 0 means deleted


def find_teacher(cur: Cursor, req: str):
    """
    Find teacher

    :param req: Request
    :param cur: Cursor
    :return: Search result as string
    """
    if len(req) < 3:
        return r_teacher_find_symbols
    req_f = f"%{req.lower()}%"
    qwe = (req_f,)
    sql = "SELECT * FROM teachers WHERE teacherClassSearchable LIKE ? LIMIT 5"
    cur.execute(sql, qwe)
    res = cur.fetchall()
    out = ""
    for c, i in enumerate(res):
        print(i)
        out += f"{i['teacherId']}. {i['teacherName']}\n({i['teacherClass']})\n"
    if not out:
        return r_teacher_find_fail.format(req)
    return r_teacher_find_success.format(out)
