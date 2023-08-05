import tensorflow as tf
from PIL import Image,ImageDraw
import os,tempfile
import numpy as np
# from absl.flags import FLAGS

#Debug mode will show the bboxes
#TF records need to be created from lock_data
debug=False
from cral.models.object_detection.yolov3_2.utils import Yolov3Config

@tf.function
def transform_targets_for_output(y_true, grid_size, anchor_idxs):
    # y_true: (N, boxes, (x1, y1, x2, y2, class, best_anchor))
    N = tf.shape(y_true)[0]

    # y_true_out: (N, grid, grid, anchors, [x, y, w, h, obj, class])
    y_true_out = tf.zeros(
        (N, grid_size, grid_size, tf.shape(anchor_idxs)[0], 6))

    anchor_idxs = tf.cast(anchor_idxs, tf.int32)

    indexes = tf.TensorArray(tf.int32, 1, dynamic_size=True)
    updates = tf.TensorArray(tf.float32, 1, dynamic_size=True)
    idx = 0
    for i in tf.range(N):
        for j in tf.range(tf.shape(y_true)[1]):
            if tf.equal(y_true[i][j][2], 0):
                continue
            anchor_eq = tf.equal(
                anchor_idxs, tf.cast(y_true[i][j][5], tf.int32))

            if tf.reduce_any(anchor_eq):
                box = y_true[i][j][0:4]
                box_xy = (y_true[i][j][0:2] + y_true[i][j][2:4]) / 2

                anchor_idx = tf.cast(tf.where(anchor_eq), tf.int32)
                grid_xy = tf.cast(box_xy // (1/grid_size), tf.int32)

                # grid[y][x][anchor] = (tx, ty, bw, bh, obj, class)
                indexes = indexes.write(
                    idx, [i, grid_xy[1], grid_xy[0], anchor_idx[0][0]])
                updates = updates.write(
                    idx, [box[0], box[1], box[2], box[3], 1, y_true[i][j][4]])
                idx += 1

    # tf.print(indexes.stack())
    # tf.print(updates.stack())

    return tf.tensor_scatter_nd_update(
        y_true_out, indexes.stack(), updates.stack())


def transform_targets(y_train, anchors, anchor_masks, size):
    y_outs = []
    grid_size = size // 32

    # calculate anchor index for true boxes
    anchors = tf.cast(anchors, tf.float32)
    anchor_area = anchors[..., 0] * anchors[..., 1]
    box_wh = y_train[..., 2:4] - y_train[..., 0:2]
    box_wh = tf.tile(tf.expand_dims(box_wh, -2),
                     (1, 1, tf.shape(anchors)[0], 1))
    box_area = box_wh[..., 0] * box_wh[..., 1]
    intersection = tf.minimum(box_wh[..., 0], anchors[..., 0]) * \
        tf.minimum(box_wh[..., 1], anchors[..., 1])
    iou = intersection / (box_area + anchor_area - intersection)
    anchor_idx = tf.cast(tf.argmax(iou, axis=-1), tf.float32)
    anchor_idx = tf.expand_dims(anchor_idx, axis=-1)

    y_train = tf.concat([y_train, anchor_idx], axis=-1)

    for anchor_idxs in anchor_masks:
        y_outs.append(transform_targets_for_output(
            y_train, grid_size, anchor_idxs))
        grid_size *= 2

    return tuple(y_outs)


def transform_images(x_train, size):
    x_train = tf.image.resize(x_train, (size, size))
    return x_train
def yolo_preprocessing(x):
    x=tf.divide(tf.cast(x, tf.float32) ,255.0)
    return x


# https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/using_your_own_dataset.md#conversion-script-outline-conversion-script-outline
# Commented out fields are not required in our project
IMAGE_FEATURE_MAP = {
    # 'image/width': tf.io.FixedLenFeature([], tf.int64),
    # 'image/height': tf.io.FixedLenFeature([], tf.int64),
    # 'image/filename': tf.io.FixedLenFeature([], tf.string),
    # 'image/source_id': tf.io.FixedLenFeature([], tf.string),
    # 'image/key/sha256': tf.io.FixedLenFeature([], tf.string),
    'image/encoded': tf.io.FixedLenFeature([], tf.string),
    # 'image/format': tf.io.FixedLenFeature([], tf.string),
    'image/object/bbox/xmin': tf.io.VarLenFeature(tf.float32),
    'image/object/bbox/ymin': tf.io.VarLenFeature(tf.float32),
    'image/object/bbox/xmax': tf.io.VarLenFeature(tf.float32),
    'image/object/bbox/ymax': tf.io.VarLenFeature(tf.float32),
    'image/object/class/text': tf.io.VarLenFeature(tf.string),
    # 'image/object/class/label': tf.io.VarLenFeature(tf.int64),
    # 'image/object/difficult': tf.io.VarLenFeature(tf.int64),
    # 'image/object/truncated': tf.io.VarLenFeature(tf.int64),
    # 'image/object/view': tf.io.VarLenFeature(tf.string),
}
TF_RECORD_FEATURES = {
  'image/height': tf.io.FixedLenFeature([], tf.int64),
  'image/width': tf.io.FixedLenFeature([], tf.int64),
  'image/encoded': tf.io.FixedLenFeature([],tf.string),
  'image/object/bbox/xmin': tf.io.VarLenFeature(tf.keras.backend.floatx()),
  'image/object/bbox/xmax': tf.io.VarLenFeature(tf.keras.backend.floatx()),
  'image/object/bbox/ymin': tf.io.VarLenFeature(tf.keras.backend.floatx()),
  'image/object/bbox/ymax': tf.io.VarLenFeature(tf.keras.backend.floatx()),
  'image/f_id': tf.io.FixedLenFeature([], tf.int64),
  'image/object/class/label':tf.io.VarLenFeature(tf.int64)
  }

##ADDED max_boxes (REMEMBER TO CHANGE IN TRAIN)
def parse_tfrecord(tfrecord, size,max_boxes):
    x = tf.io.parse_single_example(tfrecord, TF_RECORD_FEATURES)
    
    x_train = tf.image.decode_jpeg(x['image/encoded'], channels=3)
    x_train = tf.image.resize(x_train, (size, size))
    
    height=tf.cast(x['image/height'],dtype=tf.keras.backend.floatx())
    width=tf.cast(x['image/width'],dtype=tf.keras.backend.floatx())
    
    
    labels = tf.cast(tf.sparse.to_dense(x['image/object/class/label'], default_value=-1),dtype=tf.keras.backend.floatx())
    
    xmins=tf.sparse.to_dense(x['image/object/bbox/xmin'])
    ymins=tf.sparse.to_dense(x['image/object/bbox/ymin'])
    xmaxs= tf.sparse.to_dense(x['image/object/bbox/xmax'])
    ymaxs=tf.sparse.to_dense(x['image/object/bbox/ymax'])
    ##To convert to yolo from pascal 
    xmins=tf.divide(xmins,width)
    ymins=tf.divide(ymins,height)
    xmaxs=tf.divide(xmaxs,width)
    ymaxs=tf.divide(ymaxs,height)

    y_train = tf.stack([xmins,ymins,xmaxs,ymaxs,labels], axis=1)

    paddings = [[0, max_boxes - tf.shape(y_train)[0]], [0, 0]]
    y_train = tf.pad(y_train, paddings)
    return x_train, y_train


def load_tfrecord_dataset(file_pattern, config):
    files = tf.data.Dataset.list_files(file_pattern)
    dataset = files.flat_map(tf.data.TFRecordDataset)
    return dataset.map(lambda x: parse_tfrecord(x,config.size,config.max_boxes))

def give_yolo_dataset(Tfrecord_pattern,batch_size,config,preprocess_func):
    dataset= load_tfrecord_dataset(file_pattern=Tfrecord_pattern,config=config)
    dataset = dataset.shuffle(buffer_size=512)
    dataset = dataset.batch(batch_size)
    
    dataset = dataset.map(lambda x, y: (
        transform_images(x, config.size),
        transform_targets(y, config.anchors, config.anchor_masks, config.size)))
    if preprocess_func is not None:
        dataset=dataset.map(lambda x,y: (preprocess_func(x),y) )
    else :
        dataset=dataset.map(lambda x,y: (yolo_preprocessing(x),y) )

    dataset = dataset.prefetch(buffer_size=tf.data.experimental.AUTOTUNE)
    dataset = dataset.repeat(-1)
    return dataset


    # def load_fake_dataset():
    #     x_train = tf.image.decode_jpeg(
    #         open('./data/girl.png', 'rb').read(), channels=3)
    #     x_train = tf.expand_dims(x_train, axis=0)

    #     labels = [
    #         [0.18494931, 0.03049111, 0.9435849,  0.96302897, 0],
    #         [0.01586703, 0.35938117, 0.17582396, 0.6069674, 56],
    #         [0.09158827, 0.48252046, 0.26967454, 0.6403017, 67]
    #     ] + [[0, 0, 0, 0, 0]] * 5
    #     y_train = tf.convert_to_tensor(labels, tf.float32)
    #     y_train = tf.expand_dims(y_train, axis=0)

    #     return tf.data.Dataset.from_tensor_slices((x_train, y_train))



def debug_func(dataset,num):
    for x,y in dataset.take(num):
        w=h=416
        proto_tensor=tf.make_tensor_proto(y)
        bbox_array=tf.make_ndarray(proto_tensor)
        proto_tensor=tf.make_tensor_proto(x)
        img_arr=tf.make_ndarray(proto_tensor)
        img_arr=np.array(img_arr,dtype=np.uint8)
        img=Image.fromarray(img_arr,'RGB')
        img1=ImageDraw.Draw(img)
        
        for bbox in bbox_array:
            xmin=bbox[0]*w
            ymin=bbox[1]*h
            xmax=bbox[2]*w
            ymax=bbox[3]*h
            img1.rectangle([xmin,ymin,xmax,ymax])
        img.show()



if debug:
    train_dataset_patern=os.path.join(tempfile.gettempdir(),'train*.tfrecord')
    dataset=load_tfrecord_dataset(file_pattern=train_dataset_patern,config=Yolov3Config())
    debug_func(dataset,1)