import numpy as np
import matplotlib.pyplot as plt
import copy
import time

from point import Axis, Point

start = Point()
start.vel.x = 2
start.vel.y = -5

end = Point()
end.pos.y = 0
end.pos.x = 30

trajectory = []
trajectory.append(start)

max_vel = 8
max_acc = 3
end_vel = 0.5

time_step = 0.05
max_iter = 400

cur_iter = 0
pt_x = []
pt_y = []
vel_x = []
vel_y = []
acc_x = []
acc_y = []

while True:
    if(cur_iter > max_iter): break
    cur_iter += 1
    
    pt_x.append(trajectory[-1].pos.x)
    pt_y.append(trajectory[-1].pos.y)
    vel_x.append(trajectory[-1].vel.x)
    vel_y.append(trajectory[-1].vel.y)
    acc_x.append(trajectory[-1].acc.x)
    acc_y.append(trajectory[-1].acc.y)

    ## intial change of speed with constant acceleration
    # calculate the direction that the robot should move (speed vector) 
    # calculate the difference between current robot velocity and the direction that the robot should be moving
    # if the previous velocity difference (acceleration) is more than the allowed max acceleration, use max accel. if not, leave it
    # use the new acceleration to calculate next point

    ## deceleration to destination point
    # calculate the distance needed to safely decelerate with current speed and the set deceleration value
    # if current point is within that distance, start decelerating

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

    decelerating = False
    # v_final^2 = v_initial^2 + 2 * deceleration * distance
    distance_needed_to_decelerate = (end_vel**2 - trajectory[-1].vel.magnitude()**2) / (2 * -max_acc)
    distance_to_destination = (end.pos - trajectory[-1].pos).magnitude()

    print(f"dist_decel:{distance_needed_to_decelerate:.2f}, dist_to_dest:{distance_to_destination:.2f}", end=" ")
    if(distance_to_destination < distance_needed_to_decelerate):
        decelerating = True
        print("we should be decelerating right now")

    next_point = copy.deepcopy(trajectory[-1])
    next_point.acc = acceleration_used
    
    if(decelerating):
        next_point.acc = dir_of_travel.unit() * -max_acc
        if(trajectory[-1].vel.magnitude() < end_vel):
            next_point.vel = dir_of_travel.acc.unit() * end_vel
        else:
            next_point.vel += trajectory[-1].acc * time_step
        next_point.pos += trajectory[-1].vel * time_step

        # if(next_point.vel.magnitude() <= end_vel):
        #     next_point.acc.zero_self()
        #     next_point.vel = next_point.acc.unit() * end_vel
        # else: 
        #     next_point.acc = next_point.acc.unit() * -max_acc

            
    # this part is used to maximize speed when not accelerating close the limit
    else:
        next_point.vel += trajectory[-1].acc * time_step
        next_point.pos += trajectory[-1].vel * time_step

        if(next_point.vel.magnitude() > max_vel):
            next_point.vel = next_point.vel.unit() * max_vel
    
    trajectory.append(next_point)
    # print("vel:{0:0.2f},acc:{0:0.2f}".format(trajectory[-1].vel.magnitude(), trajectory[-1].acc.magnitude()))
    print(f"vel:{trajectory[-1].vel.magnitude():0.2f} acc:{trajectory[-1].acc.magnitude():0.2f}")
    if((end.pos - trajectory[-1].pos).magnitude() < 0.5): break

    plt.clf()
    plt.plot(start.pos.x,start.pos.y,'ro')
    plt.plot(end.pos.x,end.pos.y,'ro') 
    plt.plot(pt_x,pt_y, "bo-")
    # plt.quiver(pt_x, pt_y, vel_x, vel_y)
    plt.quiver(pt_x[-1], pt_y[-1], vel_x[-1], vel_y[-1], color="black")
    plt.quiver(pt_x[-1], pt_y[-1], acc_x[-1], acc_y[-1], color="red")
    plt.grid()

    plt.xlim(-10, 35)
    plt.ylim(-10, 10)
    plt.draw()
    plt.pause(time_step * 0.1)
    # plt.show()

    # time.sleep(time_step)

plt.show()