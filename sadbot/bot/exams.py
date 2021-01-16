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
Exams functions
"""
import sqlite3
from datetime import datetime
from bot.exams_vocabulary import *
from bot.user_functions import get_user


async def add_exam(db: sqlite3.Connection,
                   r: str,
                   u: int):
    """Add exam to database

    :param db: Connection to database
    :param r: Request
    :param u: User ID who added the exam
    :return: Operation result. Success or fail (with error description)
    """
    cur = db.cursor()
    user = await get_user(cur, u)

    if not user:  # This is case is mostly impossible but still there
        return r_exam_add_fail_not_reg

    # Must be 2 parameters examDate and examGroup
    request = r.split('=')
    if len(request) < 2:
        return r_exam_add_fail_params

    # Max length of text snackbar is 90,
    # so we need to limit name of the exam (31 is the max of text before name of the exam, i.e. date, time, id)
    if len(request[1]) > 59:
        return r_exam_add_fail_name.format(len(request[1]))

    try:
        exam_date = datetime.strptime(request[0], "%d-%m-%Y %H:%M")  # Convert into datetime to be sure it has no errors
    except ValueError:
        return r_exam_add_fail_date
    sql = "INSERT INTO exams (examDate, examName, examGroup, examUser) VALUES (?, ?, ?, ?)"
    cur.execute(sql, (exam_date.strftime('%Y%m%d%H%M'), request[1], user.group_peer_id, u))
    db.commit()
    return r_exam_add_success


async def delete_exam(db: sqlite3.Connection,
                      r: str,
                      u: int):
    """Delete exam from database

    :param db: Connection to database
    :param r: Request
    :param u: User ID who added the exam
    :return: Result of operation. Success or fail as string
    """
    sql = db.cursor().execute("DELETE FROM exams WHERE examId = ? AND examUser = ?", (r, u)).rowcount
    db.commit()
    return r_exam_delete_success if (sql != 0) else r_exam_delete_fail


async def get_next_exam(group: int,
                        limit: int,
                        cur: sqlite3.Cursor):
    """Get exams

    :param group: Group uid
    :param limit: How many exams do we need
    :param cur: Database cursor
    :return: Closest exams from database for
    """
    # Output message
    out = []

    # Setting limit to 30 to avoid errors
    if limit > 30:
        limit = 30
        out.append(r_closest_exam_limir_warning)

    today = datetime.today().strftime("%Y%m%d%H%M")
    cur.execute(
        'SELECT * FROM exams WHERE (examDate > ?) AND (examGroup = ?) ORDER BY examDate LIMIT ?',
        (today, group, limit))
    res = cur.fetchall()
    for i in res:
        e_d = datetime.strptime(str(i['examDate']), "%Y%m%d%H%M")
        e_t = e_d.strftime("%H:%M")

        # 📝 Экзамен 15 Cентября в 10:00
        # 99. Name
        out.append(r_closest_exam.format(e_d.day, r_months[e_d.month - 1], e_t, i['examId'], i['examName']))

    if len(res) == 0:
        return r_closest_exam_empty
    return '\n\n'.join(out)
