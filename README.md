![Cover](./project_files/pics/Cover.png)
# About
Чат бот для студентов

# Основные функции
### Начало
Начало работы с ботом. Также можно просто воспользоваться дефолтной клавиатурой бота.<br>
> Start <br>
> Начать <br>

### Регистрация
Бот работает только с теми, кто состоит в учебной группе.<br>
> /группа **[Название учебной группы]**<br>

### Список групп
Можно получить список учебных групп. Если вашей группы нет, то пишите в ЛС.<br>
> /список <br>

## Расписание

### Пары сегодня
Получить расписание на целый день.<br>
> /сегодня <br>

### Пары завтра
Заглянуть в завтрашний день и узнать пары.<br>
> /завтра <br>

### Пары в другой день
Если нужно узнать какие пары будут через n дней.<br>
> /пары  **[Количество дней]**<br>

Например, чтобы узнать, какие пары будут через 3 дня, нужно отправить
> /пары  **3**<br>

### Пара сейчас
Покажет snackbar с текущей парой (для десктопа отправит сообщение).<br>
> /сейчас <br>

### Следующая пара
То же самое, но со следующей парой.<br>
> /далее <br>

### Неделя?
Узнать какая сейчас неделя (верхняя или нижняя).<br>
> /неделя <br>

### Когда звонок?
Узнать через сколько минут звонок.<br>
> /звонок <br>

## Препод
### Поиск
Найдёт имя препода по названию его предмета.<br>
> /препод **[Предмет]**<br>

### Добавление
Если кого-то не хватает, то можно добавить самому.<br>
> /добавь **[Препод=Предмет]**<br>

### Удаление
Накосячил, когда добавлял препода? Хотя бы эту ошибку можно исправить...<br>
> /удали **[Препод=Предмет]**<br>

## Важное сообщение
Сделать объявление на весь чат (@everyone).<br>
> /важно **[Сообщение]**<br>

# Помощь
### Карусель, карусель...
Карусель с самым необходимым.<br>
> /помощь <br>

# Misc.
## Клавиатура бота
### Показать клавиатуру
Обычно она показывается после регистрации, но вдруг...<br>
> /кнопки вкл <br>

### Скрыть клавиатуру
Не нравится клавиатура? (Клавиатура пропадёт для всех участников чата)<br>
> /кнопки выкл <br>

## Uptime
Бот отправит аптайм<br>
> /ping <br>

## Random reply
Бот что-то отправит...<br>
> sadbot <br>

## Остановить работу бот (отключено)
Требуются права админа. Сохраняет анонимную статистику и убивает бота.
> Стоп <br>
> Stop <br>
> Kill <br>

# Console commands
Если вы хотите запустить бота у себя. <br>
`--initiate` Создаст пустую базу данных и добавит в неё group0, чтобы вы сразу могли внести изменения. 
Не забудьте отредактировать расписание звонков в groups. <br>
`--generate_template` Создаст пустой .xls файл, необходимый для регистрации новой группы. 
Отредактируйте его, заполнив туда ваше расписание для верхней и нижней недели в соответсвии с заголовком столбца. 
1 означает нижняя неделя, 2 — верхняя. <br>
`--register_new_group` Добавит новую группу в базу данных. Требуется .xls файл (см. выше). <br>
`--update_group` Обновит расписание и/или название группы <br>
`--start` Запустит бота. Не забудьте проверить config.py <br>
# Credits:
#### Design
defaulterror (Derek Clark): [Commando Font](https://www.dafont.com/commando.font) <br>
Gary D. Jessey: [Art Brush](https://www.dafont.com/artbrush.font) <br>