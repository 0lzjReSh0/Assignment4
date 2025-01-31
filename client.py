import socket
import threading
import random

ports = [8001, 8002, 8003]

def receive_messages(client):
    # while loop to continue receiving messages from server
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message:
                print(f"\n{message}")
        # show the reason why disconnection 
        except Exception as e:
            print("The connection has been stopped by:", str(e))
            client.close()
            break

def start_client():
    nickName = ''
    #randomly choose am available port
    initial_port = random.choice(ports)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', initial_port))
    

    while not nickName.strip():
        nickName = input("Enter your nickname: ")
        if not nickName.strip():
            print("Username cannot be empty!")
    client.send(nickName.encode('utf-8'))
    
    rooms_message = client.recv(1024).decode('utf-8')
    print(rooms_message)
    
    room_name = input("Select a chat room:")
    client.send(room_name.encode('utf-8'))

    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.start()
    
    print("Enter '#private' to request all user nicknames for the current chat room.")
    print("Enter 'Target nickname >> Content' to send a private chat.")
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
