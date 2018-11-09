import os

from controllers.DetectCode import detect_codes
from controllers.RecFaces import RecognizeFaces
from controllers.tensor.manage import recognize_ide


class RecognizeContent:

    def start_recog(images_folder, cascade_path, ROOT_DIR):

        face_count = 0
        # file_count = 0
        code_count = 0
        face_visibility = False
        code_visibility = False
        # file_count_in_dir = 0
        ide_list = []

        # # get total file count
        # for file in os.listdir(images_folder):
        #     if file.endswith('.jpg'):
        #         file_count_in_dir += 1

        # loop over the images
        for file in os.listdir(images_folder):
            # file_count += 1
            file = os.fsdecode(file)
            if file.endswith(".jpg"):

                # detect faces
                if face_count < 1:
                    if RecognizeFaces.detect_face(images_folder, file, cascade_path):
                        face_count += 1
                        face_visibility = True

                # detect ide
                # using text recognition
                # ide = detect_ide(directory + file)

                # using machine learning
                ide = recognize_ide(images_folder + file, ROOT_DIR)
                if ide != 'no':
                    ide_list.append(ide)

                # detect code visibility
                # using text recognition
                if code_count < 1:
                    if detect_codes(images_folder + file):
                        code_count += 1
                        code_visibility = True
            else:
                continue

        ide = max(ide_list, key=ide_list.count).strip()

        return face_visibility, code_visibility, ide
