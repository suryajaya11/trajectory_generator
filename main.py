import numpy as np
import math
import matplotlib.pyplot as plt
import copy
import time

t = [0]

class Axis():
    def __init__(self):
        self.x = 0.0
        self.y = 0.0

    def __add__(self, other):
        result = Axis()
        result.x = self.x + other.x
        result.y = self.y + other.y
        return result

    def __mul__(self, other):
        result = Axis()
        result.x = self.x * other
        result.y = self.y * other
        return result

    def __truediv__(self, other):
        result = Axis()
        result.x = self.x / other
        result.y = self.y / other
        return result
    
    def __sub__(self, other):
        result = Axis()
        result.x = self.x - other.x
        result.y = self.y - other.y
        return result
    
    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)
    
    def unit(self):
        return self / self.magnitude()
    
    def unit_self(self):
        resultant = self.magnitude()
        self.x /= resultant
        self.y /= resultant

class Point():
    def __init__(self):
        self.pos = Axis()
        self.vel = Axis()
        self.acc = Axis()

start = Point()
start.vel.x = 0
start.vel.y = -5

end = Point()
end.pos.y = 0
end.pos.x = 20

trajectory = []
trajectory.append(start)

max_vel = 10
max_acc = 7

time_step = 0.05
max_iter = 400

cur_iter = 0
pt_x = []
pt_y = []
vel_x = []
vel_y = []

while True:
    if(cur_iter > max_iter): break
    cur_iter += 1
    
    pt_x.append(trajectory[-1].pos.x)
    pt_y.append(trajectory[-1].pos.y)
    vel_x.append(trajectory[-1].vel.x)
    vel_y.append(trajectory[-1].vel.y)

    # calculate the direction that the robot should move (speed vector) 
    # calculate the difference between current robot velocity and the direction that the robot should be moving
    # if the previous velocity difference (acceleration) is more than the allowed max acceleration, use max accel. if not, leave it
    # use the new acceleration to calculate next point

    dir_of_travel = end.pos - trajectory[-1].pos
    dir_of_travel.unit_self()
    dir_of_travel *= max_vel

    # print(f"dir of travel:{dir_of_travel.x},{dir_of_travel.y}")

    acceleration_intended = dir_of_travel - trajectory[-1].vel
    
    acceleration_used = Axis()
    if(acceleration_intended.magnitude() > max_acc):
        acceleration_used = acceleration_intended.unit() * max_acc
    else: 
        if(trajectory[-1].vel.magnitude() < max_vel):
            acceleration_used = acceleration_intended.unit() * max_acc        
        else:
            acceleration_used = acceleration_intended

    # acceleration_used = acceleration_intended.unit() * max_acc

    next_point = copy.deepcopy(trajectory[-1])
    next_point.acc = acceleration_used
    next_point.vel += trajectory[-1].acc * time_step
    next_point.pos += trajectory[-1].vel * time_step
    
    # if(next_point.vel.magnitude() > max_vel):
    #     next_point.vel = next_point.vel.unit() * max_vel
    
    trajectory.append(next_point)
    # print("vel:{0:0.2f},acc:{0:0.2f}".format(trajectory[-1].vel.magnitude(), trajectory[-1].acc.magnitude()))
    print(f"vel:{trajectory[-1].vel.magnitude():0.2f} acc:{trajectory[-1].acc.magnitude():0.2f}")
    if((end.pos - trajectory[-1].pos).magnitude() < 0.5): break

    t.append(t[-1] + time_step)

    plt.clf()
    plt.plot(start.pos.x,start.pos.y,'ro')
    plt.plot(end.pos.x,end.pos.y,'ro') 
    plt.plot(pt_x,pt_y, "bo-")
    # plt.quiver(pt_x, pt_y, vel_x, vel_y)
    plt.quiver(pt_x[-1], pt_y[-1], vel_x[-1], vel_y[-1])
    plt.grid()

    plt.xlim(-10, 25)
    plt.ylim(-10, 10)
    plt.draw()
    plt.pause(time_step)
    # plt.show()

    # time.sleep(time_step)

plt.show()