# schedule_utils.py
from selenium.webdriver.common.by import By

# from database import insert_lecture  # 데이터베이스 함수 import

import re
from selenium.webdriver.common.by import By

total_page = 0
base_url = "https://kutis.kyonggi.ac.kr/webkutis/view/hs/wssu2/wssu222s.jsp"


def get_total_pages(driver):
    # 페이지 정보가 포함된 요소 찾기
    element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/p")
    text = element.text  # 예시: "총 :3 page"

    # 정규식을 사용해 숫자 부분 추출
    match = re.search(r"총 :(\d+) page", text)
    if match:
        total_pages = int(match.group(1))
        return total_pages
    else:
        return None  # 페이지 수를 찾지 못한 경우


def clean_text(text):
    return text.replace("\n보기", "").strip()


def get_schedule_list(driver, hakgwa_cd):
    """
    학과 코드에 따른 시간표 데이터를 추출하여 DB에 삽입하는 함수.

    :param driver: Selenium WebDriver 인스턴스
    :param hakgwa_cd: 학과 코드
    """
    # 모든 tbody 요소 가져오기
    tbodies = driver.find_elements(By.XPATH, '//table[@class="list02"]/tbody')

    # 각 tbody에서 데이터를 추출
    for tbody in tbodies:
        rows = tbody.find_elements(By.TAG_NAME, "tr")  # tbody 내 모든 tr 요소 가져오기
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            row_data = [clean_text(col.text) for col in cols]

            row_data.insert(0, hakgwa_cd)  # 학과 코드 추가

            print(row_data)
            # TODO : 데이터배이스 추가 부분
            # insert_lecture(*row_data)


def go_to_schedule_page(driver, curPage, gyear, ghakgi, hakgwa_cd, gwamok_name=""):
    """
    동적으로 URL을 생성하고 해당 페이지로 이동.

    :param driver: Selenium WebDriver 인스턴스
    :param curPage: 현재 페이지 번호 (페이지네이션)
    :param gyear: 조회할 년도
    :param ghakgi: 학기 정보 (10: 1학기, 20: 2학기)
    :param hakgwa_cd: 학과 코드
    :param gwamok_name: 과목명 (옵션, 기본은 빈 문자열)
    """
    url = f"{base_url}?curPage={curPage}&gyear={gyear}&ghakgi={ghakgi}&hakgwa_cd={hakgwa_cd}&gwamok_name={gwamok_name}"
    driver.get(url)
    get_schedule_list(driver, hakgwa_cd)

    total_page = get_total_pages(driver)
    sub_schedule_page(driver, total_page, gyear, ghakgi, hakgwa_cd, gwamok_name="")


def sub_schedule_page(driver, total_page, gyear, ghakgi, hakgwa_cd, gwamok_name=""):
    for curPage in range(2, total_page + 1):

        url = f"{base_url}?curPage={curPage}&gyear={gyear}&ghakgi={ghakgi}&hakgwa_cd={hakgwa_cd}&gwamok_name={gwamok_name}"
        driver.get(url)
        get_schedule_list(driver, hakgwa_cd)
