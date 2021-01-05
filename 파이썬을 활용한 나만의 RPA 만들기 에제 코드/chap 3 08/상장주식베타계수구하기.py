import pandas as pd
import numpy as np

# 라이브러리 불러오기
import FinanceDataReader as fdr
import xlwings as xw
pd.set_option('display.max_columns', None)  

# 베이스 디렉토리 설정
베이스_디렉토리 = os.getcwd()

# 종목코드 엑셀을 불러와서 DataFrame으로 만들기
df_종목코드 = pd.read_excel(베이스_디렉토리 + '\\종목코드.xlsx')

# 검색 칼럼이 1인 것만 필터링
df_종목코드 = df_종목코드[df_종목코드['검색'] == 1]
df_종목코드 = df_종목코드.reset_index()

# 기준일
시작일자 = '2019-01-01'
종료일자 = '2020-09-07'


# for 문

테이블_리스트 = []

for i in range(len(df_종목코드)):

    개별종목코드 = df_종목코드.loc[i, '종목코드']
    개별종목명 = df_종목코드.loc[i, '회사명']
    df_개별종목 = fdr.DataReader(개별종목코드, 시작일자, 종료일자)

    # KOSPI 200 list
    df_코스피지수 = fdr.DataReader('KS11', 시작일자, 종료일자)

    # df의 Date와 Close, 코스피지수 Date와 Close만 갖고 옴
    df_종가_변동 = df_개별종목['Change']
    df_코스피지수_종가_변동 = df_코스피지수 ['Change']
    
    # 조인
    df_조인 = pd.merge(df_종가_변동, df_코스피지수_종가_변동, how='left', 
                     left_on = ['Date'], right_on = ['Date'],suffixes=('_개별', '_코스피지수'))
                     
    
    
    # 베타 구하기                 
    공분산_개별_코스피 = df_조인.cov().iloc[0]['Change_코스피지수'] 
    분산_코스피 = df_조인['Change_코스피지수'].var()
    베타 = 공분산_개별_코스피/분산_코스피
    
    print('종목코드 {} {}의 {}일부터 {}일까지 KOSPI 대비 daily B(베타)는 {:.2f} 입니다.'.format(개별종목코드,개별종목명,시작일자,종료일자,베타)) 
    테이블_리스트 = 테이블_리스트 + [[개별종목코드, 개별종목명, 시작일자, 종료일자, 베타]]
    
    df_베타결과 = pd.DataFrame.from_records(테이블_리스트, columns = ['개별종목코드', '개별종목명', '시작일자', '종료일자', '베타'])

    # 주가 및 변동 history 테이블 구하기  
    df_종가변동_조인 = pd.merge(df_개별종목, df_코스피지수, how='left', 
                     left_on = ['Date'], right_on = ['Date'],suffixes=('_{}'.format(개별종목명), '_코스피지수'))

    # 주가 및 변동 history 테이블에서 필요한 칼럼 선택
    df_종가변동_조인 = df_종가변동_조인.iloc[:,[3,6,5,11]]
    
    # 엑셀 출력
    xw.view(df_종가변동_조인)
    
xw.view(df_베타결과)