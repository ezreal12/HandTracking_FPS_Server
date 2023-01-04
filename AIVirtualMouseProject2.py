import cv2
smoothening = 5
##################################
import numpy as np
import HandTrackingModule as htm
import time
import autopy
import CameraPositionEvent
import LastFindHands
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

#detector = htm.handDetector(maxHands= 1) ----------------------------------- !!
# 놀랍게도 기본값은 처음부터 2였음
detector = htm.handDetector(maxHands= 2)
wSrc, hSrc = autopy.screen.size()
#print(wSrc, hSrc)
# 서버 시작해놓고 루프문 진입
TestServer2.StratServer()
# 마지막으로 추적했던 손 위치 정보 : CameraPosEvent로 저장됨.
lastHands = None

# 개선사항 1. OPenCV 카메라 60프레임  설정
# 2. 메시지 전송할때 1회성스레드 이용
# 3. 카메라 좌우반전 대칭적용

while True:
    # 1. Find hand landmarks
    success, img = cap.read()
    # 손찾기 (시작부분)
    img = detector.findHands(img)

    # getDetecedHandsCount는 내가 임의로 만든 함수 : 추적해낸 손의 갯수를 리턴함.
    if(detector.getDetecedHandsCount() > 1):
        # 230103 알아낸 사실 : detector.findHands(img)의 Draw가 True면 찾아낸 손의 갯수는 일단 고려하지않고 찾아낸 손에 모두 빨간색 표시를함.
        # 230103 알아낸 사실2 : detector.findPosition(img, handNo=INT)의 Draw가 True면 handNo를 정수값으로 입력받고 해당 handNo 인덱스에 해당하는 손(인덱스 순서는 추적되는 손부터?)에 파란색과 바운딩 표시를 한다.
        # 손을 찾은 이미지 IMG에서 (handNo를 입력받아) 손의 위치를 그리고 위치가 담긴 바운딩 박스 반환
        lmList, bbox = detector.findPosition(img, handNo=0)
        lmList2, bbox2 = detector.findPosition(img, handNo=1)

        if (len(lmList) != 0) and (len(lmList2) != 0):
            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]
            caPos1 = CameraPositionEvent.CameraPosEvent(x1,y1,x2,y2)
            x1, y1 = lmList2[8][1:]
            x2, y2 = lmList2[12][1:]
            caPos2 = CameraPositionEvent.CameraPosEvent(x1, y1, x2, y2)

            if (lastHands != None):
                caPos1.setDiff(lastHands.handOne.x2, lastHands.handOne.y2)
                caPos2.setDiff(lastHands.handTwo.x2, lastHands.handTwo.y2)
                #sendMsg = caPos.getDataFormat(0)
                sendMsg1 = caPos1.getDataFormat(0)
                sendMsg2 = caPos2.getDataFormat(0)
                if ((sendMsg1 != None) and (sendMsg2 != None)):
                    # 00001/00000/00000/00000/1/00001/00000/00000/00000/0
                    # 00001/00000/00000/00000/1 /00001/00000/00000/00000/0 - 51자
                    TestServer2.SendMessageAllClinet(sendMsg1+"/"+sendMsg2)  # 서버 전송부분
                    print("TEST : {0}".format(sendMsg1+"/"+sendMsg2))

            #lastHandPos = caPos1
            lastHands = LastFindHands.LastFindHands(caPos1,caPos2)

    else:
        # 마지막 손 위치 정보 리셋
        lastHands = None



    # 11. Frame rate
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    # 12. Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)