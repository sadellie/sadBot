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
from typing import Union

from vkbottle import Bot
from vkbottle.bot import rules, Message

from sadbot.base_vocabulary import r_important_ok, r_important_not_ok, r_important_template, r_register_fail, \
    r_register_success
from utils.element_builders import kb_imp_builder
from utils.utils import get_random


class UserClass:
    """
    User class which represents one user(yes floor is made of floor)
    """

    def __init__(self, user_id: int, group_peer_id: int, is_admin: bool):
        self.user_id = user_id
        self.group_peer_id = group_peer_id
        self.is_admin = is_admin


class GroupClass:
    """
    Class which represents one group
    """
    def __init__(self,
                 group_id: str,
                 group_name: str):
        self.group_id = group_id
        self.group_name = group_name


def get_user(cur: Cursor, user_id: int = 0):
    """
    Get user from database

    :param cur: Cursor
    :param user_id: User id
    :return: Ready to use UserClass
    """
    cur.execute("SELECT * from users WHERE userId=?", (user_id,))
    res = cur.fetchall()
    if len(res) > 0:
        res = res[0]
        return UserClass(res['userId'], res['groupPeerId'], res['isAdmin'])
    else:
        return None


def register_user(db: Connection,
                  user_id: int,
                  group_name: str):
    """
    Register user or chat. Add it to database

    :param db: Database
    :param user_id: User id (peer_id if it's called in group')
    :param group_name: Group name in database
    """
    cur = db.cursor()
    find_res = find_group_by_name(cur, group_name)

    # First we check if requested group exists in database
    if find_res is not None:  # Requested group is in database
        sql = "INSERT INTO users (userId, groupPeerId) VALUES (?, ?)"
        values = (user_id, find_res.group_id)
        cur.execute(sql, values)
        db.commit()
        return r_register_success
    else:
        return r_register_fail.format(group_name)


def find_group_by_name(cur: Cursor, group_name: str):
    """
    Find group in database by given name

    :param cur: Database Cursor
    :param group_name: Group name
    :return: Returns first found group
    """
    cur.execute("SELECT * from groups WHERE groupName=?", (group_name,))
    res = cur.fetchone()
    if res is not None:  # Found group
        return GroupClass(res['groupId'], res['groupName'])


def get_all_groups(cursor: Cursor, names: bool = False):
    """
    Get all groups from database

    :param cursor: Cursor
    :param names: If true will return only list of group names
    :return: List of groups
    """
    sql_result = cursor.execute("SELECT * FROM groups").fetchall()
    result = []
    if names:
        for i in sql_result:
            result.append(i['groupName'])
    else:
        for i in sql_result:
            result.append(GroupClass(i['groupId'], i['groupName']))
    return result


def get_all_groups_formatted(cur: Cursor) -> str:
    """
    Get formatted string with all groups

    :param cur: Cursor
    :return: Formatted string
    """
    all_group_names = get_all_groups(cur)
    result: str = "Список доступных групп:"
    for index, group in enumerate(all_group_names):
        result += f"\n{index + 1}. {group.group_name}"
    return result


class ImportantMessage:
    """
    Class for important message. Represents one message for each group chat
    """

    def __init__(self,
                 message: str,
                 payload: str,
                 users: list):
        self.message = message
        self.payload = payload
        self.users = users


class ImportantMessagesCollection:
    """
    Class for a collection of ImportantMessages.
    """

    def __init__(self):
        self.all: dict[int, ImportantMessage] = {}

    def add_new_important_message(self,
                                  peer_id: int,
                                  text: str):
        """
        Adds important message to collection

        :param peer_id: Peer_id of group chat
        :param text: Text of important message
        :return: Formatted reply and new inline keyboard
        """
        r = str(get_random())
        message = r_important_template.format(m=text)
        important_mes = ImportantMessage(message=message,
                                         payload=r,
                                         users=[])
        self.all.update({peer_id: important_mes})
        return message, kb_imp_builder(r)

    async def imp(self,
                  bot: Union[Bot],
                  user_id: int,
                  peer_id: int,
                  message_id: int) -> str:
        """
        IMPORTANT function. Reacts to button clicks.

        :param bot: Bot (from vkbottle)
        :param user_id: User_id (who clicked)
        :param peer_id: Chat peer_id (where it was clicked)
        :param message_id: Message_id (which message was clicked and will be edited)
        :return: Result
        """

        u_info = await bot.api.users.get(user_ids=[user_id])
        f_name = u_info[0].first_name
        l_name = u_info[0].last_name
        m = self.all[peer_id]
        if user_id in m.users:  # Check if user has already clicked the button
            return r_important_not_ok.format(f_name)
        else:  # User has never clicked this button
            # Adding user name to the end of the message
            m.users.append(user_id)
            message_local = f"{m.message}\n{f_name} {l_name[0]}."
            self.all.update(
                {
                    peer_id: ImportantMessage(
                        message=message_local,
                        payload=m.payload,
                        users=m.users
                    )
                }
            )
            # Finally we can edit the message
            await bot.api.messages.edit(peer_id=peer_id,
                                        message=message_local,
                                        conversation_message_id=message_id,
                                        keyboard=kb_imp_builder(m.payload))
            return r_important_ok


class OnlyRegistered(rules.ABCMessageRule):
    """
    Rule which makes some features available only for registered in local database users
    """

    def __init__(self, conn: Connection):
        self.conn = conn

    async def check(self, message: Message):
        """
        Checks if user is in database

        :param message: Incoming Message object
        :return: Returns True if check is passed. False if not.
        """
        if get_user(self.conn.cursor(), message.peer_id) is not None:
            return True
        return False