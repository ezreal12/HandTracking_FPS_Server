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


        if(lastHandPos != None):
            caPos.setDiff(lastHandPos.x2,lastHandPos.y2)
            sendMsg = caPos.getDataFormat(0)
            if(sendMsg != None):
                TestServer2.SendMessageAllClinet(sendMsg) # 서버 전송부분
            print("HS LOG 1 ----- " + caPos.getDataFormat(0))

        lastHandPos = caPos

        # 2. Get tip of the index and middle finger
        # 3. Chaeck which fingers are up
        fingers = detector.fingersUp()
        #print(fingers)
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
        # 4. Only Inder fingers : Moving mode
        if fingers[1] == 1 and fingers[2] == 0:
            # 5. convert coordinates
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wSrc))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hSrc))
            # 6. Smoothen Values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            # 7. Move Mouse
            #autopy.mouse.move(wSrc - clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 0), cv2.FILLED)
            plocX, plocY = clocX, clocY

        # 8. Both index and middle fingers are up : clicking mode
        if fingers[1] == 1 and fingers[2] == 1:
            # 9. find distance between fingers
            length, img, lineInfo = detector.findDistance(8, 12, img)
            print(length)
            # 10. Click mouse if distance are short
            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                #autopy.mouse.click()

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