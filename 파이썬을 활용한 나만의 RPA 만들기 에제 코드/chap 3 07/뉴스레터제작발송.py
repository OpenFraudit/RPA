import pandas as pd
import numpy as np

#
pd.set_option('display.max_columns', None)  


# 셀레니움 드라이버 임포트
import selenium

# 웹드라이버 임포트
from selenium import webdriver
from selenium.webdriver.common.by import By # WebDriverWait는 Selenium 2.4.0 이후 부터 사용 가능합니다.
from selenium.webdriver.support.ui import WebDriverWait  # expected_conditions는 Selenium 2.26.0 이후 부터 사용 가능합니다.
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.keys import Keys

# BeautifulSoup 임포트 
from bs4 import BeautifulSoup

# pyperclip 임포트
import pyperclip

# time 임포트
import time


# 크롬 창 크기를 최대화 한다.
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome('chromedriver.exe',chrome_options=options)

# 브라우저를 2개를 연다. 3개 이상을 열려면 아래를 카피해서 밑에다 하나 더 코드로 넣는다.
driver.execute_script('window.open("about:blank", "_blank");')

tabs = driver.window_handles

# 탭 1
driver.switch_to_window(tabs[0])
driver.get('https://www.naver.com')
# 탭 2
driver.switch_to_window(tabs[1])
driver.get('https://mail.daum.net/')


driver.switch_to_window(tabs[0])


# 검색창 클릭
검색어 = 'RPA 파이썬'
driver.find_element_by_xpath('//*[@id="query"]').send_keys(검색어)

#검색버튼 누르기 
#driver.find_element_by_xpath('//*[@id="search_btn"]/span[2]').click()
driver.find_element_by_id('search_btn').click()

#뉴스 메뉴 버튼 누르기 
driver.find_element_by_class_name('lnb4').click()

# 최신순 메뉴 버튼 누르기 : css_selector로 
#driver.find_element_by_xpath('//*[@id="main_pack"]/div/div[1]/div[3]/ul/li[2]/a').click()

driver.find_element_by_css_selector('#main_pack > div > div.section_head > div.news_option > ul > li:nth-child(2) > a').click()


# 뉴스건수 갖고오기 : 2020-08-12 오후 2:50 현재 828건임
뉴스건수_텍스트 = driver.find_element_by_xpath('//*[@id="main_pack"]/div/div[1]/div[1]/span').text

tmp = [i.split() for i in 뉴스건수_텍스트.split('/')]

신_뉴스건수 = int(tmp[1][0][:-1].replace(',',''))

# 메모장을 열고 0을 입력한 다음 '총뉴스건수.txt'로 저장한다.

# 메모장을 열고 0을 임시 변수로 저장한다.
f = open("총뉴스건수.txt", 'r')
구_뉴스건수 = int(f.readline())
print(구_뉴스건수)
f.close()


# 새로운 뉴스가 있으면 신규추가_뉴스건수 정하기 : 
# 신_뉴스건수 > 구_뉴스건수 이면, (신_뉴스건수 - 구_뉴스건수)가 신규추가_뉴스건수이다.

if 신_뉴스건수 > 구_뉴스건수 :
    신규추가_뉴스건수 = 신_뉴스건수 - 구_뉴스건수
    f = open("총뉴스건수.txt", 'w')
    f.write(str(신_뉴스건수))
    f.close()
    
else :
    신규추가_뉴스건수 = 0
    

# for문 돌리기
if 신규추가_뉴스건수 == 0 :
    페이지수 = 0
else :
    페이지수 = 신규추가_뉴스건수 // 10 + 1

# 
테이블_리스트 = []

