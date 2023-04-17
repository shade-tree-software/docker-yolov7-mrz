import os
import io
from hubconf import custom
from typing import Any
from PIL import Image

from passporteye import read_mrz

from flask import Flask
from flask import request

app = Flask(__name__)

model = custom(path_or_model='/app/src/yolov7/yolov7-tiny-mrz.pt') 

@app.route("/ping")
def ping() -> dict[str, bool]:
    return {"success": True}

@app.route("/mrz", methods=["POST"])
def mrz() -> dict[str, Any]:
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
