import threading

from flask import Flask, request
import requests
from pandas.io.json import json

from controllers.MongoClient import MongoClient
from controllers.Process import Process
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
    print("process ", process)

    if process is not None:
        MongoClient.updateProcesses(process.get("_id"), mongo_url, "2")
        Process.start_process(str(process.get("_id")), process.get("linksList"), mongo_url)
        MongoClient.updateProcesses(process.get("_id"), mongo_url, "0")

        #  {"urlList":["https://www.youtube.com/watch?v=zdYPQH7aR8k"]}
        urlList = {"urlList": process.get("linksList")}

        print("urlList", urlList)

        requests.post(url='192.168.12.1:8080/api/index/create', data=urlList)

        print("post sent")


if __name__ == '__main__':
    app.run('192.168.154.129', 5000, True)
