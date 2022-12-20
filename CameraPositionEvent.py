
class CameraPosEvent:

    def __init__(self,x1,y1,x2,y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2


    # x1~y2를 바로 전송 가능한 형태의 string 으로 반환
    # event는 정수형 0 , 1 등
    # 주의 : 데이터 포멧은 x1/y1/x2/y2/이벤트 순서임
    # 데이터 포멧 변경 (x,y만 마우스 2D값으로 필요하니까 x,y값에 이벤트만 첨부
    # 00123/00084/0
    def getDataFormat(self, event):
        strX = str(self.x2).zfill(5)
        strY = str(self.y2).zfill(5)
        return "{0}/{1}/{2}".format(strX,strY,event)
