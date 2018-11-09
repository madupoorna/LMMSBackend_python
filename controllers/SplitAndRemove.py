import os

import cv2
import dhash as dhash
from PIL import Image


class SplitAndRemove:

    def start_splitting(video_id, video_download_path):

        split_path = video_download_path + video_id + "_images"

        if not os.path.exists(split_path):
            os.makedirs(split_path, 0o777)

        files_array = []

        vidcap = cv2.VideoCapture(video_download_path + video_id + ".mp4")
        success, image = vidcap.read()
        x = 1

        # splitting frames from video
        print("splitting video " + video_id + ".mp4....")
        while vidcap.isOpened():
            frameId = vidcap.get(1)  # current frame number
            ret, frame = vidcap.read()
            print(frameId)
            if not ret:
                break
            if frameId % 150 == 0:
                x += 1
                cv2.imwrite(split_path + "/frame%d.jpg" % x, image)

        vidcap.release()

        # resizing images
        print("resizing frames..")
        for subdir, dirs, files in os.walk(split_path + "/"):
            for file in files:
                image = cv2.imread(split_path + "/" + file)
                img = cv2.resize(image, (640, 480))
                cv2.imwrite(split_path + "/" + file, img)

        # insert images to file array
        for subdir, dirs, files in os.walk(video_download_path):
            for file in files:
                if file.endswith(".jpg"):
                    files_array.append(file)

        # remove duplicates
        print("removing duplicate frames..")
        i = 0
        while i < len(files_array):
            file = files_array[i]
            hash_value = SplitAndRemove.generate_hash(file, split_path)

            j = i + 1
            while j < len(files_array):
                file1 = files_array[j]
                hash_value1 = SplitAndRemove.generate_hash(file1, split_path)
                hamming_distance = dhash.get_num_bits_different(hash_value, hash_value1)
                if (hamming_distance <= 5) and (file1 != file):
                    os.remove(split_path + "/" + file1)
                    files_array.remove(file1)
                j += 1
            i += 1

        print("Finish")

    # hash generate
    def generate_hash(file_name, split_path):
        image = Image.open(split_path + "/" + file_name)
        row, col = dhash.dhash_row_col(image)
        hash = int(dhash.format_hex(row, col), 16)
        return hash
