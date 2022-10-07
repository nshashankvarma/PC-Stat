import socket
import pickle
import psutil
import cv2
from matplotlib import pyplot as plt
import numpy as np

CLIENT_NAME = "Client 1"
CLIENT_ID = 1001
client = socket.socket()
PORT = 1112
a = 10

# client.connect((socket.gethostname(), PORT))
client.connect(('192.168.240.228', PORT))
res = client.recv(1024)
print(res)
client.send(bytes(str(CLIENT_ID), "utf-8"))
while True:
    # Saving stats in dictionary
    if(client.recv(1024).decode() == "START"):
        stats={}
        stats['client_name'] = CLIENT_NAME
        stats['client_id'] = CLIENT_ID
        stats['total_memory'] = str(round(psutil.virtual_memory().total/(1024*1024*1024), 2)) + "Gb"
        stats['used_memory'] = str(round(psutil.virtual_memory().used/(1024*1024*1024), 2)) + "Gb"
        stats['free_memory'] = str(round(psutil.virtual_memory().free/(1024*1024*1024), 2)) + "Gb"
        stats['percent_memory'] = psutil.virtual_memory().percent
        stats['total_disk'] = str(round(psutil.disk_usage('/').total/(1024*1024*1024), 2)) + "Gb"
        stats['used_disk'] = str(round(psutil.disk_usage('/').used/(1024*1024*1024), 2)) + "Gb"
        stats['free_disk'] = str(round(psutil.disk_usage('/').free/(1024*1024*1024), 2)) + "Gb"
        stats['percent_disk'] = psutil.disk_usage('/').percent
        stats['battery'] = psutil.sensors_battery().percent
        data = pickle.dumps(stats)
        data = bytes(f'{len(data):<{a}}', "utf-8") + data
        client.send(data)

        #Create graph of stats
        figure, axis = plt.subplots(1,3)

        # plt.pie(y, labels = mylabels)
        y = np.array([stats['battery'],100-stats['battery']])
        axis[0].pie(y, labels=['Battery', ''])
        y= np.array([stats['percent_memory'],100-stats['percent_memory']])
        axis[1].pie(y, labels = ["Memory", ""])
        y = np.array([stats['percent_disk'],100-stats['percent_disk']])
        axis[2].pie(y, labels = ["Disk Storage", ""])
        plt.savefig(str(CLIENT_ID) + '.jpg')
        # Send graph of stats
        file = open(str(CLIENT_ID)+'.jpg', 'rb')
        data = file.read(2048)
        while data:
            client.send(data)
            data = file.read(2048)
        file.close()
        # for i in file:
        #     client.send(i)
        
        # option="Sent"
        # client.send(option.encode(encoding="utf-8"))
        print("Sent graph of stats")
    else:
        pass
    # res = client.recv(1024)
    # if res.decode() == "Server connected successfully!":
    #     break
client.close()