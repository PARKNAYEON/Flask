# 파이썬 데이터베이스 연동
# 테이블 생성 및 삽입

import sqlite3
import datetime

# 삽입 날짜 생성
now = datetime.datetime.now()

nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')


# sqlite3
print('sqlite3.version : ', sqlite3.version)
print('sqlite3.sqite_version : ', sqlite3.sqlite_version)

# db 생성 & Auto commit(Rollback) -> 그때 그때 데이터베이스에 넣는다
conn = sqlite3.connect('C:/Users/netid/Desktop/git/Flask/python/database.db', isolation_level=None)

#Cursor
c = conn.cursor()
print('cursor Type : ', type(c))



# 테이블 생성(Data Type : TEXT, NUMERIC INTEGER REAL BLOB)
c.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username text, email text, phone text, website text, regdate text)") 

# 데이터 삽입
c.execute("INSERT INTO users VALUES(1, 'Kim', 'kim@naver.com', '010-0000-0000', 'kim.com', ?)", (nowDatetime,))
c.execute("INSERT INTO users(id, username, email, phone, website, regdate) VALUES (?,?,?,?,?,?)", (2, 'Park', 'Park@daum.net', '010-1111-1111','park,com', nowDatetime))

# Many 삽입(튜플, 리스트)
userList = (
    (3, 'Lee', 'Lee@naver.com', '010-2222-2222', 'Lee.com', nowDatetime),
    (4, 'cho', 'cho@naver.com', '010-2222-2222', 'cho.com', nowDatetime),
    (5, 'You', 'You@naver.com', '010-2232-2222', 'You.com', nowDatetime)
)

c.executemany("INSERT INTO users(id, username, email, phone, website, regdate) VALUES(?,?,?,?,?,?)", userList)


# 테이블 데이터 삭제
# conn.execute("DELETE FROM users")
# print("user db deleted : ", conn.execute("DELETE FROM users").rowcount)


# 커밋 : isolation_level = None 일 경우 자동 반영(오토 커밋)
# conn.commit()

# 롤백
# conn.rollback()

conn.close()