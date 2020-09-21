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

"""Everything related to users and groups"""
from sqlite3 import Connection, Cursor


class UserClass:
    """
    User class which represents one user(yes floor is made of floor)
    """

    def __init__(self, user_id: str, group_peer_id: str, group_name: str, is_admin: bool):
        self.user_id = user_id
        self.group_peer_id = group_peer_id
        self.group_name = group_name
        self.is_admin = is_admin


class Group:
    """
    group_uid: Unique group id in database (not same as group id)
    group_name: Group name
    """

    def __init__(self, group_uid, group_name: str):
        self.group_uid = group_uid
        self.group_name = group_name


def get_user(cur: Cursor, user_id: str = "", only_admin_ids: bool = False):
    """
    Get user from database
    
    :param only_admin_ids: If True will return lsit of admins' ids
    :param cur: Cursor
    :param user_id: User id
    :return: Ready to use UserClass
    """
    if only_admin_ids:
        res = []
        sql = "SELECT userId FROM users WHERE isAdmin == '1'"  # 1 means admin

        for i in cur.execute(sql).fetchall():
            res.append(i['userId'])
        return res
    else:
        cur.execute("SELECT * from users WHERE userId=" + str(user_id))
        res = cur.fetchall()
        if len(res) > 0:
            res = res[0]
            return UserClass(res['userId'], res['groupPeerId'], res['groupName'], res['isAdmin'])
        else:
            return None


def register_user(db: Connection, cur: Cursor, user_id: str, group_uid: str, group_name: str):
    """
    Register user or chat. Add it to database

    :param db: Database
    :param cur: Cursor
    :param user_id: User id (peer_id if it's called in group')
    :param group_uid: Group uid
    :param group_name: Group name, where to register
    """
    sql = '''INSERT INTO users (userId, groupPeerId, groupName) VALUES (?, ?, ?)'''
    values = (user_id, group_uid, group_name)
    cur.execute(sql, values)
    db.commit()


def get_all_groups(cursor: Cursor):
    """
    Get all groups from database

    :param cursor: Cursor
    :return: List of groups
    """
    sql_result = cursor.execute("SELECT * FROM groups").fetchall()
    ids = []
    names = []
    for i in sql_result:
        ids.append(i['groupId'])
        names.append(i['groupName'])

    return ids, names
