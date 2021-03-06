import cv2, argparse
import numpy as np
import time

ap = argparse.ArgumentParser()
ap.add_argument("-s", "--src", help="path to the video file", type=int, default=0)
ap.add_argument("-f", "--file", help="file name to save to", type=str)
args = vars(ap.parse_args())

blurVal = 1
WVal = 0
HVal = 0

def time_to_string():
    """
    Returns a string of current time suitable for filenames
    20180914_234000
    """
    return str(time.strftime('%Y%m%d_%H%M%S'))

def time_to_string_human():
    """
    Returns a human readible string of current time
    2018-09-14 23:40:00
    """
    return str(time.strftime('%Y-%m-%d %H:%M:%S'))

def on_blur_trackbar(val):
    global blurVal
    blurVal = 2*val+1

def on_W_trackbar(val):
    global WVal
    WVal = val

def on_H_trackbar(val):
    global HVal
    HVal = val

def on_blurMode_trackbar(val):
    global blur_mode
    blur_mode = val

def on_blurParamX_trackbar(val):
    global blur_paramX
    blur_paramX = val*2+1

def on_blurParamY_trackbar(val):
    global blur_paramY
    blur_paramY = val*2+1

def on_blurParamZ_trackbar(val):
    global blur_paramZ
    blur_paramZ = val

def on_bitdepth_trackbar(val):
    global bitdepth
    depth = [0b10000000, 0b11000000, 0b11100000, 0b11110000,
        0b11111000, 0b11111100, 0b11111110, 0b11111111]
    bitdepth = depth[val]

W = 1280
H = 720
R = 60
blur_mode = 0
blur_paramX = 1
blur_paramY = 1
blur_paramZ = 1

bitdepth = 0b11111111

cv2.namedWindow("Frame")
#cv2.namedWindow("Gray")
cv2.createTrackbar("Bit-depth", "Frame", 0, 7, on_bitdepth_trackbar)
cv2.createTrackbar("Blurness", "Frame", 0, 50, on_blur_trackbar)
cv2.createTrackbar("Blur Mode", "Frame", 0, 4, on_blurMode_trackbar)
cv2.createTrackbar("Param X", "Frame", 0,100, on_blurParamX_trackbar)
cv2.createTrackbar("Param Y", "Frame", 0,100, on_blurParamY_trackbar)
cv2.createTrackbar("Param Z", "Frame", 0,100, on_blurParamZ_trackbar)
cv2.createTrackbar("Height", "Frame", 0, H, on_H_trackbar)
cv2.createTrackbar("Width", "Frame", 0, W, on_W_trackbar)
cap = cv2.VideoCapture(args['src'])

# cap.set(3,W)
# cap.set(4,H)
cap.set(3,640)
cap.set(4,480)

if args['file']:
    writer = cv2.VideoWriter(args['file'], cv2.VideoWriter_fourcc('X','2','6','4'), 30, (640,480))

while(True):
    ret, frame = cap.read()
    frame &= bitdepth
    # frame = cv2.flip(frame, 1)

    if blur_mode == 0:
        pass
    elif blur_mode == 1:
        frame = cv2.blur(frame, (blurVal,blurVal))
    elif blur_mode == 2:
        frame = cv2.GaussianBlur(frame, (blur_paramX,blur_paramY), 0)
    elif blur_mode == 3:
        frame = cv2.medianBlur(frame, blurVal)
    elif blur_mode == 4:
        frame = cv2.bilateralFilter(frame, blur_paramZ, blur_paramX, blur_paramY)
        
    # frame = cv2.resize(frame, (int(W/R),int(H/R)))
    # frame = cv2.resize(frame,(W,H))
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame,time_to_string_human(),(WVal,HVal), font, 0.5,(0,255,0),1,cv2.LINE_AA)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #cv2.imshow('Gray', gray)
    cv2.imshow('Frame',frame)
    if args['file']:
        writer.write(frame)
    if cv2.waitKey(33) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
