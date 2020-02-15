# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 19:13:02 2020

@author: Hitesh Pattanayak
"""

import cv2, pandas 
from datetime import datetime 
from bokeh.plotting import figure
from bokeh.io import output_file,show
from bokeh.models.annotations import Title

def create_graph():
    try:
        
        df = pandas.read_csv("Time_of_movements.csv")
        
        p=figure(x_axis_type='datetime',width=500,height=100)
        
        t = Title()
        t.text = 'Motion Graph'
        t.text_color = "Orange"
        t.text_font = "times"
        t.text_font_style = "italic"
            
        p.title = t
        
        q=p.quad(left=df["Start"], right=["End"], bottom=0, top=1, color='green')
        
        
        output_file("graph.html")
        
        show(p)
    except Exception as e:
        print(e)
    
def video_capture():
    try:
    
        first_frame=None
        # List when any moving object appear 
        motion_list = [ None, None ] 
          
        # Time of movement 
        time = [] 
          
        # Initializing DataFrame, one column is start  
        # time and other column is end time 
        df = pandas.DataFrame(columns = ["Start", "End"]) 
    
        video=cv2.VideoCapture(0)
        
        
        while True:
            check, frame = video.read()
            
            motion = 0
            
            gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray_image = cv2.GaussianBlur(gray_image, (5,5), 0)
            
            if first_frame is None:
                first_frame = gray_image
                continue
            
            delta_frame = cv2.absdiff(first_frame, gray_image)            
            thresh_delta = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]            
            thresh_delta = cv2.dilate(thresh_delta, None, iterations=2)
            
            (cnts,_) = cv2.findContours(thresh_delta.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in cnts:
                if cv2.contourArea(contour) < 10000:
                    continue
                motion = 1
                
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 3)
                
            motion_list.append(motion) 
            
            # Appending Start time of motion 
            if motion_list[-1] == 1 and motion_list[-2] == 0: 
                time.append(datetime.now()) 
          
            # Appending End time of motion 
            if motion_list[-1] == 0 and motion_list[-2] == 1: 
                time.append(datetime.now()) 
            
            cv2.imshow("Gray Frame  ", gray_image)
            cv2.imshow("Delta Frame", delta_frame)
            cv2.imshow("Threshold Frame", thresh_delta)
            cv2.imshow("Color Frame", frame)
            
            key = cv2.waitKey(1)
            
            if key == ord('q'):
                if motion == 1: 
                    time.append(datetime.now())
                break
        
        
        print(motion_list)
        print(time)
        
        # Appending time of motion in DataFrame 
        for i in range(0, len(time), 2): 
            df = df.append({"Start":time[i], "End":time[i + 1]}, ignore_index = True) 
          
#         Creating a csv file in which time of movements will be saved 
        df.to_csv("Time_of_movements.csv") 
        
        video.release()
        cv2.destroyAllWindows()
        
        create_graph(df)
        
    except Exception as e:
        print(e)
    
#video_capture()
        
create_graph()