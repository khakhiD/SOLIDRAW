import imghdr
import os
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import convert

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = 'static/img/'


def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413

#기본 주소
@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_PATH'])
    #파일 업로드 동작(드롭다운 등)은 static의 js 파일에 정의되어 있음
    return render_template('index.html', files=files)

#파일 업로드 동작
@app.route('/', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                file_ext != validate_image(uploaded_file.stream):
            return "Invalid image", 400

        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], "before.png"))
        convert.main()
    return '', 204

#캐쉬 문제 해결 코드
@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

if __name__ == '__main__':
    app.run(port=5000, debug=True)
