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


X, Y, Z = [], [], []

def handle_plot(queue):
    # plot
    frame_delay = 200           # Delay of plot update in milliseconds

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Depth')

    def update(frame):
        global X, Y, Z
        
        try:
            data = queue.get(False)
            X = [coord[0] for coord in data] if data != None  else X
            Y = [coord[1] for coord in data] if data != None  else Y
            Z = [coord[2] for coord in data] if data != None  else Z
        except queues.Empty:
            pass
        
        ax.clear()

        colors = np.random.uniform(15, 80, len(X))

        ax.scatter(X, Y, Z, c=colors, cmap='viridis', marker='.')

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

    print("Serveur en attente de connexion pour la camera 3D...")
    client_socket, addr = server_socket.accept()
    print(f"Connecté à : {addr}")


    # Ouvrir un fichier CSV pour enregistrer les données
    filename = os.path.join(dirname, "../data/camera_3d/camera_data.csv")
    with open(filename, mode="w", newline="") as camera_file:
        camera_writer = csv.writer(camera_file)

    
        header = ["Timestamp", "coordinates"]
        camera_writer.writerow(header)

        while True:
            try:
                json_data = recv_msg(client_socket)
                data = json.loads(json_data)
                
                if not data:
                    break  # Arrêt si la connexion est fermée

                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

                queue.put(data, False) # Ajoute les données à la queue

                camera_writer.writerow([timestamp] + data)
                
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
