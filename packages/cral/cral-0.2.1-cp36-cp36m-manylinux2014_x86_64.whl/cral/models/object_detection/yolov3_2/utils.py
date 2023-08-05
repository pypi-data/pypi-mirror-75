# import tensorflow as tf
from tensorflow import keras
import numpy as np
from PIL import Image,ImageDraw

from .yolov3 import _YOLO_SIZE,_YOLO_ANCHORS,_YOLO_MASKS,YoloV3,YoloLoss
class Yolov3Config:
    def __init__(self, 
        size=_YOLO_SIZE, 
        anchors=_YOLO_ANCHORS,
        anchor_masks=_YOLO_MASKS,
        max_boxes=100,
        iou_threshold=0.5,
        score_threshold=0.5):
        """For Configuring Yolo Network 
        
        Args:
            size (int or tuple(int), 416): All Images will be resized to this size
            anchors (list, optional): List of Anchors with in the same scale as size
            anchor_masks (list, optional): List of Masks to used with Anchors 
            max_boxes (int, 100): Max number of Bboxes an image can contain
            iou_threshold (float, 0.5): Any bboxes with iou greater thanthreshold will be merged by NMS
            score_threshold (float, 0.5): Any prediction with lower score will be ignored in NMS
        """
        assert isinstance(size,int) or ( isinstance(size,tuple) and len(size)==2) , f"Expected an Integer or tuple of size 2 got {size} instead"
        if isinstance(size,tuple):
            height=size[0]
            width=size[1]
            assert height==width and height%32==0, f'expected a square image with dimesions a multiple of 32, but got dimensions {height} x {width} instead'
            size=height

        assert (isinstance(anchors, list) or isinstance(anchors,np.ndarray))  and len(anchors)==9, f'expected a list of 9 elements, but got {type(anchors)} of {len(anchors)} elements instead' #TODO: check length of anchors
        if isinstance(anchors,list): 
            anchors = list(map(int, anchors))
            for i,anc in enumerate(anchors):
                for j,val in enumerate(anc):
                    anchors[i][j][0]=val[0]/size
                    anchors[i][j][1]=val[1]/size
            anchors=np.array(anchors,dtype=np.float32)

        assert (isinstance(anchor_masks,  list) or isinstance(anchor_masks,np.ndarray)), f'expected a list, but got {type(anchor_masks)} instead'
        assert isinstance(max_boxes,int) and max_boxes>0 ,f"Max boxes is expected to be a int greater than 0 got {max_boxes} instead"

        self.size = size
        self.anchors = anchors
        self.anchor_masks = anchor_masks
        self.max_boxes=max_boxes
        self.iou_threshold = iou_threshold
        self.score_threshold = score_threshold
        self.input_anno_format='yolo'
        self.num_classes=None

    def num_anchors(self):
        return len(self.anchors)
    def get_yolov3_from_config(self,base_trainable,train=True,weights=None):
        model=YoloV3(size=self.size, channels=3, anchors=self.anchors,
                     masks=self.anchor_masks, 
                     classes=self.num_classes, training=train,
                     max_boxes=self.max_boxes,
                     iou_threshold=self.iou_threshold,
                     score_threshold=self.score_threshold)
        
        #TODO:Set up weights in s3 then enable by removing and False
        if (weights is 'imagnet') and False:
            pretrained_weights=""
            model_pretrained = YoloV3(size=416, training=True, classes=80)
            model_pretrained.load_weights(pretrained_weights).expect_partial()
            model.get_layer('yolo_darknet').set_weights(model_pretrained.get_layer('yolo_darknet').get_weights())
            yolo_darknet=model.get_layer('yolo_darknet')
            yolo_darknet.trainable=base_trainable

        return model

    def get_loss_from_config(self):
        loss = [YoloLoss(self.anchors[mask], classes=self.num_classes)
        for mask in self.anchor_masks]
        return loss

    def set_num_classes(self,num_classes):
        self.num_classes=num_classes

def annotate_image(orignal_image,predictions,save_path=None,show_image=False):
    boxes=predictions[0]
    img=Image.fromarray(orignal_image)
    img_draw=ImageDraw.Draw(img)
    w,h=img.size
    for box in boxes[0]:
        box=box
        xmin=box[0]*w  
        ymin=box[1]*h  
        xmax=box[2]*w
        ymax=box[3]*h
        if (xmin<xmax and ymin<ymax and xmin>=0 and ymin>=0):
          img_draw.rectangle([xmin,ymin,xmax,ymax])
    if show_image:
        img.show()
    if save_path is not None:
        img.save(save_path)
    return img


