import os

import cv2
import numpy as np
import torch as t
from PIL import Image, ImageDraw
from doclayout_yolo import YOLOv10


class ImageExtractor():
    def __init__(self, model_path="./doclayout_yolo_docstructbench_imgsz1024.pt"):
        self.model = YOLOv10(model_path)

    def extract_img(self, img_path):
        det_res = self.model.predict(img_path, imgsz=1024, conf=0.2, device="cpu")
        result = det_res[0]
        obj_boxes = result.boxes
        obj_names = result.names
        img = result.orig_img  # get original image as NumPy array

        # Filter boxes with class 3 or 4
        keep_mask = t.isin(obj_boxes.cls.int(), t.tensor([3, 4]))
        filtered_boxes = obj_boxes.data[keep_mask]

        return img, filtered_boxes, obj_names


# Define extractor
extractor = ImageExtractor()
os.makedirs('./result', exist_ok=True)

file_list = [file for file in os.listdir('./data') if file.endswith(".jpg")]
file_list.sort()

for file in file_list:
    img_path = os.path.join('./data', file)
    img_np, filtered_boxes, obj_names = extractor.extract_img(img_path)

    # Convert to PIL for easy drawing
    img_pil = Image.fromarray(cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)

    for box in filtered_boxes:
        x1, y1, x2, y2 = box[:4].tolist()
        conf = box[4].item()
        cls = int(box[5].item())
        if cls == 3:
            draw.rectangle([x1, y1, x2, y2], outline="red", width=4)
            draw.text((x1, y1), f"cls={obj_names[cls]}, conf={conf:.2f}", fill="red")
        else:
            draw.rectangle([x1, y1, x2, y2], outline="green", width=4)
            draw.text((x1, y1), f"cls={obj_names[cls]}, conf={conf:.2f}", fill="green")

    # Convert back to OpenCV format for saving
    result_img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
    result_path = os.path.join("./result", file)
    cv2.imwrite(result_path, result_img)
