# 셀레니움 드라이버 임포트
import selenium

# 웹드라이버 임포트
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# time 임포트
import time

# 크롬 창 크기를 최대화 한다.
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome('chromedriver.exe',chrome_options=options)

#
driver.get('https://teht.hometax.go.kr/websquare/websquare.html?w2xPath=/ui/ab/a/a/UTEABAAA13.xml')

# 엑셀을 데이터프레임으로 
사업자 = pd.read_excel('사업자번호.xlsx')

# 사업자번호 
테이블_리스트 = []
for i in range(len(사업자)):
    사업자번호 = 사업자.iloc[i]['사업자번호']

    # 사업자번호 카피하여 붙이기
    elem = driver.find_element_by_xpath('//*[@id="bsno"]')
    elem.send_keys(사업자번호)
    
    # 시간 주기
    time.sleep(4.5)
    driver.find_element_by_xpath('//*[@id="trigger5"]').click()

    # 테이블_바디로 이동
    테이블_바디 = driver.find_element_by_xpath('//*[@id="grid2_body_tbody"]')
    time.sleep(1)
    print(테이블_바디.text)
    
    테이블_바디_쪼개기 = 테이블_바디.text.split(" ")
    
    테이블_리스트 = 테이블_리스트 + [[테이블_바디_쪼개기[0], " ".join(테이블_바디_쪼개기[1:-1]), 테이블_바디_쪼개기[-1]]]
    
# 결과를 엑셀로 저장하기 : list of list 는 from_records() 함수를 이용한다. 
df = pd.DataFrame.from_records(테이블_리스트, columns=['사업자등록번호', '과세여부', '조회일'] )


import xlwings as xw
xw.view(df)