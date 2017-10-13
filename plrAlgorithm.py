##先用PLR算法得到关键点

##PLR算法
from scipy.spatial import distance
import math
import time

fig_size = plt.rcParams['figure.figsize']
fig_size[0] = 12
fig_size[1] = 8

p1=plot(range(len(m)),m,'k')

def dist(x1,y1,x2,y2,x3,y3): # x3,y3 is the point
    px = x2-x1
    py = y2-y1
   
    something = px*px + py*py
#     print(something,'lalala')

    u =  ((x3 - x1) * px + (y3 - y1) * py) / float(something)

    if u > 1:
        u = 1
    elif u < 0:
        u = 0

    x = x1 + u * px
    y = y1 + u * py

    dx = x - x3
    dy = y - y3

    # Note: If the actual distance does not matter,
    # if you only want to compare what this function
    # returns to other results of this function, you
    # can just return the squared distance instead
    # (i.e. remove the sqrt) to gain a little performance

    dist = math.sqrt(dx*dx + dy*dy)

    return dist


def calculate_error(x1,y1,x2,y2,x3_range,y3_range,i):
    
    distance0 = [0]*(i-1)
    for k in range(len(x3_range)):
        distance0[k] = dist(x1,y1,x2,y2,x3_range[k],y3_range[k])
    
    distance = max(distance0)
    
    return distance
    
    
#max_error为一个重要参数，此处省去BPN与根据profit优化步骤，根据多次尝试直接设定即可
max_error = 0.1
anchor_set = []
    
anchor = 0
anchor_set.append(anchor)
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))


i_prior = 0
while anchor + i_prior < len(m):
    i = 2
    
    while calculate_error(anchor,m[anchor],anchor+i,m[anchor+i],range(anchor+1,anchor+i),m[(anchor+1):(anchor+i)],i) < max_error:
        i_prior = i
        i += 1
    
        if i >= len(m)-anchor:
            break
    else:
        
        anchor += i-1
        anchor_set.append(anchor)
        plt.scatter(anchor,m[anchor],color='red')
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),'lalala')
        
        continue
    break