import imghdr
import os
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import convert

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
#input 데이터의 확장자 조건
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
#이미지가 저장될 경로
app.config['UPLOAD_PATH'] = 'solidraw/static/img/'


def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

#오류 핸들러, 파일 크기가 너무 크면 413 에러를 뱉어냄
#에러 핸들러로 리다이렉트 되지 않아 오류 핸들러 작성
@app.errorhandler(413)
def too_large(e):
    return "파일이 너무 큽니다!", 413

#기본 주소
@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_PATH'])
    #파일 업로드 동작(드롭다운 등)은 static의 js 파일에 정의되어 있음
    #전체 사이트 껍데기 index.html에 있음
    return render_template('index2.html', files=files)

#파일 업로드 동작
@app.route('/', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        #파일 확장자가 jpg, png, gif가 아니면 400번 에러 뱉음
        if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                file_ext != validate_image(uploaded_file.stream):
            return "Invalid image", 400
        #다른 에러 처리기에 걸리지 않으면 input 이미지를 before.png라는 이름과 확장자를 가진 파일로 저장
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
