import psycopg2
import argparse

import logging

logging.basicConfig(filename = "log/quiz_creator.log", format = format, level = logging.NOTSET, datefmt = "%Y-%m-%d %H:%M:%S")

argsparser = argparse.ArgumentParser(prog = "quiz_creator", usage = '%(prog)s [options] session', description = 'Generate a quiz for the given session')
argsparser.add_argument('Session', metavar = 'session', type = int, help = 'the session to be used')
args = argsparser.parse_args()
session = args.session
