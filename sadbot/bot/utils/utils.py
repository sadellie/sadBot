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

"""Utilities. Different unsorted functions"""

# Some imports are within functions as they are called only once before shutdown
import datetime
import time
from typing import Union

import xlrd
from xlrd.sheet import Sheet
import xlwt
import os.path
from sqlite3 import Connection, connect, OperationalError


g_h = ["groupTimeTable",
       "monday1", "tuesday1", "wednesday1", "thursday1", "friday1", "saturday1", "sunday1",
       "monday2", "tuesday2", "wednesday2", "thursday2", "friday2", "saturday2", "sunday2"]


class Stats(object):
    """This class is used to have only one instance of some things"""
    _instance = None
    db: Connection = None
    m: int = 0  # Messages
    j: int = 0  # Group chat joins
    c: int = 0  # Callback
    u: int = 0  # Number of users in db
    start_time = datetime.datetime.now()  # Time when the bot was launched
    offset_time = 0  # Difference between local time and VK time

    def __new__(cls,
                db: Connection = None,
                offset_time: int = None):
        """Create new object

        :param c: Connection to database, must be given at least once
        """
        if cls._instance is None:
            cls._instance = super(Stats, cls).__new__(cls)
            # Loading previous stats from db
            try:
                cls.db = db
                cur = cls.db.cursor()
                s = cur.execute("SELECT * FROM stats ORDER BY statDate DESC LIMIT 1").fetchone()
                cls.usr_count()  # Getting current users count
                cls.m = s['statM']
                cls.c = s['statC']
                cls.j = s['statJ']
                cls.offset_time = offset_time
            except TypeError:
                print('stats table is empty')
        return cls._instance

    @classmethod
    def mincr(cls):
        """Increments messages count"""
        cls.m += 1

    @classmethod
    def jincr(cls):
        """Increments group chat joins count"""
        cls.j += 1

    @classmethod
    def cincr(cls):
        """Increments callbacks count"""
        cls.c += 1

    @classmethod
    def uincr(cls):
        """Increments callbacks count"""
        cls.u = len(cls.db.cursor().execute("SELECT * FROM users").fetchall())

    @classmethod
    def usr_count(cls):
        cls.u = len(cls.db.cursor().execute("SELECT * FROM users").fetchall())

    @classmethod
    def offset(cls, o: int):
        t = time.time()
        cls.offset_time = o - t



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
                       s: Stats):
    """
    Record statistics into database

    :param db: Database connection
    :param u: Uptime
    :param m: Messages count
    :param j: Number of joined group chats
    """
    sql = "INSERT INTO stats (statDate, statUptime, statM, statC, statJ) VALUES (?, ?, ?, ?, ?)"
    ut = datetime.datetime.now() - s.start_time
    req = (datetime.datetime.now(), ut.total_seconds(), s.m, s.c, s.j)
    db.cursor().execute(sql, req)
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
        'CREATE TABLE stats (statDate DATE, statUptime TIME, statM INTEGER, statC INTEGER, statJ INTEGER);'
    )

    # Teachers table
    cur.execute(
        'CREATE TABLE teachers (teacherId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, '
        'teacherName TEXT, teacherClassSearchable TEXT, teacherClass TEXT, userId TEXT);'
    )

    # Users table
    cur.execute(
        'CREATE TABLE users (userId TEXT PRIMARY KEY NOT NULL UNIQUE ON CONFLICT REPLACE, '
        'userGroupId INTEGER REFERENCES groups (groupId) ON DELETE CASCADE ON UPDATE CASCADE, '
        'isAdmin BOOLEAN, isBanned BOOLEAN);'
    )

    # Exams table
    cur.execute(
        'CREATE TABLE exams (examId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, examDate DATE, '
        'examName TEXT, examGroup TEXT, examUser INTEGER);'
    )

    db.commit()


