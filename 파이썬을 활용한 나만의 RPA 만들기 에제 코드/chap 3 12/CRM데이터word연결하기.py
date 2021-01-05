from __future__ import print_function
from mailmerge import MailMerge
from datetime import date

# MS Word로 만들어진 템플렛을 변수로 설정한다. MS Word로 만들어진 템플렛은 작업 폴더에 같이 저장되어 있다고 가정한다.
template_1 = "고객감사메일.docx"
template_2 = "고객감사메일-구매이력.docx"

# Show a simple example
document_1 = MailMerge(template_1)

print(document_1.get_merge_fields())


# 키워드 인자로 넣기 위한 딕셔너리 사전 작업
고객_1 = {
    '등급': 'Gold',
    '전화번호': '070-XXX-XXXX',
    '상호': '좋은 신발',
    '구입총액': '500,000원',
    '배송한도': '50,000원',
    '주소': '서울시 종로구 11번지',
    '날짜': '{:%Y-%m-%d}'.format(date.today()),
    '할인': '5%',
    '수신자': '이순신'
}

# 키워드 인자 **변수명으로 넣는다.
document_1.merge(**고객_1)


# 별도의 워드 문서로 저장하기 위해 write() 함수를 이용한다. 
document_1.write('example1.docx')

# Try example number two where we create multiple pages
# Define a dictionary for 3 customers
고객_1 = {
    '등급': 'Gold',
    '전화번호': '070-XXX-XXXX',
    '상호': '좋은 신발',
    '구입총액': '500,000원',
    '배송한도': '50,000원',
    '주소': '서울시 종로구 11번지',
    '날짜': '{:%Y-%m-%d}'.format(date.today()),
    '할인': '5%',
    '수신자': '이순신'
}

고객_2 = {
    '등급': 'Silver',
    '전화번호': '070-XXX-XXXX',
    '상호': '컴퓨터 세상',
    '구입총액': '300,000원',
    '배송한도': '60,000원',
    '주소': '경상남도 창원시',
    '날짜': '{:%Y-%m-%d}'.format(date.today()),
    '할인': '3%',
    '수신자': '강감찬'
}

고객_3 = {
    '등급': 'Bronze',
    '전화번호': '070-XXX-XXXX',
    '상호': '만나 청과',
    '구입총액': '200,000원',
    '배송한도': '70,000원',
    '주소': '대전시 123 아파트',
    '날짜': '{:%Y-%m-%d}'.format(date.today()),
    '할인': '2%',
    '수신자': '김유신'
}

document_2 = MailMerge(template_1)
document_2.merge_pages([고객_1, 고객_2, 고객_3])
document_2.write('example2.docx')

# Final Example includes a table with the sales history

구매이력 = [{
    '물품': '사과',
    '가격': '1,000원',
    '수량': '25개',
    '금액': '25,000원'
}, {
    '물품': '배',
    '가격': '2,000원',
    '수량': '10개',
    '금액': '20,000원'
}, {
    '물품': '딸기',
    '가격': '5,000원',
    '수량': '40개',
    '금액': '200,000원'
}]

document_3 = MailMerge(template_2)
document_3.merge(**고객_3)
document_3.merge_rows('물품', 구매이력)
document_3.write('example3.docx')