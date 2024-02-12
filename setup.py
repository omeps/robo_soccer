from dynamixel_sdk import *
DEVICENAME                  = '/dev/ttyUSB0' 
PROTOCOL_VERSION            = 2.0
ADDR_TORQUE_ENABLE          = 64
ADDR_GOAL_VELOCITY          = 104
ADDR_PRESENT_POSITION       = 132
OPERATING_MODE              = 11 
portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)
assert portHandler.openPort()
assert portHandler.setBaudRate(57600)
