from selenium import webdriver

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import re
from database import insert_lecture, insert_department, check_department_exists
from login import login
from schedule_utils import get_schedule_list, go_to_schedule_page


options = webdriver.ChromeOptions()
options.add_argument("--headless")  # 필요시 headless 모드 사용
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome()


driver.get("https://kutis.kyonggi.ac.kr/webkutis/view/indexWeb.jsp")


time.sleep(1)

user_id = "202014911"  # 실제 아이디로 변경
user_pw = "rlagudgh0115"

login(driver, user_id, user_pw)


def get_schedule_iframe(driver):
    driver.switch_to.frame("iframePopLayer05_2")
    plus_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, ".//a[img[contains(@src, 'plus01.png')]]")
        )
    )
    plus_button.click()
    expand_and_scrape_all_departments(driver)

    driver.switch_to.default_content()


def extract_department_info(department_string):
    """
    학과명과 학과 코드를 분리하는 함수.
    :param department_string: '대학(A1200)' 형태의 학과명 문자열
    :return: 학과명과 학과 코드
    """
    match = re.search(r"(.+)\((.+)\)", department_string)

    if match:
        department_name = match.group(1).strip()  # 괄호 밖의 학과명
        department_code = match.group(2).strip()  # 괄호 안의 학과 코드
        return department_name, department_code
    else:
        return department_string.strip(), None  # 학과 코드가 없는 경우


def expand_and_scrape_all_departments(driver, parent_cd=None):
    rows = driver.find_elements(
        By.XPATH,
        '//*[@id="is_croll"]/div/div/section[2]/form/table[@class="list06"]/tbody/tr',
    )

    for row in rows:
        try:
            # 학과명 추출
            department_string = row.find_element(By.TAG_NAME, "td").text.strip()

            # 학과명과 학과 코드를 추출
            hakgwa_name, hakgwa_cd = extract_department_info(department_string)

            # 학과 코드가 존재할 경우에만 데이터베이스에 삽입
            if hakgwa_cd:
                # 이미 데이터베이스에 존재하는지 확인하고, 없으면 삽입
                if not check_department_exists(hakgwa_cd):
                    insert_department(hakgwa_cd, hakgwa_name, parent_cd)

            # 학과의 플러스 버튼을 찾아서 클릭 (플러스 버튼이 있는지 확인)
            plus_button = row.find_element(
                By.XPATH,
                ".//a[contains(@href, 'javascript') and img[contains(@src, 'plus01.png')]",
            )

            if plus_button:
                # 플러스 버튼 클릭하여 하위 학과를 추가
                plus_button.click()
                time.sleep(1)  # 하위 학과가 로드될 시간을 기다림

                # 새롭게 추가된 학과를 처리
                new_rows = driver.find_elements(
                    By.XPATH,
                    '//*[@id="is_croll"]/div/div/section[2]/form/table[@class="list06"]/tbody/tr',
                )

                # 추가된 학과만 처리
                if len(new_rows) > len(rows):
                    new_departments = new_rows[len(rows) :]  # 새로 추가된 학과들만 처리
                    for new_row in new_departments:
                        expand_and_scrape_all_departments(
                            driver, hakgwa_cd
                        )  # 재귀적으로 하위 학과 처리

        except Exception as e:
            print(f"오류 발생: {e}")


go_to_schedule_page(driver, 1, 2024, 20, 85511, "")
time.sleep(1)
driver.quit()
