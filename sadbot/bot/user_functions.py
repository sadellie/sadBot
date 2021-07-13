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

"""Everything related to users and groups"""

from vkbottle.bot import rules, Message
from vkbottle_types.events import MessageEvent

from bot.base import db, stats

cur = db.cursor()


class UserClass:
    """User class which represents one user in database"""

    def __init__(self,
                 user_id: int,
                 group_peer_id: int,
                 is_admin: bool,
                 is_banned: bool):
        self.user_id = user_id
        self.group_peer_id = group_peer_id
        self.is_admin = is_admin
        self.is_banned = is_banned


class GroupClass:
    """Class to represent a teaching group"""

    def __init__(self,
                 group_id: int,
                 name: str,
                 admin_id: int):
        self.group_id = group_id
        self.name = name
        self.admin_id = admin_id


async def get_user(user_id: int):
    """
    Get user from database

    :param user_id: User id
    :return: Ready to use UserClass
    """
    cur.execute("SELECT * from users WHERE userId=?", (user_id,))
    res = cur.fetchall()
    if len(res) > 0:
        res = res[0]
        return UserClass(int(res['userId']),
                         int(res['userGroupId']),
                         True if res['isAdmin'] == 1 else False,
                         True if res['isBanned'] == 1 else False)


def register_user(user_id: int,
                  group_id: int):
    """
    Register user or chat. Add it to database

    :param user_id: User id (peer_id if it's called in group')
    :param group_id: Group name in database
    """
    find_res = cur.execute("SELECT * FROM groups WHERE groupId=?", (group_id,)).fetchone()
    # First we check if requested group exists in database
    if find_res is not None:  # Requested group is in database
        sql = "INSERT INTO users (userId, userGroupId) VALUES (?, ?)"
        values = (user_id, group_id)
        cur.execute(sql, values)
        db.commit()
        stats.uincr()
        return find_res['groupName']


async def get_group_by_user(user_id: int):
    """Gets name of the group of a specific user

    :param user_id: UserID (peer id for group chats)
    :return: Name of the group
    """
    u = await get_user(user_id)
    if u:
        g = db.cursor().execute("SELECT * FROM groups WHERE groupId=?", (u.group_peer_id,)).fetchone()
        return GroupClass(group_id=g['groupId'],
                          name=g['groupName'],
                          admin_id=g['groupAdmin'])


def get_all_groups_formatted():
    """
    Get formatted string with all groups

    :return: Formatted string
    """
    return '\n'.join(f"{g['groupId']}. {g['groupName']}" for g in cur.execute('SELECT * FROM groups').fetchall())


class BannedRule(rules.ABCMessageRule):
    """Exclude banned users"""

    async def check(self, message: Message):
        """Check if user is banned

        :param message: Message object
        :return: False if banned
        """
        u = await get_user(message.peer_id)
        if u is None:
            return True
        else:
            return not u.is_banned


class OnlyRegistered(rules.ABCMessageRule):
    """
    Rule which makes some features available only for registered in local database users
    """

    async def check(self, message: Message):
        """
        Checks if user is in database

        :param message: Incoming Message object
        :return: Returns True if check is passed. False if not.
        """
        if isinstance(message, Message):
            p = message.peer_id
        elif isinstance(message, MessageEvent):
            p = message.object.peer_id
        else:
            return False
        u = await get_user(p)
        if u is not None:
            return not u.is_banned
        return False


class OnlyAdmin(rules.ABCMessageRule):
    """
    Rule which makes some features available only for admins
    """

    async def check(self, message: Message):
        """
        Checks if user is an admin

        :param message: Incoming Message object
        :return: Returns True if check is passed. False if not.
        """
        u = await get_user(message.peer_id)
        if u is not None:
            return u.is_admin
        return False
