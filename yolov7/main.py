import os
import io
from hubconf import custom
from typing import Any
from PIL import Image

from passporteye import read_mrz

from flask import Flask
from flask import request

app = Flask(__name__)


@app.route("/ping")
def ping():
    return {"success": True}

@app.route('/coco', methods=["POST"])
def coco():
    model = custom(path_or_model='/app/yolov7/yolov7.pt')
    img = Image.open(io.BytesIO(request.stream.read()))
    raw_preds = model([img]).xyxy[0]
    preds = []
    names = [ 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
         'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
         'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
         'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
         'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
         'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
         'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
         'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
         'hair drier', 'toothbrush' ]
    for raw_pred in raw_preds.tolist():
        if raw_pred[4] >= 0.5:
            preds.append({
                'name': names[int(raw_pred[5])],
                'bbox': [round(i) for i in raw_pred[0:4]],
                'conf': raw_pred[4]
            })
    return preds

@app.route("/mrz", methods=["POST"])
def mrz():
    model = custom(path_or_model='/app/yolov7/yolov7-tiny-mrz.pt') 
    img = Image.open(io.BytesIO(request.stream.read()))
    img_preds = model([img]).xyxy[0]
    if len(img_preds) > 0:
        best_pred = img_preds[0].tolist()
        pred_dict = {
            'xyxy': best_pred[0:4],
            'conf': best_pred[4]
        }
        if pred_dict['conf'] >= 0.5:
            # crop image down to just the mrz to make it easier for passporteye to find it
            img_cropped = img.crop(pred_dict['xyxy'])
            with io.BytesIO() as image_bytes:
                img_cropped.save(image_bytes, 'jpeg')
                # See if passporteye can find the mrz
                mrz = read_mrz(image_bytes.getvalue())
                if mrz:
                    return mrz.to_dict()
                else:
                    return 'Unable to locate mrz\n', 400
        else:
            return 'Unable to locate mrz\n', 400
    else:
        return 'Unable to locate mrz\n', 400
    
if __name__ == "__main__":
    port = os.environ.get("PORT", 0)
    app.run(host="0.0.0.0", port=port)
