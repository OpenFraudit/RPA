# import data handling libraries
import pandas as pd
import numpy as np


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

# time 임포트
import time

# 크롬 창 크기를 최대화 한다.
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome('chromedriver.exe',chrome_options=options)


#페이지수 
페이지수 = 5 # 이 부분은 about 개념이다. 

#페이지수로 loop
테이블_리스트 = []


for i in range(페이지수) :
    공고_URL = 'http://www.g2b.go.kr:8101/ep/tbid/tbidList.do?area=&bidNm=&bidSearchType=1&fromBidDt=2020%2F08%2F03&fromOpenBidDt=&instNm=&radOrgan=1&regYn=Y&searchDtType=1&searchType=1&taskClCds=5&toBidDt=2020%2F09%2F02&toOpenBidDt=&currentPageNo=' + str(i+1) +'&maxPageViewNoByWshan=2&'     
    driver.get(공고_URL)
#    테이블 = driver.find_element_by_class_name('table_list_tbidTbl').click()
    테이블_바디 = driver.find_element_by_xpath('//*[@id="resultForm"]/div[2]/table/tbody')
    테이블_바디_행 = 테이블_바디.find_elements_by_tag_name("tr")

    for idx, value in enumerate(테이블_바디_행):
        데이터_0 = value.find_elements_by_tag_name("td")[0]
        데이터_1 = value.find_elements_by_tag_name("td")[1]
        데이터_2 = value.find_elements_by_tag_name("td")[2]
        데이터_3 = value.find_elements_by_tag_name("td")[3]
        데이터_4 = value.find_elements_by_tag_name("td")[4]
        데이터_5 = value.find_elements_by_tag_name("td")[5]
        데이터_6 = value.find_elements_by_tag_name("td")[6]
        데이터_7 = value.find_elements_by_tag_name("td")[7]
        데이터_8 = value.find_element_by_tag_name('a')
    
        print(데이터_0.text, 
              데이터_1.text,
              데이터_2.text,
              데이터_3.text,
              데이터_4.text,
              데이터_5.text,
              데이터_6.text,
              데이터_7.text,
              데이터_8.get_attribute('href'))
        테이블_리스트 = 테이블_리스트 + [[데이터_0.text, 데이터_1.text, 
                                 데이터_2.text, 데이터_3.text, 
                                 데이터_4.text, 데이터_5.text, 
                                 데이터_6.text, 데이터_7.text.split('\n')[0], 
                                 데이터_7.text.split('\n')[1],
                                 데이터_8.get_attribute('href') ]]    

# 결과를 엑셀로 저장하기 : list of list 는 from_records() 함수를 이용한다. 
df_조회결과 = pd.DataFrame.from_records(테이블_리스트, columns=['업무', 
                                                   '공고번호', 
                                                   '분류', 
                                                   '공고명', 
                                                   '공고기관', 
                                                   '수요기관', 
                                                   '계약방법', 
                                                   '입력일시', 
                                                   '입찰마감일시',
                                                   '원문주소'] )


# 입력일시로 내림차순
df_조회결과 = df_조회결과.sort_values(by = ['입력일시'], ascending = False)


# 최근공고일시.txt에서 입력된 공고일시를 임시 변수로 저장한다.
f = open("최근공고일시.txt", 'r')
구_공고일시 = f.readline()
print(구_공고일시)
f.close()


# 구_공고일시 이후 공고만 나라장터조회결과.tbl에 남기기
for i in range(len(df_조회결과))[::-1]:
    if df_조회결과.iloc[i]['입력일시'] <= 구_공고일시 :
        df_조회결과 = df_조회결과.drop(i)
        
# 공고 상세 URL에 반복해서 접속하하고 첨부파일 다운로드 받기
for i in range(len(df_조회결과)):
    공고_URL = df_조회결과.iloc[i]['원문주소'] 
    driver.get(공고_URL)
    
    # 테이블을 클래스 이름으로 찾는다.
    try :
        테이블_1 = driver.find_element_by_class_name('table_list_attchFileTbl') #element 단수 조심
    
        if "첨부된 파일이 없습니다" in 테이블_1.text:
            continue 
    
        else :
            테이블_1_바디 = 테이블_1.find_element_by_tag_name("tbody")  #element 단수 조심
            테이블_1_바디_행 = 테이블_1_바디.find_elements_by_tag_name("tr") #elements 복수 조심

            for idx, value in enumerate(테이블_1_바디_행):
                파일명 = value.find_elements_by_tag_name("td")[2]
                if 파일명.text[-4:] != 'html' :
                    파일명.find_element_by_tag_name("a").click()
                    time.sleep(1)
                    
    except :
        continue 

# 
import os
import shutil
from os import listdir
from os.path import isfile, join

#
pd.set_option('display.max_columns', None)  

# 사용자 정의 함수
def getFileList(path):
    return [[join(path,i),i] for i in listdir(path) if isfile(join(path,i))]

files =getFileList("C:/Users/사용자명/Downloads/") # 자신의 path로 수정해야 한다
#print(files)
df_다운로드파일 = pd.DataFrame(files,columns = ['path','파일명'])
print(df_다운로드파일)

#다운로드파일 = Table(data = df_다운로드파일)

# 공고파일 path 찾기 : DrProof가 파일명에 포함된 것만 찾기
공고파일_path = []

for i in df_다운로드파일['path'] :
    if any(j in i for j in df_조회결과['공고번호']) :
        공고파일_path = 공고파일_path + [i]

# 디렉토리 생성
베이스_디렉토리 = os.getcwd()

for i in df_조회결과['공고번호'] :
    path = join(베이스_디렉토리, i)
    os.mkdir(path)


for i in 공고파일_path :
    shutil.move(i, 베이스_디렉토리+"\\"+i[27:41])   