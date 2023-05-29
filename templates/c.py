import numpy as np
import pickle
import cv2
import mediapipe as mp
from googletrans import Translator
from PIL import Image, ImageDraw, ImageFont
import io

def image_processed(hand_img):
    # Image processing code goes here...

# ...Rest of your code...

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        # Load model
        with open('model.pkl', 'rb') as f:
            self.svm = pickle.load(f)

        # Specify the font file path for Tamil
        self.font_path = 'path/to/tamil_font.ttf'

    # ...Rest of your code...

    def get_frame(self):
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
        font = ImageFont.truetype(self.font_path, 40)  # Adjust the font size as needed

        # Render the Tamil text on the image
        text_position = (50, 50)  # Adjust the text position as needed
        text_color = (255, 0, 0)  # Adjust the text color as needed
        draw.text(text_position, output_text, font=font, fill=text_color)

        # Convert the image back to OpenCV format
        frame = np.array(image)

        # Encode the frame as JPEG for Flask streaming
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()