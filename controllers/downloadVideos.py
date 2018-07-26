from pytube import YouTube
import os
from controllers.SplitAndRemove import SplitAndRemove
from controllers.RecogProcess import RecognizeContent
from models.DataModel import DataModel


class Process:

    def start_process(process_id, links):

        video_download_path = "./videos/" + process_id
        video_split_path = "./videos/" + process_id + "/images"
        cascade_path = "haarcascade_frontalface_default.xml"
        data_list = {}

        if not os.path.exists(video_split_path):
            os.makedirs(video_split_path, 0o777)

        for video_id in links:
            # download youtube videos
            Process.download_youtube_video(video_download_path, video_id)
            # split and remove frames
            SplitAndRemove.start_splitting(video_id, video_download_path)
            # start recognize process
            params = RecognizeContent.start_recog(video_split_path + "/" + video_id + "_images/",
                                                  cascade_path)  # face_count, file_count, ide_list, code_count

            obj = DataModel()

            if (params[1] / 100) * 35 > params[0]:  # more than 35% of video
                obj.presenter_visibility = 'True'
            else:
                obj.presenter_visibility = 'False'

            if 'eclipse' in params[2]:
                obj.filter4 = True
            else:
                obj.filter4 = False
            if 'intellij' in params[2]:
                obj.filter5 = True
            else:
                obj.filter5 = False
            if 'visual_studio' in params[2]:
                obj.filter6 = True
            else:
                obj.filter6 = False
            if 'net_beans' in params[2]:
                obj.filter7 = True
            else:
                obj.filter7 = False
            if 'vs_code' in params[2]:
                obj.filter8 = True
            else:
                obj.filter8 = False
            if 'android_studio' in params[2]:
                obj.filter9 = True
            else:
                obj.filter9 = False

            if (params[1] / 100) * 35 > params[3]:  # more than 35% of video
                obj.code_visibility = 'True'
            else:
                obj.code_visibility = 'False'

            data_list[video_id] = obj

        print("data list ", data_list)
        return data_list

    def download_youtube_video(file_path, id):
        print("Downloading http://youtube.com/watch?v=" + id + "....")
        yt = YouTube('http://youtube.com/watch?v=' + id)
        yt.streams.filter(res="480p", only_video=True, file_extension="mp4").first().download(file_path, id)
