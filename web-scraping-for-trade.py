import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, date
import time
import sys
import msvcrt

last_datetime = None

top_shares_formatted = []	
top_prices_formatted = []	
last_10_times_formatted = []	
last_10_prices_formatted = []	
last_10_shares_formatted = []	
captured_datetime = []	
	
def mainProcess():	
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--disable-gpu')
	chrome_options.add_argument('window-size=1920x1080')

	driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)
	driver.get("https://markets.cboe.com/us/equities/market_statistics/book/AAPL/")
	driver.maximize_window()
	content = driver.page_source
	soup = BeautifulSoup(content, 'lxml')
	#time.sleep(1) # Wait for Selenium page load in background

	last_updated_time = soup.find('span', id='bkTimestamp0')
	
	driver.close()
	driver.quit()	

	if not last_updated_time.text.strip(): # Check last time is not null or empty
		print('Last updated time wasn\'t caught')
		sys.exit()

	last_updated_datetime = datetime.now().strftime('%Y-%m-%d') + " " + last_updated_time.text
	current_datetime = datetime.strptime(last_updated_datetime, '%Y-%m-%d %H:%M:%S')
	global last_datetime
	if (last_datetime is None) or (current_datetime > last_datetime):
		last_datetime = current_datetime
		
		ask_shares = []	
		tds_ask_shares = soup.findAll('td', attrs={'class':'book-viewer__ask book-viewer__ask-shares'})
		for i in tds_ask_shares:  
			ask_shares.append(i.text.replace(u"\xa0", u" "))
			
		ask_prices = []	
		tds_ask_prices = soup.findAll('td', attrs={'class':'book-viewer__ask book-viewer__ask-price book-viewer-price'})
		for i in tds_ask_prices:  
			ask_prices.append(i.text.replace(u"\xa0", u" "))	
			
		bid_shares = []	
		tds_bid_shares = soup.findAll('td', attrs={'class':'book-viewer__bid book-viewer__bid-shares'})
		for i in tds_bid_shares:  
			bid_shares.append(i.text.replace(u"\xa0", u" "))
			
		bid_prices = []	
		tds_bid_prices = soup.findAll('td', attrs={'class':'book-viewer__bid book-viewer__bid-price book-viewer-price'})
		for i in tds_bid_prices:  
			bid_prices.append(i.text.replace(u"\xa0", u" "))		
			
		last_10_times = []	
		tds_last_10_times = soup.findAll('td', attrs={'class':'book-viewer__trades-time'})
		for i in tds_last_10_times:  
			last_10_times.append(i.text.replace(u"\xa0", u" "))
			
		last_10_prices = []	
		tds_last_10_prices  = soup.findAll('td', attrs={'class':'book-viewer__trades-price'})
		for i in tds_last_10_prices:  
			last_10_prices.append(i.text.replace(u"\xa0", u" "))	
			
		last_10_shares = []	
		tds_last_10_shares  = soup.findAll('td', attrs={'class':'book-viewer__trades-shares'})
		for i in tds_last_10_shares:  
			last_10_shares.append(i.text.replace(u"\xa0", u" "))		
					
		for i in range(len(last_10_times)):
			captured_datetime.append(current_datetime.strftime('%Y-%m-%d %H:%M:%S'))
			if i < 5:
				top_shares_formatted.append(ask_shares[i])
			else:
				top_shares_formatted.append(bid_shares[i-5])
				
			if i < 5:
				top_prices_formatted.append(ask_prices[i])
			else:
				top_prices_formatted.append(bid_prices[i-5])
					
			last_10_times_formatted.append(last_10_times[i])
			last_10_prices_formatted.append(last_10_prices[i])
			last_10_shares_formatted.append(last_10_shares[i])
		
def main():
	done = False
	while not done:
		if msvcrt.kbhit(): # Click in console and press 'Esc' to exit from script
			# Create a csv file
			df = pd.DataFrame({'Top Shares':top_shares_formatted,'Top Prices':top_prices_formatted,'Last 10 Times':last_10_times_formatted,'Last 10 Prices':last_10_prices_formatted,'Last 10 Shares':last_10_shares_formatted,'Captured Datetimes':captured_datetime}) 
			df.to_csv('trades.csv', index=False, encoding='utf-8')
			# User press 'Esc' in keyboard
			done = True
		else:
			mainProcess()

if (__name__ == '__main__'): 
	main()