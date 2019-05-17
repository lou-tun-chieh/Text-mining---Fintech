
from selenium import webdriver
import requests
from bs4 import BeautifulSoup 
import pandas as pd
import time
from selenium.common.exceptions import NoSuchElementException
from io import BytesIO
import datetime
from urllib import request,error
import csv
import os
import numpy as np
import matplotlib.pyplot as plt



def yahoo_download(url):
	url = "https://finance.yahoo.com/quote/" + url + "/history"
	head = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
	main_driver = webdriver.Chrome('/Users/lou_tun_chieh/Desktop/webdriver/chromedriver')  # 注意你們放CHROMEDRIVER的位置
	#告訴chromedriver 等下要找的element 如果沒有找到，要等10秒讓他們生完
	main_driver.implicitly_wait(10)
	main_driver.get(url)
	cookie_list = main_driver.get_cookies()
	cookies_dict = {}
	for cookie in cookie_list:
		cookies_dict['B'] = cookie['value']
	print(cookies_dict)

	date_btn_ele = main_driver.find_element_by_xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/span[2]/span/input')
	date_btn_ele.click()
	main_driver.implicitly_wait(10)

	#點取date button
	date_btn_ele = main_driver.find_element_by_xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/span[2]/div/input[1]').clear()
	date_btn_ele = main_driver.find_element_by_xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/span[2]/div/input[1]').send_keys("01/01/2016")
	#date_btn_ele.click()
	main_driver.implicitly_wait(10)


	##點取done button
	done_btn_ele = main_driver.find_element_by_xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/span[2]/div/div[3]/button[1]')
	done_btn_ele.click()
	main_driver.implicitly_wait(10)


	#點取frequency button
	fre_btn_ele = main_driver.find_element_by_xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[3]/span/div/span/span')
	# print(fre_btn_ele.)
	fre_btn_ele.click()
	# main_driver.execute_script('arguments[0].innerHTML = "Weekly";', fre_btn_ele)
	fre_btn_ele = main_driver.find_element_by_xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[3]/span/div[2]/div[3]').click()
	main_driver.implicitly_wait(10)

	

	#點取apply button
	done_btn_ele = main_driver.find_element_by_xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/button')
	done_btn_ele.click()
	main_driver.implicitly_wait(10)
	time.sleep(20)
	
	#得到歷史資料的csv檔
	export_btn_ele = main_driver.find_element_by_xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[2]/span[2]/a')
	csv_url = export_btn_ele.get_attribute('href')
	main_driver.quit()
	return csv_url, cookies_dict

def write_down_csv(etf_name):
	
	filename = "./ETF_month/" + etf_name + "_month.csv"
	if os.path.isfile(filename):
		df = pd.read_csv(filename)  
		df = pd.DataFrame(df)
		df = df.rename(columns={'Adj Close': etf_name})
		return df

	else:
		print(etf_name)
		tmp_url, tmp_cookie  = yahoo_download(etf_name)
		download = requests.get(tmp_url, cookies=tmp_cookie)
		df = pd.read_csv(BytesIO(download.content))
		#將該變數轉成pandas的dataframe格式
		df = pd.DataFrame(df)
		df = df.rename(columns={'Adj Close': etf_name})
		
		
		with open (filename, 'wb') as handle:
			for block in download.iter_content(1024):
				handle.write(block)
		
		return df

head = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
#必須帶有瀏覽器等資訊
etf_list_1 = "../Municipal Bond ETF List (29).csv"
etf_list_2 = "../Target Maturity Date Corporate Bond ETF List (24).csv"

df_1 = pd.read_csv(etf_list_1)
df_2 = pd.read_csv(etf_list_2)
df = pd.concat([df_1, df_2])

df = df[df["Inception"] < "2016"]
df = df.reset_index(drop=True)

tmp_df =  write_down_csv(df["Symbol"][0])
#Date = tmp_df["Date"]
result =  pd.concat([tmp_df["Date"], tmp_df[df["Symbol"][0]]], axis=1)
for i in range(1, len(df["Symbol"])):
	tmp_df =  write_down_csv(df["Symbol"][i])
	#print(tmp_df[df["Symbol"][i]])
	result =  pd.concat([result, tmp_df[df["Symbol"][i]]], axis=1)
	#print(result)

# result.to_csv('ETF_month.csv',encoding='utf_8_sig')

etf_month = pd.read_csv("ETF_month.csv")  
etf_month = pd.DataFrame(etf_month)
etf_month = etf_month.drop(['Unnamed: 0'], axis = 1)
etf_month = etf_month.drop(index = 0 )
etf_month = etf_month.drop(index = len(etf_month.index) )
etf_month.index = etf_month["Date"]
etf_month = etf_month.drop(["Date"], axis = 1 )
print(etf_month)



# result.to_csv('ETF_week.csv',encoding='utf_8_sig')

etf_week = pd.read_csv("ETF_week.csv")  
etf_week = pd.DataFrame(etf_week)
etf_week = etf_week.drop(['Unnamed: 0'], axis = 1)
etf_week = etf_week.drop(index = 0 )
etf_week = etf_week.drop(index = len(etf_week.index) )
etf_week.index = etf_week["Date"]
etf_week = etf_week.drop(["Date"], axis = 1 )
print(etf_week)

# week_date = []
# for i in range(len(etf.index)):
# 	time = datetime.datetime.strptime(str(etf.iloc[i][0]), '%Y-%m-%d').date()
# 	if time.isoweekday() == 5:
# 		week_date.append(time)


# month_date = []
# year = 2016
# month = 1
# for i in range(41):
# 	if i == 12 or i == 24 or i ==36:
# 		year = year + 1
# 		month = 1
# 	time = datetime.date(year, month, 1)
# 	month_date.append(time)
# 	month += 1

# week_dataframe = etf.loc[week_date]
# print(week_dataframe)

etf_week_return = etf_week/etf_week.shift(1)
etf_week_return = etf_week_return.drop(index = "2016-01-04" , axis = 0)
print(etf_week_return)
etf_month_return = etf_month/etf_month.shift(1)
etf_month_return = etf_month_return.drop(index = "2016-01-01" , axis = 0)
print(etf_month_return)

# plt.figure(figsize=(10,10))
# plt.hist(etf_week_return["MUB"],bins='auto', color='#0504aa',alpha=0.7, rwidth=0.85)
# plt.show()

# USG3M 美國公債利率 
ASKSR_week = pd.DataFrame()

for i in range(len(etf_week_return.columns)):
	tmp_etf = etf_week_return.iloc[:, i]
	tmp_etf = np.log(tmp_etf)














