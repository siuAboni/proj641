import time
import csv
import socket

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
        print('loaded !!')

    def onLoad(self):
        """Initialisation des proxys pour ALMemory et activation du laser."""
        self.memory = ALProxy('ALMemory')
        self.sensors = ALProxy('ALSensors')
        print('loaded !!')

    def onUnload(self):
        """Désactive le laser lorsqu'on quitte la boîte."""
        self.sensors.unsubscribe("myApplication")

    def onInput_onStart(self):
        """Démarre la collecte et l'envoi des données laser vers un serveur."""

        SERVER_IP = "193.48.125.70"
        SERVER_PORT = 9558
    
        self.sensors.subscribe("myApplication")
        self.running = True

        # Connexion au serveur
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((SERVER_IP, SERVER_PORT))
            print("Connexion réussie !")
        except Exception as e:
            print("Erreur de connexion : {0}".format(e))
            return
        else:
            while self.running:
                front_laser_values = []
                left_laser_values = []
                right_laser_values = []
                for i in range(1,16):
                    segnum = "0" + str(i) if i<10 else str(i)
                    xf = self.memory.getData("Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg" + segnum + "/X/Sensor/Value")
                    yf = self.memory.getData("Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg" + segnum + "/Y/Sensor/Value")

                    xl = self.memory.getData("Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg" + segnum + "/X/Sensor/Value")
                    yl = self.memory.getData("Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg" + segnum + "/Y/Sensor/Value")

                    xr = self.memory.getData("Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg" + segnum + "/X/Sensor/Value")
                    yr = self.memory.getData("Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg" + segnum + "/Y/Sensor/Value")

                    front_laser_values.append(xf)
                    front_laser_values.append(yf)

                    left_laser_values.append(xl)
                    left_laser_values.append(yl)

                    right_laser_values.append(xr)
                    right_laser_values.append(yr)
                #laser_values = self.memory.getData("Device/Laser/Value")
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

                # Formatage des données sous forme de chaîne CSV
                message_front = "front, {0},".format(timestamp) + ",".join(map(str, front_laser_values))
                sock.sendall(message_front.encode())

                message_left = "left, {0},".format(timestamp) + ",".join(map(str, left_laser_values))
                sock.sendall(message_left.encode())

                message_right = "right, {0},".format(timestamp) + ",".join(map(str, right_laser_values))
                sock.sendall(message_right.encode())

                #self.bang(laser_values)
                time.sleep(1)

            sock.close()
            self.onStopped()

    def onInput_onStop(self):
        """Arrête la collecte des données et se déconnecte proprement."""
        self.running = False
        self.onUnload()
        self.onStopped()