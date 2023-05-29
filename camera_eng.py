import numpy as np
import pickle
import cv2
import mediapipe as mp
from googletrans import Translator
from PIL import Image, ImageDraw, ImageFont
import io
def image_processed(hand_img):
    # Image processing
    # 1. Convert BGR to RGB
    img_rgb = cv2.cvtColor(hand_img, cv2.COLOR_BGR2RGB)

    # 2. Flip the img in Y-axis
    img_flip = cv2.flip(img_rgb, 1)

    # accessing MediaPipe solutions
    mp_hands = mp.solutions.hands

    # Initialize Hands
    hands = mp_hands.Hands(static_image_mode=True,
                           max_num_hands=1, min_detection_confidence=0.7)

    # Results
    output = hands.process(img_flip)

    hands.close()

    try:
        data = output.multi_hand_landmarks[0]
        data = str(data)
        data = data.strip().split('\n')

        garbage = ['landmark {', '  visibility: 0.0', '  presence: 0.0', '}']

        without_garbage = []

        for i in data:
            if i not in garbage:
                without_garbage.append(i)

        clean = []

        for i in without_garbage:
            i = i.strip()
            clean.append(i[2:])

        for i in range(0, len(clean)):
            clean[i] = float(clean[i])
        return (clean)
    except:
        return (np.zeros([1, 63], dtype=int)[0])


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)


        # Load model
        with open('model.pkl', 'rb') as f:
            self.svm = pickle.load(f)

    def __del__(self):
        self.video.release()
    def release_camera(self):
        self.video.release()

    def get_frame(self):


                    ret, frame = self.video.read()

                    if frame is None:
                        self.video.release()
                        self.video = cv2.VideoCapture(0)
                        ret, frame = self.video.read()



                    data = image_processed(frame)
                    data = np.array(data)

                    # Predict gesture using model
                    y_pred = self.svm.predict(data.reshape(-1, 63))

                    # Translate output based on language choice
                    output_text = str(y_pred[0])

                    # Add text to frame
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    org = (50, 50)
                    fontScale = 1
                    color = (255, 0, 0)
                    thickness = 3

                    frame = cv2.putText(frame, output_text, org, font, fontScale, color, thickness, cv2.LINE_AA)
                    ret, jpeg = cv2.imencode('.jpg', frame)


                    return jpeg.tobytes()