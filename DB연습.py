# DB 연결

import sqlite3

# DB 연결
# conn = sqlite3.connect('c:\\work\\test.db')
# 메모리 연결로 변경
conn = sqlite3.connect(':memory:')

# 커서 생성
cursor = conn.cursor()
# SQL 실행 (PhoneBook 테이블 생성)
cursor.execute('''CREATE TABLE IF NOT EXISTS PhoneBook (
                    Name TEXT NOT NULL,
                    PhoneNum TEXT NOT NULL
                );'''
)

# SQL 실행 (데이터 삽입) 홍길동, 010-1234-5678 삽입
cursor.execute("INSERT INTO PhoneBook (Name, PhoneNum) VALUES ('홍길동', '010-1234-5678');")    

# SQL 실행 (데이터 삽입) 파라미터로 처리
name = '김철수'
phone_num = '010-9876-5432'
cursor.execute("INSERT INTO PhoneBook (Name, PhoneNum) VALUES (?, ?);", (name, phone_num))

# 여러 데이터 삽입
data = [
    ('이영희', '010-5555-6666'),
    ('박민수', '010-7777-8888'),
    ('최지훈', '010-9999-0000')
]
cursor.executemany("INSERT INTO PhoneBook (Name, PhoneNum) VALUES (?, ?);", data)

# 변경사항 커밋
conn.commit()

# SQL 실행 (데이터 조회) 반복문으로
cursor.execute("SELECT * FROM PhoneBook;")
rows = cursor.fetchall() # 모든 행을 가져옴
for row in rows:
    print(row)

# DB 연결 종료
conn.close()

