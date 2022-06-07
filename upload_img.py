import os
from flask import Flask, request, flash, redirect
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def upload_main():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>File Upload</title>
    </head>
    <body>
        <form action="http://localhost:5000/file-upload" method="POST" enctype="multipart/form-data">
            <input type="file" name="file">
            <input type="submit">
            <br><br><br>
            <a href="./list">이미지 확인</a>
        </form>
    </body>
    </html>"""

@app.route('/file-upload', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        f = request.files['file']
        f.save('./uploaded_img/' + secure_filename(f.filename))

        return """
             <script>
                alert("File upload complete");
                window.location = '/';
             </script>
        """

@app.route('/list')
def img_list():
	return """
	<!DOCTYPE html>
    <html>
    <body>
    <a href="/">홈페이지</a>
    <h2>업로드한 사진</h2>
    <img src="C:/Users/dyson/Desktop/archive/python_work/SOLIDRAW/uploaded_img/test.png">
    </body>
    </html>
	"""


if __name__ == '__main__':
    app.run(debug=True)