import psycopg2
import argparse

import logging
import random

from utility import read_db_config, connect_test

format = "%(asctime)s:%(thread)d:%(threadName)s:%(levelname)s:%(message)s"
logging.basicConfig(filename = "log/quiz_creator.log", format = format, level = logging.NOTSET, datefmt = "%Y-%m-%d %H:%M:%S")

session = 1
"""
argsparser = argparse.ArgumentParser(prog = "quiz_creator", usage = '%(prog)s [options] session', description = 'Generate a quiz for the given session')
argsparser.add_argument('Session', metavar = 'session', type = int, help = 'the session to be used')
args = argsparser.parse_args()
session = args.session
"""


quiz_numbers = [
  {"topic": "teoria-della-nave", "how_many": 2},
  {"topic": "motori-endotermici", "how_many": 2},
  {"topic": "sicurezza-della-navigazione", "how_many": 4},
  {"topic": "colreg72-e-segnalamento-marittimo", "how_many": 5},
  {"topic": "meteorologia", "how_many": 2},
  {"topic": "navigazione", "how_many": 4},
  {"topic": "normativa-diportistica", "how_many": 1},
]

db_config = read_db_config(filename = 'database.ini', section = 'quiz_postgresql')
db_test_ok = connect_test(db_config)
if not db_test_ok:
  end

quiz = []
for quiz_number in quiz_numbers:
  topic = quiz_number["topic"]
  how_many = quiz_number["how_many"]
  connection = None
  try:
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()
    query = """
      SELECT questions.id FROM questions
      WHERE topic=%s AND id NOT IN (
          SELECT questions.id FROM  questions, used_questions
          WHERE questions.id = used_questions.question_id AND used_questions.session=%s AND used_questions.used=NULL
        )
    """
    values = (topic, session)
    cursor.execute(query, values)
    ids=[]
    while True:
      rows = cursor.fetchmany(100)
      if not rows:
        break
      for row in rows:
        ids.append(row[0])
    cursor.close()
  except (Exception, psycopg2.DatabaseError) as e:
      logging.error(f'Exception "{e}"!')
      logging.error(f'query: "{query}"!')
      logging.error(f'values: "{values}"!')
      break
  finally:
      if connection is not None:
        connection.close()
        logging.debug('Database connection closed.')

  chosen = random.sample(ids, how_many)
  logging.error(f'topic: {topic}, how_many: {how_many}, ids: "{ids}", len: {len(ids)}')
  logging.error(f'chosen: "{chosen}", len: {len(chosen)}')
