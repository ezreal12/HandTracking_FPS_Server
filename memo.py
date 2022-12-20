중요
import mediapipe as mp

self.mpHands = mp.solutions.hands
self.mpDraw = mp.solutions.drawing_utils

self.hands = self.mpHands.Hands
    (self.mode, 
    self.maxHands, 
    self.modelComplex, 
    self.detectionCon, 
    self.trackCon)



img = detector.findHands(img)

def findHands(self, img, draw=True):
    # OPEN CV 이슈로 img 그냥 읽어오면 RGB가 아니라 BGR로 옴 고로 반전
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # 여기가 중요 -> 미디어파이프에서 손찾는 함수 
    # self.mpHands.Hands.process(imgRGB)
    # 반환받은 results가 그 결과 (손 찾은 위치 정보)
    # 이 한줄이 Mideapipe가 손을(손가락 아님) Obejct Detection해서 찾아낸 손의 바운딩박스를 뱉는 함수
    self.results = self.hands.process(imgRGB)
    
    # 손을 찾았으면 (즉, result에서 손 랜드마크에 대한 정보를 뱉어서 multi_hand_landmarks 변수가 NULL이 아니면
    if self.results.multi_hand_landmarks:
        # multi_hand_landmarks에서 손 위치를 나타내는 바운딩 박스 정보 조회
        for handLms in self.results.multi_hand_landmarks:
            # mpDraw라는 모듈이 임의의 이미지 img를 입력받고 , 
            # mpHands.Hands.process()가 뱉어낸 손 위치를 나타내는 오브젝트 디텍션 결과를 입력받으면
            # 알아서 입력받은 이미지 img 변수에 직접 좌표정보를 그려줌??
            self.mpDraw.draw_landmarks(img, handLms,self.mpHands.HAND_CONNECTIONS)
                
                
    return img


# 매개변수로 입력받은 img는 opencv에서 카메라로 출력한 진짜 이미지 맞음
# detector.findHands(img) 함수로 뱉는 img가 
# 온전히 opencv의 img가 아닐 가능성이 있겠는데..
img = detector.findHands(img)
# mideapipe가 mp.solutions.drawing_utils 모듈에서 draw_landmarks() 함수로 
# 만들어준 바인딩 박스 정보를 분리해내는 함수도 제공하는거같음
# 그게 findPosition 즉, 
# hands.process()에서 찾고 mpDraw.draw_landmarks()에서 기록
# 그리고 여기서 기록한 바운딩박스를 분리해내는듯?
# lmList = 손의 좌표 정보 , 이거 한개가 손 1개의 위치 x1,y1,x2,y2를 담는다

lmList , bbox = detector.findPosition(img)

# 찾아낸 손의 정보가 있으면 
if len(lmList) != 0:
    #lmList에서 x1~y2까지 4정보 가져오기
    x1, y1 = lmList[8][1:]
    x2, y2 = lmList[12][1:]
    # Up해있는 손가락 정보 찾기?
    fingers = detector.fingersUp()
    
def fingersUp(self):
    fingers = []
    if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
        fingers.append(1)
    else:
        fingers.append(0)
    # id는 그냥 1~5까지 반복해줄때 인덱스로 쓰기위한 용도인듯
    # 아! 손가락은 5개니까 그런듯?
    # 찾아낸 손에서 손가락 5개의 정보를 전부 조회하는 for문
    for id in range(1, 5):
        # 손가락이 up 상태인지 아닌지를 판단하는 부분이 여기에 있음
        # 만약 현재 조회중인 손가락의 위치가 2차례 전의 손가락보다 위치가 낮으면 Up으로 치는듯?
        # 여긴 좀더 확인해봐야할거같다. / 입력은 검지랑 중지로만 받잖아
        if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers

# 여기서 self.tipIds
self.tipIds = [4, 8, 12, 16, 20] # 이게뭐지????
# 아 이거 그거네 fingersUp은 말 그대로 Up되어있는 손가락을 찾는건데
# 손가락 길이가 다 일정한 규칙을 갖는다고 치니까 (예 : 특수한 경우가 아니면 엄지가 검지보다 긴 경우는 없음)
if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]: # 이 부분

# 아 이거네 AI~.py main쪽에 이런거있음
fingers = detector.fingersUp()
if fingers[1] == 1 and fingers[2] == 0:

# 일단 detector.fingersUp()은 모든 Up된 손가락을 찾아내 정보를 담고
# 여기에서 만약 Up된 손가락에 검지(1)와 중지(2)가 있으면 동작을 실행

