import cv2 as cv
import numpy as np

ig = cv.imread("photos/HD2.jpg")
cv.imshow("og", ig)

def translate(ig , x, y):
    mat = np.float32([[1,0,x],[0,1,y]])
    dim = (ig.shape[1], ig.shape[0])
    return cv.warpAffine(ig, mat, dim)

tlated = translate(ig, 100, 100)
cv.imshow("translated", tlated)
cv.waitKey(0)