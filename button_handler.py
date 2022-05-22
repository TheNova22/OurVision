from multiprocessing import Process
from observer import SubprocessObserver
from state import State
from paths import *
from models import *
from tts import tts, checkInternet,blurCheck
from time import sleep
from audio import play_audio
import cv2

class ButtonHandler:
    def __init__(self):
        self.state = State.DocOCR
        self.currProc = Process(target=self.perform_doc_ocr)
        self.observer = SubprocessObserver()
        
    def create(self, command):
        return self.observer.create(command)
    
        
    def perform_doc_ocr(self):
        # cmd = "libcamera-jpeg -o " + INPUT_IMAGE_PATH + " -t 1000 --width 2500 --height 2500"
        cmd = "fswebcam -d /dev/video0 -r 2500x2500 -v -S 10 --set brightness=100% --no-banner " + INPUT_IMAGE_PATH
        p = self.create(cmd)
        p.wait()
        # Creating a scan of the input image
        doc_scan.scan(INPUT_IMAGE_PATH, OUTPUT_IMAGE_PATH)

        string = doc_ocr.ocr(imagePath=OUTPUT_IMAGE_PATH)
            
        if(len(string) > 3):
            print(f"string = {string}")
            tts(string)
            self.create("sudo mpg321 ./audios/tts.mp3")
        else:
            print(f"No text detected")
            self.create("sudo mpg321 ./audios/noText.mp3")
    
    def perform_scene_ocr(self):        
        cmd = "fswebcam -d /dev/video0 -r 960x960 -v -S 10 --set brightness=100% --no-banner " + INPUT_IMAGE_PATH
        p = self.create(cmd)
        p.wait()
        string = scene_ocr.ocr()
        if(len(string) > 3):
            print(f"string = {string}")
            tts(string)
            self.create("sudo mpg321 ./audios/tts.mp3")
        else:
            print(f"No text detected")
            self.create("sudo mpg321 ./audios/noText.mp3")
    
    def perform_scene_desc(self):        
        cmd = "fswebcam -d /dev/video0 -r 960x960 -v -S 10 --set brightness=100% --no-banner " + INPUT_IMAGE_PATH
        p = self.create(cmd)
        p.wait()
        string = scene_desc.describe(cv.imread(INPUT_IMAGE_PATH))
        if(len(string) > 3):
            print(f"string = {string}")
            tts(string)
            self.create("sudo mpg321 ./audios/tts.mp3")
        else:
            print(f"No text detected")
            self.create("mpg321 ./audios/noText.mp3")

    def perform_cloud_ocr(self):
        
        
        if checkInternet():
            cmd = "fswebcam -d /dev/video0 -r 2500x2500 -v -S 10 --set brightness=100% --no-banner " + INPUT_IMAGE_PATH
            p = self.create(cmd)
            p.wait()
            #cap = cv2.VideoCapture(0)
            #cap.set(cv2.CAP_PROP_FRAME_WIDTH,2592)
            #cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1944)
            
            #ret, frame = cap.read()
            
            #img = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            
            #cv2.imwrite(INPUT_IMAGE_PATH,img)
            
            
            #img = cv2.imread(INPUT_IMAGE_PATH)
            
            #if blurCheck(img):
            #    self.create("sudo mpg321 ./audios/blurry.mp3")
                
            
            string = cloud_ocr.ocr(INPUT_IMAGE_PATH)
            if(len(string) > 3):
                print(f"string = {string}")
                tts(string)
                self.create("sudo mpg321 ./audios/tts.mp3")
            else:
                print(f"No text detected")
                self.create("sudo mpg321 ./audios/noText.mp3")
        else:
            self.create("sudo mpg321 ./audios/no-internet.mp3")

    def kill(self):
        self.observer.kill()
        
    def cycle(self):
        if self.currProc.is_alive() or self.observer.isAlive():
            return
        self.state = (self.state + 1) % State.Count
        State.play(self.state)
        
    def select(self):
        if self.currProc.is_alive() or self.observer.isAlive():
            return
        
        if self.state == State.DocOCR:
            self.currProc = Process(target=self.perform_doc_ocr)
        elif self.state == State.SceneOCR:
            self.currProc = Process(target=self.perform_scene_ocr)
        elif self.state == State.SceneDesc:
            self.currProc = Process(target=self.perform_scene_desc)
        elif self.state == State.CloudOCR:
            self.currProc = Process(target=self.perform_cloud_ocr)
            
        self.currProc.start()
    
    def cancel(self):
        self.kill()
        if self.currProc.is_alive():
            self.currProc.terminate()
