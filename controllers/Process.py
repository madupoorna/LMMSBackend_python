import errno
import os

from pytube import YouTube

from controllers import MongoClient
from controllers.RecogProcess import RecognizeContent
from controllers.SplitAndRemove import SplitAndRemove
from models.DataModel import DataModel


class Process:

    def start_process(process_id, links, mongo_url):

        dir_path = os.path.abspath('')
        ROOT_DIR = dir_path
        video_download_path = ROOT_DIR + "/videos/" + process_id + "/"
        cascade_path = ROOT_DIR + "/haarcascade_frontalface_default.xml"

        if not os.path.exists(video_download_path):
            try:
                os.makedirs(video_download_path)
            except OSError as e:
                print(str(e))
                if e.errno != errno.EEXIST:
                    raise

        for video_id in links:
            id = video_id
            video_id = video_id.replace("https://www.youtube.com/watch?v=", "")

            # download youtube videos
            Process.download_youtube_video(video_download_path, video_id)

            # split and remove duplicate frames
            SplitAndRemove.start_splitting(video_id, video_download_path)

            # start recognize process
            params = RecognizeContent.start_recog(video_download_path + "/" + video_id + "_images/", cascade_path,
                                                  ROOT_DIR)
            # face_visibility, code_visibility, ide_list

            print(params)

            obj = DataModel()

            obj.videoUrl = id

            # presenter visibility
            obj.filter2 = params[0]

            # code visibility
            obj.filter3 = params[1]

            # ide using
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

            MongoClient.MongoClient.insertVideo(mongo_url, obj)

    def download_youtube_video(file_path, id):
        print("Downloading https://www.youtube.com/watch?v=" + id + " ....")
        url = "https://www.youtube.com/watch?v=" + id
        yt = YouTube(url)
        yt.streams.filter(res="360p", only_video=True, file_extension="mp4").first().download(file_path, id)
