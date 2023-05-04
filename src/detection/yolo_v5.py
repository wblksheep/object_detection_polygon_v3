import torch
from pathlib import Path
import torchvision.transforms as transforms
from torchvision.transforms import Compose, Resize, ToTensor, Normalize
from PIL import Image
import cv2
from yolov5.models.experimental import attempt_load
from yolov5.utils.torch_utils import select_device
from yolov5.utils.general import non_max_suppression
import os
os.environ['http_proxy']='http://127.0.0.1:1080'
os.environ['https_proxy']='http://127.0.0.1:1080'
class YOLOv5:
    def __init__(self, model_path="models/yolov5s-seg.pt"):
        #设备配置
        self.device=select_device('cuda' if torch.cuda.is_available() else 'cpu')

        #加载模型
        self.model= attempt_load(model_path, device=self.device)
        # self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s-seg', pretrained=True, path=model_path)
        # Add image transforms
        self.img_transforms = Compose([
            Resize((640, 640)),
            ToTensor(),
            Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
    def capture_image(self):
        # Capture an image from the camera
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        return frame

    def detect_objects(self, img_tensor):
        with torch.no_grad():
            detections = self.model(img_tensor)
        # Apply non-maximum suppression
        nms_results = non_max_suppression(detections, conf_thres=0.25, iou_thres=0.45)
        # Convert the results to a numpy array
        detections_np = [result.cpu().numpy() for result in nms_results]
        return detections_np

