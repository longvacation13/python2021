from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World'

# 단일모듈일 경우 아래 코드 필요 
if __name__ == '__main__':
    app.run() # 디버그 모드 실행
