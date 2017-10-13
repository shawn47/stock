#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import csv
import os
import datetime
import pandas as pd
import numpy as np

def retrive_stock_data(stockid, folder, scale, dataLen):
	print('downloading %s to %s' % (stockid, folder))
	url_sina = 'http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=%s&scale=%d&ma=no&datalen=%d' % (stockid, scale, dataLen)
	fname = os.path.join(folder, '%s.csv' % stockid[2:])
	# print(url_sina)

	raw_data = urllib.urlopen(url_sina).read()
	if raw_data != 'null':
		data_std = raw_data.replace('day','"day"').replace('open', '"open"').replace('high','"high"').replace('low', '"low"').replace('close','"close"').replace('volume', '"volume"')
		data = eval(data_std)

		if not os.path.isdir(folder):
			os.mkdir(folder)

		with file(fname,"w") as csvfile: 
			writer = csv.writer(csvfile)

			writer.writerow(["date", "floor_price", "opening_price", "ceiling_price", "volume", "closing_price"])
			
			for item in data:
				writer.writerow([item['day'], item['low'], item['open'], item['high'], item['volume'], item['close']])
			#写入多行用writerows
			# writer.writerows([[0,1,3],[1,2,3],[2,3,4]])

		# urllib.urlretrieve(url_sina, fname)

def update_stock_data(stockid, folder, scale, dataLen):
	fname = os.path.join(folder, '%s.csv' % stockid[2:])
	if not os.path.exists(fname):
		retrive_stock_data(stockid, folder, scale, dataLen)
		return

    # data = pd.read_csv(fname, index_col='Date', parse_dates=True)

    # last_date = data.iloc[0:1].index.tolist()[0]
    # today = pd.Timestamp(datetime.date.today())
    # if today - last_date < pd.Timedelta(days=2):
    #     print('Nothing to update. %s last date is %s.' % (stockid, last_date))
    #     return

    # print('updatting %s to from %s to %s' % (stockid, last_date.date(), today.date()))
    # query = [
    #     ('a', last_date.month - 1),
    #     ('b', last_date.day),
    #     ('c', last_date.year),
    #     ('d', today.month - 1),
    #     ('e', today.day),
    #     ('f', today.year),
    #     ('s', stockid),
    # ]
    # url = 'http://table.finance.yahoo.com/table.csv?%s' % urllib.urlencode(query)
    # temp_file = fname + '.tmp'
    # urllib.urlretrieve(url, temp_file)
    # update_data = pd.read_csv(temp_file, index_col='Date', parse_dates=True)
    # data = data.append(update_data)
    # data.sort_index(ascending=False, inplace=True)
    # data.to_csv(fname, mode='w')
    # os.unlink(temp_file)


def stock_list(postfixs, files):
	if len(files) != len(postfixs):
		print('error: size of files and postfixs not match.')
		return

	stocks = []
	for i in range(len(files)):
		data = pd.read_csv(files[i], header=None, names=['name', 'id'], dtype={'id': np.string0})
		data['postfix'] = postfixs[i]
		stocks.append(data)

	data = pd.concat(stocks)
	print('%d files. %d stocks.' % (len(files), len(data)))
	return data

def update_stock_data_batch(folder, scale, dataLen):
	slist = stock_list(['sh', 'sz'], ['SH.txt', 'SZ.txt'])
	for i in range(len(slist)):
		s = slist.iloc[i]
		# print('postfix: %s. id: %s' % (s['postfix'], s['id']))
		update_stock_data(s['postfix'].strip() + s['id'].strip(), folder, scale, dataLen)


if __name__ == '__main__':
	update_stock_data_batch('sina-data-1d', 240, 1023)
