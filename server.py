from flask import Flask
from flask import request, redirect

app = Flask(__name__)

nextId = 4
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
            <ul>
            <li><a href="/create/">create</a></li>
            </ul>
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

@app.route('/create/', methods=['GET', 'POST'])
def create():
    print('request.method', request.method)
    if request.method == 'GET':
        content = '''
            <form action="/create/" method="POST">
                <p><input type="text" name="title" placeholder="title"></p>
                <p><textarea name="body" placeholder="body"></textarea></p>
                <p><input type="submit" value="create"></p>
            </form>
        '''
        return template(getContents(), content)
    elif request.method == 'POST':
        global nextId
        title = request.form['title']
        body = request.form['body']
        newTopic = {'id': nextId, 'title': title, 'body': body}
        topics.append(newTopic)
        url = '/read/'+str(nextId)+'/'
        nextId = nextId + 1

        return redirect(url)


app.run(debug=True)