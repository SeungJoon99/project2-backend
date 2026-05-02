import subprocess

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException
import pandas as pd
import re

chrome_browser = subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chromeCookie"')

options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--ignore-certificate-errors')
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
options.add_argument("--window-size=1280,800")
driver = webdriver.Chrome(options=options)

"""
    iframe 스크롤 끝까지 내리기
    반드시 화면에 보여야 하는 건 아니지만
    화면에 나와야 안정적으로 DOM에 모든 매장들이 들어가기 때문
    
    window.scrollBy(0, 700) : 처음부터 700씩 스크롤을 내리겠다
    window.scrollTo         : 그 위치로 이동하겠다
    
    By를 쓴 이유 : To를 쓰게 되면 스크롤을 내리면서 이동하는 게 아니라
                  한 번에 이동해버리기 때문에 
                  DOM에 데이터가 안정적으로 들어가지 않음
"""

# 스크롤 내리는 함수
"""
    element : 스크롤 내릴 요소 파라미터로 받기 
              기본값 - None = window
    네이버 지도에서 검색 iframe이 윈도우에서 스크롤을 내리는 게 아닌
    담당하는 div가 따로 있어서 스크롤을 못 내린다
    그래서 stale 예외발생
    
"""
def scroll_down(driver, element = None) :
    while True :
        if element :
            last = driver.execute_script("return arguments[0].scrollTop;", element)
            driver.execute_script("arguments[0].scrollTop += 700;", element)
            time.sleep(2)
            new = driver.execute_script("return arguments[0].scrollTop;", element)
        else :
            last = driver.execute_script("return window.scrollY")
            driver.execute_script("window.scrollBy(0, 700);")
            time.sleep(2)
            new = driver.execute_script("return window.scrollY")
        if new == last:
            break
    
df = pd.read_csv("filter_list.csv")

rest_names = df["상호명"]

repeat = rest_names[4300:]

failed_list = []

# 검색어 입력 후 엔터
for idx, rest in enumerate(repeat) :
    
    review_list = []
    
    # 봇 탐지를 피하기 위한 방법
    driver.get("https://map.naver.com/p?c=15.00,0,0,0,dh")
    driver.set_window_size(600, 400)
    print("드라이버 초기화 및 안정화 대기 (5초)")
    
    time.sleep(5)
    
    driver.switch_to.default_content()
    
    # 검색창 찾기
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".input_box > input"))
    )
    
    search_box.send_keys(Keys.CONTROL, 'a')
    search_box.send_keys(Keys.DELETE)
    search_box.send_keys(rest)
    search_box.send_keys(Keys.RETURN)
    
    try :
        iframe_search = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "iframe#searchIframe"))
        )
        driver.switch_to.frame(iframe_search)
        print("검색 iframe 진입")
    except TimeoutException :
        failed_list.append(rest)
        print("검색 iframe 진입 실패")
        continue  # iframe 없으면 스킵

    # 매장 리스트 가져오기
    try :
        shop = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="_pcmap_list_scroll_container"]/ul/li[1]')
            )
        )
    except TimeoutException :
        print(f"{rest} 매장 조회 실패")
        failed_list.append(rest)
        continue
   
    # 매장 링크 가져오기
    shop_link = shop.find_element(By.TAG_NAME, "a")
    
    # 화면에 보이게 스크롤
    driver.execute_script("arguments[0].scrollIntoView(true);", shop_link)
    time.sleep(2)
    
    try :
        # 클릭 가능할 때까지 기다리기
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(shop_link))
        
        # JS 클릭
        driver.execute_script("arguments[0].click();", shop_link)
        print(f"{rest} 매장 클릭")
    
        time.sleep(2)
    except TimeoutException :
        print(f"{rest} 매장 클릭 실패")
        failed_list.append(rest)
        continue
    
    try :
        # 최상위 페이지로 이동 : 이래야 안정적임
        driver.switch_to.default_content()
        
        time.sleep(2)
        
        iframe_entry = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "iframe#entryIframe"))
        )
        driver.switch_to.frame(iframe_entry)
        print("결과 iframe 진입")
    except TimeoutException :
        failed_list.append(rest)
        print("결과 iframe 진입 실패")
        continue
    
    # driver.current_rul : 현재 driver가 위치한 url 추출하는 함수?같은 거
    current_url = driver.current_url
    
    # 매장코드 추출
    """
        정규 표현식 :
            re.search(s, t) : 문자열 t에서 패턴 s를 찾겠다
            r"" : 안에 있는 \를 그대로 해석하겠다
            place/ : 여기서는 url에서 place/를 찾겠다
            (\d+)  : 그 뒤에 있는 연속된 숫자를 찾아서 캡쳐하겠다
            group(0) : 전체 패턴 - 여기서는 place/(\d+)
            group(1) : 1번 째 캡쳐 그룹 - 여기서는 \d+
            group(n) : n번 째 캡쳐 그롭
            --------------------------------------------
            (?:)     : 괄호 안에 있는 것들은 캡쳐 안하겠다.
            group(1) : 아래 코드에서는 \d+
    """
    split_url = re.search(r'(?:restaurant|place)/(\d+)', current_url)
    
    if split_url :
        rest_code = split_url.group(1)
    else :
        print("추출 실패")
        continue

    try :    
        # 해당 매장 리뷰 탭 클릭
        review_tab = WebDriverWait(driver, 10).until(
            # span 태그 안 텍스트가 리뷰인 요소 찾기
            EC.element_to_be_clickable((By.XPATH, "//span[text()='리뷰']"))
        )
    except TimeoutException :
        print("리뷰 탭 조회 실패")
        failed_list.append(rest)
        continue
    review_tab.click()
    print("리뷰 탭 클릭")
    time.sleep(2)
    
    scroll_down(driver)
    print("리뷰 탭 스크롤 완료")
    
    time.sleep(2)
    
    
    reviews = driver.find_elements(By.CSS_SELECTOR, "#_review_list > li")
    
    for review in reviews[:10] :
        try :
            wdate          = review.find_element(By.TAG_NAME, "time").text.strip()
            review_content = review.find_element(By.CSS_SELECTOR, "div.pui__vn15t2 > a").text.strip()
            review_content = review_content.replace("\t", "").replace("\n", "")
            review_count   = driver.find_element(By.CSS_SELECTOR, "em.place_section_count")
            review_count   = int(review_count.text.replace(",", ""))
            
            if review_content :
                review_dict = {
                                   "rest"         : rest,
                                   "rest_code"    : rest_code,
                                   "review"       : review_content,
                                   "wdate"        : wdate,
                                   "review_count" : review_count
                              }
                review_list.append(review_dict)
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException) as e :
            failed_list.append(rest)
            print(f"리뷰 추출 중 예외 발생: {e}")
            continue 
        

    df        = pd.DataFrame(review_list, columns=["rest", "rest_code", "review", "wdate", "review_count"])
    df.to_csv("review_list.csv", mode="a", header=False, index=False)
    
    failed_df = pd.DataFrame(failed_list, columns=["rest"])
    failed_df.to_csv("failed_review_list.csv", mode="a", header=False, index=False)
    
    print(f"{rest} csv 저장 {idx + 1} / {len(repeat)}")
    failed_list = []

print("전체 완료")


