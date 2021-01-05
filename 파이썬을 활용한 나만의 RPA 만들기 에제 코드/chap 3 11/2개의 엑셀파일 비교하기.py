import pandas as pd
import numpy as np
import xlwings as xw
pd.set_option('display.max_columns', None)  

# 신구 엑셀 명명
구엑셀 = '분개장_1.xlsx'
신엑셀 = '분개장_2.xlsx'

# 데이터프레임으로 변환
df_old = pd.read_excel(구엑셀, 'Sheet1', na_values=['NA'])
df_new = pd.read_excel(신엑셀, 'Sheet1', na_values=['NA'])

# 버전 칼럼 삽입
df_old['version'] = 'old'
df_new['version'] = 'new'

# groupby 
gb_old = df_old.groupby(['전표일자','전표번호'])
gb_new = df_new.groupby(['전표일자','전표번호'])

df_old['전표번호seq'] = gb_old.cumcount()
df_new['전표번호seq'] = gb_new.cumcount()

# 
df_old['version'] = 'old'
df_new['version'] = 'new'


#각 DataFrame에 '전표일자번호' 칼럼을 만들고 아래와 같이 전표일자, 전표번호, 전표번호seq를 조합해서 고유한 번호로 넣는다.
df_old['전표일자번호'] = df_old['전표일자'] + df_old['전표번호'].astype(str) + df_old['전표번호seq'].astype(str)
df_new['전표일자번호'] = df_new['전표일자'] + df_new['전표번호'].astype(str) + df_new['전표번호seq'].astype(str)

#각 DataFrame에 '전표일자번호' 칼럼에 set() 함수를 취하여 중복을 제외한 것을 변수로 설정한다.
old_전표일자번호_all = set(df_old['전표일자번호'])
new_전표일자번호_all = set(df_new['전표일자번호'])

#삭제_전표일자번호와 추가_전표일자번호 변수를 아래와 같이 설정한다. 세트끼리 (-) 연산자를 취하는 경우 앞의 세트의 원소에서 뒤의 세트의 원소를 차감한 세트를 반환한다.
삭제_전표일자번호 = old_전표일자번호_all - new_전표일자번호_all
추가_전표일자번호 = new_전표일자번호_all - old_전표일자번호_all

# 각 df_old를 위로, df_new를 아래로 합친다.
all_data = pd.concat([df_old,df_new],ignore_index=True)

# all_data에서 subset의 항목이 모두 중복인 것을 제외하여 중복되지 않은 항목만 남긴다
changes = all_data.drop_duplicates(subset=["전표일자","전표번호", "계정코드", "계정과목",
                                           "차변금액","대변금액", "거래처", "승인일자", "프로젝트코드", "전표일자번호"],
                                           keep=False)
                                           
# old와 new를 각각의 DataFrame으로 구분한다.
change_new = changes[(changes["version"] == "new")]
change_old = changes[(changes["version"] == "old")]


# 각각의 DataFrame에서 version 칼럼을 삭제한다.
change_new = change_new.drop(['version'], axis=1)
change_old = change_old.drop(['version'], axis=1)

# 각각의 DataFrame에서 전표일자번호를 새로운 인덱스로 변경한다. 
change_new.set_index('전표일자번호', inplace=True)
change_old.set_index('전표일자번호', inplace=True)



# change_old와 change_new를 아래와 같이 combine한다.

df_all_changes = pd.concat([change_old, change_new],
                            axis=1,
                            keys=['old', 'new'],
                            join='outer')


# Define the diff function to show the changes in each field
def report_diff(x):
    return x[0] if x[0] == x[1] else '{} ---> {}'.format(*x)
    
    
df_all_changes = df_all_changes.swaplevel(axis=1)[change_new.columns[0:]]
    
df_changed = df_all_changes.groupby(level=0, axis=1).apply(lambda frame: frame.apply(report_diff, axis=1))

# 칼럼순서 변경
cols = list(change_new.columns)
df_changed = df_changed[cols] 
df_changed = df_changed.reset_index()


df_removed = changes[changes["전표일자번호"].isin(삭제_전표일자번호)]
df_added = changes[changes["전표일자번호"].isin(추가_전표일자번호)]


dfs = [df_changed, df_removed, df_added]

#총괄 view
베이스_디렉토리 = os.getcwd()

wb = xw.Book(베이스_디렉토리 + '\\분개장차이.xlsx')
    
for i in range(len(dfs)):
    sht = wb.sheets[i]
    sht.range('A1').value = dfs[i]
