import psycopg2
from configparser import ConfigParser

from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request

import logging
import platform
import time

IMAGES_SUBFOLDER = "images"

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
    conn = None
    try:
        logging.info('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        logging.info(f'PostgreSQL database version: "{db_version}"!')
        cur.close()
    except (Exception, psycopg2.DatabaseError) as e:
        logging.info(f'PostgreSQL database version: "{e}"!')
    finally:
        if conn is not None:
          conn.close()
          logging.debug('Database connection closed.')

def process_url(url, question_number):
  url_elems= url.split("/")
  subject_string = url_elems[3]
  version = "1"
  theme_string = url_elems[4]
  topic_string = url_elems[5]
  
  if platform.system() == 'Windows':
      PHANTOMJS_PATH = './utility/chromedriver/chromedriver.exe'
  else:
      PHANTOMJS_PATH = './utility/phantomjs'

  try:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    browser = webdriver.Chrome(executable_path=r'C:/temp/meteo_data_repo/utility/chromedriver/chromedriver.exe', options = chrome_options)
    browser.get(url) 
    soup = BeautifulSoup(browser.page_source, "html.parser")

    section_string = "missing"
    try:
      section_string = soup.find("div", {"class": "title-section"}).text.split("\n")[1]
    except Exception as e:
      logging.error(f'Exception at: soup.find("div", {"class": "title-section"}).text.split("\n")[1]: {e}')

    question_elems = soup.find_all("div", {"class": "col-12 py-30 question"})
    for question_elem in question_elems:
      question_number = question_number + 1
      question_string = question_elem.find("div", {"class": "col-12 pb-10"}).text
      question_id = question_elem.get("id")
      question_image_elem = question_elem.find("div", {"class": "col-12 pb-10"}).find("img")
      logging.info(f'question_id: {question_id}, question_number: {question_number}, question_string: {question_string}')

      if question_image_elem:
        question_image_src = question_image_elem.get("src")
        '''
        looks like:
        looks like '/img/quiz-patente-nautica/13.jpg'
        '''
        question_image_url = "https://www.nauticando.net"+question_image_src
        '''
        looks like:
        https://www.nauticando.net/img/quiz-patente-nautica/13.jpg
        '''
        filename = f'{IMAGES_SUBFOLDER}/{str(question_number)}.jpeg'
        opener = urllib.request.build_opener()
        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(question_image_url, filename)

        question_image_width = question_image_elem.get("width")
        question_image_height = question_image_elem.get("height")
        logging.info(f'question_image_src: {question_image_src}, question_image_width: {question_image_width}, question_image_height: {question_image_height}')

        question_image = open(filename, 'rb').read()
        question_image_binary = psycopg2.Binary(question_image)

      id_of_new_row = None
      try: 
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        query = 'INSERT INTO questions (number, subject, version, theme, topic, section, question, image, image_filename, image_width, image_height) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id'
        values = (question_number, subject_string, version, theme_string, topic_string, section_string, question_string, None, None, None, None)
        if question_image_elem:
          values = (question_number, subject_string, version, theme_string, topic_string, section_string, question_string,
          question_image_binary, filename, question_image_width, question_image_height)
        cursor.execute(query, values)
        id_of_new_row = cursor.fetchone()[0]
        conn.commit()
      except (Exception, psycopg2.DatabaseError) as e:
          logging.error(f'Exception inserting question: "{e}"!')
          logging.error(query)
          logging.error(values)
      finally:
          if conn is not None:
            conn.close()
            logging.debug('Database connection closed.')
      
      answers_elems = question_elem.find_all("div", {"class": "col-12 answer"})
      answer_no = 0
      for answer_elem in answers_elems:
        answer_string = answer_elem.text.strip("\n").strip()
        answer_correct = answer_elem.get("data-correct")
        if answer_string.startswith("a)"):
          answer_no = 1
        elif answer_string.startswith("b)"):
          answer_no = 2
        elif answer_string.startswith("c)"):
          answer_no = 3
        else:
          logging.error(f'Answer does not start with a), b) or c): "{answer_string}"!')

        logging.info(f'answer_string: {answer_string}, answer_correct: {answer_correct}')

        try: 
          conn = psycopg2.connect(**db_config)
          cursor = conn.cursor()
          query = 'INSERT INTO answers (question_id, answer_no, answer, correct) VALUES (%s, %s, %s, %s)'
          values = (id_of_new_row, answer_no, answer_string, answer_correct == '1')
          cursor.execute(query, values)
          conn.commit()
        except (Exception, psycopg2.DatabaseError) as e:
            logging.error(f'Exception inserting question: "{e}"!')
            logging.error(query)
            logging.error(values)
        finally:
            if conn is not None:
              conn.close()
              logging.debug('Database connection closed.')

    logging.info(f'Done url: {url}.')
  except Exception as e:
    logging.exception(f'Exception getting getting webpage: "{e}"!')

  return question_number

format = "%(asctime)s:%(thread)d:%(threadName)s:%(levelname)s:%(message)s"
logging.basicConfig(filename = "log/quiz_site_reader.log", format = format, level = logging.NOTSET, datefmt = "%Y-%m-%d %H:%M:%S")

db_config = read_db_config(filename = 'database.ini', section = 'quiz_postgresql')
connect_test(db_config)

urls=[]
urls.append({"base_url": "https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/teoria-della-nave", "pages": "8"})
urls.append({"base_url": "https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/elica-e-timone", "pages": "7"})
urls.append({"base_url": "https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/motori-endotermici", "pages": "7"})
urls.append({"base_url": "https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/calcolo-autonomia", "pages": "3"})
urls.append({"base_url": "https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/dotazioni-di-bordo", "pages": "3"})
urls.append({"base_url": "https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/visite-periodiche", "pages": "2"})
urls.append({"base_url": "https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/sinistri-marittimi", "pages": "2"})
urls.append({"base_url": "https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/navigazione-con-tempo-cattivo", "pages": "1"})
urls.append({"base_url": "https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/assistenza-e-soccorso", "pages": "2"})
urls.append({"base_url": "https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/norme-abbordi-fanali-particolari", "pages": "18"})
urls.append({"base_url": "https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/navigazione-fluviale", "pages": "1"})
urls.append({"base_url": "https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/navigazione-in-prossimita-della-costa", "pages": "8"})
urls.append({"base_url": "https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/meteorologia", "pages": "7"})
urls.append({"base_url": "https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/coordinate-geografiche", "pages": "5"})
urls.append({"base_url": "https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/carte-nautiche", "pages": "10"})
urls.append({"base_url": "https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/orientamento-e-rosa-dei-venti", "pages": "1"})
urls.append({"base_url": "https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/bussole-magnetiche", "pages": "6"})
urls.append({"base_url": "https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/navigazione-stimata", "pages": "6"})
urls.append({"base_url": "https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/navigazione-costiera", "pages": "5"})
urls.append({"base_url": "https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/deriva-e-scarroccio", "pages": "6"})
urls.append({"base_url": "https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/portolano-elenco-fari-segnali-da-nebbia", "pages": "7"})
urls.append({"base_url": "https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/normativa-diportistica/", "pages": "12"})

question_number=0

'''
process_url("https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/teoria-della-nave/5", question_number)
'''

for url_elem in urls:
  base_url = url_elem["base_url"]
  pages = int(url_elem["pages"])
  for page in range(pages):
    url = f'{base_url}/{page + 1}'
    question_number = process_url(url, question_number)
