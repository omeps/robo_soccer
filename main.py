from class_defs import Robot, Motor, Vec2
from setup import *
import time, random
pw = 0.5
bot = Robot([Motor(1,pw),Motor(2,pw),Motor(3,pw)])
bot.toggle_torque(False)
bot.toggle_torque(True)
for i in range(50):
    bot.motors[1].set_velocity(random.randint(-265,265))
    time.sleep(2)
bot.toggle_torque(False)
