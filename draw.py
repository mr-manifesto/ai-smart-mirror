import cv2 as cv
import numpy as np

ig = cv.imread("photos/HD2.jpg")

ig[200:500 , 300:600] = 0,0,255
# cv.imshow("og",ig)

cv.rectangle(ig,(200,500),(300,600),(255,0,0),3)
cv.circle(ig,(400,350),50,(0,255,0),cv.FILLED)
cv.line(ig,(0,0),(ig.shape[1],ig.shape[0]),(255,255,255),5)
cv.putText(ig,"hello all, iam the dhanush, night lord",(200,450),cv.FONT_HERSHEY_COMPLEX,1,(0,0,0),2)
cv.imshow("model",ig)
cv.waitKey(0)

