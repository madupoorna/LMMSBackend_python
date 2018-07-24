import cv2


class RecognizeFaces:

    def detect_face(img, cascade_path):

        face_cascade = cv2.CascadeClassifier(cascade_path)

        img = cv2.imread(img, 0)
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(img, 1.3, 5)
        try:
            if faces.size > 0:
                checker = True
        except:
            checker = False

        return checker
