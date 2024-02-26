import math
from dynamixel_sdk import *
from setup import *
class Vec2:
    def __init__( self, x: float , y: float ):
        self.x = x
        self.y = y
    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)
    def size(self):
        return math.sqrt(self * self)
    def __mul__(self, const):
        if type(self) == type(const):
            return self.x*const.x+self.y*const.y
        return Vec2(self.x*const,self.y*const)
    def __truediv__(self, other):
        return Vec2(self.x/other,self.y/other)
def cos(vec: Vec2, onto: Vec2):
    return ( ( vec * onto ) / onto.size() / vec.size() )
def sin(vec: Vec2, onto: Vec2):
    vec = vec / vec.size()
    onto = onto / onto.size()
    return vec.x * onto.y - vec.y * onto.x
class Motor:
    def __init__(self, ID: int, pw: float):
        self.ID = ID
        self.pow = pw
    def toggle_torque(self, to_on: bool): 
        if to_on: packetHandler.write1ByteTxRx(portHandler, self.ID, OPERATING_MODE, 1)
        packetHandler.write1ByteTxRx(portHandler, self.ID, ADDR_TORQUE_ENABLE, to_on)
    def set_velocity(self, val): 
        print(f"set velocity of motor ID {self.ID} to {val}")
        packetHandler.write4ByteTxRx(portHandler, self.ID, ADDR_GOAL_VELOCITY, int(val*self.pow))

class Robot:
    def __init__(self, motors: list[Motor] ):
        self.motors = motors
        self.dirs = [Vec2(-math.sqrt(3)/2,-1/2), Vec2(0,1), Vec2(math.sqrt(3)/2,-1/2)]
    def toggle_torque(self, to_on: bool):
        for motor in self.motors:
            motor.toggle_torque(to_on) 
    def move_in_direction(self, direction: Vec2):
        vels = [cos(d,direction) for d in self.dirs]
        largest_vel = abs(max(vels, key = lambda x: abs(x)))
        vels = [265*vel/largest_vel for vel in vels]
        for i in range(len(self.motors)):
            self.motors[i].set_velocity(vels[i])
        return sum([vel*vel for vel in vels])
    def turn(self, velocity: float):
        for i in range(len(self.motors)):
            self.motors[i].set_velocity(velocity)
    def set_velocity(self, val):
        for m in self.motors:
            m.set_velocity(val)
    def move_and_turn(self, direction: Vec2, rotation: float):
        vels = [cos(d,direction) for d in self.dirs]
        vel_size = sum([vel*vel for vel in vels])
        tot = [vels[i]/vel_size + rotation/265 for i in range(len(vels))]
        largest = abs(max(tot, key = lambda x: abs(x)))
        packetHandler = PacketHandler(PROTOCOL_VERSION)
        [self.motors[i].set_velocity(265*tot[i]/largest) for i in range(len(vels))]
        return largest/abs(rotation)*265*3.12
def test():
    motors = [Motor(2),Motor(3)]
    for m in motors:
        m.toggle_torque(0)
    for m in motors:
        m.toggle_torque(1)
        m.set_velocity(265)
    time.sleep(10)
    for m in motors:
        m.toggle_torque(0)
