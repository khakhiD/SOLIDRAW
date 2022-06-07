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
            <a href="./list">파일 목록</a>
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
	file_list = os.listdir("./uploaded_img")
	html = """<center><a href="/">홈페이지</a><br><br>"""
	html += "file_list: {}".format(file_list) + "</center>"
	return html


if __name__ == '__main__':
    app.run(debug=True)