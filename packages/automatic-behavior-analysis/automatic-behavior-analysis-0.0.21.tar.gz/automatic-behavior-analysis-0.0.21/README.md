# AutomaticBehaviorAnalysis

## Installation
### pip
Client (in cache mode)
To work with the cache, you need to place the video and cache file in the same folder.

Package installation:

`pip install --user automatic-behavior-analysis`

Package update:

`pip install --upgrade --user automatic-behavior-analysis`

Client launch:

`aba-client`

ATTENTION!
For correct operation, the package path should not contain Cyrillic characters.

## Requirements

* Python 3
* TensorFlow
* [Tensorflow Object Detection API](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/installation.md)
* Keras
* numpy
* PIL
* appdirs
* openCV
* websocket
* imageio

### Client2

* pip install PyQt5 opencv-python appdirs requests matplotlib scipy pandas

## Build a container with a server

### Development container

There are no files and models in the development container in order to minify the image and increase the usability.

The container is collected by the following command:

```bash
# For container with GPU support 
docker build -t registry.gitlab.com/digiratory/automatic-behavior-analysis/dev-gpu .
# For container with CPU support only 
docker build  -f Dockerfile.dev.cpu -t registry.gitlab.com/digiratory/automatic-behavior-analysis/dev-cpu .
```

There's no need to rebuild the container for work and you can pick up the assembled from the repository using the following commands:

```bash
docker login registry.gitlab.com
# To run a container with GPU support 
docker run --runtime=nvidia -it -v <workspace>:/home/user/ -p 1217:1217 registry.gitlab.com/digiratory/automatic-behavior-analysis/dev-gpu:latest

# For container with CPU support only 
docker run -it -v <workspace>:/home/user/ -p 1217:1217 registry.gitlab.com/digiratory/automatic-behavior-analysis/dev-cpu:latest
```

For CPU-only:

```bash
docker login registry.gitlab.com
docker run -it -v <workspace>:/home/user/ -p 1217:1217 registry.gitlab.com/digiratory/automatic-behavior-analysis/dev-cpu:latest
```

If the machine does not have gpu, then the key `--runtime=nvidia` no need to specify.

ATTENTION! The development container does not include source code, models, and more.

## Launch applications

Launch order:

1. Server part
2. Client side

Shutdown Procedure:

1. Client side
2. Server part

### Server

To start the server side, you must run ./server.py

```bash
python3 ./server.py
```

Team Arguments:
[ip= ] — Ip wiretap address (Default 172.0.0.1 )
[port= ] — Server Port (Default 1217)

### Client part (GUI)

To start the client side, you must run ./client_gui.py

```bash
python3 ./client_gui.py
```

Team Arguments:
[ip= ] — Ip server address (Default 172.0.0.1 )
[port= ] — Server Port (Default 1217)
