import cv2


class RecognizeFaces:

    def detect_face(directory, img, cascade_path):
        # img = "/home/lab/Desktop/LMMSBackend_python/videos/5b56f469352c000f103b0309/images/zdYPQH7aR8k_images/frame243.jpg"
        # cascade_path = "/home/lab/Desktop/LMMSBackend_python/haarcascade_frontalface_default.xml"

        print("cascade path" + cascade_path)
        print("Identifying faces in " + directory + img)

        checker = False

        face_cascade = cv2.CascadeClassifier(cascade_path)

        img = cv2.imread(directory +  img)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        try:
            if faces.size > 0:
                checker = True
        except:
            print("error")
            checker = False

        print(" faces : " + str(checker))
        return checker
