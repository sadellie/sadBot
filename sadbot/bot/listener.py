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

"""Event Listener"""

import asyncio
import datetime
import logging

from vkbottle import Bot, LoopWrapper

from bot.base import db, cp, stats
from bot.blueprints import bps
from bot.utils.utils import record_stats

sad_bot = Bot(cp['DEFAULT']['Token'])  # Passing token from config file
lw = LoopWrapper()


async def sleep_for(freq: int):
    n = datetime.datetime.now()
    a = freq + freq * divmod(n.hour, freq)[0]  # At what time to start recording stats
    if a == 24:
        t = n.replace(day=n.day + 1, hour=0, minute=0, second=0, microsecond=0)
    else:
        t = n.replace(hour=a, minute=0, second=0, microsecond=0)
    d = (t - n).total_seconds()
    logging.info(f'Will start to record stats at {t} in {d} seconds')
    return d


async def stat_write(freq: int):
    """Write stats every N hours"""
    # TODO Update sad_replias for no f_cking reason

    stats.offset((await sad_bot.api.utils.get_server_time()))  # Checking time on VK server
    while True:
        # We need to correct the amount of seconds every call to prevent shift
        await asyncio.sleep(await sleep_for(freq))
        # FIXME This is dumb just increment this value after succesful registration
        stats.usr_count()  # Updating the number of users. We defenitely do not want to call this too often so it is here
        await record_stats(db, stats)
        logging.info('Recorded a stat')


def start_listening():
    """
    Start listening to events. Will work non-stop
    """
    for bp in bps:
        bp.load(sad_bot)

    l = asyncio.get_event_loop()
    l.create_task(stat_write(int(cp['DEFAULT']['StatFreq'])))
    l.create_task(sad_bot.run_polling())
    l.run_forever()
