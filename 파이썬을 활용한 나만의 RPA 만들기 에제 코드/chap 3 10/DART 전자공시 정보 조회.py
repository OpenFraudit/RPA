import dart_fss as dart

# Open DART API KEY 설정
api_key = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'  

dart.set_api_key(api_key=api_key)


# 
베이스_디렉토리 = os.getcwd()

# 종목코드 엑셀을 불러와서 DataFrame으로 만들기
df_종목코드 = pd.read_excel(베이스_디렉토리 + '\\종목코드.xlsx')

# 검색 칼럼이 1인 것만 필터링
df_종목코드 = df_종목코드[df_종목코드['검색'] == 1]
df_종목코드 = df_종목코드.reset_index()



# DART 에 공시된 회사 리스트 불러오기
corp_list = dart.get_corp_list()

# 
for i in range(len(df_종목코드)):
    개별종목명 = df_종목코드.loc[i, '회사명']

    # 개별회사 검색
    개별회사 = corp_list.find_by_corp_name(개별종목명, exactly=True)[0]


    # 2012년부터 연간 연결재무제표 불러오기
    fs = 개별회사.extract_fs(bgn_de='20180101')


    # 재무제표 검색 결과를 엑셀파일로 저장 ( 기본저장위치: 실행폴더/fsdata )
    fs.save()