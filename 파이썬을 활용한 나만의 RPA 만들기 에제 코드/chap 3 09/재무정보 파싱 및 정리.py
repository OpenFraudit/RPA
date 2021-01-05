import pandas as pd
from pandas import DataFrame
import numpy as np

#
pd.set_option('display.max_columns', None)  

# pyperclip 라이브러리 불러오기
import pyperclip

# 셀레니움 드라이버 임포트
import selenium

# 웹드라이버 임포트
from selenium import webdriver
from fraudit.gui import Utils 
from selenium.webdriver.common.by import By # WebDriverWait는 Selenium 2.4.0 이후 부터 사용 가능합니다.
from selenium.webdriver.support.ui import WebDriverWait  # expected_conditions는 Selenium 2.26.0 이후 부터 사용 가능합니다.
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.keys import Keys

# BeautifulSoup 임포트 
import requests
from bs4 import BeautifulSoup


# pyautogui 임포트
import pyautogui as p

# time 임포트
import time

# xlwlings 임포트 
import xlwings as xw

#베이스 디렉토리
베이스_디렉토리 = os.getcwd()

# 종목코드 엑셀을 불러와서 DataFrame으로 만들기
df_종목코드 = pd.read_excel(베이스_디렉토리 + '\\종목코드.xlsx')

# 검색 칼럼이 1인 것만 필터링
df_종목코드 = df_종목코드[df_종목코드['검색'] == 1]
df_종목코드 = df_종목코드.reset_index()

# for 문

for i in range(len(df_종목코드)):
    개별종목코드 = df_종목코드.loc[i, '종목코드']
   
    # 페이지 소스에서 src로 검색하면서 수동으로 찾아야 한다.
    개별종목링크 = 'https://navercomp.wisereport.co.kr/v2/company/c1010001.aspx?cmp_cd={}'.format(개별종목코드)
    
    # 개별종목링크를 DataFrame 리스트로 열기 encoding을 python 또는 euc-kr, utf-8로 해보자
    dfs = pd.read_html(개별종목링크, encoding = 'utf-8')

    # 총괄 view
    wb = xw.Book(베이스_디렉토리 + '\\네이버재무정보.xlsx')
    
    for j in range(len(dfs)):
        sht = wb.sheets['Sheet{}'.format(j+1)]
        sht.range('A1').value = dfs[j]