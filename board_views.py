# 참고자료 : https://dongchans.github.io/2019/25/ 
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3 
from sqlite3.dbapi2 import Cursor
from flask import send_file
app = Flask(__name__)

########################################################################
## 페이징 관련 
from tempfile import NamedTemporaryFile
import webbrowser

base_html = """
<!doctype html>
<html><head>
<meta http-equiv="Content-type" content="text/html; charset=utf-8">
<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/2.2.2/jquery.min.js"></script>
<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.16/css/jquery.dataTables.css">
<script type="text/javascript" src="https://cdn.datatables.net/1.10.16/js/jquery.dataTables.js"></script>
</head><body>%s<script type="text/javascript">$(document).ready(function(){$('table').DataTable({
    "pageLength": 50
});});</script>
<button>테스트버튼</button>
</body></html>
"""

def df_html(df):
    """HTML table with pagination and other goodies"""
    df_html = df.to_html()
    return base_html % df_html

# def df_window(df):
#     """Open dataframe in browser window using a temporary file"""
#     with NamedTemporaryFile(delete=False, suffix='.html') as f:
#         f.write(df_html(df))
#     webbrowser.open(f.name)

########################################################################

@app.route('/')
def index():       
    return render_template('index.html')

@app.route('/create')   # 잠깐 들어갔다 나오는 페이지 
def create():    
    db = sqlite3.connect(r"D:\python project\flask\DBData\board.db")
    
    cursor = db.cursor() # 커서는 쿼리문 전달 가능한 객체 

    # 초기화 ( 아래 작업이 없을 경우 계속 데이터 쌓이게 됨 )
    # cursor.execute("DROP TABLE IF EXISTS board")
    # cursor.execute("CREATE TABLE board(id INTEGER PRIMARY KEY autoincrement, title TEXT, content TEXT)")    

    title = request.args.get('title')
    content = request.args.get('content')
    cursor.execute('insert into board(title, content) values(?,?)', (title, content))
    db.commit()
    db.close()
    return redirect("/")


@app.route('/page/<int:num>') # 게시판 페이지 
def page(num): 
    db = sqlite3.connect(r"D:\python project\flask\DBData\board.db")
    cursor = db.cursor()
    sql_read = "select * from board limit 10 OFFSET ?"
    print(num)    
    res = cursor.execute(sql_read, (10*num,)).fetchall()
    db.close()
    return render_template('page.html', res=res)



# https://gist.github.com/mjanv/90d4ef43edbff3f3b0fc
@app.route('/analysis')    
def analysis():     
    # https://frhyme.github.io/python-lib/flask_pandas/
    import pandas as pd 
    import numpy as np         
    import matplotlib.pylab as plt        

    plt.rcParams["figure.figsize"] = (14,10)
    plt.rcParams['lines.linewidth'] = 2
    plt.rcParams['lines.color'] = 'r'
    plt.rcParams['axes.grid'] = True 

    df = pd.read_csv('static/202007_promdata.csv', encoding='utf-8')              
    plt.plot(df['OFFER_KIND_NM'], df['RLOAD_AMT_SUM'], 'bo')      
    f = plt.savefig('static/202007_promdata.png')
    return send_file('static/202007_promdata.png', mimetype='image/png')     

@app.route('/select')    
def select():     
    # https://frhyme.github.io/python-lib/flask_pandas/
    import pandas as pd 
    import numpy as np           

    df = pd.read_csv('static/202007_promdata.csv', encoding='utf-8')                  
    return base_html % df.to_html()        


        
# 단일모듈일 경우 아래 코드 필요 
if __name__ == '__main__':
    app.run() # 디버그 모드 실행    