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
Everything related to pandas and table management
"""
import sqlite3
import pandas as pd


def remove_table(cur: sqlite3.Cursor, old_table: str):
    """
    Remove table from database

    :param cur: Cursor
    :param old_table: Table name
    """
    try:
        cur.execute("DROP TABLE '" + old_table + "'")
        cur.fetchall()
    except Exception as e:
        print("Error while removing table: " + str(e))


def rename_table(cur: sqlite3.Cursor, old_table: str, new_table: str):
    """
    Rename table in database

    :param cur: Cursor
    :param old_table: Old table name
    :param new_table: New table name
    """
    try:
        cur.execute("ALTER TABLE '" + old_table + "' RENAME TO '" + new_table + "'")
        cur.fetchall()
    except Exception as e:
        print("Error while renaming table: " + str(e))


def add_table(table_name: str, db: sqlite3.Connection, file):
    """
    Convert Excel file to table and add it to database

    :param table_name: Table name
    :param db: Database
    :param file: Excel file
    """
    # Errors and logs
    dfs: pd.DataFrame = pd.read_excel(file, sheet_name=None)
    for table, df in dfs.items():
        df.to_sql(name=str(table_name), con=db, index_label="classId", if_exists='replace')
    print("Table has been added")
