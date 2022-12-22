
class CameraPosEvent:

    def __init__(self,x1,y1,x2,y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.moveXPlus = 0
        self.moveXMinus = 0
        self.moveYPlus = 0
        self.moveYMinus = 0
        
    # 이전 x2,y2값을 입력받아서 차이 계산해 저장하기
    def setDiff(self,oldX,oldY):
        diffX = self.x2 - oldX
        diffY = self.y2 - oldY
        if(diffX >= 0):
            self.moveXPlus = diffX
        else:
            self.moveXMinus = diffX * -1

        if(diffY >= 0):
            self.moveYPlus = diffY
        else:
            self.moveYMinus = diffY * -1



    # x1~y2를 바로 전송 가능한 형태의 string 으로 반환
    # event는 정수형 0 , 1 등
    # 주의 : 데이터 포멧은 x1/y1/x2/y2/이벤트 순서임
    # 데이터 포멧 변경 x+이동값/x-이동값/y+이동값/y-이동값/이벤트코드
    # 00033/00000/00000/00000/0
    # 00000/00022/00000/00000/0
    def getDataFormat(self, event):
        strLength = 5
        xp = str(self.moveXPlus).zfill(strLength)
        xm = str(self.moveXMinus).zfill(strLength)
        yp = str(self.moveYPlus).zfill(strLength)
        ym = str(self.moveYMinus).zfill(strLength)
        # 글자길이 25
        return "{0}/{1}/{2}/{3}/{4}".format(xp,xm,yp,ym,event)
