from configparser import ConfigParser
import psycopg2
import logging
from datetime import datetime
import base64

def read_db_config(filename = 'database.ini', section = 'quiz_postgresql'):
  parser = ConfigParser()
  parser.read(filename)

  db = {}
  if parser.has_section(section):
      params = parser.items(section)
      for param in params:
          db[param[0]] = param[1]
  else:
      e = Exception('Section {0} not found in the {1} file'.format(section, filename))
      logging.info(f'{e}')
      raise e

  return db

def connect_test(db_config):
  connection = None
  try:
      logging.info('Connecting to the PostgreSQL database...')
      connection = psycopg2.connect(**db_config)
      cursor = connection.cursor()
      cursor.execute('SELECT version()')
      db_version = cursor.fetchone()
      logging.info(f'PostgreSQL database version: "{db_version}"!')
      cursor.close()
  except (Exception, psycopg2.DatabaseError) as e:
      logging.error(f'Exceptinon testing database: "{e}"!')
      return False
  finally:
      if connection is not None:
        connection.close()
        logging.debug('Database connection closed.')

  return True

QUIZ_SUBFOLDER = "quiz"

def create_quiz_html(quiz_items, session, with_answers = True, datetimestamp = datetime.now()):
  html_out_header = '''<!DOCTYPE html>
  <html>

  <head>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <style>
          * {
              box-sizing: border-box;
          }
          
          .row {
              display: flex;
          }
          /* Create three equal columns that sits next to each other */
          
          .column1 {
              flex: 80%;
              padding: 5px;
          }
          
          .column2 {
              flex: 20%;
              padding: 5px;
          }
      </style>
  </head>

  <body>

      <h2>Text and image side by side</h2>
      <p>How to put text and image side by side with CSS Flexbox:</p>
  '''

  html_out = html_out_header
  for quiz_item in quiz_items:
    if with_answers:
      answer_a_checked = ('', ', checked')[quiz_item["answers"][0]["correct"]]
      answer_b_checked = ('', ', checked')[quiz_item["answers"][1]["correct"]]
      answer_c_checked = ('', ', checked')[quiz_item["answers"][2]["correct"]]
    else:
      answer_a_checked = answer_b_checked = answer_c_checked = ''
      
    html_out = html_out + f"""    <div class="row">
            <div class="column1">
                <p><b>{quiz_item["question_no"]}</b> {quiz_item["question"]}</p>
                <ul>
                  <li style="list-style-type:none">
                      <dl>
                          <dt><input type="checkbox"{answer_a_checked}>  {quiz_item["answers"][0]["answer"]}</dt>
                      </dl>
                  </li>
                  <li style="list-style-type:none">
                      <dl>
                          <dt><input type="checkbox"{answer_b_checked}>  {quiz_item["answers"][1]["answer"]}</dt>
                      </dl>
                  </li>
                  <li style="list-style-type:none">
                      <dl>
                          <dt><input type="checkbox"{answer_c_checked}>  {quiz_item["answers"][2]["answer"]}</dt>
                      </dl>
                  </li>

                </ul>
            </div>
            <div class="column2">"""
    if quiz_item["image"]:
      #html_out = html_out +'<img src="images/13.jpeg" alt="" width="150" height="130">'
      image_string_base64 = base64.b64encode(quiz_item["image"]["image_binary"])
      image_string_base64_stripped = str(image_string_base64, 'utf-8')
      html_out = html_out +f'<img src="data:image/png;base64,{image_string_base64_stripped}" width="150" height="130">'
    html_out = html_out +"""
            </div>
        </div>"""

  html_out_trailer = """</body>

  </html>"""

  html_out = html_out + html_out_trailer
  return html_out

def create_quiz(quiz_items, session, with_answers = True, datetimestamp = datetime.now()):  

  quiz_number = 1
  html_out = create_quiz_html(quiz_items, session, with_answers = False)
  datetimestamp_string = datetimestamp.strftime("%Y%m%d%H%M%S") 
  filename = f'{QUIZ_SUBFOLDER}/quiz_{str(session)}_{str(quiz_number)}_{datetimestamp_string}.html'
  html_out_file = open(filename, 'w')
  html_out_file.write(html_out)
  html_out_file.close()

  if (with_answers):
    html_out = create_quiz_html(quiz_items, session, with_answers = True)
    filename = f'{QUIZ_SUBFOLDER}/quiz_{str(session)}_{str(quiz_number)}_{datetimestamp_string}_WA.html'
    html_out_file = open(filename, 'w')
    html_out_file.write(html_out)
    html_out_file.close()

  return datetimestamp