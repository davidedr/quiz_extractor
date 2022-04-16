import psycopg2
import argparse

import logging
import random

from utility import read_db_config, connect_test, create_quiz

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

broken = False
chosen_ids = []
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

  chosen = []
  try: 
    chosen = random.sample(ids, how_many)
  except (Exception) as e:
    logging.error(f'Exception in random: {e}')
    logging.error(f'ids: "{ids}" (len: {len(ids)}), how_many: {how_many}!')
    broken = True
    break

  logging.info(f'topic: {topic}, how_many: {how_many}, ids: "{ids}", len: {len(ids)}')
  logging.info(f'chosen: "{chosen}", len: {len(chosen)}')
  chosen_ids.append(chosen)

print(broken, chosen_ids)
if broken:
  logging.error(f'Broken "{broken}"!')
  end

quiz_items = []
for chosen_id in chosen_ids:
  for chosen in chosen_id:
    row_question = None
    rows_answers = None
    try:
      connection = psycopg2.connect(**db_config)
      cursor = connection.cursor()
      query = "SELECT * FROM questions WHERE id=%s"
      values = (chosen,)
      logging.error(f'query: "{query}"!')
      logging.error(f'values: "{values}"!')
      cursor.execute(query, values)
      row_question = cursor.fetchone()
      cursor.close()

      cursor = connection.cursor()
      query = "SELECT * FROM answers WHERE question_id=%s ORDER BY answer_no"
      values = (chosen,)
      logging.error(f'query: "{query}"!')
      logging.error(f'values: "{values}"!')
      cursor.execute(query, values)
      rows_answers = cursor.fetchmany(3)
      cursor.close()

    except (Exception, psycopg2.DatabaseError) as e:
        logging.error(f'Exception "{e}"!')
        break
    finally:
        if connection is not None:
          connection.close()
          logging.debug('Database connection closed.')

    if not row_question or not rows_answers or len(rows_answers)<3:
      break
    
    question_id = row_question[0]
    question_number = row_question[1]
    question_subject = row_question[2]
    question_version = row_question[3]
    question_theme = row_question[4]
    question_topic = row_question[5]
    question_section = row_question[6]
    question_question = row_question[7]
    question_image = row_question[8]
    question_image_filename = row_question[9]
    question_image_width = row_question[10]
    question_image_height = row_question[11]

    answers = []
    for rows_answer in rows_answers:
      answer_id = rows_answer[0]
      answer_question_id = rows_answer[1]
      answer_no = rows_answer[2]
      answer_answer = rows_answer[3]
      answer_correct = rows_answer[4]
      answer = {"answer_no": answer_no, "answer": answer_answer, "correct": answer_correct}
      answers.append(answer)

    quiz_item = {
      "question_no": question_number,
      "question": question_question,
      "image": {"image_binary": question_image, "image_width": question_image_width, "image_height": question_image_height},
      "answers": answers
    }

    quiz_items.append(quiz_item)

create_quiz(quiz_items, session)