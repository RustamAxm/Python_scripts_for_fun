import cv2
img = cv2.imread(r"Test.jpg")
def nothing(args):pass
cv2.namedWindow("setup")
cv2.createTrackbar("er","setup",0,10,nothing)
cv2.createTrackbar("di","setup",0,10,nothing)
cap = cv2.VideoCapture(0)
while(True):
   er=cv2.getTrackbarPos("er","setup")
   di=cv2.getTrackbarPos("di","setup")
   maskEr=cv2.erode(img,None,iterations = er)
   maskDi=cv2.dilate(maskEr,None,iterations = di)
   cv2.imshow('img', maskDi)
   if cv2.waitKey(1) & 0xFF == ord('q'):
      break
cap.release()
cv2.destroyAllWindows()