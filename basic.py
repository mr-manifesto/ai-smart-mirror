import cv2 as cv

ig = cv.imread("photos/HD2.jpg")

ig = cv.cvtColor(ig, cv.COLOR_BGR2GRAY)

# ig = cv.GaussianBlur(ig,(7,7),cv.BORDER_DEFAULT)

# ig = cv.Canny(ig,125,175)

# ig = cv.dilate(ig,(7,7),iterations=3)
# ig = cv.erode(ig,(7,7),iterations=3)
ig = cv.resize(ig,(1600,900))
ig = ig[20:200, 700:900]
cv.imshow("og", ig)
cv.waitKey(0)
