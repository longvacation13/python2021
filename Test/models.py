# DB 관련 
# 참조 블로그 : https://dog-foot-story.tistory.com/71 
# 1.연결 객체 생성 
import sqlite3
from sqlite3.dbapi2 import Cursor
db = sqlite3.connect(r"D:\python project\flask\DBData\test1.db")
print(db)

# 2. 커서(쿼리문 전달 가능객체) 생성  
cursor = db.cursor()
print(cursor)

# 3. 테이블 생성 
# 초기화 ( 아래 작업이 없을 경우 계속 데이터 쌓이게 됨 )
cursor.execute("DROP TABLE IF EXISTS stInfo")
cursor.execute("CREATE TABLE stInfo(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER)")

# 4. 데이터 삽입    
# 4-1. 데이터 단건 삽입
cursor.execute("INSERT INTO stInfo(name, age) VALUES('홍길동', 20)")

# 4-2. 데이터 복수건 삽입 
cursor.executescript("""
    INSERT INTO stInfo(name, age) VALUES ('김길동','20');
    INSERT INTO stInfo(name, age) VALUES ('안길동','20');
    INSERT INTO stInfo(name, age) VALUES ('윤길동','20');
    INSERT INTO stInfo(name, age) VALUES ('이길동','20');
    INSERT INTO stInfo(name, age) VALUES ('신길동','20');
""")

# 5. 데이터 검색 
cursor.execute("SELECT * FROM stInfo")

# 5-1. 모든 행 읽기 
print(cursor.fetchall())

# 종료 
print('db test end')