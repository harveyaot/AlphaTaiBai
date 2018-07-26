#coding:utf-8
import os
from flask import Flask, render_template, request, send_from_directory
from label_image import *
from PIL import Image

app = Flask(__name__)


UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
sents = [("山有木兮木有枝，心悦君兮君不知。", 0.9), 
         ("人生自是有情痴，此恨不关风与月。", 0.8),
         ("自在飞花轻似梦，无边丝雨细如愁。", 0.7),
         ("疏影横斜水清浅，暗香浮动月黄昏。", 0.6)
         ]


### Global Variable##
input_height = 299
input_width = 299
input_mean = 0
input_std = 255
input_layer = "Placeholder"
output_layer = "final_result"

model_file = "./models/output_graph.pb"
label_file = "./models/output_labels.txt"


## Global Initialization##

graph = load_graph(model_file)

input_name = "import/" + input_layer
output_name = "import/" + output_layer
input_operation = graph.get_operation_by_name(input_name)
output_operation = graph.get_operation_by_name(output_name)
labels = load_labels(label_file)

sess = tf.Session(graph=graph)
mingju_d = load_mingju()



@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['image']
    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filename)
    ## logic to call the service
    t = read_tensor_from_image_file(
      filename,
      input_height=input_height,
      input_width=input_width,
      input_mean=input_mean,
      input_std=input_std)
    ##
    results = sess.run(output_operation.outputs[0], {input_operation.outputs[0]:t})
    results = np.squeeze(results)
    top_k = results.argsort()[-10:][::-1]
    sents = [(labels[i], results[i]) for i in top_k]
    res = [(sent[0], mingju_d.get(sent[0],("", ""))[0], mingju_d.get(sent[0], ("", ""))[1], "%.3f"%sent[1]) for sent in sents]
    invalidImage = False

    return render_template('index.html',sents=res,filename=filename, invalidImage=invalidImage, init=True)

@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
