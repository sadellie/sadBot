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
Everything related to teachers
"""
from sqlite3 import Cursor, Connection


def add_teacher(cur: Cursor, db: Connection, req: str, user_id: str):
    """
    Add teacher to database
    
    :param user_id: User id, who is adding
    :param cur: Cursor
    :param db: Database
    :param req: Request. For example, пример: '/добавь Имя Препода=Предмет'
    :return: Result
    """
    try:
        if req.lower() == "/добавь имя=предмет":
            return "🤬 Когда ИИ захватит мир, к тебе придут первым... [Имя=Предмет это лишь пример, дятел]"
        # We delete command '/добавь' and create list, where 0 is Teacher, and 1 is Class
        req = req[8:].split("=")
        req = (req[0], req[1], req[1].lower(), user_id)  # Teacher, Class, Tags(same as class by default)
        sql = '''INSERT INTO teachers (teacherName, teacherClass, teacherClassSearchable, userId) VALUES (?, ?, ?, ?)'''
        cur.execute(sql, req)
        db.commit()
        return req[0] + " преподаёт " + req[1] + ", понял"
    except Exception as e:
        print(str(e))
        return "/добавь Имя=Препод \nТак сложно запомнить?"


def delete_teacher(cur: Cursor, db: Connection, req: str, user_id: str):
    """
    Delete teacher from database

    :param cur: Cursor
    :param db: Database
    :param req: Request, class name
    :param user_id: User id
    :return: Result (success or fail)
    """
    try:
        req_to_find = (req[7:],)
        sql_to_find = "SELECT userId FROM teachers WHERE teacherClass = (?)"
        find = cur.execute(sql_to_find, req_to_find).fetchall()
        if len(find) > 0:
            users = []
            for i in find:
                users.append(i['userId'])
            if user_id in users:
                req_to_delete = (req[7:], user_id)
                sql = "DELETE FROM teachers WHERE teacherClass == ? AND userId == ?"
                cur.execute(sql, req_to_delete)
                db.commit()
                return "Готово, теперь его никто не найдёт..."
            else:
                return "Не ты добавлял, сорян"
        else:
            return "Такого не знаю [мне нужно полное название предмета]"
    except Exception as e:
        print(e)
        return "Я сломался, твоя очередь..."


def find_teacher(cur: Cursor, req: str):
    """
    Find teacher

    :param req: Request
    :param cur: Cursor
    :return: Search result as string
    """
    req_f = "%" + req[8:].lower() + "%"
    if len(req_f) < 3:
        return "Маловато символов"
    try:
        sql = "SELECT * FROM teachers WHERE teacherClassSearchable LIKE ?"
        # cur.execute("SELECT * FROM teachers WHERE teacherClassSearchable LIKE '%" + req_f + "%'")
        qwe = (req_f,)
        cur.execute(sql, qwe)
        res = cur.fetchall()
        print(res)
        out = ""
        for counter, i in enumerate(res):
            out = out + "\n" + str(counter+1) + ". " + str(i['teacherName'] + "\n(" + str(i['teacherClass']) + ")")
        print("RESULTS" + str(out))
        if not out:
            return "🤷🏼‍♂️ Я не знаю кто преподаёт {g}, может сам добавишь, когда узнаешь?\n\n" \
                   "Спроси у меня 'Как добавить?'".format(g=req[8:])
        return "🔍 Результаты поиска: " + out
    except Exception as exc:
        print("Find error " + str(exc))
        return "❌ Кто-то упал... ой, это я..."
