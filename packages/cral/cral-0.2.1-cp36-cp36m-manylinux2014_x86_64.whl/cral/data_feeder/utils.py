import tensorflow as tf

from cral.tracking.tracking.fluent import log_artifact
from cral.tracking.utils.autologging_utils import try_mlflow_log

import glob, os


def _bytes_feature(value):
  """Returns a bytes_list from a string / byte."""
  return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def _float_feature(value):
  """Returns a float_list from a float / double."""
  return tf.train.Feature(float_list=tf.train.FloatList(value=[value]))

def _int64_feature(value):
  """Returns an int64_list from a bool / enum / int / uint."""
  return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

def _bytes_list_feature(value):
  """Returns a bytes_list from a list of string / byte."""
  return tf.train.Feature(bytes_list=tf.train.BytesList(value=value))

def _float_list_feature(value):
  """Returns a float_list from a list of float / double."""
  return tf.train.Feature(float_list=tf.train.FloatList(value=value))

def _int64_list_feature(value):
  """Returns an int64_list from a list of bool / enum / int / uint."""
  return tf.train.Feature(int64_list=tf.train.Int64List(value=value))


def generate_stats(stats_folder):
    import tensorflow_data_validation as tfdv
    from tensorflow_data_validation.utils.display_util import get_statistics_html

    semantic_stats_options = tfdv.StatsOptions(enable_semantic_domain_stats=True)

    for tfrecord in glob.glob(os.path.join(stats_folder,'*.tfrecord')):
        stats = tfdv.generate_statistics_from_tfrecord(
            data_location=tfrecord, 
            stats_options=semantic_stats_options)

        html = get_statistics_html(
            lhs_statistics=stats, 
            rhs_statistics=None, 
            lhs_name='lhs_statistics', 
            rhs_name='rhs_statistics')

        stats_html_file = tfrecord.replace('.tfrecord','.html')
        with open(stats_html_file, 'w') as f:
            f.write(html)

        try_mlflow_log(log_artifact, local_path=stats_html_file)
    #tfdv.visualize_statistics(stats)