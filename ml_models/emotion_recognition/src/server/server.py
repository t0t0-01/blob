import os
from flask import Flask, request

os.chdir(r"C:\Users\Anton\Desktop\FYP\emotion_recognition\src\server")
UPLOAD_FOLDER = './static/uploads/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return {"status": "No file selected"}
    file = request.files['file']
    if file.filename == '':
        return {"status": "No file selected"}
    
    else:
        filename = file.filename
        print(filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        return {"status": "ok"}


app.run("0.0.0.0", port=5000)