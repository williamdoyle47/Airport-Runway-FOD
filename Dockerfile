# For more information, please refer to https://aka.ms/vscode-docker-python
# from .../Airport-Runway-FOD build with, docker build . -t <image name>
FROM python:3.8-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

#install git
RUN apt-get update
RUN apt-get install -y git
# Install pip requirements
# lines that are the least changd so go as high as possible (re ordering needed) (some commands that change often need to before others for orders sake)
# the docker file does every line after a changed line as if it were changed
COPY requirements.txt .
RUN pip install --upgrade setuptools
RUN pip install Cython --upgrade
RUN pip install numpy --upgrade 
RUN apt-get install gcc -y
RUN python -m pip install -r requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN apt install -y protobuf-compiler

# install file structure
# COPY command should be replaced by importing from a github location
WORKDIR /app
COPY . /app

# this does the rest of the readme/file structure and is for object detection creation
RUN git clone https://github.com/tensorflow/models.git /FodApp/src/Tensorflow/models
WORKDIR /FodApp/src/Tensorflow/models/research
RUN protoc object_detection/protos/*.proto --python_out=.
RUN cp object_detection/packages/tf2/setup.py setup.py
RUN python setup.py build
RUN python setup.py install

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
WORKDIR /app
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# run with, docker run --rm -it -p 8000:8000 <image name>
# this makes it so the docker localhost and your localhost are conected via 0.0.0.0:8000

# dealing with lag advice
# upon running a image things may get laggy the --rm makes it so it automiatcally removes itself upon stopping
# this stops most of the lag but same may remain, restarting will erase the lag
# using notepad make file called .wslconfig (no .txt or .txt extension) at User/%User Profile%/.wslconfig, pu in
# [wsl2]
# memory=2GB # can do more if you want
CMD ["python", "./FodApp/src/main.py"]
# known issues: camera connection and websockets connection can be iffy but i think i had it work before