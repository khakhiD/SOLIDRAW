import os
from flask import Flask, request
from werkzeug.utils import secure_filename

UPLOAD_DIR = "D:/"

app = Flask(__name__)
app.config['UPLOAD_DIR'] = UPLOAD_DIR

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
        </form>
    </body>
    </html>"""

@app.route('/file-upload', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return 'File upload complete'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)