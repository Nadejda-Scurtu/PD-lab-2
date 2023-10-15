import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from urllib.request import urlretrieve


def DownloadFromYandexPhotos(query, amount):
  os.makedirs(f"dataset/{query}", exist_ok=True)

  driver = webdriver.Chrome()
  driver.get(f"https://yandex.ru/images/search?text={query}")
  time.sleep(5)
  scroll_amount = amount // 20

  for scroll_count in range(scroll_amount):
        element = driver.find_element(By.TAG_NAME, 'body')
        element.send_keys(Keys.END)
        time.sleep(2)

  html = driver.page_source
  soup = BeautifulSoup(html, "html.parser")

  thumbnails = soup.find_all("img", class_="serp-item__thumb")
  count = 0

  for thumbnail in thumbnails[:amount]:
      try:
          full_image_url = thumbnail["src"]

          filename = f"{str(count).zfill(4)}.jpg"
          urlretrieve("https:" + full_image_url, os.path.join(f"dataset/{query}", filename))

          count += 1

          if count >= amount:
              break
      except Exception as e:
          print(f"Ошибка при загрузке изображения: {e}")

  driver.quit()

query1 = "cat"
amount = 1000


DownloadFromYandexPhotos(query1, amount)
