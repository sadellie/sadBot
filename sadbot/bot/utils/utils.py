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
Utilities. Different unsorted functions
"""
# Some imports are within functions as they are called only once before shutdown
import datetime
import time
from sqlite3 import Connection, connect


def get_random():
    """
    Generate random message_id. Necessary to send message

    :return: random number
    """

    return time.time() * 1000000


def get_uptime(start_time):
    """
    Get current uptime

    :return: Formatted string DD:HH:MM:SS (for example, 13:20:17:25)
    """

    current_time = datetime.datetime.now()
    uptime: datetime.timedelta = current_time - start_time
    days = uptime.days
    hours = uptime.seconds // 3600
    minutes = uptime.seconds // 60 % 60
    seconds = uptime.seconds % 60
    return "{d:02}:{h:02}:{m:02}:{s:02}".format(d=days, h=hours, m=minutes, s=seconds)


def custom_factory(cursor,
                   row):
    """
    Custom factory, makes working with database operations results easier

    :param cursor: Database Cursor
    :param row: Row, idk...
    :return: Dictionary
    """
    cf = {}
    for i, x in enumerate(cursor.description):
        cf[x[0]] = row[i]
    return cf


def connect_to_database(path: str):
    """
    Connect to database and setup row_factory

    :return: Connection to database
    """
    conn = connect(path)
    conn.row_factory = custom_factory
    return conn


def load_sad_replies(conn: Connection):
    """
    Load all random replies from database

    :param conn: Database connection
    :return: List of random replies
    """
    return conn.cursor().execute("SELECT * FROM sad_replies").fetchall()


async def record_stats(db: Connection,
                       uptime: datetime.timedelta):
    """
    Record statistics into database

    :param db: Database connection
    :param uptime: Uptime
    """
    sql = "INSERT INTO stats (statDate, statUptime) VALUES (?, ?)"
    req = (datetime.datetime.now(), uptime.seconds)
    db.cursor().execute(sql, req)
    print(datetime.datetime.timetuple(datetime.datetime.now()))
    db.commit()


def create_database(db: Connection):
    """
    Creates empty database with group0 in it which has 4 classes in groupTiming.
    Once it's created you should open it in editor and insert your data or use xls file
    """
    cur = db.cursor()

    # Groups table
    cur.execute(
        'CREATE TABLE groups (groupId INTEGER PRIMARY KEY ON CONFLICT ROLLBACK AUTOINCREMENT NOT NULL, '
        'groupName TEXT NOT NULL);'
    )

    # Random replies table
    cur.execute(
        'CREATE TABLE sad_replies (replyText TEXT, replyAtt TEXT, replySticker TEXT);'
    )

    # Stats table
    cur.execute(
        'CREATE TABLE stats (statDate DATE, statUptime TIME);'
    )

    # Teachers table
    cur.execute(
        'CREATE TABLE teachers (teacherId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, '
        'teacherName TEXT, teacherClassSearchable TEXT, teacherClass TEXT, userId TEXT);'
    )

    # Users table
    cur.execute(
        'CREATE TABLE users (userId TEXT PRIMARY KEY NOT NULL UNIQUE ON CONFLICT REPLACE, '
        'groupPeerId INTEGER REFERENCES groups (groupId) ON DELETE CASCADE ON UPDATE CASCADE, '
        'isAdmin BOOLEAN, isBanned BOOLEAN);'
    )

    # Exams table
    cur.execute(
        'CREATE TABLE exams (examId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, examDate DATE, '
        'examName TEXT, examGroup TEXT, examUser INTEGER);'
    )

    db.commit()


def check_sheet(file_path: str) -> bool:
    """
    Checks sheet for typos in column headers

    :param file_path: Path to Excel file
    :return: Return True if everything is ok
    """
    import xlrd
    check = ["groupTimeTable", "monday1", "tuesday1", "wednesday1", "thursday1", "friday1", "saturday1", "sunday1",
             "monday2", "tuesday2", "wednesday2", "thursday2", "friday2", "saturday2", "sunday2"]
    sheet = xlrd.open_workbook(file_path).sheet_by_index(0)
    for indx, val in enumerate(check):
        cell = sheet.cell(0, indx).value
        if cell != val:
            print(f"{cell} != {val}")  # Prints what header didn't pass the check
            return False
    return True


def xl_to_database(path: str,
                   group_id: str,
                   conn: Connection):
    """
    Insert data from xls file to database

    :param path: Path to Excel file
    :param group_id: Id of the group
    :param conn: Database
    """
    import pandas as pd
    dfs: pd.DataFrame = pd.read_excel(path, sheet_name=None)
    for table, df in dfs.items():
        df.to_sql(
            name=f"group{group_id}",
            con=conn,
            index_label='class_id',
            if_exists='replace'
        )


def register_new_group(conn: Connection,
                       path: str,
                       group_name: str):
    """Registers new group in database. Will convert Excel file to table and add record to groups table

    :param conn: Database
    :param path: Path to Excel file
    :param group_name: Name of the group
    :return: True if Excel file was OK, False if there was something wrong with it
    """
    if check_sheet(path):
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO groups (groupName) VALUES (?)",
            (group_name,)
        )
        conn.commit()
        cur.execute("SELECT * FROM groups ORDER BY groupId DESC LIMIT 1;")
        fetch = cur.fetchone()
        group_id = fetch[0]
        xl_to_database(
            path=path,
            group_id=group_id,
            conn=conn,
        )
        return True
    else:
        return False


# Not tested properly
def update_group(conn: Connection,
                 group_name: str,
                 path: str,
                 new_group_name: str):
    """
    Update group schedule/name

    :param conn: Database
    :param group_name: Name of the group
    :param path: Path to .xls file with schedule
    :param new_group_name: New name of the group
    :return: True if everything is ok. False is something went wrong
    """
    r = False
    cur = conn.cursor()
    cur.execute(
        "SELECT groupId FROM groups WHERE groupName = ?",
        (group_name,)
    )
    fetch = cur.fetchone()
    if fetch is None:
        print(f'No such group {group_name}')
        r = False
    if len(path) > 0:  # User wants to update schedule
        if check_sheet(path):
            group_id = fetch[0]
            xl_to_database(
                path=path,
                group_id=group_id,
                conn=conn
            )
            r = True
        else:
            r = False
    if len(new_group_name) > 0:  # User wants to update group name
        cur.execute(
            "UPDATE groups SET groupName = ? WHERE groupName = ?",
            (new_group_name, group_name)
        )
        conn.commit()
        cur.execute(
            "SELECT groupName FROM groups WHERE groupName = ?",
            (new_group_name,)
        )
        if len(cur.fetchall()) > 0:
            r = True
        else:
            r = False

    return r


def generate_template_file():
    """
    Generates .xls file with headers

    :return: Path, where template was saved
    """
    import xlwt
    import os.path
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('schedule')
    path = os.path.dirname(__file__) + '/template.xls'

    headers = ["groupTimeTable", "monday1", "tuesday1", "wednesday1", "thursday1", "friday1", "saturday1", "sunday1",
               "monday2", "tuesday2", "wednesday2", "thursday2", "friday2", "saturday2", "sunday2"]

    for index, value in enumerate(headers):
        sheet.write(
            0,
            index,
            value
        )
    sheet.write(1, 0, '9:00-9:45')  # Just to show the example of how time must be formatted

    workbook.save(path)
    return path
