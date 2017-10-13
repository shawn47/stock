##用Bottum-Up算法求关键点
from pandas import Series


p1=plot(range(len(m)),m,'k')

def cal_error(x1,y1,x2,y2,x3_range,y3_range,w):

    distance0 = [0]*w
    for k in range(w):
        distance0[k] = dist(x1,y1,x2,y2,x3_range[k],y3_range[k])
    
    distance = max(distance0)        
  
    return distance

    
#max_error重要参数
max_error = 0.2

segment_0 = []
for i in range(0,len(m),2):
    segment_0_portion = (m[i],m[i+1])
    segment_0.append(segment_0_portion) 

times = 300
    
merge_cost = [0]*(len(segment_0)-1)
for i in range(len(segment_0)-1):
    
    merge = []
    for k in range(len(segment_0[i])):
        merge.append(segment_0[i][k])
    
    for k in range(len(segment_0[i+1])):
        merge.append(segment_0[i+1][k])
    
    
    j = len(merge)-1
    merge_cost[i]=cal_error(0,merge[0],len(merge)-1,merge[-1],range(1,j),merge[1:j],len(merge)-2)
    
    
count = 0
while min(merge_cost) < max_error and count<=times and len(merge_cost)>1:
    count += 1
    merge_cost_array = np.array(merge_cost)
    i = np.argmin(merge_cost_array)          #i是最小数值的那个index
    
    print(i,len(merge_cost))
    
    segment_0[i] = segment_0[i] + segment_0[i+1]
    del segment_0[i+1]
    
    if i ==0 :
        
        del merge_cost[i+1]
        merge = []
        for k in range(len(segment_0[i])):
            merge.append(segment_0[i][k])
    
        for k in range(len(segment_0[i+1])):
            merge.append(segment_0[i+1][k])
            
        j = len(merge)-1
        merge_cost[i] = cal_error(0,merge[0],len(merge),merge[-1],range(1,j),merge[1:j],j-1)
    
    elif i == len(merge_cost)-1:

        del merge_cost[i]
        merge = []
        for k in range(len(segment_0[i-1])):
            merge.append(segment_0[i-1][k])
    
        for k in range(len(segment_0[i])):
            merge.append(segment_0[i][k])
        
        j = len(merge)-1
        merge_cost[i-1] = cal_error(0,merge[0],len(merge),merge[-1],range(1,j),merge[1:j],j-1)
        
    else:

        del merge_cost[i+1]
        
        merge = []
        for k in range(len(segment_0[i])):
            merge.append(segment_0[i][k])
    
        for k in range(len(segment_0[i+1])):
            merge.append(segment_0[i+1][k])
        
        j = len(merge)-1
        merge_cost[i] = cal_error(0,merge[0],len(merge),merge[-1],range(1,j),merge[1:j],j-1)
        
        merge = []
        for k in range(len(segment_0[i-1])):
            merge.append(segment_0[i-1][k])
    
        for k in range(len(segment_0[i])):
            merge.append(segment_0[i][k])
            
        j = len(merge)-1
        merge_cost[i-1] = cal_error(0,merge[0],len(merge),merge[-1],range(1,j),merge[1:j],j-1)
        

m_price=Series([0])
index_set = []
for k in range(len(segment_0)):
    for i in range(len(segment_0[k])):
        m_price.set_value(max(m_price.index) + 1, segment_0[k][i] )
        if i == 0:
            index_set.append(m_price.index[-1]) 
    if k!=0:
        plt.scatter(index_set[k]-1,segment_0[k][0],color='red')