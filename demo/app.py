
import os
from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)


UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
sents = ["山有木兮木有枝，心悦君兮君不知", 
         "人生自是有情痴，此恨不关风与月",
         "自在飞花轻似梦，无边丝雨细如愁",
         "疏影横斜水清浅，暗香浮动月黄昏",
         ]

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['image']
    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

    file.save(filename)
    invalidImage = False

    return render_template('index.html',sents=sents,filename=filename, invalidImage=invalidImage, init=True)

@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
