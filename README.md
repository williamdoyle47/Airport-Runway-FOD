# Airport-Runway-FOD

## Requirements

- Python 3.8
- tensorflow 2.9.2
- Protoc 3.19
- Tensorflow Object Detection API
- Cython
- Numpy library
- gcc compiler

if you want to use your GPU:

- Cuda 11.2
- CUDDNN 8.2

## Installation

The following video explains how to set up Tensorflow, and the general workflow for gathering data and training a model: https://youtu.be/yqkISICHH-U
If you encounter any issues setting up the project, the video covers common issues and troubleshooting. Most errors can be resolved by using pip to install any missing packages.

`git clone https://github.com/scaltintasli/Airport-Runway-FOD.git`

move into Tensorflow/models then run command

`git clone https://github.com/tensorflow/models`

move into Tensorflow/workspace/scripts then run command

`git clone https://github.com/nicknochnack/GenerateTFRecord`

In order to generate a TFRecord file for training the model you must ensure you have linked it to a properly formatted and annotated (VOC format) image folder

Run the following two commands in the dir above Tensorflow/ to install the object detection api and its needed dependencies

`pip install -r requirements.txt`

`cd Tensorflow\models\research && protoc object_detection\protos\*.proto --python_out=. && copy object_detection\packages\tf2\setup.py setup.py && python setup.py build && python setup.py install`

`cd Tensorflow/models/research/slim && pip install -e .`

## Usage

### TRAINING

Use the following jupyter notebook as a template for training, SSD_MOB_640_Training_and_Detection.ipynb. This file was designed for training using Google Colab with xml image annotaion in VOC format.

### DETECTION

Ensure your camera is connected via usb, a web cam is okay although you should ensure that OpenCv2 is able to reach it.
Run command `python FodApp/src/main.py` to start the web server and click on the localhost link to begin running the detection program. It will use your connected camera to detected FOD.

Prior to detection one must ensure that the DetectionModel.py has a detection model to reference, by default we use a custom SSD_Mobnet_640 data model in `FodApp/src/Tensorflow/workspace/models/my_ssd_mobnet`.
To modify the checkpoint, weights, labelmap paths to use your custome model, look into file `FodApp/src/detection_modules/DetectionModel.py` in the **init** variables. Beaware some object detection models arent fit to use for realtime applications.

For Manual test run `python FodApp/src/detection_modules/DetectionModel.py`
