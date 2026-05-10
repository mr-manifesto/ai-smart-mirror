import cv2 as cv

ig = cv.imread("photos/HD2.jpg")




def rescalef(frame , scale = 0.75):
    w = int(frame.shape[1]*scale)
    h = int(frame.shape[0]*scale)
    d = (w,h)
    return cv.resize(frame,d,interpolation=cv.INTER_AREA)

# def changeres(wid,hei):
#     capture.set(3, wid)
#     capture.set(4, hei)
    

cv.imshow("nightking", ig)
cv.imshow("nightlord",rescalef(ig,0.5))

cv.waitKey(0)

cap = cv.VideoCapture("videos/virat.mp4")

while True:
    isT , frame = cap.read()
    reframe = rescalef(frame,0.5)
    if cv.waitKey(20) & 0xFF == ord("d") or not isT:
        break
    cv.imshow("virat", frame)
    cv.imshow("kohli", reframe)

cap.release()
cv.destroyAllWindows() 