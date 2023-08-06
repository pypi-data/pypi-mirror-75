# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['analitics',
 'analitics.trajectory',
 'blyzer',
 'blyzer.analitics',
 'blyzer.analitics.trajectory',
 'blyzer.client2',
 'blyzer.client2.gui',
 'blyzer.client2.tools',
 'blyzer.common',
 'blyzer.server',
 'blyzer.server.model_wrappers',
 'blyzer.server.python_api',
 'blyzer.tools',
 'blyzer.tools.labelImg',
 'blyzer.tools.labelImg.libs',
 'blyzer.tools.labelImg.tests',
 'blyzer.tools.vienna_analysis.Controller',
 'blyzer.tools.vienna_analysis.Model',
 'blyzer.tools.vienna_analysis.Utils',
 'blyzer.tools.vienna_analysis.View',
 'blyzer.tools.vienna_analysis.dog_vision',
 'blyzer.util',
 'blyzer.visualization',
 'client2',
 'client2.gui',
 'client2.tools',
 'common',
 'gui',
 'model_wrappers',
 'python_api',
 'server',
 'server.model_wrappers',
 'server.python_api',
 'tools',
 'tools.labelImg',
 'tools.labelImg.libs',
 'tools.labelImg.tests',
 'tools.vienna_analysis.Controller',
 'tools.vienna_analysis.Model',
 'tools.vienna_analysis.Utils',
 'tools.vienna_analysis.View',
 'tools.vienna_analysis.dog_vision',
 'trajectory',
 'util',
 'visualization']

package_data = \
{'': ['*'],
 'blyzer.client2': ['gui/resources/*'],
 'blyzer.tools': ['labelImg/build-tools/*',
                  'labelImg/demo/*',
                  'labelImg/requirements/*',
                  'labelImg/resources/icons/*',
                  'labelImg/resources/strings/*'],
 'client2.gui': ['resources/*'],
 'gui': ['resources/*'],
 'tools.labelImg': ['build-tools/*',
                    'demo/*',
                    'requirements/*',
                    'resources/icons/*',
                    'resources/strings/*']}

install_requires = \
['PyQt5',
 'appdirs',
 'imageio',
 'matplotlib',
 'numpy',
 'opencv-python',
 'pandas',
 'scipy']

entry_points = \
{'console_scripts': ['blyzer-client = blyzer.client2.run:main']}

setup_kwargs = {
    'name': 'automatic-behavior-analysis',
    'version': '0.0.21',
    'description': 'Program complex for automated behavior analysis',
    'long_description': "# AutomaticBehaviorAnalysis\n\n## Installation\n### pip\nClient (in cache mode)\nTo work with the cache, you need to place the video and cache file in the same folder.\n\nPackage installation:\n\n`pip install --user automatic-behavior-analysis`\n\nPackage update:\n\n`pip install --upgrade --user automatic-behavior-analysis`\n\nClient launch:\n\n`aba-client`\n\nATTENTION!\nFor correct operation, the package path should not contain Cyrillic characters.\n\n## Requirements\n\n* Python 3\n* TensorFlow\n* [Tensorflow Object Detection API](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/installation.md)\n* Keras\n* numpy\n* PIL\n* appdirs\n* openCV\n* websocket\n* imageio\n\n### Client2\n\n* pip install PyQt5 opencv-python appdirs requests matplotlib scipy pandas\n\n## Build a container with a server\n\n### Development container\n\nThere are no files and models in the development container in order to minify the image and increase the usability.\n\nThe container is collected by the following command:\n\n```bash\n# For container with GPU support \ndocker build -t registry.gitlab.com/digiratory/automatic-behavior-analysis/dev-gpu .\n# For container with CPU support only \ndocker build  -f Dockerfile.dev.cpu -t registry.gitlab.com/digiratory/automatic-behavior-analysis/dev-cpu .\n```\n\nThere's no need to rebuild the container for work and you can pick up the assembled from the repository using the following commands:\n\n```bash\ndocker login registry.gitlab.com\n# To run a container with GPU support \ndocker run --runtime=nvidia -it -v <workspace>:/home/user/ -p 1217:1217 registry.gitlab.com/digiratory/automatic-behavior-analysis/dev-gpu:latest\n\n# For container with CPU support only \ndocker run -it -v <workspace>:/home/user/ -p 1217:1217 registry.gitlab.com/digiratory/automatic-behavior-analysis/dev-cpu:latest\n```\n\nFor CPU-only:\n\n```bash\ndocker login registry.gitlab.com\ndocker run -it -v <workspace>:/home/user/ -p 1217:1217 registry.gitlab.com/digiratory/automatic-behavior-analysis/dev-cpu:latest\n```\n\nIf the machine does not have gpu, then the key `--runtime=nvidia` no need to specify.\n\nATTENTION! The development container does not include source code, models, and more.\n\n## Launch applications\n\nLaunch order:\n\n1. Server part\n2. Client side\n\nShutdown Procedure:\n\n1. Client side\n2. Server part\n\n### Server\n\nTo start the server side, you must run ./server.py\n\n```bash\npython3 ./server.py\n```\n\nTeam Arguments:\n[ip= ] — Ip wiretap address (Default 172.0.0.1 )\n[port= ] — Server Port (Default 1217)\n\n### Client part (GUI)\n\nTo start the client side, you must run ./client_gui.py\n\n```bash\npython3 ./client_gui.py\n```\n\nTeam Arguments:\n[ip= ] — Ip server address (Default 172.0.0.1 )\n[port= ] — Server Port (Default 1217)\n",
    'author': 'Aleksandr Sinitca',
    'author_email': 'siniza.s.94@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/digiratory/automatic-behavior-analysis/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
