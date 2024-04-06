import socket
import threading
import random

ports = [8001, 8002, 8003]

def receive_messages(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message:
                print(f"\n{message}")
        except Exception as e:
            print("The connection has been stopped by:", str(e))
            client.close()
            break

def start_client():
    nickname = ''
    initial_port = random.choice(ports)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', initial_port))
    

    while not nickname.strip():
        nickname = input("Enter your username: ")
        if not nickname.strip():
            print("Username cannot be empty!")
    client.send(nickname.encode('utf-8'))
    
    rooms_message = client.recv(1024).decode('utf-8')
    print(rooms_message)
    
    room_name = input("Select a chat room:")
    client.send(room_name.encode('utf-8'))

    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.start()
    
    print("Enter '#private' to request all user nicknames for the current chat room.")
    print("Enter 'Target nickname >> Message' to send a private chat message.")
    print("Type '#quit' to leave the current chat room.")
    print("Type '#exit' to exit the system.\n")
    
    while True:
        message = input('')
        if message.lower() == '#exit':
            client.send(message.encode('utf-8'))
            break
        elif message.lower() == '#quit':
            client.send(message.encode('utf-8'))
            # rooms_message = client.recv(1024).decode('utf-8')
            # print(rooms_message)

            
        else:
            client.send(message.encode('utf-8'))

    client.close()

if __name__ == "__main__":
    start_client()
