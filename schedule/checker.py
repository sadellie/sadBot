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
Файл с функциями для проверки всего. От файлов для обновления расписания, до юзера (находится ли он в базе)
"""
import xlrd
import requests
from os.path import dirname

# Папка с файлами
directory = dirname(__file__)

# Список нужных названий заголовков таблиц
check = ["monday1", "tuesday1", "wednesday1", "thursday1", "friday1", "saturday1", "sunday1",
         "monday2", "tuesday2", "wednesday2", "thursday2", "friday2", "saturday2", "sunday2"]


def download_sheet(url: str, filename: str):
    """Функция, чтобы скачать .xlsx файл в папку
    :param url: Url откуда скачивать
    :param filename: Название файла
    :return: Возвращает директорию, в которой находится скачаенный файл
    """
    docu = requests.get(url)
    path = directory + filename
    g = open(path, "wb")
    g.write(docu.content)
    g.close()
    return path


def open_sheet(file):
    """Функция, чтобы открыть первый лист Excel файлы
    :param file: Файл Excel
    :return: Содержимое первой страницы
    """
    sheet = xlrd.open_workbook(file).sheet_by_index(0)
    return sheet


def check_sheet(url: str, name: str):
    """Функция, которая проверяет заголовки таблицы с checker
    :param url: Url, по которому будет скачан файл для проверка (параметр нужен лишь для download_sheet())
    :param name: Имя файла, для download_sheet()
    :return: Возвращает результат проверки файла. 'Ошибка ... ...' если есть ошибка, 'OK RESULT', если всё ОК
    """
    path = download_sheet(url, name)
    rd = open_sheet(path)

    for idx, val in enumerate(check):
        if rd.cell(0, idx).value != val:
            # Значениме в заголовке табллицы не совпадает с необходимым
            print("Checker ERROR: text doesn't match with" + val)
            return "Ошибка в названии столбца " + str(idx + 1) + ". Должно быть " + val
        else:
            return "OK RESULT"
