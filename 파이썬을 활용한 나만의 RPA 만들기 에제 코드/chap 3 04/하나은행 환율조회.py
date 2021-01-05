# 셀레니움 드라이버 임포트
import selenium

# 웹드라이버 임포트
from selenium import webdriver

# time 임포트
import time

# 크롬 창 크기를 최대화 한다.
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome('chromedriver.exe',chrome_options=options)

#원하는 URL 접속한다.
driver.get('https://www.kebhana.com/cont/mall/mall15/mall1503/index.jsp')

#시간 주기
time.sleep(1)

#switch_to_frame
driver.switch_to_frame('bankIframe')

#기간환율변동 라디오버튼 누르기
driver.find_element_by_xpath('//*[@id="inqFrm"]/table/tbody/tr[1]/td/span/p/label[3]/span').click()

#시작일자 입력하기
시작일자 = '20200501'
driver.find_element_by_id('tmpInqStrDt_p').clear()
driver.find_element_by_id('tmpInqStrDt_p').send_keys(시작일자)


#종료일자 입력하기
종료일자 = '20200829'
driver.find_element_by_id('tmpInqEndDt_p').clear()
driver.find_element_by_id('tmpInqEndDt_p').send_keys(종료일자)

#통화선택 환율 선택하기
선택환율 = 'EUR:유로(유럽연합)'
driver.find_element_by_id("curCd").send_keys(선택환율)

#고시회차 선택
driver.find_element_by_xpath('//*[@id="inqFrm"]/table/tbody/tr[6]/td/span/p/label[2]').click()

#조회버튼 클릭
time.sleep(1)
driver.find_element_by_xpath('//*[@id="HANA_CONTENTS_DIV"]/div[2]/a/span').click()
#driver.find_element_by_xpath('//*[contains(@ID, "HANA_CONTENTS_DIV")]/div[2]/a').click()

#엑셀파일 클릭하기
time.sleep(1)
driver.find_element_by_xpath('//*[@id="searchContentDiv"]/div[1]/a[2]/span').click()