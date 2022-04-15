from configparser import ConfigParser
import psycopg2
import logging

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

def create_quiz(quiz_items):
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
    html_out = html_out + f"""    <div class="row">
            <div class="column1">
                <p><b>{quiz_item["question_no"]}</b> {quiz_item["question"]}</p>
                <ul>
                  <li style="list-style-type:none">
                      <dl>
                          <dt><input type="checkbox">  {quiz_item["answers"][0]["answer"]}</dt>
                      </dl>
                  </li>
                  <li style="list-style-type:none">
                      <dl>
                          <dt><input type="checkbox">  {quiz_item["answers"][1]["answer"]}</dt>
                      </dl>
                  </li>
                  <li style="list-style-type:none">
                      <dl>
                          <dt><input type="checkbox">  {quiz_item["answers"][2]["answer"]}</dt>
                      </dl>
                  </li>

                </ul>
            </div>
            <div class="column2">
                <img src="images/13.jpeg" alt="" width="150" height="130">
            </div>
        </div>"""

  html_out_trailer = """</body>

  </html>"""

  quiz_number = 1
  html_out = html_out + html_out_trailer
  filename = f'{QUIZ_SUBFOLDER}/{str(quiz_number)}.html'
  html_out_file = open(filename, 'w')
  html_out_file.write(html_out)
  html_out_file.close()