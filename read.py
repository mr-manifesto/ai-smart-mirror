import cv2 as cv

ig = cv.imread("photos/promise.jpg")

cv.imshow("promise", ig)

cv.waitKey(0)

# cap = cv.VideoCapture("videos/virat.mp4")

# while True:
#     isT , frame = cap.read()

#     if cv.waitKey(20) & 0xFF == ord("d") or not isT:
#         break
#     cv.imshow("videos", frame)

# cap.release()
# cv.destroyAllWindows() 