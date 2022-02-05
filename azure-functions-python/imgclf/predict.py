from datetime import datetime
from PIL import Image
from torchvision import transforms
from urllib.request import urlopen, urlretrieve
from .model import ImageClf18
from torch import nn

import logging
import os
import sys
import torch
import tempfile

def reporthook(blocknum, blocksize, totalsize):
    readsofar = blocknum * blocksize
    if totalsize > 0:
        percent = readsofar * 1e2 / totalsize
        s = "\r%5.1f%% %*d / %d" % (
            percent, len(str(totalsize)), readsofar, totalsize)
        sys.stderr.write(s)
        if readsofar >= totalsize: # near the end
            sys.stderr.write("\n")
    else: # total size is unknown
        sys.stderr.write("read %d\n" % (readsofar,))

model = ImageClf18()
# load best checkpoint
dirname = os.path.dirname(__file__)
#tmp_dir = "/tmp"
tmp_dir = tempfile.gettempdir() # prints the current temporary directory

model_url = "https://longriverstorage.blob.core.windows.net/alphataibai/models/imgclf/imgclf18.pt?sv=2020-10-02&st=2022-02-05T05%3A10%3A01Z&se=2022-10-06T05%3A10%3A00Z&sr=b&sp=r&sig=FTcIlE7vaJsbUp3gzSkTmO9Mtbp7sOfH3cb1wkghYGk%3D"


#conn_str = os.getenv('longriverblob')
"""
if not os.path.exists(os.path.join(dirname, model_local_clf)):
    logging.info("Loading CLF model remotely")
    urlretrieve(model_clf_url, os.path.join(tmp_dir, model_local_clf), reporthook)
    clf_checkpoint = torch.load(os.path.join(tmp_dir, model_local_clf), map_location=torch.device('cpu'))
else:
    logging.info("Loading CLF model locally")
    clf_checkpoint = torch.load(os.path.join(dirname, model_local_clf), map_location=torch.device('cpu'))
model.clf.load_state_dict(clf_checkpoint)

if not os.path.exists(os.path.join(dirname, model_local_encoder)):
    logging.info("Loading encoder model remotely")
    urlretrieve(model_encoder_url, os.path.join(tmp_dir, model_local_encoder), reporthook)
    encoder_checkpoint = torch.load(os.path.join(tmp_dir, model_local_encoder), map_location=torch.device('cpu'))
else:
    logging.info("Loading encoder model locally")
    encoder_checkpoint = torch.load(os.path.join(dirname, model_local_encoder), map_location=torch.device('cpu'))
model.img_encoder.load_state_dict(encoder_checkpoint)
"""

#model.load_state_dict(best_checkpoint["state_dict"])
model_clf18 = "imgclf18.pt"
if not os.path.exists(os.path.join(dirname, model_clf18)):
    logging.info("Loading model remotely")
    urlretrieve(model_url, os.path.join(tmp_dir, model_clf18), reporthook)
    model_checkpoint = torch.load(os.path.join(tmp_dir, model_clf18), map_location=torch.device('cpu'))
else:
    logging.info("Loading model model locally")
    model_checkpoint = torch.load(os.path.join(dirname, model_clf18), map_location=torch.device('cpu'))

model.load_state_dict(model_checkpoint)
model.eval()
logging.info("model_loading complete")

def get_model_and_labels():
    class_dict = {}
    counter = 0
    try:
        #load labels data
        with open(os.path.join(dirname, 'labels.txt'), 'r',encoding='utf-8') as infile:
            for line in infile.readlines():
                out = line.split("\t")
                class_dict[int(out[0])] = out[1] + " " + out[3]
                counter += 1
    except FileNotFoundError:
        logging.info(os.listdir(os.curdir))
        logging.info(os.curdir)
        raise

    return class_dict

def predict_image_from_url(image_url, top=20):
    class_dict = get_model_and_labels()
    with urlopen(image_url) as testImage:
        input_image = Image.open(testImage).convert('RGB')
        preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
        ])
        input_tensor = preprocess(input_image)
        input_batch = input_tensor.unsqueeze(0) # create a mini-batch as expected by the model

        # move the input and model to GPU for speed if available
        device = 'cpu'
        if torch.cuda.is_available():
            input_batch = input_batch.to('cuda')
            device = 'cuda'
            model.to(device)

        with torch.no_grad():
            predicts = model(input_batch)
        # Tensor of shape 1000, with confidence scores over Imagenet's 1000 classes
        predicts = predicts.squeeze()
        if device == "cuda":
            predicts = predicts.cpu()
        # The output has unnormalized scores. To get probabilities, you can run a softmax on it.
        score, indices = torch.sort(nn.functional.softmax(predicts[:]), descending=True)
        res = []
        for idx, i in enumerate(indices.numpy()[:top]):
            res.append([int(i), class_dict[i],score[idx].item()])

        response = {
            'created': datetime.utcnow().isoformat(),
            'num':len(res),
            'predicts': res
        }

        logging.info(f'returning {response}')
        return response

if __name__ == '__main__':
    predict_image_from_url(sys.argv[1])