# 이게 대충 위에서 설명한 로직에서 마우스 움직이는 부분
# 보면 fingers[1]은 검지 , fingers[2] 중지
# 만약 검지가 올라가있고 (ingers[1] == 1)
# 중지는 내려가있으면 (fingers[2] == 0)
# 마우스 무빙 로직에 들어간다.
if fingers[1] == 1 and fingers[2] == 0:
    # 5. convert coordinates
    x3 = np.interp(x1, (frameR, wCam - frameR), (0, wSrc))
    y3 = np.interp(y1, (frameR, hCam - frameR), (0, hSrc))
    # 6. Smoothen Values
    clocX = plocX + (x3 - plocX) / smoothening
    clocY = plocY + (y3 - plocY) / smoothening

    # 7. Move Mouse
    autopy.mouse.move(wSrc - clocX, clocY)
    cv2.circle(img, (x1, y1), 15, (255, 0, 0), cv2.FILLED)
    plocX, plocY = clocX, clocY

# 이건 또 다른 부분 (마우스 클릭부분)
# 만약 검지가 올라가있고 (ingers[1] == 1)
# 중지도 올라가있으면 (fingers[2] == 1)
# 마우스 클릭 관련 로직에 들어간다.
if fingers[1] == 1 and fingers[2] == 1:

# 아래가 마우스 클릭 전체부분
if fingers[1] == 1 and fingers[2] == 1:
    # 9. find distance between fingers
    # 거리계산이 힘든가본데 ; findDistance로 가네
    # 8 : p1 , 추적할 손가락 1번 (여기선 검지를 의미)
    # 12: p2 , 추적할 손가락 2번 (여기선 중지를 의미)
    # length : math로 계산한 p1, p2 사이의 거리
    # lineInfo : findDistance에서 사용했던 p1,p2의 위치 , cx,cy등

    length, img, lineInfo = detector.findDistance(8, 12, img)
    print(length)
    # p1(검지), p2(중지) 사이의 거리가 40 미만으로 좁혀지면 클릭 이벤트 발동
    if length < 40:
        cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
        autopy.mouse.click()


# ----------------

# 설마 p1,p2가 핑거1, 핑거2인가?
# img는 opencv+mideapipe를 거친 이미지 벡터 img고
# draw는 그릴지말지를 정할뿐이니까 신경 X
length, img, lineInfo = detector.findDistance(8, 12, img)
def findDistance(self, p1, p2, img, draw = True):
    # 핑거 1의 위치 정보 xy를 x1,y1로 잡고
    x1, y1 = self.lmList[p1][1], self.lmList[p1][2]
    # 핑거 2의 위치 정보 xy를 x2,y2의 범위로 x1~y2 사각 범위를 잡는다.
    x2, y2 = self.lmList[p2][1], self.lmList[p2][2]
    # 우와;; 이거뭐임?
    # 이중 슬래시(//) 연산자는 파이썬에서 다양한 목적으로 사용됩니다. 이 연산자의 한 가지 용도는 나눗셈 결과를 얻는 것입니다.
    # 단일 슬래시 연산자는 부동 소수점 결과에 대한 적절한 출력을 반환하지만
    # 이중 슬래시 연산자는 부동 소수점 결과의 소수 부분을 반환할 수 없다는 것입니다.
    # '/'는 그냥 나누기임 근데 이걸 따블'//'로 얹어쓰면 나는 나누기는 할건데 소수점은 버리고 정수로만 받을거야 라는 줄임말인듯
    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

    if draw:
        # OPENCV 툴을 이용해서
        cv2.circle(img, (x1, y1), 15, (225, 0, 225), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (225, 0, 225), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (225, 0, 225), 3)
        cv2.circle(img, (cx, cy), 15, (225, 0, 225), cv2.FILLED)

    # 여기가 중요! : x2와 x1 / y2와 y1의 차이를 math 함수로 구할뿐임 의외로 단순한듯?
    length = math.hypot(x2 - x1, y2 - y1)
    # 계산했던 손가락 2개의 거리값 , draw가 참일때 표시 그려줬던 img 값,
    # 이 함수에서 사용했던 설정값들 (손가락 1번의 위치 x1,y1)(손가락 2번의 위치 x2, y2) cx,cy를 배열로 반환
    # 이 배열은 나중에 lineInfo라는 이름으로 쓰이게됨.
    return length, img, [x1, y1, x2, y2, cx, cy]

# --- 여기까지 작성 완료하고 검토해보니 findPosition가 빠져있었음
# --- 아래서부터 누락 findPosition 보충
    success, img = cap.read()
    img = detector.findHands(img)
    lmList , bbox = detector.findPosition(img)

lmList , bbox = detector.findPosition(img)
def findPosition(self, img, handNo=0, draw=True):




    
    
