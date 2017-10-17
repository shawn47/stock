import pandas as pd
import numpy as np
import pylab as pl
from pandas import DataFrame , Series
import math
import csv
import os
from BlackList import BlackList

pool = []

POOLLIST = [
    '000001.csv',
    '603019.csv'
]

def get_code_list():
    codeList = [files for root, dirs, files in os.walk('sina-data-1d')]
    return codeList[0]

def get_target_stock(target):
    stockInfo = pd.read_csv('sina-data-1d/%s' % target, index_col='date', parse_dates=True)
    return stockInfo

def get_stock_pool(poolList = POOLLIST):
	blackList = BlackList()
    for stockFile in poolList:
        if stockFile[:6] not in blackList.blackList:
	        stockInfo = pd.read_csv('sina-data-1d/%s' % stockFile, index_col='date', parse_dates=True)
	        stockInfo['code'] = stockFile[:6]
	        pool.append(stockInfo)

def get_price(index, startDate, endDate, priceTag):
    priceList = np.array(pool[index][startDate: endDate][priceTag]).tolist()
    return priceList

def get_target_price(targetStockInfo, startDate, endDate, priceTag):
    priceList = np.array(targetStockInfo[0][startDate: endDate][priceTag]).tolist()
    return priceList

def sqrtList(numbers):
    m = sum(numbers) / len(numbers)    
    a = 0
    for i in range(len(numbers)):
        a += (numbers[i] - m)**2
    n = a**0.5 
    
    return n

def write2CSVFile(result, fname):
    with file(fname,"w") as csvfile: 
        writer = csv.writer(csvfile)

        writer.writerow(["code", "low_threshold", "high_threshold", "current_fisher_price", "strategy"])
        
        for item in result:
            writer.writerow([item[:6], item.split(",")[1], item.split(",")[2], item.split(",")[3], item.split(",")[4]])

def main(targetStock):
	close_dict = {}
	targetFisherPrice = 0
	watchList = []

	for k in range(len(pool)):
	    a = get_price(k, '2013-07-30', '2017-10-11', 'closing_price')

	    ma_len = 20
	    standard_price = []
	    for i in range(ma_len - 1, len(a) - 1):
	    	try:
	    		standard_price.append((a[i] - sum(a[(i - ma_len + 1): (i + 1)]) / ma_len) / sqrtList(a[(i - ma_len + 1): (i + 1)]))
	    	except Exception as e:
	    		print("error %s" % (pool[k].ix[1:2]['code'].get(0)))
	    		raise e


	    fisher_price = [0] * len(standard_price)
	    for i in range(len(standard_price)):
	        fisher_price[i] = 0.5 * math.log((1 + standard_price[i]) / (1 - standard_price[i]))

	    if (len(fisher_price) > 0):
	    	watchList.append(fisher_price[-1])
	    else:
	    	watchList.append(-1000)
	    # if pool[k].ix[1:2]['code'].get(0) == targetStock:
	    # 	targetFisherPrice = fisher_price[-1]
	    
	    b = sorted(fisher_price)
	    close_dict[k] = b

	threshold_dict = []
	for i in range(len(pool)):
		print("processing %s" % (pool[i].ix[1:2]['code'].get(0)))
		if len(close_dict[i]) != 0:
			low_threshold = close_dict[i][int(len(close_dict[i]) * 0.03)]
			high_threshold = close_dict[i][int(len(close_dict[i]) * 0.97)]
		else:
			low_threshold = 0
			high_threshold = 0

		saleTag = 'none'
		if high_threshold < watchList[i]:
			saleTag = 'out'
		if low_threshold > watchList[i]:
			saleTag = 'in'
		if math.isnan(low_threshold) != True and math.isnan(high_threshold) != True:
			# threshold_dict[i] = [low_threshold, high_threshold]
			threshold_dict.append('%s,%s,%s,%s,%s' % (pool[i].ix[1:2]['code'].get(0), low_threshold, high_threshold, watchList[i], saleTag))



	write2CSVFile(threshold_dict, 'fisher_result.csv')
	print("target stock %s, fisher price: %s" % (targetStock, targetFisherPrice))

if __name__ == '__main__':
	poolList = get_code_list()
	get_stock_pool(poolList)
	main('002304')
