from flask import Flask

app = Flask(__name__)

#리스트, 딕셔너리를 활용하여 메모리를 사용하기 때문에 나중에 값 수정할 경우 날아감,,, 일반적으로 DB에서 다룸

topics = [
    {'id': 1, 'title': 'html', 'body': 'html is ...'},
    {'id': 2, 'title': 'css', 'body': 'css is ...'},
    {'id': 3, 'title': 'javascript', 'body': 'javascript is ...'}
]

def template(contents, content):
    return f'''<!doctype html>
    <html>
        <body>
            <h1><a href="/">WEB</a></h1>
            <ol>
                {contents}
            </ol>
            {content}
        </body>
    </html>
    '''

def getContents():
    liTags = ''
    for topic in topics:
        liTags = liTags + f'<li><a href="/read/{topic["id"]}/">{topic["title"]}</a></li>'
    return liTags

@app.route('/')
def index():

    return template(getContents(), '<h2>Welcome</h2>Hello, WEB')

@app.route('/read/<int:id>/')   #<> 이렇게 하면, 이 자리에 있는 값을 받아올 수 있음
def read(id):
        title = ''
        body = ''
        for topic in topics:
            if id == topic['id']:
                title = topic['title']
                body = topic['body']
                break
        return template(getContents(), f'<h2>{title}</h2>{body}')

@app.route('/create/')
def create():
    return 'Create'

app.run(debug=True)