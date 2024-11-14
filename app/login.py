# login.py
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


def login(driver, user_id, user_pw):
    driver.get("https://kutis.kyonggi.ac.kr/webkutis/view/indexWeb.jsp")
    time.sleep(1)

    input_id = driver.find_element(By.XPATH, '//*[@id="id"]')
    input_pw = driver.find_element(By.XPATH, '//*[@id="pw"]')

    input_id.send_keys(user_id)
    input_pw.send_keys(user_pw)
    input_pw.send_keys(Keys.RETURN)
