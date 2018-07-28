import pymongo


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

        return x

    @staticmethod
    def updateProcesses(process_id, url, flag):
        processes_collection = MongoClient.getConnection(url)["video_processes"]
        processes_collection.find_and_modify({'_id': process_id},
                                             {'$set': {'processFlag': flag}})

    @staticmethod
    def insertVideo(url, data_list):
        videos_collection = MongoClient.getConnection(url)["videos"]

        query = {"videoUrl": data_list.videoUrl,
                 "title": "",
                 "thumbnailUrl": "",
                 "description": "",
                 "searchKeywords": "",
                 "duration": "",
                 "duration1": "",
                 "duration2": "",
                 "duration3": "",
                 "filter1": "",
                 "filter2": data_list.filter2,
                 "filter3": data_list.filter3,
                 "filter4": data_list.filter4,
                 "filter5": data_list.filter5,
                 "filter6": data_list.filter6,
                 "filter7": data_list.filter7,
                 "filter8": data_list.filter8,
                 "filter9": data_list.filter9}

        videos_collection.insert_one(query)
