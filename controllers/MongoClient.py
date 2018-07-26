import pymongo
import urllib.request

from pandas.io.json import json


class MongoClient:

    @staticmethod
    def getConnection(url):
        mongodb_client = pymongo.MongoClient(url)
        database = mongodb_client["videos_mongodb_db"]
        return database

    @staticmethod
    def getProcesses(url):
        processes_collection = MongoClient.getConnection(url)["video_processes"]
        x = processes_collection.find_one({"processFlag": "1"})
        print(x)
        return x

    @staticmethod
    def updateProcesses(process_id, url, flag):
        processes_collection = MongoClient.getConnection(url)["video_processes"]
        processes_collection.find_one({"processId": process_id}, {"processFlag": flag})

    @staticmethod
    def insertVideo(url, data_list):
        videos_collection = MongoClient.getConnection(url)["videos"]

        for key, value in data_list:
            video_url = "https://www.youtube.com/watch?v=" + key
            presenter_visibility = value.presenter_visibility
            code_visibility = value.code_visibility
            filter4 = value.filter4
            filter5 = value.filter5
            filter6 = value.filter6
            filter7 = value.filter7
            filter8 = value.filter8
            filter9 = value.filter9

            query = {"videoUrl": video_url,
                     "filter2": presenter_visibility,
                     "filter3": code_visibility,
                     "filter4": filter4,
                     "filter5": filter5,
                     "filter6": filter6,
                     "filter7": filter7,
                     "filter8": filter8,
                     "filter9": filter9}
            videos_collection.insert_one(query)
