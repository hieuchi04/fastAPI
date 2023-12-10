import cv2
import requests
import numpy as np
from fastapi.responses import JSONResponse


def checking_img(image_url):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    response = requests.get(image_url)
    img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
    image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    # Chuyển ảnh sang ảnh xám
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Phát hiện khuôn mặt trong ảnh
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    if len(faces) == 1:
        eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        if len(eyes) > 0:
            eye_glasses_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')
            eye_glasses = eye_glasses_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
            if len(eye_glasses) > 0:
                return JSONResponse(content={"message": "OK!"}, status_code=200)
            else:
                return JSONResponse(content={"message": "Eyeglasses detected!"}, status_code=400)
        else:
            return JSONResponse(content={"message": "Your image is invalid!"}, status_code=400)
    else:
        return JSONResponse(content={"message": "No face detected!"}, status_code=400)
