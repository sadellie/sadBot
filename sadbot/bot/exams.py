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

"""Exams functions"""

from datetime import datetime

from bot.base import db
from bot.exams_vocabulary import *
from bot.user_functions import get_user

cur = db.cursor()


async def add_exam(r: str,
                   u: int):
    """Add exam to database

    :param r: Request
    :param u: User ID who added the exam.
    :return: Operation result. Success or fail (with error description)
    """
    user = await get_user(u)
    if not user:  # This is case is mostly impossible but still there
        return r_exam_add_fail_not_reg

    # Must be 2 parameters examDate and examGroup
    request = r.split('=')
    if len(request) < 2:
        return r_exam_add_fail_params
    # Max length of text snackbar is 90,
    # so we need to limit name of the exam (about 25 symbols for date, time and id of the exam)
    if len(request[1]) > 65:
        return r_exam_add_fail_name.format(len(request[1]))

    try:
        exam_date = datetime.strptime(request[0], "%d-%m-%Y %H:%M")  # Convert into datetime to be sure it has no errors
    except ValueError:
        return r_exam_add_fail_date
    sql = "INSERT INTO exams (examDate, examName, examGroup, examUser) VALUES (?, ?, ?, ?)"
    cur.execute(sql, (exam_date.strftime('%Y%m%d%H%M'), request[1], user.group_peer_id, u))
    db.commit()
    return r_exam_add_success


async def delete_exam(r: str,
                      u: int):
    """Delete exam from database

    :param r: Request
    :param u: User ID who added the exam
    :return: Result of operation. Success or fail as string
    """
    sql = db.cursor().execute("DELETE FROM exams WHERE examId = ? AND examUser = ?", (r, u)).rowcount
    db.commit()
    return r_exam_delete_success if (sql != 0) else r_exam_delete_fail


async def get_next_exam(user_id: int,
                        limit: int):
    """Get exams

    :param user_id: User id (VK)
    :param limit: How many exams do we need
    :return: Closest exams from database for
    """
    # Output message
    out = []
    group: int = (await get_user(user_id)).group_peer_id

    # Formatting if requested a list
    if limit > 1:
        out.append(r_closest_exam_list)

    # Setting limit to 10 to avoid errors
    if limit > 10:
        limit = 10
        out.append(r_closest_exam_limit_warning)

    today = datetime.today().strftime("%Y%m%d%H%M")
    cur.execute(
        'SELECT * FROM exams WHERE (examDate > ?) AND (examGroup = ?) ORDER BY examDate LIMIT ?',
        (today, group, limit))
    res = cur.fetchall()

    if len(res) == 0:
        return r_closest_exam_empty

    for i in res:
        e_d = datetime.strptime(str(i['examDate']), "%Y%m%d%H%M")  # Date
        # 📝 [15 Cен. в 10:00]\n99. Name
        out.append(r_closest_exam.format(e_d.day,
                                         r_months[e_d.month - 1],
                                         e_d.strftime("%H:%M"),  # Time
                                         i['examId'],
                                         i['examName']))

    return '\n\n'.join(out)