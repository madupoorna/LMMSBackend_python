import os

from controllers.RecFaces import RecognizeFaces
from controllers.tensor.manage import recognize_ide


class RecognizeContent:

    def start_recog(directory, cascade_path):

        face_count = 0
        file_count = 0
        code_count = 0
        file_count_in_dir = 0
        ide_list = []

        # get total file count
        for file in os.listdir(directory):
            if file.endswith('.jpg'):
                file_count_in_dir += 1

        # loop over the images
        for file in os.listdir(directory):
            file_count += 1
            file = os.fsdecode(file)
            if file.endswith(".jpg"):

                # detect faces
                if face_count <= (file_count_in_dir / 100) * 35:
                    has_face = RecognizeFaces.detect_face(directory, file, cascade_path)
                    if has_face:
                        face_count += 1

                # detect ide
                print("Identifying IDE in " + file)
                # ide = detect_ide(directory + file)  # using text recognition
                ide = recognize_ide(directory + file)  # using machine learning

                # detect code visibility
                if code_count <= (file_count_in_dir / 100) * 35:
                    print("Identifying code visibility in " + file)
                    has_code = True
                    if has_code:
                        code_count += 1

                if ide != 'no':
                    if ide not in ide_list:
                        ide_list.append(ide)

            else:
                continue

        print("face count", face_count)
        print("file count ", file_count)
        print("code count", code_count)
        print("ide list", ide_list)

        return face_count, file_count, ide_list, code_count
