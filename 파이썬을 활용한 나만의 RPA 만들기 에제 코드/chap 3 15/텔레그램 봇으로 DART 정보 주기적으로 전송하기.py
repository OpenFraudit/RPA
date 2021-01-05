import telegram
import json
import requests
import pandas as pd
from datetime import datetime, timedelta
import time

#
pd.set_option('display.max_columns', None) 

# 텔레그램 api
API_TOKEN = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
bot = telegram.Bot(token = API_TOKEN)
chat_id = "XXXXXXXXX"

# 텔레그램 updater
updater = Updater(token=API_TOKEN, use_context=True)
job_queue = updater.job_queue # job_queue는 텔레그램 오브젝트

# 텔레그램 Dispatcher 얻기
dispatcher = updater.dispatcher

# Open DART API KEY 설정
import dart_fss as dart
from dart_fss import get_corp_list

dart_key = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'  
dart.set_api_key(api_key=dart_key)

# 시작일자, 종료일자
종료일자 = datetime.now().strftime('%Y%m%d')
시작일자 = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')


단어 = ['최대주주', '기재정정', '공급계약']

# 공시정보 검색 사용자 정의 함수
def 공시정보검색(시작일자, 종료일자):
    reports = dart.filings.search(bgn_de=시작일자, end_de=종료일자, sort='date', page_count=10)
    
    # reports의 type은 클래스이며 이를 to_dict()를 써서 딕려너리로 바꾸어야 함
    reports = reports.to_dict()
    data = reports['report_list']
    df = pd.DataFrame.from_records(data)
    return df

# Open DART 마지막 rcp no
last_rcp_no = '' # 최종 접수번호(rcp_no)

# 조건부 전송함수 만들기



def 조건부전송():
    global last_rcp_no #전역변수를 불러와서 계속하여 업데이트 시킨다. 
    df_1 = 공시정보검색(시작일자,종료일자) # 위의 공시정보 검색 사용자 정의 함수를 사용한다.
    df_1 = df_1.sort_values('rcp_no') # rcp_no로 소팅한다.
    
    for ix, row in df_1.iterrows():
        corp_name = row['corp_name']
        report_nm =row['report_nm']
        rcp_no = row['rcp_no'] 

        if rcp_no <= last_rcp_no: # 업데이트 된 공시정보가 없다면
            continue

        if any([w in row['report_nm'] for w in 단어]):
            text = "[{}] {} http://dart.fss.or.kr/dsaf001/main.do?rcpNo={}".format(corp_name,report_nm,rcp_no)
            bot.send_message(chat_id=chat_id, text=text) 
            print(chat_id, text)
          
        last_rcp_no = rcp_no

time.sleep(1)

while True : #⑥ 조건문이 참이므로 무한반복
    공시정보검색(시작일자, 종료일자) 
    조건부전송()
    time.sleep(60)  # 60초마다 반복 수행