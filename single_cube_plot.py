import matplotlib.pyplot as plt
import numpy as np
import math
import collections

Point = collections.namedtuple("Point", ["x", "y"])

def flat_hex_corner(center, size, i):
    angle_deg = 60 * i
    angle_rad = math.pi / 180 * angle_deg
    return Point(center.x + size * math.cos(angle_rad),
                 center.y + size * math.sin(angle_rad))

my_center_point = Point(0,0)
my_corner_list = []
size = 1
for i in range(6):
    my_corner_list.append(flat_hex_corner(my_center_point,1,i))
    
my_corner_list_x = []
my_corner_list_y = []
for i in my_corner_list:
    my_corner_list_x.append(i.x)
    my_corner_list_y.append(i.y)
    
plt.figure(figsize=(5,5))
plt.plot(my_corner_list_x,my_corner_list_y,'*')
plt.plot(my_corner_list_x+[my_corner_list_x[0]],my_corner_list_y+[my_corner_list_y[0]])
plt.show()