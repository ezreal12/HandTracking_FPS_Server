import cv2
smoothening = 5
##################################
import numpy as np
import HandTrackingModule as htm
import time
import autopy
import CameraPositionEvent
import TestServer2
##################################
wCam, hCam = 640, 480
frameR = 100 # Frame Reduction

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = htm.handDetector(maxHands= 1)
wSrc, hSrc = autopy.screen.size()
#print(wSrc, hSrc)
# 서버 시작해놓고 루프문 진입
TestServer2.StratServer()
# 마지막으로 추적했던 손 위치 정보 : CameraPosEvent로 저장됨.
lastHandPos = None

# 개선사항 1. OPenCV 카메라 60프레임  설정
# 2. 메시지 전송할때 1회성스레드 이용
# 3. 카메라 좌우반전 대칭적용

while True:
    # 1. Find hand landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList , bbox = detector.findPosition(img)
    # !! 221221 : 하다말았음. 클라쪽 수정해라
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        caPos = CameraPositionEvent.CameraPosEvent(x1,y1,x2,y2)

        # 2. Get tip of the index and middle finger
        # 3. Chaeck which fingers are up
        fingers = detector.fingersUp()
        #print(fingers)
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

        if (lastHandPos != None):
            # 4. Only Inder fingers : Moving mode
            caPos.setDiff(lastHandPos.x2, lastHandPos.y2)
            if fingers[1] == 1:
                sendMsg = caPos.getDataFormat(1)
            else:
                sendMsg = caPos.getDataFormat(0)
            print(sendMsg)
            TestServer2.SendMessageAllClinet(sendMsg)  # 서버 전송부분

        lastHandPos = caPos
    else:
        # 마지막 손 위치 정보 리셋
        lastHandPos = None

    # 11. Frame rate
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    # 12. Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)