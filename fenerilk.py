
# Selenium & BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings("ignore")


game_id = 12528186

driver = webdriver.Chrome()

url = f'https://api.sofascore.com/api/v1/event/{game_id}/shotmap'
driver.get(url)

try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "pre")))
    # Bu, sayfanın kaynak kodunda bulunan bir öğeyi bekler
except Exception as e:
    print(f"Sayfa yüklenirken hata oluştu: {e}")
    driver.quit()

page_source = driver.page_source

soup = BeautifulSoup(page_source, 'html.parser')

data = soup.get_text()

all_shot_maps_data = pd.read_json(data)

all_shot_maps_data["game_id"] = game_id

shotmap_data = pd.json_normalize(all_shot_maps_data['shotmap'])

all_shot_maps_data = pd.concat([all_shot_maps_data.drop(['shotmap'], axis=1), shotmap_data], axis=1)

time.sleep(5) 

driver.quit()



print(all_shot_maps_data.head())

all_shot_maps_data.head()
all_shot_maps_data.columns