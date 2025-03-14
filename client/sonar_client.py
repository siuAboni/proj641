import time
import csv
import socket

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)

    def onLoad(self):
        """Initializes sonar and memory proxies."""

        self.sonar = ALProxy('ALSonar')
        self.memory = ALProxy('ALMemory')

    def onUnload(self):
        """Stops sonar and unsubscribes from sonar events."""

        self.sonar.unsubscribe("myApplication")

    def onInput_onStart(self):
        """Subscribes to sonar events, retrieves sonar data, and signals completion."""
        SERVER_IP = "193.48.125.70"  # Remplace par l'IP de ton PC
        SERVER_PORT = 9558  # Même port que sur le serveur

        self.sonar.subscribe("myApplication")
        self.running = True

        # Connexion au serveur
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((SERVER_IP, SERVER_PORT))
            print("Connexion au serveur réussie !")
        except Exception as e:
            print("Erreur de connexion : {0}".format(e))
            return

        else:

            while(self.running):
                sonar_value = self.memory.getData("Device/SubDeviceList/Platform/Front/Sonar/RawData/Sensor/Value")
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

                message = "{0},{1}".format(timestamp, sonar_value)
                try:
                    sock.sendall(message.encode())  # Envoi des données
                except Exception as e:
                    print("Erreur d'envoi : {0}".format(e))
                    break

                self.bang(sonar_value)
                time.sleep(1)
        self.onStopped()

    def onInput_onStop(self):
        """Unsubscribes from sonar events and signals completion."""

        self.onUnload()
        self.onStopped()