import cv2
import os
import dlib
from imutils import face_utils
from math import sqrt
print('Initialising...')
print('Setting up camera...')
cam = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_DUPLEX
bottomLeftCornerOfText = (10, 400)
fontScale = .5
fontColor = (255, 255, 255)
lineType = 1
def minus(p1,p2):
    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]
    out = sqrt( (x2 - x1)**2 + (y2 - y1)**2 )
    return out
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarkst.dat")
num_setup_frames = 90
frame_count = 0
alert_count = 0
EAR_vals = []
while True:
    if alert_count > 12:
        print('\n\n\t\t\tDANGER!!!\n\t\tDrowsiness Detected')
        break
    frame_count += 1
    ret, frame = cam.read()
    k = cv2.waitKey(1)

    if k % 256 == 27:
        
        print("Escape hit, closing...")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
   
    rects = detector(gray, 0)
    
    if len(rects) == 0:
        continue
    elif len(rects) == 1:
        rect = rects[0]
    else:
        rect = rects[0]
        
        
   
    shape1 = predictor(gray, rect)
    shape1 = face_utils.shape_to_np(shape1)
    print(' ')
    print(str(frame_count) + '__________________________'+str(alert_count))

    left_eye = shape1[36:42]
    right_eye = shape1[42:48]
  
    for (x, y) in left_eye:
            
        cv2.circle(frame, (x, y), 2, (255, 0, 0), -10)

    
    for (x, y) in right_eye:
            
        cv2.circle(frame, (x, y), 2, (255, 0, 0), -10)
   
        
    p = shape1
        
    
    EAR = (minus(p[37],p[41]) + minus(p[38],p[40]))/(2*minus(p[39],p[36]))
    print("EAR: "+ str(EAR))  
        
     
        
    if frame_count < num_setup_frames:
        EAR_vals.append(EAR)
        
       
    elif frame_count == num_setup_frames:
        print('\n\nSetup phase completed.')
        
        EAR_vals.sort()
        EAR_thres = sum(EAR_vals[0:len(EAR_vals)/2])/(len(EAR_vals)/2)

        
        print('EAR Threshold: ' + str(EAR_thres))
        
    else:
       
        if EAR < EAR_thres:
            alert_count +=1
            print('\n\tAlert!!! Eyes Closing!!!\n')
            continue
        
    
    cv2.putText(
        frame, 'Driver',
        tuple(p[17]),
        font,
        fontScale,
        fontColor,
        lineType
        )
    
    cv2.imshow("Frame", frame)        
   
    key = cv2.waitKey(1) & 0xFF
    
 
    
    if key == ord("q"):
        break


cam.release()
cv2.destroyAllWindows()
