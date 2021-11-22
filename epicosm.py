
#~ Standard library imports
import os
import sys
import subprocess
import glob
import json
import time
import datetime
import argparse
import signal

#~ 3rd party imports
import schedule
import pymongo
from retry import retry
import requests
from requests.exceptions import *
from alive_progress import alive_bar

#~ Local application imports
from modules import (
    mongo_ops,
    epicosm_meta,
    twitter_ops,
    follows_ops,
    env_config,
    mongodb_config)
try:
    import bearer_token
    bearer_token = bearer_token.token
except ModuleNotFoundError as e:
    print("Your bearer_token.py doesn't seem to be here. Please see documentation for help.")
    sys.exit(1)


def args_setup():

    parser = argparse.ArgumentParser(description="Epidemiology of Cohort Social Media",
                                     epilog="Example: python3 epicosm.py --harvest --repeat")
    parser.add_argument("--harvest", action="store_true",
      help="Harvest tweets from all users from a file called user_list (provided by you) with a single user per line.")
    parser.add_argument("--get_follows", action="store_true",
      help="Create a database of the users that are being followed by the accounts in your user_list. (This process can be very slow, especially if your users are prolific followers.)")
    parser.add_argument("--pseudofeed", action="store_true",
      help="Harvest recent tweets from the users being followed by a user. (This process can be very slow and take up a lot of storage, especially if your users are prolific followers.)")
    parser.add_argument("--repeat", action="store", type=int,
      help="Repeat the harvest every given number of days. This process will need to be put to the background to free your terminal prompt.")
    parser.add_argument("--refresh", action="store_true",
      help="If you have a new user_list, this will tell Epicosm to switch to this list.")
    parser.add_argument("--start_db", action="store_true",
      help="Start the MongoDB daemon in this folder, but don't run any Epicosm processes.")
    parser.add_argument("--stop", action="store_true",
      help="Stop all Epicosm processes.")
    parser.add_argument("--shutdown_db", action="store_true",
      help="Stop all Epicosm processes and shut down MongoDB.")
    parser.add_argument("--log", action="store_true",
      help="Create a logfile rather than printing progress to console.")

    args = parser.parse_args()

    return parser, args


def main():

    #~ Set paths as instance of EnvironmentConfig
    env = env_config.EnvironmentConfig()

    #~ print help message if no/wrong args provided
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(0)

    if args.stop or args.shutdown_db:

        print(f"OK, stopping Epicosm processes.")
        subprocess.call(["pkill", "-15", "-f", "epicosm"])

        if args.shutdown_db:
            mongo_ops.stop_mongo(env.db_path)

        sys.exit(0)

    print(f"Running Epicosm with Python version {sys.version}.")
    #~ check environment
    (mongod_executable_path, mongoexport_executable_path,
    mongodump_executable_path) = epicosm_meta.check_env()

    #~ start mongodb daemon
    mongo_ops.start_mongo(mongod_executable_path,
                          env.db_path,
                          env.db_log_filename,
                          env.epicosm_log_filename)
    if args.start_db:
        print(f"OK, MongoDB started, but without Epicosm processes.")
        sys.exit(0)

    #~ set up logging (or not)
    if args.log:
        epicosm_meta.logger_setup(env.epicosm_log_filename)

    #~ setup signal handler
    signal.signal(signal.SIGINT, epicosm_meta.signal_handler)

    #~ tidy up the database for better efficiency
    mongo_ops.index_mongo(env.run_folder)

    #~ get persistent user ids from screen names
    if args.refresh or not os.path.exists(env.run_folder + "/user_details.json"):
        twitter_ops.user_lookup()

    #~ get tweets for each user and archive in mongodb
    if args.harvest:
        twitter_ops.timeline_harvest(mongodb_config.db, mongodb_config.collection)

    #~ if user wants the follows list, make it
    if args.get_follows:
        follows_ops.follows_list_harvest(mongodb_config.db, mongodb_config.follows_collection)

    #~ if we want to do the recent follows stuff
    if args.pseudofeed:
        follows_ops.pseudofeed_harvest(mongodb_config.db, mongodb_config.follows_collection)

    #~ backup database into BSON
    mongo_ops.backup_db(mongodump_executable_path,
                        env.database_dump_path,
                        env.epicosm_log_filename,
                        env.processtime)

    #~ rotate backups - if there are more than 3, remove the oldest one
    current_backup_count = len([name for name in os.listdir(env.database_dump_path + "/twitter_db") if os.path.isfile(os.path.join(env.database_dump_path + "/twitter_db", name))])
    #~ each backup is one bson and one json of metadata, so 6 = 3 backups.
    if current_backup_count > 6:
        print("Rotating backups.")
        bu_list = glob.glob(env.database_dump_path + "/twitter_db/tweets*")
        bu_list.sort()
        #~ remove the oldest two, a bson and a json
        subprocess.call(["rm", bu_list[0]])
        subprocess.call(["rm", bu_list[1]])

    print(f"Job finished at {datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.\n")


if __name__ == "__main__":

    parser, args = args_setup()

    if args.repeat:

        main()
        schedule.every(args.repeat).days.do(main)

        while True:
            schedule.run_pending()
            time.sleep(15)

    else:
        main()

