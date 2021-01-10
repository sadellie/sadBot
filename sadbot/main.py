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
import configparser
import sqlite3
import sys
from pathlib import Path

from bot.utils import utils


def main():
    """
    Main function expects to receive arguments. Otherwise will show help
    """
    import os
    cp = configparser.ConfigParser()
    cp.read(os.path.join(sys.path[0], 'config.ini'), encoding='utf-8')
    dp = os.path.join(sys.path[0] + cp['DEFAULT']['DatabaseName'])

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
    parser.add_argument("--update_group",
                        help="Update group schedule and/or name",
                        action="store_true")
    parser.add_argument("--start",
                        help="Start listening",
                        action="store_true")
    args = parser.parse_args()

    if args.initiate:
        import os
        import warnings
        d_path = Path(dp)
        try:
            os.mkdir(d_path.parent)
        except FileExistsError:
            warnings.warn('Folder already exists')

        conn = sqlite3.connect(dp)
        utils.create_database(conn)
        print('DATABASE FILE WAS CREATED. YOU CAN NOW OPEN IT IN EDITOR')
        conn.close()

    elif args.register_new_group:
        print("Use --generate_template_file to create template .xls file where you can enter your schedule")
        print("Path to .xls file with schedule:")
        path = input()
        print("Name of the group")
        group_name = input()
        conn = sqlite3.connect(dp)
        result = utils.register_new_group(conn=conn, path=path, group_name=group_name)
        print("Done" if result else "Something went wrong. See output above")

    elif args.update_group:
        print("Use --generate_template_file to create template .xls file where you can enter your schedule")
        print("Path to .xls file with schedule. Leave empty if you don't want to change it:")
        path = input()
        print("Old name of the group.")
        group_name = input()
        print("New name of the group. Leave empty if you don't want to change it")
        new_group_name = input()
        conn = sqlite3.connect(dp)
        result = utils.update_group(
            conn=conn,
            path=path,
            group_name=group_name,
            new_group_name=new_group_name
        )
        print("Done" if result else "Something went wrong")

    elif args.generate_template:
        print(f"Done. Template file is here:\n{utils.generate_template_file()}")

    elif args.start:
        from bot.listener import start_listening
        start_listening()

    else:
        print("Type -h for help")


if __name__ == "__main__":
    main()
