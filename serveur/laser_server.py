import socket
import csv
import os
import time
import traceback

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import random
from multiprocessing import Process, Manager, Value, Array, Pipe, SimpleQueue, queues, Queue
import struct
import json


dirname = os.path.dirname(__file__)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

### StackOverflow
def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)

### StackOverflow
def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data


X, Y = [], []

def handle_plot(queue):
    # plot
    nb_point = 50               # Maximum number of point to output
    nb_point_added = []         # List of the number of point added at each plot update
    frame_delay = 200           # Delay of plot update in milliseconds
    point_persistency = 3000    # Delay of appearence of a point in milliseconds
    # nb_stages = int(point_persistency/frame_delay)      # Number of update per interval of point_persistency delay

    fig, ax = plt.subplots()
    fig.set_figheight(10)
    fig.set_figwidth(10)

    def update(frame):
        global X, Y
        
        c = 0
        while c < nb_point:
            try:
                data = queue.get(False)
                X.append(data[0])
                Y.append(data[1])
                c += 1
            except queues.Empty:
                break
        nb_point_added.append(c)
        if ((frame+1) * frame_delay >= point_persistency):
            c = nb_point_added.pop(0)
            X = X[c:]                   # remove the first c element from X
            Y = Y[c:]                   # remove the first c element from Y
        
        ax.clear()

        # Xc = X if len(X) <= nb_point else X[-nb_point:]
        # Yc = Y if len(Y) <= nb_point else Y[-nb_point:]

        sizes = np.random.uniform(15, 80, len(X))
        colors = np.random.uniform(15, 80, len(X))

        ax.scatter(X, Y, s=sizes, c=colors, vmin=0, vmax=100) # only output the last nb_point points

        ax.set(xlim=(0, 7), xticks=np.arange(1, 8),
        ylim=(-7, 5), yticks=np.arange(1, 8))

        ax.set_aspect('equal')
        ax.grid(True, which='both')

        ax.axhline(y=0, color='red')
        ax.axvline(x=0, color='blue')
        fig.canvas.draw()

    anim = FuncAnimation(fig, update, interval=frame_delay)
    plt.show()

def data_handler(queue):
    HOST = "0.0.0.0"  # Accepte les connexions de n'importe quelle adresse
    PORT = 9558      # Port d'écoute

    # Création du socket serveur
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)  # Attend une connexion

    print("Serveur en attente de connexion pour laser...")
    client_socket, addr = server_socket.accept()
    print(f"Connecté à : {addr}")


    # Ouvrir un fichier CSV pour enregistrer les données
    filename_front = os.path.join(dirname, "../data/laser/laser_data_front.csv")
    filename_left = os.path.join(dirname, "../data/laser/laser_data_left.csv")
    filename_right = os.path.join(dirname, "../data/laser/laser_data_right.csv")
    with open(filename_front, mode="w", newline="") as file_front, open(filename_left, mode="w", newline="") as file_left, open(filename_right, mode="w", newline="") as file_right:
        front_writer = csv.writer(file_front)
        left_writer = csv.writer(file_left)
        right_writer = csv.writer(file_right)
        
        header = ["Timestamp"]
        for i in range(1,16):
            header.append(f"Seg0{i}X")
            header.append(f"Seg0{i}Y")
        front_writer.writerow(header)
        left_writer.writerow(header)
        right_writer.writerow(header)


        while True:
            try:
                # data = client_socket.recv(2048).decode()  # Réception des données
                json_data = recv_msg(client_socket)
                data = json.loads(json_data)
                
                if not data:
                    break  # Arrêt si la connexion est fermée

                #list = data.split(",")
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

                sorted_data = {
                    "front": [timestamp],
                    "left": [timestamp],
                    "right": [timestamp],
                }

                write_in = data[0]
                for elt in data:
                    if isinstance(elt, str):
                        write_in = elt
                    else:
                        sorted_data[write_in].append(elt)
                        queue.put(elt, False)
                
                front_writer.writerow(sorted_data["front"])
                left_writer.writerow(sorted_data["left"])
                right_writer.writerow(sorted_data["right"])
                #print(sorted_data)
                
            except Exception as e:
                print(f"Une erreur est survenue : {e}")
                print(traceback.format_exc())
                break

    client_socket.close()
    server_socket.close()
    print("Connexion fermée.")


if __name__ == '__main__':
    # shared pipe
    queue = Queue()

    # processes
    p1 = Process(target=data_handler, args=(queue,))
    p2 = Process(target=handle_plot, args=(queue,))
    p1.start()
    p2.start()
    p2.join()
    p1.join()
