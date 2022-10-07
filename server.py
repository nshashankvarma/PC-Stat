import socket
from _thread import *
import pickle
from datetime import datetime

PORT = 1112
threadCount = 0
a = 10
clients = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((socket.gethostname(), PORT))
server.listen(5)
def new_thread(client):
    client.send(b'Server connected successfully!')
    while 1:
        complete_data = b''
        rcv_data = True
        print("Waiting for data...")
        while 1:
            #print("Recieveing Data...")
            data = client.recv(16)
            if rcv_data:
                x = int(data[:a])
                rcv_data = False
            complete_data += data
            if len(complete_data) - a == x:
                obj = pickle.loads(complete_data[a:])
                print(obj)
                file = open(obj['client_name']+str(datetime.now().strftime("%H %M %S"))+'.jpg', 'wb')
                # data = client.recv(2048)
                # while data:
                #     file.write(data)
                #     data = client.recv(2048)                    
                # file.close(
                cond = True
                while cond:
                    file = client.recv(1024)
                    if(str(file)==b''):
                        cond = False
                rcv_data = True
                complete_data = b''
                print("rec")
                break 
        
    client.close()

def listenToClients():
    print("Listening to clients...\n")
    while 1:
        client, addr = server.accept()
        start_new_thread(new_thread, (client,))        
        cl_id = client.recv(1024)
        clients.append((client, cl_id.decode()))
        print(client)
        # threadCount += 1

start_new_thread(listenToClients, ())
while 1:
    command = input()
    if command == 'exit':
        server.close()
        exit()
    else:
        requested_client = [client for client in clients if client[-1] == command]
        if requested_client:
            # print(requested_client[0][0])
            requested_client[0][0].send(b'START')
            print("Request Sent!")
# while True:
#     client, address = server.accept()
#     print("Connected to: ", str(address))

#     # start_new_thread(new_thread, (client,))
#     client_id = int(input("Enter id: "))
#     client_id = 1001
#     requested_client = [client for client in clients if client[1] == str(client_id)]
#     print(requested_client)
#     if requested_client:
#         start_new_thread(new_thread, (requested_client[0],))
#     threadCount += 1
# server.close()

# start_new_thread(listenToInput, ())
