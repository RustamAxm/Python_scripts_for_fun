import cv2


def nothing(args): pass


cap = cv2.VideoCapture(0)
l = [];
while True:
    ret, frame = cap.read()
    min_p = (0, 0, 93)
    max_p = (255, 62, 255)
    img_mask = cv2.inRange(frame, min_p, max_p)
    blur_img = cv2.medianBlur(img_mask, 1 + 10 * 2)
    img_m = cv2.bitwise_and(frame, frame, mask=blur_img)
    contours, ret = cv2.findContours(blur_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    img_m_copy = img_m.copy()
    if contours:
        # contours = contours[0] if imutils.is_cv2() else contours[1]
        cntsSorted = sorted(contours, key=lambda x: cv2.contourArea(x))
        (x, y), radius = cv2.minEnclosingCircle(contours[0])
        center = (int(x), int(y))
        radius = int(radius)
        cv2.circle(img_m_copy, center, radius, (0, 255, 0), 2)
        steps = 15  # количество используемых точек
        if len(l) == 15:
            l = l[1:]
        l.append(center);
        for i in range(len(l) - 1):
            cv2.line(img_m_copy, l[i], l[i + 1], (255, 250, 250), 2)

    cv2.imshow('base', img_m_copy)

    # cv2.imshow('Video', blur_img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()