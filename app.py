from bson import json_util
from flask import Flask, request
import threading

from pandas.io.json import json
from bson import ObjectId

from controllers.MongoClient import MongoClient
from controllers.downloadVideos import Process
from models.ReturnModel import ReturnModel

app = Flask(__name__)
app.config.from_pyfile("config.cfg")


@app.route('/start', methods=['POST'])
def check_process():
    content = json.loads(request.data.decode('utf-8'))
    cmd = content['start']

    if cmd == 'start':
        print("starting process")
        t1 = threading.Thread(target=start_process)
        t1.start()
    else:
        print("skipping process, Maximum no of videos processing")

    return "done"


def start_process():
    mongo_url = app.config['MONGODB_URL']
    process = MongoClient.getProcesses(mongo_url)
    if process != 'None':

        MongoClient.updateProcesses(str(process.get("_id")), mongo_url, "2")
        obj = Process.start_process(str(process.get("_id")), process.get("linksList"))
        MongoClient.insertVideo(mongo_url, obj)
        MongoClient.updateProcesses(str(process.get("_id")), mongo_url, "0")

        obj = ReturnModel()
        obj.process_id = str(process.get("_id"))

        request.post('http://localhost:8080/api/index/create', json=obj)


if __name__ == '__main__':
    app.run('localhost', 5000, True)
