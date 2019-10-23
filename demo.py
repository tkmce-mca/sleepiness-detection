import cv2
import os
import dlib
from imutils import face_utils
from math import sqrt
#import matplotlib.pyplot as plt

print('Initialising..........')

print('Setting up camera...')
cam = cv2.VideoCapture(0)

def minus(p1,p2):
    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]
    out = sqrt( (x2 - x1)**2 + (y2 - y1)**2 )
    return out
  
# the facial landmark predictor
print("[INFO] loading facial landmark predictor.........")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarkst.dat")
num_setup_frames = 90
frame_count = 0
alert_count = 0
EAR_vals = []

 # determine the facial landmarks for the face region, then
    # convert the facial landmark (x, y)-coordinates to a NumPy
    # array
   
    shape1 = face_utils.shape_to_np(shape1)
    
    # loop over the (x, y)-coordinates for the left eye landmarks
    # and draw them on the image
    for (x, y) in left_eye:
            #print(x,y)
        cv2.circle(frame, (x, y), 2, (255, 0, 0), -10)

    # loop over the (x, y)-coordinates for the right eye landmarks
    # and draw them on the image
    for (x, y) in right_eye:
            #print(x,y)
        cv2.circle(frame, (x, y), 2, (255, 0, 0), -10)
        
            
    p = shape1
        
    # Calculate Eye Aspect Ratio
    EAR = (minus(p[37],p[41]) + minus(p[38],p[40]))/(2*minus(p[39],p[36]))
    print("EAR: "+ str(EAR))  
        
      if frame_count < num_setup_frames:
        EAR_vals.append(EAR)
        
          elif frame_count == num_setup_frames:
        print('\n\nSetup phase completed.')
        
        EAR_vals.sort()
        EAR_thres = sum(EAR_vals[len(EAR_vals)/2])/(len(EAR_vals)/2)
        
          if EAR < EAR_thres:
            alert_count +=1
            print('\n\tAlert!!! Eyes Closing!!!\n')
            
            # show the frame
    cv2.imshow("Frame", frame)        
    #cv2.imshow("Faces found", frame)    
    key = cv2.waitKey(1) & 0xFF
    
 
 

#plt.plot(EAR_vals,'--r^')
# do a bit of cleanup
cam.release()
cv2.destroyAllWindows()
