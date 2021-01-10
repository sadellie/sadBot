import sqlite3
from datetime import datetime
from .base_vocabulary import months


def add_exam(db: sqlite3.Connection,
             r: str,
             g: int,
             u: int):
    """Add exam to database

    :param db: Connection to database
    :param r: Request
    :param g: Group uid in database
    :param u: User ID who added the exam
    :return:
    """
    request = r.split('=')

    # Must be 2 parameters examDate and examGroup
    if len(request) < 2:
        return 'Not enough parameters'
    exam_date = datetime.strptime(request[0], "%d-%m-%Y %H:%M")  # Convert into datetime to be sure it has no errors
    sql = "INSERT INTO exams (examDate, examName, examGroup, examUser) VALUES (?, ?, ?, ?)"
    db.cursor().execute(sql, (exam_date.strftime('%Y%m%d%H%M'), request[1], g, u))
    return db.commit()


def get_next_exam(group: int,
                  limit: int,
                  cur: sqlite3.Cursor):
    """Get nearest exams

    :param group: Group uid
    :param limit: How many exams do we need
    :param cur: Database cursor
    :return:
    """
    today = datetime.today().strftime("%Y%m%d%H%M")
    cur.execute(
        'SELECT * FROM exams WHERE (exam_date > ?) AND (exam_group = ?) ORDER BY exam_date LIMIT ?',
        (today, group, limit))
    res = cur.fetchall()
    out = []
    for i in res:
        e_d = datetime.strptime(str(i['exam_date']), "%Y%m%d%H%M")
        e_t = e_d.strftime("%H:%M")
        out.append(f'📝 Экзамен {e_d.day} {months[e_d.month-1]} в {e_t}\n{i["exam_name"]}')
    if len(res) == 0:
        return 'Экзаменов больше нет'
    return '\n\n'.join(out)
