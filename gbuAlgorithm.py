
# The Generic Bottom-Up Algorithm

# 设定distance的阈值
dist_threshold = 3
stockpairs=[]
window = len(close_benchmark)       #滑动窗口
for i in pool.index:
    if i in closeprice.keys():
        
        for k in range(len(closeprice[i])+1-window):
            try:
                dist, cost, acc, path = dtw(close_benchmark,closeprice[i][k:(k+window-1)],dist=euclidean_distances)
            except:
                continue
            else:
                distance_ = acc[-1][-1]   
        
                if distance_ < dist_threshold:
                    print(pool[i],distance_,k)
                    stockpairs.append((pool[i],k))

print(stockpairs)