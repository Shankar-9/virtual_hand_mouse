import cv2
import cv2 as cv
import mediapipe as mp
import ctypes
import mouse as m
import numpy as np
import math
import time
vid= cv.VideoCapture(0)
mpHands=mp.solutions.hands
hands=mpHands.Hands(max_num_hands=1)
Draw=mp.solutions.drawing_utils
wcam, hcam=640,480
rect_cordinate=100
place_cordinate=100
vid.set(3, wcam)
vid.set(4, hcam)
wscrn,hscrn=ctypes.windll.user32.GetSystemMetrics(0),ctypes.windll.user32.GetSystemMetrics(1)
print(wscrn,hscrn)
def fingerup(handlm):
    arr=[0]*5
    if( handlm.landmark[4].y<handlm.landmark[5].y):
        arr[4]=1
    if(handlm.landmark[8].y<handlm.landmark[6].y):
        arr[3]=1
    if(handlm.landmark[12].y<handlm.landmark[10].y):
        arr[2]=1
    if(handlm.landmark[16].y<handlm.landmark[14].y):
        arr[1]=1
    if(handlm.landmark[20].y<handlm.landmark[18].y):
        arr[0]=1
    return arr
def distance_btw_fingers(index1, index2, handlm):
    x1, y1 = handlm.landmark[index1].x*wscrn, handlm.landmark[index1].y*hscrn
    x2, y2 = handlm.landmark[index2].x*wscrn, handlm.landmark[index2].y*hscrn
    dis=math.sqrt((x2-x1)**2+(y2-y1)**2)
    return dis, x1,y1,x2,y2



while True:
    success, img= vid.read()
    img=cv.flip(img, 1)
    imgRGB=cv.cvtColor(img, cv.COLOR_BGR2RGB)
    result=hands.process(imgRGB)
    list1, list2 = [], []
    cv.rectangle(img,(rect_cordinate-place_cordinate,rect_cordinate-place_cordinate),(wcam-rect_cordinate-place_cordinate, hcam-rect_cordinate-place_cordinate),(255,0,0),10)
    if result.multi_hand_landmarks:
        for handlm in result.multi_hand_landmarks:
            for id, land_mark in enumerate(handlm.landmark):
                # finding co-ordinates of middle and index fingers
                x1, y1= round(handlm.landmark[8].x*wcam), round(handlm.landmark[8].y*hcam)
                x2,y2=round(handlm.landmark[12].x*wcam), round(handlm.landmark[12].y*hcam)
                # print(x1,y1,x2,y2)
                finger=fingerup(handlm)
                if finger[3]==1 and finger[2]==0:
                    x3=np.interp(x1,(rect_cordinate-place_cordinate,wcam-rect_cordinate-place_cordinate), (0,wscrn))
                    y3=np.interp(y1,(rect_cordinate-place_cordinate,hcam-rect_cordinate-place_cordinate),(0,hscrn))
                    m.move(x3,y3)
                    cv.circle(img,(x1,y1),10,(255,0,0),cv2.FILLED)
                if finger[3]==1 and finger[2]==1:
                    dis=distance_btw_fingers(8,12,handlm)
                    cv.circle(img, (x1, y1), 10, (0,255,255), cv2.FILLED)
                    cv.circle(img, (x2, y2), 10, (0,255,255), cv2.FILLED)
                    if(dis[0]<=40):
                        m.click()
                if finger[3] == 1 and finger[2] == 1 and finger[1]==1:
                    m.wheel()

                height, width, c = img.shape
                cx, cy= int(land_mark.x*width), int(land_mark.y*height)


                if id==4 or id==8:
                    if(id==4):
                        list1.append((cx,cy))
                    else:
                        list2.append((cx,cy))
                    cv.circle(img, (cx,cy),10, (0,0,255),cv.FILLED )
                    if(len(list1)>=1 and len(list2)>=1):
                        cv.line(img, list1[0], list2[0], (0,0,255), 10)
                # print(type(img.shape))
            Draw.draw_landmarks(img, handlm, mpHands.HAND_CONNECTIONS,  Draw.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=2))
            # print(mpHands.HAND_CONNECTIONS) this is a set determines the line start and end positions
    cv.imshow("video", img)
    if cv.waitKey(1)==ord('q'):
        break


