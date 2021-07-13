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

"""
Main file. Run it and provide some arguments.
-h for help
"""

import argparse
import asyncio
import warnings
from pathlib import Path

from bot.base import db, cp
from bot.utils import utils


def main():
    """
    Main function expects to receive arguments. Otherwise will show help
    """

    if cp['DEFAULT']['Token'] == '':
        warnings.warn("Don't forget to add your bot token in config.ini!")

    parser = argparse.ArgumentParser()
    parser.add_argument("--initiate",
                        help="Create empty database",
                        action="store_true")
    parser.add_argument("--generate_template",
                        help="Generate template .xlsx file",
                        action="store_true")
    parser.add_argument("--register_new_group",
                        help="Register new group",
                        action="store_true")
    parser.add_argument("--update_group_schedule",
                        help="Update group schedule",
                        action="store_true")
    parser.add_argument("--update_group_name",
                        help="Update group name",
                        action="store_true")
    parser.add_argument("--start",
                        help="Start listening",
                        action="store_true")
    args = parser.parse_args()

    if args.initiate:
        import os
        d_path = Path(cp['DEFAULT']['DatabaseName'])
        try:
            os.mkdir(d_path.parent)
        except FileExistsError:
            warnings.warn('Folder already exists')
        utils.create_database(db)
        print('DATABASE FILE WAS CREATED. YOU CAN NOW OPEN IT IN EDITOR')
        db.close()

    elif args.register_new_group:
        print("Use --generate_template_file to create template .xls file where you can enter your schedule")
        path = input("Path to .xls file with schedule:")
        group_name = input("Name of the group")
        result = utils.register_new_group(conn=db, path=path, group_name=group_name)
        print("Done" if result else "Something went wrong. See output above")

    elif args.update_group_schedule:
        path = input('Path to .xls file')
        g_id = input('Group id')
        utils.update_schedule(db, path, int(g_id))

    elif args.update_group_name:
        g_id = input('Group id')
        n = input('New name')
        utils.update_name(db, g_id, n)

    elif args.generate_template:
        print(f"Done. Template file is here:\n{utils.generate_template_file()}")

    elif args.start:
        from bot.listener import start_listening
        start_listening()

    else:
        print("Type -h for help")


if __name__ == "__main__":
    main()
