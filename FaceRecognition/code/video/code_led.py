import serial
import time
import face_recognition as fr
import os
import cv2
import numpy as np
from PIL import Image
import pickle

arduino = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(1)
print (arduino.readline())

def read (filename):
    file = open(filename, 'rb')
    temp_list = pickle.load(file)
    file.close()
    return temp_list

known_faces = read('./data/encoded_faces.data')
known_names = read('./data/encoded_names.data')
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

MODEL = "hog"
TOLERANCE = 0.5
FRAME_THICKNESS = 3
FONT_THICKNESS = 1
PROCESSED = "processed"
filename = "test.jpg"
flag = '0'

vid = cv2.VideoCapture(0)

while (True):
    ret, image = vid.read()
    print (flag)
    arduino.write(flag.encode())
    # arduino.write(flag)
    flag = '0'
    time.sleep(0)
    # Image.fromarray(image).save(f"{PROCESSED}/{filename}")
    # image = Image.open(f"{PROCESSED}/{filename}")
    # image.thumbnail((600, 600), Image.ANTIALIAS)
    # image.save (f"{PROCESSED}/{filename}", dpi=(600,600))
    # image = fr.load_image_file(f"{PROCESSED}/{filename}")
    locations = fr.face_locations(image, model=MODEL)
    # os.remove (f"{PROCESSED}/{filename}")
    # loc = face_cascade.detectMultiScale(image, 1.5, 5)
    # locations = []
    # for (x, y, w, h) in locations:
    #     locations.append((y, x+w, y+h, x))

    encodings = fr.face_encodings(image, locations)

    for face_encoding, face_location in zip(encodings, locations):
        recognized = []
        index = -1
        for face in known_faces:
            results = fr.compare_faces(face, face_encoding, TOLERANCE)
            index = index + 1
            match = None
            # print (results)

            if True in results:
                flag = '1'
                match = known_names[index]
                # print (f"Match found: {match}")

                top_left = (face_location[3]-5, face_location[0]-10)     #fr.face_locations sends coordinates top, right, bottom, left, in that order
                bottom_right = (face_location[1]+10, face_location[2])
                color = [0, 255, 0]
                cv2.rectangle(image, top_left, bottom_right, color, FRAME_THICKNESS)

                top_left = (face_location[3]-20, face_location[2])
                bottom_right = (face_location[1]+30, face_location[2]+20)
                color = [0, 0, 0]
                cv2.rectangle(image, top_left, bottom_right, color, cv2.FILLED)
                # cv2.imread(image)
                cv2.putText(image,
                            match,
                            (face_location[3]-10, face_location[2]+15),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            (200, 200, 200),
                            FONT_THICKNESS)
                break


    cv2.imshow ('image', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