if 페이지수 > 0 :
    for i in range(페이지수) :
        if i == 0 :
            뉴스_URL = 'https://search.naver.com/search.naver?where=news&query='+검색어+'&sm=tab_srt&sort=1&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=so%3Add%2Cp%3Aall%2Ca%3Aall&mynews=0&refresh_start='+str(i)+'&related=0'    
            driver.get(뉴스_URL)
            테이블 = driver.find_element_by_class_name('type01') # type01을 바깥에서 먼저 가장 크게 설정한다.
            테이블_행 = 테이블.find_elements_by_tag_name("li") # 테이블에 다시 li로 시퀀스(여기서는 1-10)를 설정한다. 
        
            for idx, value in enumerate(테이블_행):
                뉴스_제목 = value.find_element_by_class_name('_sp_each_title')
                뉴스_매체 = value.find_element_by_class_name('_sp_each_source')
            
                #뉴스 등록일은 좀 복잡하다. 태그 안에 있는 것이 아니라 바깥에 있기 때문에 아래와 같이 몇 단계를 거쳐야 한다. 
                임시 = value.find_element_by_class_name('txt_inline') # get the container
                뉴스_등록일_html = BeautifulSoup(임시.get_attribute("outerHTML")) # parse the HTML from the container
                텍스트 = 뉴스_등록일_html.body.dd.find_all(text=True, recursive=False) # 텍스트가 있는 부분을 리스트로
                뉴스_등록일 = 텍스트[1].strip()
            
                #뉴스_원문주소
                뉴스_원문주소 = value.find_element_by_tag_name('a')
            
                print(뉴스_제목.text, 뉴스_매체.text, 뉴스_등록일, 뉴스_원문주소.get_attribute('href'))
            
                테이블_리스트 = 테이블_리스트 + [[뉴스_제목.text, 뉴스_매체.text, 뉴스_등록일, 뉴스_원문주소.get_attribute('href')]]

        else :
            뉴스_URL = 'https://search.naver.com/search.naver?&where=news&query=' + 검색어 + '&sm=tab_pge&sort=1&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=so:dd,p:all,a:all&mynews=0&start=' +str(i) +'1' +'&refresh_start=0' 
            driver.get(뉴스_URL)
            테이블 = driver.find_element_by_class_name('type01') # type01을 바깥에서 먼저 가장 크게 설정한다.
            테이블_행 = 테이블.find_elements_by_tag_name("li") # 테이블에 다시 li로 시퀀스(여기서는 1-10)를 설정한다. 
        
            for idx, value in enumerate(테이블_행):
                뉴스_제목 = value.find_element_by_class_name('_sp_each_title')
                뉴스_매체 = value.find_element_by_class_name('_sp_each_source')
                
                #뉴스 등록일은 좀 복잡하다. 태그 안에 있는 것이 아니라 바깥에 있기 때문에 아래와 같이 몇 단계를 거쳐야 한다. 
                임시 = value.find_element_by_class_name('txt_inline') # get the container
                뉴스_등록일_html = BeautifulSoup(임시.get_attribute("outerHTML")) # parse the HTML from the container
                텍스트 = 뉴스_등록일_html.body.dd.find_all(text=True, recursive=False) # 텍스트가 있는 부분을 리스트로
                뉴스_등록일 = 텍스트[1].strip()
                
                #뉴스_원문주소
                뉴스_원문주소 = value.find_element_by_tag_name('a')
                
                print(뉴스_제목.text, 뉴스_매체.text, 뉴스_등록일, 뉴스_원문주소.get_attribute('href'))
                테이블_리스트 = 테이블_리스트 + [[뉴스_제목.text, 뉴스_매체.text, 뉴스_등록일, 뉴스_원문주소.get_attribute('href')]]


    # 결과를 엑셀로 저장하기 : list of list 는 from_records() 함수를 이용한다. 
    df_뉴스 = pd.DataFrame.from_records(테이블_리스트, columns = ['뉴스제목', '매체', '등록일', '원문주소'])

    # fuzzywuzzy 라이브러리 임포트
    import fuzzywuzzy
    from fuzzywuzzy import fuzz, process


    # fuzzy로 뉴스 유사도 점검
    # 뉴스유사도 칼럼 삽입
    df_뉴스['뉴스유사도'] = None

    # 유사도 입력
    for i in range(len(df_뉴스)):
        if i < len(df_뉴스) - 1 :
            df_뉴스.loc[i,'뉴스유사도'] = fuzz.ratio(df_뉴스.iloc[i]['뉴스제목'], df_뉴스.iloc[i+1]['뉴스제목'])
        else :
            df_뉴스.loc[i,'뉴스유사도'] = 0

    # 뉴스유사도_shift 칼럼 삽입
    df_뉴스['뉴스유사도_Shift'] = df_뉴스['뉴스유사도'].shift(1)
    df_뉴스['뉴스유사도_Shift'] = df_뉴스['뉴스유사도_Shift'].fillna(0)

    # 뉴스유사도_Min 칼럼 삽입
    df_뉴스['뉴스유사도_Min'] = df_뉴스.apply(lambda x : min(x['뉴스유사도'], x['뉴스유사도_Shift']), axis = 1)

    # df_뉴스_최종 생성
    df_뉴스_최종 = df_뉴스[:]


    # 뉴스등록일 없는 경우 위 데이터에서 카피하기
    for i in range(len(df_뉴스_최종)):
        if df_뉴스_최종.loc[i,'등록일'] == "" :
            df_뉴스_최종.loc[i,'등록일'] = df_뉴스_최종.loc[i-1,'등록일']

    # 유사한 뉴스 삭제하기 
    for i in range(len(df_뉴스_최종))[::-1]:
        if df_뉴스_최종.loc[i,'뉴스유사도_Min'] >= 40 :
            df_뉴스_최종 = df_뉴스_최종.drop(i)

    # df_뉴스_최종 reset_index()
    df_뉴스_최종 = df_뉴스_최종.reset_index()


    # 뉴스목록을 HTML 형식으로 만들기 
    뉴스_html = ""
    for i in  range(10): # 원래는 len(df_뉴스_최종)으로 해야 하는데 여기서는 10개로 한다. 
        뉴스_html = 뉴스_html + "<div><p><a href = '" + str(df_뉴스_최종.loc[i,'원문주소']) + "'>" + str(df_뉴스_최종.loc[i,'뉴스제목']) + "</a> " + str(df_뉴스_최종.loc[i,'매체']) + " " + str(df_뉴스_최종.loc[i,'등록일']) + "</p></div>"

    driver.switch_to_window(tabs[1])

    # 로그인 버튼 누르기 
    driver.find_element_by_class_name('btn_login').click()
    
    # Daum 아이디로 로그인 버튼 누르기 
    driver.find_element_by_class_name('link_dlogin').click()
    

    # 아이디 입력하기 
    아이디 = 'XXXXX' #자신의 아이디로 변경
    driver.find_element_by_id('id').send_keys(아이디)

    # 비번 입력하기  
    비밀번호 = 'XXXXX' #자신의 비밀번호로 변경
    driver.find_element_by_id('inputPwd').send_keys(비밀번호)

    # 로그인 버튼 누르기
    driver.find_element_by_id('loginBtn').click()

    # 구독자목록을 DataFrame으로 불러들이기
    구독자목록 = pd.read_excel('구독자목록.xlsx')

    # 뉴스_html pyperclip으로 카피하기 
    time.sleep(1)
    pyperclip.copy(뉴스_html)

    


    # 메일보내기 : for문을 이용한다. 
    for i in range(len(구독자목록)):

        # 메일쓰기 버튼 누르기 
        driver.find_element_by_class_name('btn_write').click()
        받는메일 = 구독자목록.loc[i,'이메일']
        time.sleep(1)
        driver.find_element_by_id('toTextarea').send_keys(받는메일)
        time.sleep(1)
        driver.find_element_by_id('toTextarea').send_keys(Keys.ENTER)
        

        제목 = '뉴스레터 샘플' # 여기를 적절하게 고치면 된다.
        time.sleep(1)
        driver.find_element_by_id('mailSubject').send_keys(제목)
        time.sleep(1)
        driver.find_element_by_id('mailSubject').send_keys(Keys.ENTER)
          
        
        # html 탭 버튼 누르기
        driver.find_element_by_class_name('btn_html').click()
        time.sleep(2)
        
        # 텍스트 박스 안에 커서 옮긴 후 뉴스_html 붙이기  
        driver.switch_to.frame('tx_canvas_wysiwyg')
        elem = driver.find_element_by_class_name('tx-content-container')
        time.sleep(2)
        elem.send_keys(Keys.CONTROL + "v")

        # default contents로 돌아오기
        driver.switch_to.default_content()
        
        # 보내기 버튼 누르기 
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="composer"]/div/div[1]/div[2]/div/div/button[1]/span').click()
        time.sleep(1)


else :
    print('새로운 뉴스가 없습니다')