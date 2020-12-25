import socket
import threading


HEADER = 64
PORT = 3000
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"



# pour se connecter au server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)



def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)



def receive_from_server():
    connected = True 
    while connected:
        msg_length = client.recv(HEADER).decode(FORMAT) # message pour taille du message
        if msg_length:
            msg = client.recv(int(msg_length)).decode(FORMAT) # message a envoyer
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(msg)



def start():
    # thread pour ecouter le serveur
    thread = threading.Thread(target=receive_from_server)
    thread.daemon = True
    thread.start()

    # pour envoyer les messages
    while True:
        msg = input()
        if msg == "!DISCONNECT":
            send(DISCONNECT_MESSAGE)
            break
        
        send(msg)



send(input("your name : "))
start()
