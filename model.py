import os 

CUSTOM_MODEL_NAME = 'ssd_mobnet640' 
PRETRAINED_MODEL_NAME = 'ssd_mobilenet_v2_fpnlite_640x640_coco17_tpu-8'
PRETRAINED_MODEL_URL = 'http://download.tensorflow.org/models/object_detection/tf2/20200711/ssd_mobilenet_v2_fpnlite_640x640_coco17_tpu-8.tar.gz'
TF_RECORD_SCRIPT_NAME = 'generate_tfrecord.py'
LABEL_MAP_NAME = 'label_map.pbtxt'

paths = {
    'WORKSPACE_PATH': os.path.join('TensorExp', 'Tensorflow', 'workspace'),
    'SCRIPTS_PATH': os.path.join('TensorExp', 'Tensorflow','scripts'),
    'APIMODEL_PATH': os.path.join('TensorExp','Tensorflow','models'),
    'ANNOTATION_PATH': os.path.join('TensorExp','Tensorflow', 'workspace','annotations'),
    'IMAGE_PATH': os.path.join('drive', 'MyDrive','images'), #Edit
    'MODEL_PATH': os.path.join('TensorExp','Tensorflow', 'workspace','models'),
    'PRETRAINED_MODEL_PATH': os.path.join('TensorExp','Tensorflow', 'workspace','pre-trained-models'),
    'CHECKPOINT_PATH': os.path.join('TensorExp','Tensorflow', 'workspace','models',CUSTOM_MODEL_NAME), 
    'OUTPUT_PATH': os.path.join('TensorExp','Tensorflow', 'workspace','models',CUSTOM_MODEL_NAME, 'export'), 
    'TFJS_PATH':os.path.join('TensorExp','Tensorflow', 'workspace','models',CUSTOM_MODEL_NAME, 'tfjsexport'), 
    'TFLITE_PATH':os.path.join('TensorExp','Tensorflow', 'workspace','models',CUSTOM_MODEL_NAME, 'tfliteexport'), 
    'PROTOC_PATH':os.path.join('TensorExp','Tensorflow','protoc'),
    'MODEL_STORAGE_PATH': os.path.join('drive', 'MyDrive', 'store_model_versions_here')
 }
files = {
    'PIPELINE_CONFIG':os.path.join('TensorExp','Tensorflow', 'workspace','models', CUSTOM_MODEL_NAME, 'pipeline.config'),
    'TF_RECORD_SCRIPT': os.path.join(paths['SCRIPTS_PATH'], TF_RECORD_SCRIPT_NAME), 
    'LABELMAP': os.path.join(paths['ANNOTATION_PATH'], LABEL_MAP_NAME)
}

TRAINING_SCRIPT = os.path.join(paths['APIMODEL_PATH'], 'research', 'object_detection', 'model_main_tf2.py')
command = "python {} --model_dir={} --pipeline_config_path={} --checkpoint_dir={}".format(TRAINING_SCRIPT, paths['CHECKPOINT_PATH'],files['PIPELINE_CONFIG'], paths['CHECKPOINT_PATH'])
print(command)