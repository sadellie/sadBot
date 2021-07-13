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

"""Unittest here. Uses temporary database."""

import shutil
import sqlite3
import tempfile
import unittest

from bot.classes import get_class, time_to_next, change_db
from bot.utils.utils import create_database


def create_empty_database(path):
    """
    Creates empty database with all tables.
    Also creates table for group0 with dummy data and registers it in groups table

    :param path: Path where database will be saved
    :return: Returns sqlite3.Connection
    """

    def custom_factory(cursor, row):
        """
        Custom factory, makes working with database operations results easier

        :param cursor: Database Cursor
        :param row: Row, idk...
        :return: Dictionary
        """
        cf = {}
        for i, j in enumerate(cursor.description):
            cf[j[0]] = row[i]
        return cf

    conn = sqlite3.connect(path + '/test.db')
    conn.row_factory = custom_factory
    create_database(conn)
    cur = conn.cursor()

    cur.execute(
        'CREATE TABLE group0 (classId INTEGER PRIMARY KEY AUTOINCREMENT, groupTimeTable TEXT, '
        'monday1 TEXT, tuesday1 TEXT, wednesday1 TEXT, thursday1 TEXT, friday1 TEXT, saturday1 TEXT, sunday1 TEXT, '
        'monday2 TEXT, tuesday2 TEXT, wednesday2 TEXT, thursday2 TEXT, friday2 TEXT, saturday2 TEXT, sunday2 TEXT);'
    )
    cur.execute(
        "INSERT INTO groups (groupId, groupName) "
        "VALUES (?, ?);",
        (0, 'testGroup')
    )

    # One class is 1 hour 20 minutes + 10 minutes break between classes
    timings = ['9:00-10:20', '10:30-11:50', '12:00-13:20', '13:30-14:50', '15:00-16:20', '16:30-17:50']

    for t in range(1, 7):
        actual_start = timings[t - 1]
        start = t * 10 + 1
        end = t * 10 + 15
        values = [actual_start]
        for x in range(start, end):
            values.append(x)
        cur.execute(
            "INSERT INTO group0 (groupTimeTable,"
            "monday1, tuesday1, wednesday1, thursday1, friday1, saturday1, sunday1, "
            "monday2, tuesday2, wednesday2, thursday2, friday2, saturday2, sunday2) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            values
        )

    conn.commit()
    print('Created temporary database')
    return conn


def permission_error_fix(path):
    """
    Changes permission so directory can be deleted

    :param path: path to directory
    """
    import os
    import _stat
    try:
        os.chmod(path, _stat.S_IWUSR)
    except Exception as e:
        print(e)
        raise


