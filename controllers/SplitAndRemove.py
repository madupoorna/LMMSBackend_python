import cv2
from PIL import Image
import imagehash
import os


class SplitAndRemove:

    def start_splitting(video_name, directory):
        print("splitting video " + video_name + ".mp4....")

        if not os.path.exists(directory + "/images/" + video_name + "_images"):
            os.makedirs(directory + "/images/" + video_name + "_images", 0o777)

        count = 0
        hash_array = []

        vidcap = cv2.VideoCapture(directory + "/" + video_name + ".mp4")
        success, image = vidcap.read()

        # splitting frames from video
        while success:
            cv2.imwrite(directory + "/images/" + video_name + "_images/" + "frame%d.jpg" % count, image)
            success, image = vidcap.read()
            count += 1

        # loop over the images
        print("removing duplicates..")
        for file in os.listdir(directory + "/images/" + video_name + "_images/"):
            filename = os.fsdecode(file)
            if filename.endswith(".jpg"):
                hash = SplitAndRemove.generateHash(filename, directory, video_name)
                if hash not in hash_array:
                    hash_array.append(hash)
                else:
                    os.remove(directory + "/images/" + video_name + "_images/" + filename)
            else:
                continue

        print("Finish")

    # hash generate
    def generateHash(file_name, directory, video_name):
        image = Image.open(directory + "/images/" + video_name + "_images/" + file_name)
        return imagehash.average_hash(image)
