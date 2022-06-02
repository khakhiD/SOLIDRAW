from flask import Flask
app = Flask(__name__)
@app.route('/')
@app.route('/home')
def home():
    return 'Hello, World!'
@app.route('/user')
def user():
    return 'Hello, User!'
if __name__ == '__main__':
    app.run(debug=True)