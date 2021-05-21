import matplotlib.pyplot as plt
import numpy as np
import math

def doubleheight_to_cube(hexagon):
    x = hexagon.col
    z = (hexagon.row - hexagon.col) / 2
    y = -x-z
    return cube_hex(x, y, z)

def cube_to_doubleheight(cube):
    col = cube.x
    row = 2 * cube.z + cube.x
    return doubled_height_hex(col, row)

def flat_hex_to_pixel(hex):
    x = size *  3./2 * hex.dx
    y = (size * (sqrt(3)/2 * hex.dx  +  sqrt(3) * hex.dz))
    return Point(x, y)

def pixel_to_flat_hex(point):
    q = ( 2/3 * point.x) / size
    r = (-1/3 * point.x + sqrt(3)/3 * point.y) / size
    return cube_hex_round(point3(q, r))

class point():
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def __add__(self, r):
        return point(self.x+r.x,self.y+r.y)

    def __sub__(self, r):
        return point(self.x-r.x,self.y-r.y)
    
    def __repr__(self):
        return 'point({},{})'.format(self.x,self.y)

class point3():
    # class cube_hex 中有断言，则经过cube_hex_round转化之前的（x,y,z)使用point3临时保存。
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
    def __repr__(self):
        return 'point3({},{},{})'.format(self.x,self.y,self.z)
    
class cube_hex:
    # 初始化size = 1
    def __init__(self,dx,dy,dz,size = 1):
        self.dx = dx
        self.dy = dy  
        self.dz = dz
        self.size = size
        if dx+dy+dz != 0:
            raise Exception('六边形索引错误')
        
    def center(self):
        x = self.size*3/2*self.dx
        y = (math.sqrt(3)/2*self.dx+ math.sqrt(3)*self.dz)
        return point(x,y)
    
    def __str__(self):
        return "cube_hex({},{},{},[{}])".format(self.dx,self.dy,self.dz,self.size)
    def __repr__(self):
        return "cube_hex({},{},{},[{}])".format(self.dx,self.dy,self.dz,self.size)

def cube_hex_add(a,b):
    return cube_hex(a.dx+b.dx,a.dy+b.dy,a.dz+b.dz)

cube_hex_directions =  [
    cube_hex(+1, -1, 0), cube_hex(+1, 0, -1), cube_hex(0, +1, -1), 
    cube_hex(-1, +1, 0), cube_hex(-1, 0, +1), cube_hex(0, -1, +1), 
]

def cube_hex_direction(direction):
    return cube_hex_directions[direction]

def cube_hex_neighbor(a_cub_hex, direction):
    return cube_hex_add(a_cub_hex, cube_hex_direction(direction))

def cube_distance(a,b):
    return max(abs(a.dx - b.dx), abs(a.dy - b.dy), abs(a.dz - b.dz))

def flat_hex_corner(center,size,i):
    angle_deg = 60 * i
    angle_rad = math.pi / 180 * angle_deg
    return point(center.x + size * math.cos(angle_rad),
                 center.y + size * math.sin(angle_rad))

def draw_hex(a_cub_hex,line_color = 'black',fill_color = False):
    center = a_cub_hex.center()
    size = a_cub_hex.size
    
    corner_list_x = []
    corner_list_y = []

    for i in range(6):
        corner_list_x.append(flat_hex_corner(center,size,i).x)
        corner_list_y.append(flat_hex_corner(center,size,i).y)
    
    #plt.plot(corner_list_x,corner_list_y,'*',c = 'red')
    plt.plot(corner_list_x+[corner_list_x[0]],corner_list_y+[corner_list_y[0]],c = line_color)
    if fill_color != False:
        plt.fill(corner_list_x+[corner_list_x[0]],corner_list_y+[corner_list_y[0]],c = fill_color)
    plt.xticks([])
    plt.yticks([])

def draw_map(cube_hex_list,line_color = 'black',fill_color = False, is_arrow = False):
    for i in cube_hex_list:
        draw_hex(i,line_color,fill_color)
    if is_arrow:
        for i in range(len(cube_hex_list)-1):
            x = cube_hex_list[i].center().x
            y = cube_hex_list[i].center().y
            dx = cube_hex_list[i+1].center().x - x
            dy = cube_hex_list[i+1].center().y - y
            plt.arrow(x,y,dx,dy,shape = 'full',width = 0.1,head_width = 0.5,length_includes_head = True,head_length = 0.7,ls ='-')
            
def cube_hex_range(center_hex,radius):
    results = []
    for x in range(-radius,radius+1): # -r <= x <= r
        for y in range(max(-radius, -x-radius),min(+radius, -x+radius)+1): # 由距离定义，得 y 
            z = -x-y
            results.append(cube_hex_add(center_hex, cube_hex(x, y, z)))
    return results

def cube_hex_scale(a, k):
    return cube_hex(a.dx * k, a.dy * k, a.dz * k)

def cube_hex_ring(center_hex, radius):
    results = []
    # this code doesn't work for radius == 0; can you see why?
    cube = cube_hex_add(center_hex, 
                        cube_hex_scale(cube_hex_direction(4), radius))
    for i in range(6):
        for j in range(radius):
            cube = cube_hex_neighbor(cube, i)
            results.append(cube)
    return results

def cube_spiral(center, radius):
    results = [center]
    for i in range(radius+1):
        results = results + cube_hex_ring(center, i)
    return results

def cube_hex_round(point3_hex):
    rx = round(point3_hex.x)
    ry = round(point3_hex.y)
    rz = round(point3_hex.z)

    x_diff = abs(rx - point3_hex.x)
    y_diff = abs(ry - point3_hex.y)
    z_diff = abs(rz - point3_hex.z)

    if x_diff > y_diff and x_diff > z_diff:
        rx = -ry-rz
    elif y_diff > z_diff:
        ry = -rx-rz
    else:
        rz = -rx-ry

    return cube_hex(rx, ry, rz)

def lerp(a, b, t): # for floats
    return a + (b - a) * t

def cube_lerp(a, b, t): # for hexes
    return point3(lerp(a.dx, b.dx, t), 
                    lerp(a.dy, b.dy, t),
                    lerp(a.dz, b.dz, t))


def cube_linedraw(a, b):
    N = cube_distance(a, b)
    results = []
    for i in range(0,N+1):
        results.append(cube_hex_round(cube_lerp(a, b, 1.0/N * i)))
    return results

def pixel_to_flat_hex(point,size = 1):
    dx = ( 2/3 * point.x) / size
    dz = (-1/3 * point.x + math.sqrt(3)/3 * point.y) / size
    dy = -dx-dz
    return cube_hex_round(point3(dx, dy,dz))
