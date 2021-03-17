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

