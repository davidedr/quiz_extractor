import psycopg2
import argparse

argsparser = argparse.ArgumentParser(prog = "quiz_creator", usage = '%(prog)s [options] session', description = 'Generate a quiz for the given session')
argsparser.add_argument('Session', metavar = 'session', type = int, help = 'the session to be used')
args = argsparser.parse_args()
session = args.session
