import socket
import threading

class ChatServer:
    def __init__(self, host='localhost', port=5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        
        self.clients = []
        self.nicknames = []
        
        print(f"Server is running on {host}:{port}")
    
    def broadcast(self, message):
        for client in self.clients:
            client.send(message)
    
    def handle_client(self, client):
        while True:
            try:
                message = client.recv(1024)
                self.broadcast(message)
            except:
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                nickname = self.nicknames[index]
                self.broadcast(f'{nickname} left the chat!'.encode('utf-8'))
                self.nicknames.remove(nickname)
                break
    
    def start(self):
        while True:
            client, address = self.server.accept()
            print(f"Connected with {str(address)}")
            
            client.send('NICK'.encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')
            self.nicknames.append(nickname)
            self.clients.append(client)
            
            print(f'Nickname of the client is {nickname}!')
            self.broadcast(f'{nickname} joined the chat!'.encode('utf-8'))
            client.send('Connected to the server!'.encode('utf-8'))
            
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.daemon = True
            thread.start()

if __name__ == "__main__":
    server = ChatServer()
    server.start()
