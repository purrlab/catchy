import os

import cv2
import numpy as np
import torch as t
from PIL import Image, ImageDraw
from doclayout_yolo import YOLOv10


class ImageExtractor:
    def __init__(
        self,
        model_path="src/feature_extraction/doclayout_yolo_docstructbench_imgsz1024.pt",
    ):
        self.model = YOLOv10(model_path)
        self.name_dict = {
            0: "title",
            1: "plain text",
            2: "abandon",
            3: "figure",
            4: "figure_caption",
            5: "table",
            6: "table_caption",
            7: "table_footnote",
            8: "isolate_formula",
            9: "formula_caption",
        }
        if t.cuda.is_available():
            self.device = "cuda:0"
        else:
            self.device = "cpu"

    def extract_objects(self, img_path):
        det_res = self.model.predict(
            img_path, imgsz=1024, conf=0.2, device=self.device, verbose=False
        )
        result = det_res[0]
        obj_boxes = [box.numpy() for box in result.boxes.data]
        obj_names = [self.name_dict[int(item)] for item in result.boxes.cls]

        return {"bboxes": obj_boxes, "labels": obj_names}
