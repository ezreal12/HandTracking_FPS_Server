import socket

import threading

import keyboard
host = "127.0.0.1"
port = 8888
clientSocketArr = []
def handle_client(client_socket, addr):
    print("접속한 클라이언트의 주소 입니다. : ", addr)
    user = client_socket.recv(1024)
    string = "1111111111111"
    client_socket.sendall(string.encode())
    #time.sleep(1)
    #client_socket.close()

def accept_func():
    global server_socket
    #IPv4 체계, TCP 타입 소켓 객체를 생성
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #포트를 사용 중 일때 에러를 해결하기 위한 구문
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #ip주소와 port번호를 함께 socket에 바인드 한다.
    #포트의 범위는 1-65535 사이의 숫자를 사용할 수 있다.
    server_socket.bind((host, port))

    #서버가 최대 5개의 클라이언트의 접속을 허용한다.
    server_socket.listen(5)

    while 1:
        try:
            #클라이언트 함수가 접속하면 새로운 소켓을 반환한다.
            client_socket, addr = server_socket.accept()
            # 클라이언트 소켓 추가 (전송용)
            clientSocketArr.append(client_socket)
        except KeyboardInterrupt:
            server_socket.close()
            print("Keyboard interrupt")

        print("클라이언트 핸들러 스레드로 이동 됩니다.")
        #accept()함수로 입력만 받아주고 이후 알고리즘은 핸들러에게 맡긴다.
        t = threading.Thread(target=handle_client, args=(client_socket, addr))
        # 데몬 쓰레드란 백그라운드에서 실행되는 쓰레드로 메인 쓰레드가 종료되면 즉시 종료되는 쓰레드이다. 반면 데몬 쓰레드가 아니면 해당 서브쓰레드는 메인 쓰레드가 종료할 지라도 자신의 작업이 끝날 때까지 계속 실행된다.
        t.daemon = True
        t.start()


if __name__ == '__main__':
    t2 = threading.Thread(target=accept_func)
    t2.daemon = True
    t2.start()
    #accept_func()
    while True :
        x = input()
        if(len(clientSocketArr) > 0):
            clientSocketArr[0].sendall("1111111111111".encode())
            print("SENDMSG")
        else:
            print("NONE")
