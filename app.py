import cv2.cv2 as cv2
import time
from datetime import datetime
import pandas



# 0 or 1 or 2 or ..... dependes on how many cameras you have 
# here we only have the internal web cam so it's index is Zero (0)
video = cv2.VideoCapture(0,cv2.CAP_DSHOW)

first_frame = None
status_list = [None,None]
times = []


# To make Times.csv file
def make_times_file():
    df = pandas.DataFrame(columns= ["Start","End"])
    for i in range(0,len(times),2):
        df = df.append({"Start":times[i],"End":times[i+1]},ignore_index=True)

    df.to_csv("Times.csv")




while(True):
    
    # read video 
    check, frame = video.read()

    # init status with 0
    status = 0
    
    # convert frame  into gray  
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray,(21,21,),0)

    # init the first frame with gray colors
    if first_frame is None:
        first_frame = gray 
        continue

    # diffrence between the first frame and other frames
    delta_frame = cv2.absdiff(first_frame , gray)
    
    # make a threshold image version
    thresh_frame = cv2.threshold(delta_frame, 30 , 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame,None, iterations=2)
    
    # find the contours     
    (cnts,_) = cv2.findContours(thresh_frame.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

   
    # check  for the contour area
    # if the moving area is greater than 10000 draw a rectangle and change the status
    for countour in  cnts:
        if cv2.contourArea(countour) < 10000:
            continue
           
        status = 1
        (x , y, w, h) = cv2.boundingRect(countour)
        cv2.rectangle(frame,(x,y), (x+w,y+h), (0,255,0),3)
        
    
    # adding status of each frame to the list
    status_list.append(status)
    
    # status_list = [None, None, 0] frame 1 no >>>> movement
                #   [None, None, 0, 0] frame 2 >>>> no movement
                #   [None, None, 0, 0, 0] frame 3 >>>> no movement
                #   [None, None, 0, 0, 0, 1] frame 4 >>>> move detected <<<<< Start time 
                #   [None, None, 0, 0, 0, 1, 1] frame 5 >>>> still moving
                #   [None, None, 0, 0, 0, 1, 1, 1] frame 6 >>>> still moving
                #   [None, None, 0, 0, 0, 1, 1, 1, 1] frame 7 >>>> still moving
                #   [None, None, 0, 0, 0, 1, 1, 1, 1, 0] frame 8 >>>> no movement <<<< End time
                #   [None, None, 0, 0, 0, 1, 1, 1, 1, 0, 0] frame 9 >>>> no movement
                #   [None, None, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0] frame 10 >>>> no movement
    
    # Adding Start time
    if status_list[-1] == 1 and status_list[-2] == 0:
        now = datetime.now()
        times.append(now.strftime("%D %H:%M:%S"))
        
    # Adding End time
    if status_list[-1] == 0 and status_list[-2] == 1:
        now = datetime.now()
        times.append(now.strftime("%D %H:%M:%S"))
        
    
    cv2.imshow("Gray_Frame",gray)
    cv2.imshow("Delta_frame",delta_frame)
    cv2.imshow("Threshold_frame",thresh_frame)    
    cv2.imshow("Color_Frame",frame)    
  

    # Close the windows when q pressed
    key = cv2.waitKey(1)
    if key == ord('q'):
        # if the object still moving 
        # add the last time before close the windows 
        if status == 1: 
            now = datetime.now()
            times.append(now.strftime("%D %H:%M:%S")) 
        break

video.release()
make_times_file()
cv2.destroyAllWindows()
