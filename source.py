import numpy as np
import cv2
from PIL import Image
import threading

def get_limits(color):
    c = np.uint8([[color]])
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)
    hue = hsvC[0][0][0]

    if hue >= 165:
        lowerLimit = np.array([hue - 10, 100, 100], dtype=np.uint8)
        upperLimit = np.array([180, 255, 255], dtype=np.uint8)
    elif hue <= 15:
        lowerLimit = np.array([0, 100, 100], dtype=np.uint8)
        upperLimit = np.array([hue + 10, 255, 255], dtype=np.uint8)
    else:
        lowerLimit = np.array([hue - 10, 100, 100], dtype=np.uint8)
        upperLimit = np.array([hue + 10, 255, 255], dtype=np.uint8)

    return lowerLimit, upperLimit

def user_input_thread():
    global user_input
    user_input = input("Enter the color to detect (e.g., 'yellow', 'red', 'blue', etc.): ").lower()


user_input = ""

# Start a separate thread for user input
input_thread = threading.Thread(target=user_input_thread)
input_thread.daemon = True
input_thread.start()

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    hsvimage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    color_dict = {
        'yellow': [0, 255, 255],
        'red': [0, 0, 255],
        'blue': [255, 0, 0],
        'green': [0, 255, 0],
        'white': [255, 255, 255],
        'black': [0, 0, 0],
        'orange': [0, 165, 255],
        'pink' :[255, 192, 203]
    }

    if user_input in color_dict:
        lowerlimit, upperlimit = get_limits(color=color_dict[user_input])
        mask = cv2.inRange(hsvimage, lowerlimit, upperlimit)
        mask_ = Image.fromarray(mask)
        bbox = mask_.getbbox()

        if bbox is not None:
            x1, y1, x2, y2 = bbox
            frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)

        print(bbox)

    cv2.imshow('Color Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()