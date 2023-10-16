import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup 
from urllib.request import urlretrieve

query1 = "cat"
query2 = "dog"
amount = 1000

def DownloadFromYandexPhotos(query, amount):
 
  os.makedirs(f"dataset/{query}", exist_ok=True)

  #инициализация обьекта для взаимодействия с веб-браузером
  driver = webdriver.Chrome()

  #открытие веб-страницы по заданному URL-адресу
  driver.get(f"https://yandex.ru/images/search?text={query}")
  #вызов функции выделяет браузеру время для загрузки страницы 
  time.sleep(5)
  #количество прокруток страницы
  scroll_amount = amount // 20

  #цикл для прокрутки страницы вниз 
  for scroll_count in range(scroll_amount):
        element = driver.find_element(By.TAG_NAME, 'body')
        #нажатие кнопки скролла
        element.send_keys(Keys.END)
        time.sleep(2)

        #поиск кнопки "Показать еще"
        try:
            button = driver.find_element(By.CLASS_NAME, 'more__button')
            button.click()
        except:
            pass
  
  #извлекает HTML-код веб-страницы
  html = driver.page_source
  #html.parser преобразует HTML-код в структурированный объект
  soup = BeautifulSoup(html, "html.parser")
  #поиск элементов <img>
  thumbnails = soup.find_all("img", class_="serp-item__thumb")
  count = 0

  for thumbnail in thumbnails[:amount]:
      try:
          #извлечение URL-адреса изображения
          full_image_url = thumbnail["src"]
          #процесс названия файлов по порядковому номеру
          filename = f"{str(count).zfill(4)}.jpg"
          #загрузка изображений в локальный файл
          urlretrieve("https:" + full_image_url, os.path.join(f"dataset/{query}", filename))

          count += 1

          #цикл на проверку если загружены 1000 изображений
          if count >= amount:
              break
      except Exception as e:
          print(f"Ошибка при загрузке изображения: {e}")

  driver.quit()


DownloadFromYandexPhotos(query1, amount)
DownloadFromYandexPhotos(query2, amount)
