import psycopg2
from configparser import ConfigParser

from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request

import logging
import platform
import time

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
          logging.info('Database connection closed.')

format = "%(asctime)s %(thread)d %(threadName)s: %(message)s"
logging.basicConfig(filename="log/quiz_syite_reader.log", format=format, level=logging.NOTSET, datefmt="%Y-%m-%d %H:%M:%S")

db_config = read_db_config(filename = 'database.ini', section = 'quiz_postgresql')
connect_test(db_config)

urls=[]
urls.append("https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/teoria-della-nave/1")
urls.append("https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/teoria-della-nave/2")
urls.append("https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/teoria-della-nave/3")
urls.append("https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/teoria-della-nave/4")
urls.append("https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/teoria-della-nave/5")
urls.append("https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/teoria-della-nave/6")
urls.append("https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/teoria-della-nave/7")
urls.append("https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/teoria-della-nave/8")

urls.append("https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/elica-e-timone/1")
urls.append("https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/elica-e-timone/2")
urls.append("https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/elica-e-timone/3")
urls.append("https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/elica-e-timone/4")
urls.append("https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/elica-e-timone/5")
urls.append("https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/elica-e-timone/6")
urls.append("https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/elica-e-timone/7")

urls.append("https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/motori-endotermici/1")
urls.append("https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/motori-endotermici/2")
urls.append("https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/motori-endotermici/3")
urls.append("https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/motori-endotermici/4")
urls.append("https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/motori-endotermici/5")
urls.append("https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/motori-endotermici/6")
urls.append("https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/motori-endotermici/7")
urls.append("https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/motori-endotermici/8")

urls.append("https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/calcolo-autonomia/1")
urls.append("https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/calcolo-autonomia/2")
urls.append("https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/calcolo-autonomia/3")

urls.append("https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/dotazioni-di-bordo/1")
urls.append("https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/dotazioni-di-bordo/2")
urls.append("https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/dotazioni-di-bordo/3")


question_number=0

for url in urls:
  
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
    '''
    browser.get("https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/teoria-della-nave/2/")
    '''
    browser.get(url)
    '''time.sleep(15)'''
    soup = BeautifulSoup(browser.page_source, "html.parser")

    ''' soup.find_all("div", {"class": "watu-question"})[0].find_all("div", {"class": "question-content"})[0].text.split(".") '''
    section_string = soup.find("div", {"class": "title-section"}).text.split("\n")[1]
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
        filename = str(question_number)+".jpeg"
        opener = urllib.request.build_opener()
        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)
        # calling urlretrieve function to get resource
        urllib.request.urlretrieve(question_image_url, filename)

        question_image_width = question_image_elem.get("width")
        question_image_height = question_image_elem.get("height")
        print(question_image_src, question_image_width, question_image_height)

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
            logging.info('Database connection closed.')
      
      answers_elems = question_elem.find_all("div", {"class": "col-12 answer"})
      answer_no = 0
      for answer_elem in answers_elems:
        answer_string = answer_elem.text.strip("\n")
        answer_correct = answer_elem.get("data-correct")
        if answer_string.startswith("a)"):
          answer_no = 1
        elif answer_string.startswith("b)"):
          answer_no = 2
        elif answer_string.startswith("c)"):
          answer_no = 3
        else:
          logging.error('Answer does not start with a), b) or c)!')

        print(answer_string, answer_correct)

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
              logging.info('Database connection closed.')

      '''  
      question_number_string = question_string[:dot_index]
      question_string = question_string[dot_index+1:]
      question_string = question_string.strip()
      '''

    print("done")
  except Exception as e:
    logging.exception('exception getting getting webpage: "{e}"!')
