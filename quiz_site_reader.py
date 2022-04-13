from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request

import logging
import platform
import time

urls=[]
urls.append("https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/teoria-della-nave/")
urls.append("https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/teoria-della-nave/2")
urls.append("https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/teoria-della-nave/3")
urls.append("https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/teoria-della-nave/4")
urls.append("https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/teoria-della-nave/6")
urls.append("https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/teoria-della-nave/7")
urls.append("https://www.nauticando.net/quiz-patente-nautica/entro-12-miglia/teoria-della-nave/8")
question_number=0

for url in urls:
  section_string = url.split("/")
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
    section_title = soup.find("div", {"class": "title-section"}).text.split("\n")[1]
    question_elems = soup.find_all("div", {"class": "col-12 py-30 question"})
    for question_elem in question_elems:
      question_number = question_number + 1
      question_string = question_elem.find("div", {"class": "col-12 pb-10"}).text
      question_id = question_elem.get("id")
      question_image_elem = question_elem.find("div", {"class": "col-12 pb-10"}).find("img")
      print(question_id, question_string)
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
      
      answers_elems = question_elem.find_all("div", {"class": "col-12 answer"})
      for answer_elem in answers_elems:
        answer_string = answer_elem.text.strip("\n")
        answer_correct = answer_elem.get("data-correct")
        print(answer_string, answer_correct)

      '''  
      question_number_string = question_string[:dot_index]
      question_string = question_string[dot_index+1:]
      question_string = question_string.strip()
      '''

    print("done")
  except Exception as e:
    logging.exception('exception getting getting webpage: "{e}"!')