class TodayClass(unittest.TestCase):
    conn: sqlite3.Connection
    test_dir: str

    @classmethod
    def setUpClass(cls):
        """
        Creates temporary directory and creates database with dummy data in it.
        Also changes current date, so results will not be affected by date.
        """
        cls.test_dir = tempfile.mkdtemp()
        print(cls.test_dir)
        cls.conn = create_empty_database(cls.test_dir)
        cls.cur = cls.conn.cursor()
        cls.custom_day = [15, 10, 2020]
        change_db(cls.conn)

    @classmethod
    def tearDownClass(cls):
        """
        Deletes temporary directory with database
        """
        print('Deleting temporary directory...')
        cls.conn.close()
        shutil.rmtree(cls.test_dir, onerror=permission_error_fix(cls.test_dir))
        print("Temporary directory was deleted")

    def test_get_time_to_next_before(self):
        """
        Must return 1h 5m
        """
        result = time_to_next(
            g=0,
            custom_time=[7, 55]
        )
        self.assertEqual(result, '⏰ Звонок через 1 ч. 5 мин.')

    def test_get_time_to_next_during(self):
        """
        Must return 20m
        """
        result = time_to_next(
            g=0,
            custom_time=[10, 00]
        )
        self.assertEqual(result, '⏰ Звонок через 20 мин.')

    def test_get_time_to_next_between(self):
        """
        Must return 9m
        """
        result = time_to_next(
            g=0,
            custom_time=[10, 21]
        )
        self.assertEqual(result, '⏰ Звонок через 9 мин.')

    def test_get_time_to_next_during_last(self):
        """
        Must return 1m
        """
        result = time_to_next(
            g=0,
            custom_time=[17, 49]
        )
        self.assertEqual(result, '⏰ Звонок через 1 мин.')

    def test_get_time_to_next_after_last(self):
        """
        Must return no classes
        """
        result = time_to_next(
            g=0,
            custom_time=[17, 55]
        )
        self.assertEqual(result, '❌ Больше пар нет')

    def test_get_before_class(self):
        """
        Must return 1st class
        """
        result = get_class(
            p=0,
            custom_time=[8, 59],
            custom_day=self.custom_day
        )
        self.assertEqual(result[2:], 'Пара 1 (в 9:00):\n21')

    def test_get_first_class(self):
        """
        Must return 1st class
        """
        result = get_class(
            p=0,
            custom_time=[9, 15],
            custom_day=self.custom_day
        )
        self.assertEqual(result[2:], 'Пара 1 (в 9:00):\n21')

    def test_get_class_after_second_class_during_break(self):
        """
        Must return 3rd class
        """
        result = get_class(
            p=0,
            custom_time=[11, 51],
            custom_day=self.custom_day
        )
        self.assertEqual(result[2:], 'Пара 3 (в 12:00):\n41')

    def test_get_third_class(self):
        """
        Must return 3rd class
        """
        result = get_class(
            p=0,
            custom_time=[13, 00],
            custom_day=self.custom_day
        )
        self.assertEqual(result[2:], 'Пара 3 (в 12:00):\n41')

    def test_get_last_class(self):
        """
        Must return last class (6th)
        """
        result = get_class(
            p=0,
            custom_time=[17, 40],
            custom_day=self.custom_day
        )
        self.assertEqual(result[2:], 'Пара 6 (в 16:30):\n71')


class NextClass(unittest.TestCase):
    conn: sqlite3.Connection
    test_dir: str

    @classmethod
    def setUpClass(cls):
        """
        Creates temporary directory and creates database with dummy data in it.
        Also changes current date, so results will not be affected by date.
        """
        # We create temporary database and test fill it with dummy data
        cls.test_dir = tempfile.mkdtemp()
        print(cls.test_dir)
        cls.conn = create_empty_database(cls.test_dir)
        cls.cur = cls.conn.cursor()
        change_db(cls.conn)

        cls.custom_day = [15, 10, 2020]

    @classmethod
    def tearDownClass(cls):
        """
        Deletes temporary directory with database
        """
        print('Deleting temporary directory...')
        cls.conn.close()
        shutil.rmtree(cls.test_dir, onerror=permission_error_fix(cls.test_dir))

    def test_get_after_classes(self):
        """
        Must return no classes
        """
        result = get_class(
            p=0,
            custom_time=[17, 51],
            custom_day=self.custom_day
        )
        self.assertEqual(result, '❌ Больше пар нет')

    def test_get_next_class_before_first(self):
        """
        Must return 2nd class
        """
        result = get_class(
            p=0,
            modifier=1,
            custom_time=[8, 59],
            custom_day=self.custom_day
        )
        # Everything before first class start time is first class.
        # If it's 8:59, but 1st class starts at 9:00 it still counts as 1st class
        self.assertEqual(result[2:], 'Пара 2 (в 10:30):\n31')

    def test_get_next_class_after_first(self):
        """
        Must return 3rd class
        """
        result = get_class(
            p=0,
            modifier=1,
            custom_time=[10, 21],  # Time is 10:21, 1st class has just ended
            custom_day=self.custom_day
        )
        self.assertEqual(result[2:], 'Пара 3 (в 12:00):\n41')

    def test_get_next_class_last(self):
        """
        Must return last class message
        """
        result = get_class(
            p=0,
            modifier=1,
            custom_time=[17, 49],  # It's last class for today, so nothing comes after it
            custom_day=self.custom_day
        )
        self.assertEqual(result, '❌ Сейчас последняя пара, дальше ничего нет')

    def test_get_next_class_after_last(self):
        """
        Must return no classes
        """
        result = get_class(
            p=0,
            modifier=1,
            custom_time=[17, 51],  # Last class has just ended
            custom_day=self.custom_day
        )
        self.assertEqual(result, '❌ Больше пар нет')


if __name__ == '__main__':
    unittest.main(
        failfast=False,
        catchbreak=False
    )
