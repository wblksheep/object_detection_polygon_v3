import torch
from pathlib import Path
import torchvision.transforms as transforms
from torchvision.transforms import Compose, Resize, ToTensor, Normalize
from PIL import Image
import cv2
from yolov5.models.experimental import attempt_load
from yolov5.utils.torch_utils import select_device
from yolov5.utils.general import non_max_suppression,check_img_size,scale_boxes
from yolov5.utils.dataloaders import LoadImages
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

    def detect(self, image_path, conf_thres=0.25, iou_thres=0.45):
        imgsz = check_img_size(640, s=self.model.stride.max())  # 检查图片大小
        half = self.device.type != 'cpu'  # 半精度只支持GPU

        if half:
            self.model.half()

        # 设置模型为评估模式
        self.model.eval()

        # 加载图像
        dataset = LoadImages(image_path, img_size=imgsz)

        for path, img, im0s, _, _ in dataset:
            img = torch.from_numpy(img).to(self.device)
            img = img.half() if half else img.float()  # uint8 to fp16/32
            img /= 255.0  # 图像归一化
            if img.ndimension() == 3:
                img = img.unsqueeze(0)

            # 推理
            with torch.no_grad():
                pred = self.model(img, augment=False)[0]

            # 应用NMS
            pred = non_max_suppression(pred, conf_thres, iou_thres)

            # 处理检测结果
            for i, det in enumerate(pred):
                det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], im0s.shape).round()

                # 打印结果
                return det


