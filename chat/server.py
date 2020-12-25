import socket
import threading

HEADER = 64
PORT = 3000
SERVER = input("Enter the IP address you will use : ") # obtenir l'ip local de l'ordinateur
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

# elt = ( connection, addr, name ) connection: objet socket,  addr = (ip, port)
list_clients = []


# creer une adresse pour le server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # declare le type de socket
server.bind(ADDR)   # lie l'ip et le port



def add_client(connection, addr):
    name = ""
    msg_length = connection.recv(HEADER).decode(FORMAT) # message pour taille du message
    if msg_length:
        msg_length = int(msg_length)
        name = connection.recv(msg_length).decode(FORMAT)

    client = (connection, addr, name)
    list_clients.append(client)

    print(f"[NEW CONNECTION] {addr} connected")

    return client



def send_to_others(sender, msg):
    # encode messages a envoyer
    message = (f"[{sender[2]}] "+ msg).encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))

    # envoie messages aux autres
    for client in list_clients:
        if client[1][1] != sender[1][1]:

            client[0].send(send_length)
            client[0].send(message)



def remove_client(client):
    for i in range(len(list_clients)):
        if (list_clients[i][1][1] == client[1][1]):
            list_clients.pop(i)
            break
    print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 2}")



def handle_client(connection, addr):
    #  enrengistre name du client
    client = add_client(connection, addr)


    connected = True 
    while connected:
        msg_length = connection.recv(HEADER).decode(FORMAT) # message pour taille du message
        if msg_length:
            msg_length = int(msg_length)
            msg = connection.recv(msg_length).decode(FORMAT) # message a envoyer
            if msg == DISCONNECT_MESSAGE:
                connected = False
            else:
                # thread pour envoyer le message aux autres
                thread = threading.Thread(target=send_to_others, args=(client, msg))
                thread.start()

            print(f"[{addr}] {msg}")

    # quand fin de la connexion, enleve supprime le client
    remove_client(client)



def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        connection, addr = server.accept()  # fct blocante jusqu'a avoir une connection
        

        # un thread par client pour recevoir leur message
        thread = threading.Thread(target=handle_client, args=(connection, addr))
        thread.daemon = True
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")



print("[STARTING] server is starting...")
start()
