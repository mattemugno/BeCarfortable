import socket

ip = "192.168.1.59"
ipRaspberry = "192.168.1.54"

emotion_list = ['sad', 'angry', 'disgust', 'happy', 'fear', 'surprise']


def receiveExcludedEmotion():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('socket instantiated')

    sock.bind((ip, 8080))
    print('socket binded')

    sock.listen()
    print('socket now listening')

    conn, addr = sock.accept()
    print('socket accepted, got connection object')
    encodedMessage = bytes("OK", 'utf-8')

    while 1:
        excluded_emotion = conn.recv(4096).decode()

        if excluded_emotion not in emotion_list:
            print("SERVER: Emotion not valid.")
            continue
        else:
            print("SERVER: Emotion received: " + excluded_emotion + ".")
            conn.send(encodedMessage)
            return excluded_emotion


def send_skip():

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ipRaspberry, 8080))

    encodedMessage = bytes("skip", 'utf-8')
    print("MANDO SKIP")
    client.send(encodedMessage)

    encodedAckText = client.recv(1024)
    ackText = encodedAckText.decode('utf-8')

    if ackText == "OK":
        print('server acknowledged reception of text')
    else:
        print('error: server has sent back ' + ackText)
