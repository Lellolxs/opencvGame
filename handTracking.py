import cv2 as cv
import mediapipe as mp

cap = cv.VideoCapture(0, cv.CAP_DSHOW)
cap.set(cv.CAP_PROP_FPS, 30)

mp_Hands = mp.solutions.hands
hands = mp_Hands.Hands()
mpDraw = mp.solutions.drawing_utils
finger_Coord = [(8, 6), (12, 10), (16, 14), (20, 18)]
thumb_Coord = (2,4)

while True:
    success, image = cap.read()
    RGB_image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    results = hands.process(RGB_image)
    multiLandMarks = results.multi_hand_landmarks

    if multiLandMarks:
        handList = []
        for handLms in multiLandMarks:
            mpDraw.draw_landmarks(image, handLms, mp_Hands.HAND_CONNECTIONS)
            for idx, lm in enumerate(handLms.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                handList.append((cx, cy))
        for point in handList:
            cv.circle(image, point, 10, (255, 255, 0), cv.FILLED)
        upCount = 0
        for coordinate in finger_Coord:
            if handList[coordinate[0]][1] < handList[coordinate[1]][1]:
                upCount += 1
        if handList[thumb_Coord[0]][0] > handList[thumb_Coord[1]][0]:
            upCount += 1
        cv.putText(image, str(upCount), (150,150), cv.FONT_HERSHEY_PLAIN, 12, (0,255,0), 12)
        print(upCount,file=open('status.txt','a',encoding='UTF-8'))

    cv.imshow("Counting number of fingers", image)

    k = cv.waitKey(1) & 0xFF
    if k == 27:
        break