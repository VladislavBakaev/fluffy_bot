from numpy.lib.npyio import loads
import pypot.dynamixel as pd
from time import sleep
import pathlib
import json
from math import pi
from threading import Thread
from fluffy_bot.motor import Motors

class MotorControl(Motors):
    def __init__ (self):
        super().__init__()
        parent_dir = str(pathlib.Path(__file__).parent.absolute())
        self.emotion_dir = parent_dir + "/emotions/"
        self.stop_control = False
        self.new_pose = False
        self.new_emotion = False
        self.emotion = ''
        self.speed = [200,200,200,200,200]
        self.slope = [200,200,200,200,200]
        self.position = [0,0,0,0,180]

    def play_emotion(self, emotion):
        # json.loads(self.emotion_dir+emotion+".json")
        if isinstance(emotion, dict):
            data = emotion
        else:
            with open(self.emotion_dir+emotion+".json", "r") as read_file:
                data = json.load(read_file)
        
        for key in data["frame_list"]:
            if self.new_emotion == False: #checking for interruption with new emotion set
                pos = []
                for p in key["pos"]:
                    pos.append(int((pi-p)*self.angle_constant))
                self.set_slope(key["slope"])
                self.set_speed(key["vel"])
                self.set_position(pos)
                delta = [100]*len(self.ids)
                while (max(delta) > 10):
                    c_p = self.get_positions()
                    # print(c_p)
                    for i in range (len(self.ids)):
                        if abs(pos[i]) > self.limit:
                            pos[i] = self.limit
                        delta[i] = abs(pos[i]- c_p[i])
            # sleep(key["delay"])

    def control(self):
        while(self.stop_control == False):
            if self.new_emotion == True:
                self.new_emotion = False
                self.play_emotion(self.emotion)
            if self.new_pose == True:
                self.new_pose = False
                self.set_slope(self.slope)
                self.set_speed(self.speed)
                self.set_position(self.position)            
        
if __name__ == '__main__':
    con = MotorControl()
    # con.set_speed([100,100,100,100,900])
    # for i in range(0,10):    
        # con.set_position([0,0,0,0,180])
        # sleep(0.5)
        # con.set_position([0,0,0,0,0])
        # sleep(0.5)
    x = Thread(target = con.control, args = ())
    # x.start()
    con.play_emotion("fear")
    # con.get_all_motion_name()
    # con.stop_control = True
