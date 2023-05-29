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


class VideoCamera_hindi(object):
    def __del__(self):
        self.video.release()

    def release_camera(self):
        self.video.release()

    def __init__(self):
        self.video = cv2.VideoCapture(0)
        # Load model
        with open('model.pkl', 'rb') as f:
            self.svm = pickle.load(f)

        # Specify the font file path for Tamil
        self.font_path = 'C:/Users/sange/AppData/Local/Microsoft/Windows/Fonts/kruti-dev-021.ttf'

        # ...Rest of your code...

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
        translator = Translator()
        translation = translator.translate(output_text, src='en', dest='hi')
        translated_text = translation.text
        output_text = translated_text

        # Create a blank image using Pillow
        image = Image.fromarray(frame)
        draw = ImageDraw.Draw(image)

        # Load the Tamil font
        font = ImageFont.truetype(self.font_path, 10)  # Adjust the font size as needed

        # Render the Tamil text on the image
        text_position = (10, 50)  # Adjust the text position as needed
        text_color = (255, 0, 0)  # Adjust the text color as needed
        draw.text(text_position, output_text, font=font, fill=text_color)

        # Convert the image back to OpenCV format
        frame = np.array(image)

        # Encode the frame as JPEG for Flask streaming
        ret, jpeg = cv2.imencode('.jpg', frame)

        return jpeg.tobytes()
#---------------------------------------------------------------------------------------------------------------------
class VideoCamera_tamil(object):
    def __del__(self):
        self.video.release()
    def release_camera(self):
        self.video.release()
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        # Load model
        with open('model.pkl', 'rb') as f:
            self.svm = pickle.load(f)



        # Specify the font file path for Tamil
        self.font_path = 'C:/Windows/Fonts/NirmalaB.ttf'


    # ...Rest of your code...

    def get_frame(self):


        # Continue with the rest of your code

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
        translator = Translator()
        translation = translator.translate(output_text, src='en', dest='ta')
        translated_text = translation.text
        output_text = translated_text

        # Create a blank image using Pillow
        image = Image.fromarray(frame)
        draw = ImageDraw.Draw(image)

        # Load the Tamil font
        font = ImageFont.truetype(self.font_path, 15)  # Adjust the font size as needed

        # Render the Tamil text on the image
        text_position = (10, 50)  # Adjust the text position as needed
        text_color = (255, 0, 0)  # Adjust the text color as needed
        draw.text(text_position, output_text, font=font, fill=text_color)

        # Convert the image back to OpenCV format
        frame = np.array(image)

        # Encode the frame as JPEG for Flask streaming
        ret, jpeg = cv2.imencode('.jpg', frame)


        return jpeg.tobytes()


#----------------------------------------------------------------------------------------------------------------------------