def xl_to_sql(file_path: str,
              db: Connection,
              gid: int):
    """Converts xls file to sqlite table. Same as pandas function but has to be reinvented coz hardware limitations
    Since it is custom it made specifically to convert schedules and nothing else
    (will not work properly with other xls files)

    :param file_path: Path to xls file
    :param db: Database connection
    :param gid: Group id
    """
    t_name = f"'group{gid}'"  # Group table name
    cur = db.cursor()  # Cursor
    sheet: Sheet = xlrd.open_workbook(file_path).sheet_by_index(0)  # Sheet with schedule
    columns = sheet.row_slice(0)  # Headers
    n_cl = len(sheet.col_slice(0)) - 1  # Number of classes
    to_ins = []  # Data to insert
    for i in range(1, n_cl + 1):
        sl = sheet.row_slice(i)
        vls = []
        for v in sl:
            vls.append(v.value if v.value != '' else None)
        to_ins.append(vls)

    # Very dumb way to construct sql request and avoid bugs. (had no time to thing of anything else)
    ex = f"CREATE TABLE {t_name} (classId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL"
    head = []  # Collection of table headers
    for item in columns:  # Yep, second loop. Ugly, but works. Probably will improve
        ex += f", {item.value} TEXT"
        head.append(item.value)
    ex += ")"

    # Since we mostly use this function to update existing schedule we try drop the table. On error will just skip it
    try:
        cur.execute(f"DROP TABLE {t_name}")
        print('db is not new')
    except OperationalError as e:
        print('DB is new')

    cur.execute(ex)  # Now we can create a new table

    # Another ugly way to construct request
    head_sq = ', '.join(head)  # Collection of column but separated with comma
    val_sq = ', '.join((len(head) * '?'))  # Some amount of ?

    # Inserting new data
    for d in to_ins:
        com = f"INSERT INTO {t_name} ({head_sq}) VALUES ({val_sq})"
        cur.execute(com, d)
    # All good, can commit now
    db.commit()


def xls_has_errors(file_path: str) -> str:
    """
    Checks sheet for typos in column headers and in groupTimeColumn

    :param file_path: Path to Excel file
    :return: Returns error description or nothing if everything is ok
    """
    sheet = xlrd.open_workbook(file_path).sheet_by_index(0)
    n = datetime.datetime.now()

    for indx, val in enumerate(g_h):
        cell = sheet.cell(0, indx).value
        if cell != val:
            return f"{cell} != {val}"

    for indx, i in enumerate(sheet.col_slice(0, start_rowx=1)):
        v: str = str(i.value)
        try:
            c = v.split('-')
            for x in c:
                x = x.split(':')
                dt = n.replace(hour=int(x[0]), minute=int(x[1]))
        except Exception as e:
            print(e)
            return f'Ошибка в строке {indx+2} в столбце {g_h[0]}, неправильное значение: {i.value}'


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
    if not xls_has_errors(path):
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO groups (groupName) VALUES (?)",
            (group_name,)
        )
        conn.commit()
        cur.execute("SELECT * FROM groups ORDER BY groupId DESC LIMIT 1;")
        fetch = cur.fetchone()
        print(fetch)
        group_id = fetch['groupId']
        xl_to_database(
            path=path,
            group_id=group_id,
            conn=conn,
        )
        return True
    else:
        return False


# Not tested properly
def update_schedule(db: Connection,
                    path: str,
                    g_id: int) -> Union[None, str]:
    """Method to update schdule in database for a group. Basically just convert xls file to sqlite table.

    :param db:
    :param path:
    :param g_id:
    """
    r = db.cursor().execute("SELECT groupId FROM groups WHERE groupId = ?", (g_id,)).fetchone()
    if not r:
        raise RuntimeError('Incorrect group id')
    c = xls_has_errors(path)  # We check if xls file has any sort of errors
    if not c:  # There are bo errors, we can convert it
        xl_to_sql(file_path=path, db=db, gid=g_id)
    else:  # There are some errors
        return c


def update_name(db: Connection,
                g_id: int,
                new: str):
    db.cursor().execute("UPDATE groups SET groupName = ? WHERE groupId = ?", (new, g_id))
    db.commit()


def generate_template_file():
    """
    Generates .xls file with headers

    :return: Path, where template was saved
    """
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('schedule')
    path = os.path.dirname(__file__) + '/template.xls'

    for index, value in enumerate(g_h):
        sheet.write(
            0,
            index,
            value
        )
    sheet.write(1, 0, '9:00-9:45')  # Just to show the example of how time must be formatted

    workbook.save(path)
    return path
