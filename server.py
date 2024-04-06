import socket
import threading

clients = []  
chatrooms = {}

ports = [8001, 8002, 8003]

def execute_client(client_socket,port):
    
    nickname = client_socket.recv(1024).decode('utf-8')
    print(f"Handling client {nickname} on port {port}")
    available_rooms = ", ".join(chatrooms.keys())
    client_socket.send(f"Available Chat Room: {available_rooms}".encode('utf-8'))
    room_name = client_socket.recv(1024).decode('utf-8').strip()
    #avoid empty string as a room name
    if not room_name:
        raise Exception("Room name is required")
    
    current_room = room_name
    if current_room not in chatrooms:
        chatrooms[current_room] = []
        
    chatrooms[current_room].append((client_socket, nickname))
    #avoid repeat removing
    for client, _ in chatrooms[current_room]:
        if client != client_socket:
            client.send(f"{nickname} joined the chatroom.".encode('utf-8'))
    #handle client-side messages
    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                raise Exception("Client disconnected")
            #quit from chat room
            if message.startswith("#quit"):
                available_rooms = ", ".join(chatrooms.keys())
                client_socket.send(f"Available Chat Room: {available_rooms}".encode('utf-8'))
                new_room = client_socket.recv(1024).decode('utf-8').strip()
                

                if new_room.startswith("#exit"):
                    break
                if new_room in chatrooms:
                    if (client_socket, nickname) in chatrooms[current_room]:
                        chatrooms[current_room].remove((client_socket, nickname))
                        for client, _ in chatrooms[current_room]:
                            if client != client_socket:
                                client.send(f"{nickname} left the chatroom.".encode('utf-8'))
                        
                    
                    current_room = new_room
                    chatrooms[current_room].append((client_socket, nickname))
                    
                    for client, _ in chatrooms[current_room]:
                        if client != client_socket:
                            client.send(f"{nickname} joined the chatroom.".encode('utf-8')) 
                    
                #disconnect
                
                else:
                    client_socket.send("Invalid room.".encode('utf-8'))
            #private function
            if message.startswith("#private"):
                members = [n for _, n in chatrooms[current_room] if _ != client_socket]
                response_message = "Chat Room member: " + ", ".join(members) if members else "There is no member here."
                client_socket.send(response_message.encode('utf-8'))
            #rules of private chat
            if ">>" in message:
                target_nickname, private_message = message.split(">>", 1)
                target_nickname = target_nickname.strip()
                private_message = private_message.strip()

                for client, n in chatrooms[current_room]:
                    if n == target_nickname:
                        client.send(f"{nickname} (private): {private_message}".encode('utf-8'))
                        break
            else:
                #only send messages to current chat room members
                for client, _ in chatrooms[current_room]:
                    if client != client_socket:
                        try:
                            client.send(f"{nickname}: {message}".encode('utf-8'))
                        except Exception as e:
                            print(f"Error sending message to {client.getpeername()}: {e}")
                            chatrooms[current_room].remove((client, _))
                            client.close()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        #close socket
        client_socket.close()
        if (client_socket, nickname) in chatrooms[current_room]:
            chatrooms[current_room].remove((client_socket, nickname))
            for client, _ in chatrooms[current_room]:

                client.send(f"{nickname} has left the chatroom.".encode('utf-8'))
            

def multi_thread(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', port))
    server.listen()
    print(f"Server listening on port: {port}")

    while True:
        client_socket, addr = server.accept()
        print(f"Connection from {addr} on port {port}")
        thread = threading.Thread(target=execute_client, args=(client_socket, port))
        thread.start()

        
if __name__ == "__main__":
    #initial three empty chatrooms
    chatrooms["Room1"] = []
    chatrooms["Room2"] = []
    chatrooms["Room3"] = []
    # for loop listening on all available ports
    for port in ports:
        threading.Thread(target=multi_thread, args=(port,)).start()
