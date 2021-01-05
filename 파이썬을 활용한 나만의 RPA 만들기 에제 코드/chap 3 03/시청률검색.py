# 셀레니움 드라이버 임포트
import selenium

# 웹드라이버 임포트
from selenium import webdriver

# pyautogui 임포트
#import pyautogui as p

# time 임포트
import time

# 크롬 창 크기를 최대화 한다.
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome('chromedriver.exe',chrome_options=options)

#원하는 URL 접속한다.
driver.get('http://www.daum.net')


# 검색창 클릭
검색어 = '시청률'
driver.find_element_by_xpath('//*[@id="q"]').send_keys(검색어)


#검색버튼 누르기 
driver.find_element_by_xpath('//*[@id="daumSearch"]/fieldset/div/div/button[2]').click()
time.sleep(1)

# 일일시청률 버튼 누르기
driver.find_element_by_xpath('//*[@id="jupTvRatingColl"]/div[2]/div[1]/div[1]/ul/li[1]/a').click()
time.sleep(1)


# 일일시청률 테이블 형식의 text 갖고 오기
시청률_텍스트 = driver.find_element_by_xpath('//*[@id="jupTvRatingColl"]/div[2]/div[1]/div[3]/div/table/tbody').text


time.sleep(1)
tmp = [i.split() for i in 시청률_텍스트.split('\n')]
tmp_1 = [tmp[i]+tmp[i+1] for i in range(0,len(tmp),2)]
테이블_리스트 = [[tmp_1[i][0]," ".join(tmp_1[i][1:-2]),tmp_1[i][-2],tmp_1[i][-1]] for i in range(len(tmp_1))]

time.sleep(1)
df = pd.DataFrame.from_records(테이블_리스트, columns=['순위', '프로그램', '채널', '시청률'])

import xlwings as xw

xw.view(df)