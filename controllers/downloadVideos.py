from pytube import YouTube
import os
from controllers.SplitAndRemove import SplitAndRemove
from controllers.RecogProcess import RecognizeContent
from models.DataModel import DataModel


class Process:

    def start_process(user_id, links):

        video_download_path = "./videos/" + user_id
        video_split_path = "./videos/" + user_id + "/images"
        casc_path = "haarcascade_frontalface_default.xml"
        data_list = []

        if not os.path.exists(video_split_path):
            os.makedirs(video_split_path, 0o777)

        for video_id in links:
            # download youtube videos
            Process.download_youtube_video(video_download_path, video_id)
            # split and remove frames
            SplitAndRemove.start_splitting(video_id, video_download_path)
            # start recognize process
            params = RecognizeContent.start_recog(video_split_path + "/" + video_id + "_images/", casc_path)

            obj = DataModel()
            if (params[1] / 100) * 35 > params[0]:
                obj.presenter_visibility = True
            else:
                obj.presenter_visibility = False
            obj.code_visibility = True
            obj.ide_list = params[2]
            data_list[video_id] = obj

        print("data list ", data_list)
        return data_list

    def download_youtube_video(file_path, id):
        print("Downloading http://youtube.com/watch?v=" + id + "....")
        yt = YouTube('http://youtube.com/watch?v=' + id)
        yt.streams.filter(res="480p", only_video=True, file_extension="mp4").first().download(file_path, id)
