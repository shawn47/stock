#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from pandas import DataFrame,Series
import matplotlib.pyplot as plt
from dtw import dtw
from sklearn.metrics.pairwise import euclidean_distances
import time
from numpy import inf
from numpy import NaN
import os


# pool = Series(get_index_stocks('000016.XSHG'))
pool = []

POOLLIST = [
    '000001.csv',
    '603019.csv'
]

dist_threshold = 1.2

def get_code_list():
    codeList = [files for root, dirs, files in os.walk('sina-data')]
    # for root, dirs, files in os.walk('sina-data'):
    #     codeList.append(files)
    # print(codeList)
    return codeList[0]

def get_target_stock(target):
    stockInfo = pd.read_csv('sina-data/%s' % target, index_col='date', parse_dates=True)
    return stockInfo

def get_stock_pool(poolList):
    # raw_pool = []
    for stockFile in poolList:
        if stockFile != '002304.csv':
            stockInfo = pd.read_csv('sina-data/%s' % stockFile, index_col='date', parse_dates=True)
            stockInfo['code'] = stockFile[:6]
            pool.append(stockInfo)

def get_price(index, startDate, endDate, priceTag):
    # print(pool[index].ix[1:3][priceTag])
    # transform Series into np.ndarray(), then it can be transformed into List
    priceList = np.array(pool[index][startDate: endDate][priceTag]).tolist()
    return priceList

def get_target_price(targetStockInfo, startDate, endDate, priceTag):
    priceList = np.array(targetStockInfo[0][startDate: endDate][priceTag]).tolist()
    return priceList

def main():
    print(time.strftime('1 %Y-%m-%d %H:%M:%S', time.localtime()))
    closeprice = {}

    for i in range(len(pool)):
        closeprice[i] = get_price(i, '2017-10-11 09:35:00', '2017-10-11 11:30:00', 'closing_price')
        for k in range(len(closeprice[i])):
            if max(closeprice[i]) == min(closeprice[i]):
                closeprice[i][k] = max(closeprice[i])
            else:
                closeprice[i][k] = (closeprice[i][k] - min(closeprice[i])) / (max(closeprice[i]) - min(closeprice[i]))

            if closeprice[i][k] == NaN or closeprice[i][k] == inf:
                del closeprice[i]
                continue
            else:
                closeprice[i][k] = float("%.9f" % closeprice[i][k])
            
        print(time.strftime('2 %Y-%m-%d %H:%M:%S', time.localtime()))

    for i in range(len(pool)):
        k = i + 1

        if i != len(pool) - 1:
            for m in range(k, len(pool)):
                try:
                    dist, cost, acc, path = dtw(closeprice[i], closeprice[m], dist = euclidean_distances)
                    # print(acc)
                    # print('###')
                except:
                    continue
        else:
            distance_ = acc[-1][-1]
            print(distance_)
            print('***')
                
            print(time.strftime('3 %Y-%m-%d %H:%M:%S', time.localtime()))    

            if distance_ < dist_threshold:
                print(distance_)
                
                fig_size = plt.rcParams['figure.figsize']
                fig_size[0] = 12
                fig_size[1] = 8
                
                fig, ax1 = plt.subplots()
                ax2 = ax1.twinx()
            
                p1 = ax1.plot(range(len(closeprice[i])), closeprice[i], 'r')
                p1 = ax2.plot(range(len(closeprice[i])), closeprice[m], 'k')

                plt.show()
                break
            else:
                continue

def run(target):
    targetStockInfo = []
    targetStockInfo.append(get_target_stock(target))
    targetStockPriceInfo = get_target_price(targetStockInfo, '2017-10-11 09:35:00', '2017-10-11 11:30:00', 'closing_price')

    for k in range(len(targetStockPriceInfo)):
        targetStockPriceInfo[k] = (targetStockPriceInfo[k] - min(targetStockPriceInfo)) / (max(targetStockPriceInfo) - min(targetStockPriceInfo))

        if targetStockPriceInfo[k] == NaN or targetStockPriceInfo[k] == inf:
            del targetStockPriceInfo
            continue
        else:
            targetStockPriceInfo[k] = float("%.9f" % targetStockPriceInfo[k])


    # print(time.strftime('1 %Y-%m-%d %H:%M:%S', time.localtime()))
    closeprice = {}

    for i in range(len(pool)):
        closeprice[i] = get_price(i, '2017-10-11 09:35:00', '2017-10-11 11:30:00', 'closing_price')
        for k in range(len(closeprice[i])):
            if max(closeprice[i]) == min(closeprice[i]):
                closeprice[i][k] = max(closeprice[i])
            else:
                closeprice[i][k] = (closeprice[i][k] - min(closeprice[i])) / (max(closeprice[i]) - min(closeprice[i]))

            if closeprice[i][k] == NaN or closeprice[i][k] == inf:
                del closeprice[i]
                continue
            else:
                closeprice[i][k] = float("%.9f" % closeprice[i][k])
            
        # print(time.strftime('2 %Y-%m-%d %H:%M:%S', time.localtime()))

    # watchList = []

    for i in range(len(pool)):
        # if i != len(pool) - 1:
        try:
            dist, cost, acc, path = dtw(targetStockPriceInfo, closeprice[i], dist = euclidean_distances)
        except:
            continue
        # else:
        distance_ = acc[-1][-1]
        print(distance_)
        # print('***')
            
        # print(time.strftime('3 %Y-%m-%d %H:%M:%S', time.localtime()))    

        if distance_ < dist_threshold:
            # print(distance_)
            
            fig_size = plt.rcParams['figure.figsize']
            fig_size[0] = 12
            fig_size[1] = 8
            
            fig, ax1 = plt.subplots()
            ax2 = ax1.twinx()

            print(len(closeprice[i]))
            print(len(targetStockPriceInfo))

            print(pool[i].ix[1:2]['code'])
        
            p1 = ax1.plot(range(len(closeprice[i])), closeprice[i], 'r')
            p1 = ax2.plot(range(len(targetStockPriceInfo)), targetStockPriceInfo, 'k')

            # plt.show()
            # break
        else:
            continue
    # plt.show()

if __name__ == '__main__':
    # main()
    poolList = get_code_list()
    get_stock_pool(poolList)
    # get_price(1, '2017-10-11 10:05:00', '2017-10-11 11:05:00', 'volume')
    # main()
    run('002304.csv')
    # print(len(pool))
    # print(pool[1].ix[2]['volume'])
