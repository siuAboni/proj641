import socket
import sys
import os

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
        self.resolutionMap = {
            '160 x 120': 0,
            '320 x 240': 1,
            '640 x 480': 2
        }
        self.cameraMap = {
            'Top': 0,
            'Bottom': 1
        }
        self.recordFolder = "/home/nao/recordings/cameras/"
        self.fileName = "test_video"

    def onLoad(self):
        #~ puts code for box initialization here
        try:
            self.videoRecorder = ALProxy("ALVideoRecorder")
        except Exception as e:
            self.videoRecorder = None
            self.logger.error(e)


    def onUnload(self):
        #~ puts code for box cleanup here
        if( self.videoRecorder and self.videoRecorder.isRecording() ):
            self.videoRecorder.stopRecording()
            SERVER_IP = "193.48.125.70"
            SERVER_PORT = 9558
            filePath = self.recordFolder + self.fileName + '.avi'
            filesize = os.path.getsize(filePath)

            # Connexion au serveur
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((SERVER_IP, SERVER_PORT))
                print("Connexion au serveur réussie !")
                #envoi du fichier
                f = open (filePath, "rb")
                l = f.read(1024)
                while (l):
                    sock.send(l)
                    l = f.read(1024)
                sock.close()

            except Exception as e:
                print("Erreur de connexion : {0}".format(e))
                return

    def onInput_onStart(self):

        resolutionValue = self.resolutionMap['320 x 240']
        cameraID = self.cameraMap['Top']
        formatValue = str('MJPG')
        frameRateValue = 10
        #fileName = self.getParameter("File name")
        if self.videoRecorder:
            self.videoRecorder.setResolution(resolutionValue)
            self.videoRecorder.setCameraID(cameraID)
            self.videoRecorder.setVideoFormat(formatValue)
            self.videoRecorder.setFrameRate(frameRateValue)
            self.videoRecorder.startRecording(self.recordFolder, self.fileName)

    def onInput_onStop(self):
        self.onUnload()
        self.onStopped()