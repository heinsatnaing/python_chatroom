import threading
import socket

host = "127.0.0.1"
port = 12345
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
clients = []
aliases = []


def broadcast(message):
    for client in clients:
        client.send(message)


# function to handle clients' connection
def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f"{alias} has left the chatroom!".encode('utf-8'))
            aliases.remove(alias)
            break


def receive():
    while True:
        print('Server is ruunning and listening ...')
        client, address = server.accept()
        print(f"Connection is established with {str(address)}")
        client.send('Alias?'.encode("utf-8"))
        alias = client.recv(1024)
        aliases.append(alias)
        clients.append(client)
        print(f"The alias of the client is {alias}".encode("utf=8"))
        broadcast(f"{alias} has connected to the chatroom.".encode("utf-8"))
        client.send("You are connected to the chatroom!".encode("utf-8"))
        thread = threading.Thread(target = handle_client, args = (client,))
        thread.start()

if __name__ == "__main__":
    receive()