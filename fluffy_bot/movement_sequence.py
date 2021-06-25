from fluffy_bot.motor_control import MotorControl
import json
import pathlib
import os
from threading import Thread
from time import sleep
import glob
import os

class NewMovement():
    def __init__(self):
        self.sequence = None
        self.num_of_moves = None
        dir_path_full = str(pathlib.Path(__file__).parent.absolute())
        self.emotions_dir_path = os.path.join(dir_path_full, "emotions")
        print(self.emotions_dir_path)
        self.control = MotorControl()
        self.x = Thread(target = self.control.control, args = ())
        self.x.start()
    
    def add_new(self, name):
        self.sequence = {"emotion": name, "frame_list": []}
        self.num_of_moves = 0
        
    def add_state(self, pose, vel, slope, delay):
        frame = {"num": self.num_of_moves,
        "pos": pose,
        "vel": vel,
        "slope": slope,
        "delay": delay}
        self.num_of_moves+=1
        self.sequence['frame_list'].append(frame)        
   
    def save_move(self):
        with open(self.emotions_dir_path + "/"+self.sequence["emotion"]+'.json', 'w') as outfile:
            json.dump(self.sequence, outfile, sort_keys=True, indent=2)
   
    def play_current(self):
        a = 1
   
    def play_previous(self):
        self.control.position = self.sequence['frame_list'][self.num_of_moves]['pos']
        self.control.speed = self.sequence['frame_list'][self.num_of_moves]['vel']
        self.control.slope = self.sequence['frame_list'][self.num_of_moves]['slope']
        self.control.new_pose = True
   
    def play_emotion(self, emotion):
        self.control.emotion = emotion
        self.control.new_emotion = True

    def get_all_motion_name(self):
        files = glob.glob(self.emotions_dir_path+"/*.json")

        for i, el in enumerate(files):
            files[i] = os.path.basename(el)
            files[i] = files[i].replace('.json','')
        
        return files
    
    def stop_emotion(self):
        self.control.new_emotion = False

if __name__ == '__main__': 
    m = NewMovement()
    m.play_emotion("yes")
    print("done")
    sleep(1)
    m.play_emotion("anger")
    print("done")

