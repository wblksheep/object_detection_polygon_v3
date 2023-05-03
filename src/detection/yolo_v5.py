import torch
from pathlib import Path
import torchvision.transforms as transforms
from PIL import Image
import cv2
from yolov5.models.experimental import attempt_load
from yolov5.utils.torch_utils import select_device
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

    def capture_image(self):
        # Capture an image from the camera
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        return frame

    def detect_objects(self, frame=None):
        if frame is None:
            frame = self.capture_image()
        results = self.model(frame)
        self.detections = results.xyxy[0].cpu().numpy()
        return self.detections

def load_yolo_model():
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    model.to('cuda' if torch.cuda.is_available() else 'cpu')
    model.eval()
    return model

def preprocess_image(image):
    preprocess = transforms.Compose([
        transforms.Resize((640, 640)),
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
    ])
    return preprocess(image).unsqueeze(0)

def detect_objects(image, model):
    with torch.no_grad():
        image_tensor = preprocess_image(image)
        detections = model(image_tensor)
        detections = detections.xyxy[0].cpu().numpy()
        return detections
