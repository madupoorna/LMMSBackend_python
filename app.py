from flask import Flask, request
from controllers.downloadVideos import Process
from models.ReturnModel import ReturnModel

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/start', methods=['POST'])
def start_process():

    content = request.get_json()
    process_id = content['process_id']
    link_list = content['link_list']
    list = Process.start_process(process_id, link_list)

    obj = ReturnModel()
    obj.process_id = process_id
    obj.data_model = list

    return obj


if __name__ == '__main__':
    app.run('localhost', 5000, True)
