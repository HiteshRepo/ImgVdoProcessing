# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 16:37:57 2020

@author: Hitesh Pattanayak
"""

import cv2, time
import glob

def video_capture():

    video=cv2.VideoCapture(0) # captures video from webcam
    
#    print(video.isOpened()) # False
#    print(video.read()) # (False, None)
    
    #video=cv2.VideoCapture("Rain.mp4") 
    
    a = 1
    
    while True:
        a = a+1
        check, frame = video.read()
        print(check)
        print(frame.sum())
        
        gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        cv2.imshow("Capturing", gray_image)
        
        key = cv2.waitKey(2000)
        
        if key == ord('q'):
            break
        
    print('Number of iterations : ' + str(a))
        
    video.release()
    cv2.destroyAllWindows

def detect_face():

    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    img = cv2.imread("photo.jpg")
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(gray_image,
     scaleFactor=1.05,
     minNeighbors=5)
    
    for x,y,w,h in faces:
        img=cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0))
    
    print(faces)
    print(type(faces))
    
    resized=cv2.resize(img, (int(img.shape[1]/3), int(img.shape[0]/3)))
    
    cv2.imshow("Gray", resized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    

def resize_images():

    images = glob.glob("*.jpg")
    
    for image in images:
        #    print(type(img))
        img = cv2.imread(image,0)
        re = cv2.resize(img, (100,100))
        cv2.imshow("hey", re)
        cv2.waitKey(500)
        cv2.destroyAllWindows()
        resizeImageName = "resized_" + image
        print(resizeImageName)
        cv2.imwrite(resizeImageName, re)
     
#resize_images()
#detect_face()
video_capture()


#img = cv2.imread("galaxy.jpg",0)
#print((img))
#print((img.shape))
#print((img.ndim))
#
#resized_image = cv2.resize(img, (int(img.shape[1]/2), int(img.shape[0]/2)))
#
#cv2.imshow("Galaxy", resized_image)
#cv2.imwrite("Galaxy_resized.jpg", resized_image)
#cv2.waitKey(0)
#cv2.destroyAllWindows()