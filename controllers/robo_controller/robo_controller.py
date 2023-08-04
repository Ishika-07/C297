from controller import Robot, DistanceSensor
import math, random

robot = Robot()
timestep = int(robot.getBasicTimeStep())
movement = 0
robot_orientation = random.randint(0, 360)
reached_end = 0

left_motor = robot.getDevice("left wheel motor")
right_motor = robot.getDevice("right wheel motor")

left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))

left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)

ds_front = robot.getDevice("ds_front")
ds_left = robot.getDevice("ds_left")
ds_right = robot.getDevice("ds_right")

ds_front.enable(timestep)
ds_left.enable(timestep)
ds_right.enable(timestep)

imu = robot.getDevice("inertial unit")
imu.enable(timestep)

def move(left_speed, right_speed):
    left_motor.setVelocity(left_speed)
    right_motor.setVelocity(right_speed)

def turn_towards_angle(target_angle, movement):
    if target_angle != yaw_current:
        move(-5,5)
    else:
        move(0,0)
        movement += 1
        
    return movement


def move_forward_till_wall_detection(movement):
    if ds_front_value > 300:
        move(15,15)
    else:
        movement += 1
        
    return movement
    

def find_corner(movement):
    if(movement == 0):
        movement = turn_towards_angle(robot_orientation%360, movement)
    
    if(movement == 1):
        movement = move_forward_till_wall_detection(movement)
    
    if(movement == 2):
        movement = turn_towards_angle((robot_orientation-90)%360,movement)
        
    if(movement == 3):
        movement = move_forward_till_wall_detection(movement)
     
    if(movement == 4):
       movement = turn_towards_angle((robot_orientation-180)%360,movement)
       
    return movement
 
 
def back_and_forth_movement(movement):
    if(movement == 5):
        movement = move_forward_till_wall_detection(movement)
        
    if(movement == 6):
        movement = turn_towards_angle((robot_orientation+90)%360,movement)
      
    if(movement == 7):
        if(robot_orientation%360 != yaw_current):
            move(3,1)
        else:
            movement+=1
            
    if(movement == 8):
         movement = move_forward_till_wall_detection(movement)
      
    if(movement == 9):
         movement = turn_towards_angle((robot_orientation+90)%360, movement)
         
    if(movement == 10):
        if((robot_orientation-180)%360 != yaw_current):
            move(1,3)
        else:
            move(0,0)
            movement = 5
             
    return movement               


while robot.step(timestep) != -1:
    
    angle = imu.getRollPitchYaw()
    #print(angle)
    
    yaw_current = round(math.degrees(angle[2])) + 180
    #print(yaw_current)
    
    ds_front_value = ds_front.getValue()
    ds_left_value = ds_left.getValue()
    ds_right_value = ds_right.getValue()
    
    #move_forward_till_wall_detection()
    
    movement = find_corner(movement)
    movement = back_and_forth_movement(movement)
    
    if(reached_end == 0 and ds_front_value < 500 and ds_left_value < 1000 and (yaw_current == 180 or yaw_current == 270)):
          
        movement = 0
        robot_orientation = 270
        reached_end = 1
    
    if(ds_front_value<500 and ds_left_value < 500 and (yaw_current == 360 or yaw_current == 0) and reached_end == 1):
        reached_end = 2