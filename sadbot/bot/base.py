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

"""Base module"""
import asyncio
import configparser
import logging.config
from pathlib import Path

from bot.utils.utils import connect_to_database, Stats

work_dir = Path(__file__)

# Setting up config and logging
cp = configparser.ConfigParser()
cp.read(str(work_dir.parent.parent) + '/config.ini', encoding='utf-8')  # Reading config file
logging.config.fileConfig(cp, disable_existing_loggers=False)  # Setting up logging

# Setting up download directory
dd = str(work_dir.parent) + cp['DEFAULT']['DownloadDir']
Path(dd).mkdir(exist_ok=True)

club_id = int(cp['DEFAULT']['Club_id'])  # VK Group club id
db = connect_to_database(str(work_dir.parent) + cp['DEFAULT']['DatabaseName'])  # Database connection

stats = Stats(db)  # Init it here, singleton
