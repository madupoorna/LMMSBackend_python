import cv2


class RecognizeFaces:

    def detect_face(images_folder, img_name, cascade_path):
        print("Identifying faces in " + images_folder + img_name)

        checker = False

        face_cascade = cv2.CascadeClassifier(cascade_path)

        img_name = cv2.imread(images_folder + img_name)
        gray = cv2.cvtColor(img_name, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        try:
            if faces.size > 0:
                checker = True
        except Exception as e:
            checker = False

        print(" faces : " + str(checker))
        return checker
