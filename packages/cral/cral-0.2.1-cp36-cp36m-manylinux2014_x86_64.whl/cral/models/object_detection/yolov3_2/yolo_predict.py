from cral.models.object_detection.yolov3_2.yolov3 import YoloV3
from cral.models.object_detection.yolov3_2.dataset import yolo_preprocessing
import numpy as np
# from cral.models.object_detection.object_detection_utils import Predictor 
import os
from cral.data_versioning.cral_util import _ALLOWED_IMAGE_FORMATS
from tensorflow import keras
import tensorflow as tf
class YoloPredictor():
    def __init__(self,num_classes,config,preprocessing_func,checkpoint_file):
        self.num_classes=num_classes
        self.size=config.size
        self.preprocessing_func=preprocessing_func
        self.prediction_model=config.get_yolov3_from_config(base_trainable=False,train=False)
        self.prediction_model.load_weights(filepath=os.path.join(checkpoint_file,'variables','variables'))

    def predict(self,image_path):
        assert os.path.isfile(image_path) and image_path.endswith(_ALLOWED_IMAGE_FORMATS), f"{image_path} is not a valid image file of format {_ALLOWED_IMAGE_FORMATS}"
        image_array=self.load_image(image_path)
        orignal_image=image_array
        image_array=tf.image.resize(image_array,(self.size,self.size))
        ##TODO Support custom preprocessing function      
        # if self.preprocessing_func is not None:
        #     image_array=self.preprocessing_func(image_array)
        # else:
        image_array=yolo_preprocessing(image_array)
        image_array=tf.expand_dims(image_array,0) 
        return orignal_image,self.prediction_model.predict(image_array)

    def load_image(self, image_path) :
        img_array= np.array(keras.preprocessing.image.load_img(path=image_path))
        # print(img_array.shape,img_array.dtype)
        return img_array


