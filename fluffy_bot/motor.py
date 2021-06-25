from numpy.lib.npyio import loads
import pypot.dynamixel as pd

class Motors():
    def __init__(self):
        ports = pd.get_available_ports()
        self.dxl_io = pd.DxlIO(ports[0])
        self.ids = self.dxl_io.scan([1, 2, 3, 4, 5])
        print(self.ids)
        self.dxl_io.set_joint_mode(self.ids)
        print(self.dxl_io.get_present_position(self.ids))
        self.dxl_io.set_goal_position(dict(zip(self.ids,[0,0,0,0,180])))
        self.dxl_io.set_compliance_slope(dict(zip(self.ids,[[200,200],[200,200],[200,200]])))
        self.limit = 150
        self.angle_constant = 57
        self.dxl_io.set_angle_limit(dict(zip(self.ids, 
        [[-self.limit,self.limit],
        [-self.limit,self.limit],
        [-self.limit,self.limit]])))
        print("initalized")

    def set_slope(self, slope):
        self.dxl_io.set_compliance_slope(dict(zip(self.ids,[
        [slope[0],slope[0]],[slope[0],slope[0]]])))

    def set_speed(self, speed):
        self.dxl_io.set_moving_speed(dict(zip(self.ids,speed)))

    def set_position(self, pos):
        self.dxl_io.set_goal_position(dict(zip(self.ids,pos)))
        
    def get_positions(self):
        return self.dxl_io.get_present_position(self.ids)
   

