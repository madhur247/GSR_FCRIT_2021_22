import torch
import cv2
import os
from models.common import DetectMultiBackend
from utils.dataloaders import LoadImages

from utils.general import (non_max_suppression, check_img_size, scale_boxes,xyxy2xywh, Profile)
import time

def run_yolov5(source_path,weights_path,conf_thresh,iou_thresh,space_path):
    spacefile = open(space_path,"r",encoding="utf-8")
    lines = spacefile.readlines()
    classes = [x[:-1] for x in lines]
    st = time.time()
    model = DetectMultiBackend(weights_path)
    source = source_path
    bs=1
    conf_thres=conf_thresh  # confidence threshold
    iou_thres=iou_thresh  # NMS IOU threshold
    result = []
    print("weights loaded")
    print("Load time",time.time()-st)
    stride, names, pt = model.stride, model.names, model.pt
    imgsz = check_img_size((608,608), s=stride)
    # img = cv2.imread(source)
    # shape = img.shape
    dataset = LoadImages(source, img_size=imgsz, stride=stride, auto=pt, vid_stride=1)
    model.warmup(imgsz=(1 if pt or model.triton else bs, 3, *imgsz))
    dt = (Profile(), Profile(), Profile())
    for path, im, im0s, vid_cap, s in dataset:
        with dt[0]:
            im = torch.from_numpy(im).to(model.device)
            im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
            im /= 255  # 0 - 255 to 0.0 - 1.0
            if len(im.shape) == 3:
                im = im[None]  # expand for batch dim

        # Inference
        with dt[1]:
            # visualize = increment_path(save_dir / Path(path).stem, mkdir=True) if visualize else False
            pred = model(im, augment=False, visualize=False)

        # NMS
        with dt[2]:
            pred = non_max_suppression(pred, conf_thres, iou_thres, None, False, max_det=1000)
        
        for det in pred:
            im0 = im0s.copy()
            # gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]
            if len(det):
                det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0.shape).round()
                for c in det[:, 5].unique():
                        n = (det[:, 5] == c).sum()  # detections per class
                        # s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "
                for *xyxy, conf, cls in reversed(det):
                    xyxy = list(map(int,xyxy))
                    # cv2.rectangle(img,(xyxy[0],xyxy[1]),(xyxy[2],xyxy[3]),(0,255,0),2)
                    result.append([classes[int(cls)],xyxy,float(conf)])
    # cv2.imshow("frame",img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return result
# res = run_yolov5("testing_images\૦૫૨ 218 ળડશ ળીઅંથ વઅઃપ ૫૨૧ ધઠગ રચસ એભીઅંયં આછૂબ_71.jpg","./YoloV5_model2/yolov5x_latest_8000/weights/best.pt",0.55,0.5,"space.names")
# print(res)