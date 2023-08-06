#from flask import send_from_directory
import os
import sys
from flask import Flask, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from time import sleep
from celery import Celery

from threading import BoundedSemaphore
import numpy as np
import cv2
import random
import string
import tempfile
import zipfile

# to import from this project without instalation
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')))

from blyzer.server.model_controller import ModelController
from blyzer.common.singleton import Singleton
from blyzer.common.video import Video
#from celery.app.control import revoke

app = Flask(__name__)
cur_dir = os.getcwd()

app.config['CELERY_BROKER_URL'] = 'amqp://localhost:5672/'
app.config['CELERY_RESULT_BACKEND'] = 'amqp'
app.config['CELERYD_CONCURRENCY'] = 1
#app.config['CELERY_TIMEZONE'] =


# thats where celery will store scheduled tasks in case you restart the broker:

#app.config['CELERY_ACCEPT_CONTENT'] = ['json']
#app.config['CELERY_TASK_SERIALIZER'] = 'json'
#app.config['CELERY_RESULT_SERIALIZER'] = 'json'

celery = Celery(app.name, backend = app.config['CELERY_RESULT_BACKEND'], broker=app.config['CELERY_BROKER_URL'] )
celery.conf.update(app.config)

temp_dir = tempfile.TemporaryDirectory()
UPLOAD_FOLDER = temp_dir.name
print("UPLOAD_FOLDER is {}".format(UPLOAD_FOLDER))
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'avi', 'mkv', 'mp4'])
PORT = '1217'
IP = '0.0.0.0'


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

class ImageProcessor(object, metaclass = Singleton):
    def __init__(self):
        self.model_workers_pool = BoundedSemaphore(1)
        self._model = None
        self._model_path = None

    def load_model(self, filename):
        with self.model_workers_pool:
            folder_path = os.path.join(UPLOAD_FOLDER, "NN_Model")
            os.mkdir(folder_path)
            with zipfile.ZipFile(filename, 'r') as zip_ref:
                zip_ref.extractall(folder_path)
            self._model_path = folder_path

    def process_image(self, image):
        with self.model_workers_pool:
            if self._model is None:
                self._model = ModelController()
                print("__________________________Start inference engine_______________________________")
                self._model.init_model(self._model_path)
                print("__________________________Inference engine started_____________________________")
            response = self._model.process_image(image, is_decoded=True) # Work with model
        return response


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@celery.task(bind=True)
def process_file(self, filename, progress = 0):
    _, file_extension = os.path.splitext(filename)
    if file_extension == '.jpg':
        #assync part
        with open(filename, "rb") as f:
            chunk = f.read()
            chunk_arr = np.frombuffer(chunk, dtype=np.uint8)
            img = cv2.imdecode(chunk_arr, cv2.IMREAD_COLOR)
        response = ImageProcessor().process_image(img) #Sync part
        os.remove(filename)
        return response
    else:
        response = {}
        progress = int(progress)
        video = Video(filename)
        frames_count = video.get_frames_count()
        for current_frame in range(progress, frames_count):
            image_np = video.get_raw_frame(current_frame)
            response[current_frame] = ImageProcessor().process_image(image_np) #Sync part # Work with model
            response[current_frame]["frame_index"] = current_frame
            if not self.request.called_directly:
                self.update_state(state='PROGRESS',
                    meta={'intermedian_response': response, 'total': frames_count})
        os.remove(filename)
        return response

@celery.task
def setup_model(filename):
    ImageProcessor().load_model(filename)

@app.route('/api/blyzer/storage/image', methods=['POST'])
def upload_image():
    files = request.files['file']
    if files and allowed_file(files.filename):
        filename = randomString(10) + "_" + secure_filename(files.filename)
        files.save(os.path.join(UPLOAD_FOLDER, filename))
        files = os.path.join(UPLOAD_FOLDER, filename)
        new_task = process_file.delay(files)
        #print(new_task.backend)
        return jsonify(task_id = new_task.id), 202 #202 code for responce
    return "No images", 400 #Bad request

@app.route('/api/blyzer/storage/video/<progress>', methods=['POST'])
def upload_video(progress):
    files = request.files['file']
    if files and allowed_file(files.filename):
        filename = randomString(10) + "_" + secure_filename(files.filename)
        files.save(os.path.join(UPLOAD_FOLDER, filename))
        files = os.path.join(UPLOAD_FOLDER, filename)
        new_task = process_file.delay(files, progress)
        print(new_task.backend)
        return jsonify(task_id = new_task.id), 202 #202 code for responce
    return "No videos", 400 #Bad request

@app.route('/api/blyzer/task/<task_id>/result', methods = ['GET'])
def answer(task_id):
    task = process_file.AsyncResult(task_id)
    status = task.state
    print(status)
    #return jsonify(result_id = status)

    if status in ["PENDING", "STARTED"]:
        return jsonify(result_id = status), 201
    elif status == "PROGRESS":
        return jsonify(result = task.info['intermedian_response']), 206 # Для частичного ответа по видео
    elif status == "FAILURE":
        return "Analysis task falure" , 422
    elif status == "SUCCESS":
        result = task.get(0.1)
        return jsonify(result = result), 200

@app.route('/api/blyzer/model/upload', methods=['POST'])
def upload_model():
    print("upload_model")
    files = request.files['file']
    if files and '.' in files.filename and files.filename.rsplit('.', 1)[1] == 'zip':
        filename = randomString(10) + "_" + secure_filename(files.filename)
        files.save(os.path.join(UPLOAD_FOLDER, filename))
        files = os.path.join(UPLOAD_FOLDER, filename)
        print("Model recieved")
        new_task = setup_model.delay(files)
        print(new_task.backend)
        return jsonify(task_id=new_task.id), 202 #202 code for responce
    return "No model", 400 #Bad request

@app.route('/api/blyzer/reset', methods=['GET'])
def reset():
    return "Not supported", 405 # Method Not Allowed

#@celery
"""@app.route('', method = ['GET'])
def get_result():
pass"""
@app.route('/')
def test():
    return 'SUCCESS'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = PORT)
