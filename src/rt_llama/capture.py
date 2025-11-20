import base64
import time
from collections import deque

import cv2

from rt_llama.smbnv_client import image_response
# from rt_llama.groq_client import image_response


def capture_loop(camera_index: int = 0):
    cv2.namedWindow("capture", cv2.WINDOW_NORMAL)
    cap = cv2.VideoCapture(camera_index)
    max_history_len = 1
    image_history = deque(maxlen=max_history_len)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("capture", frame)
        frame = cv2.resize(frame, (640, 480))
        image_history.append(frame)
        if len(image_history) == max_history_len:
            cat_image = cv2.vconcat(image_history)
            image_base64 = base64.b64encode(cv2.imencode('.jpg', cat_image)[1].tobytes()).decode('utf-8')
            time_start = time.time()
            res = image_response(image_base64)
            time_end = time.time()
            print(f"time: {time_end - time_start:.2f}s: {res}")
        time.sleep(0.1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
