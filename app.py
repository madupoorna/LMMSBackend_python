import requests
from flask import Flask, request
from pandas.io.json import json

from controllers.MongoClient import MongoClient
from controllers.Process import Process

app = Flask(__name__)
app.config.from_pyfile("config.cfg")


@app.route('/start', methods=['POST'])
def check_process():
    content = json.loads(request.data.decode('utf-8'))
    cmd = content['start']

    if cmd == 'start':
        print("starting process")
        # t1 = threading.Thread(target=start_process)
        # t1.start()
        start_process()
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

        data = {}
        data['urlList'] = process.get("linksList")
        data['process_id'] = str(process.get("_id"))
        json_data = json.dumps(data)

        print("urlList", json_data)
        headers = {'Content-Type': 'application/json'}

        requests.post(url='http://localhost:8080/api/index/create', headers=headers, data=json_data)
        print("post sent")


if __name__ == '__main__':
    app.run('localhost', 5000, True)
