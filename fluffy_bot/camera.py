import motorcortex
import time
import mcx_tracking_cam_pb2 as tracking_cam_msg
import cv2
import os
from math import cos, sin, sqrt
import numpy as np

class tc3_node(Node):
    def __init__(self):
        super().__init__('tc3_node')
        self.ip = '192.168.42.1'
        print("ss")
        
        parameter_tree = motorcortex.ParameterTree()
        # Loading protobuf types and hashes
        motorcortex_types = motorcortex.MessageTypes()
        # Open request connection
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.req, self.sub = motorcortex.connect("ws://"+self.ip+":5558:5557", motorcortex_types, parameter_tree,
                                    certificate=dir_path+"/motorcortex.crt", timeout_ms=1000,
                                    login="root", password="vectioneer")
        
        self.face_cascade = cv2.CascadeClassifier('/home/rodion/PROJECTS/robot_grisha/face_recognition/src/haarcascade_frontalface_default.xml')
        
        self.subscription6 = self.sub.subscribe(["root/Comm_task/utilization_max","root/Processing/image"], "camera", 1)
        self.subscription6.get()
        self.subscription6.notify(self.onImage)
    
    def onLog(self,val):
        print(val[0].value)
    def onError(self,val):
        try:
            errors = motorcortex.ErrorList()
            if errors.ParseFromString(val[0].value):
                print(errors)
        except Exception as e:
            print(e)
    def onImage(self,val):
        frame = cv2.imdecode(np.frombuffer(val[1].value, np.uint8), -1)
        small_frame = cv2.resize(frame, (640,int(640*(frame.shape[0]/frame.shape[1]))), interpolation = cv2.INTER_AREA)
        gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        for fx, fy, fw, fh in faces:
            face_gray = gray[fy:fy+fh, fx:fx+fw]
            # cv2.imshow('face', face_gray)
            cv2.rectangle(small_frame, (fx, fy), (fx+fw, fy+fh), (255, 0, 0), 2)
            mouth = self.mouth_cascade.detectMultiScale(face_gray)
            for mx, my, mw, mh in mouth:
                if fh*0.55 < my+mh/2 < fh*0.85 and fw*0.35 < mx+mw/2 < fw*0.65:
                    # mouth_gray = face_gray[my:my+mh, mx:mx+mw]
                    self.new_mw = int(fw*0.5)
                    self.new_mh = int(self.new_mw*0.6)
                    mx = mx + int(mw*0.5) - int(self.new_mw*0.5)
                    my = my + int(mh*0.4) - int(self.new_mh*0.5)
                    mw = self.new_mw
                    mh = self.new_mh
                    cv2.rectangle(face_gray, (mx, my), (mx+mw, my+mh), (255, 255, 0), 2)
                    cv2.imshow('face', face_gray)
                    break
        # cv2.imshow("img", small_frame)
def main():
    node = tc3_node()

if __name__ == '__main__':
    main()