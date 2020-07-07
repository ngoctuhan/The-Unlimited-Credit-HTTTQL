import cv2
import numpy as np 
import os 
from keras_facenet import FaceNet
from utils import identification
import threading
from notice import get_notice
from mtcnn  import MTCNN
embedder = FaceNet()
detector = MTCNN()

# define ROI to reduce time 

ROI = [100, 50, 550,400]

employees = []

start_point = (ROI[0], ROI[1]) 
# Ending coordinate, here (220, 220) 
# represents the bottom right corner of rectangle 
end_point = (ROI[2], ROI[3]) 
  
# Blue color in BGR 
color = (255, 0, 0) 
  
# Line thickness of 2 px 
thickness = 2
  
# Using cv2.rectangle() method 
# Draw a rectangle with blue line borders of thickness of 2 px 

font = cv2.FONT_HERSHEY_SIMPLEX 
  
# org 
org = (50, 50) 
  
# fontScale 
fontScale = 1

hists = []

cap  = cv2.VideoCapture(0)
n_frame = 0
# Check if camera opened successfully
if (cap.isOpened()== False): 
    print("Error opening video stream or file")

while(cap.isOpened()):

  # Capture frame-by-frame

    ret, frame = cap.read()

    n_frame += 1

    kt = False

    if ret == True:

        # frame = cv2.rectangle(frame, start_point, end_point, color, thickness) , 
        img = frame[ROI[1]:ROI[3], ROI[0]: ROI[2]]
        
        faces = detector.detect_faces(img)
        data = []
        draw = []
        
        for face in faces:
            start_point = (face['box'][0], face['box'][1])
            end_point = (face['box'][0] + face['box'][2], face['box'][1] + face['box'][3])
            color = (255, 0, 0) 
            thickness = 2
            cv2.rectangle(img, start_point, end_point, color, thickness)
            
            draw.append(start_point)
            data.append(img[start_point[1] : end_point[1], start_point[0]: end_point[0]])
        
        if len(data) == 0:
            hists = []

        if n_frame % 10 == 0 and len(data) > 0:
            
            # print(len(data))
            hists = []
            vts = embedder.embeddings(data)
            n_frame = 0 
            for i,vt in enumerate(vts):
                id, name, distance = identification(vt)
                if name is not None:
                    cv2.putText(img, name, draw[i], font, 1,(0,255,0),2,cv2.LINE_AA )

                if name is not None and (name not in employees):
                    x = threading.Thread(target=get_notice, args=(data[i], id, name, distance))
                    x.start()

                    employees.append(name)

                    # save in database

                hists.append([id, name, draw[i]])

        elif len(hists) > 0 and len(faces) > 0:
            for his in hists:
                cv2.putText(img, his[1], his[2], font, 1,(0,255,0),2,cv2.LINE_AA )

        cv2.imshow('frame', img)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# When everything done, release the video capture object
cap.release()
# Closes all the frames
cv2.destroyAllWindows()



