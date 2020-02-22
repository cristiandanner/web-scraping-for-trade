import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, date

driver = webdriver.Chrome(ChromeDriverManager().install())

last_datetime = None

driver.get("https://markets.cboe.com/us/equities/market_statistics/book/AAPL/")

content = driver.page_source
soup = BeautifulSoup(content, 'lxml')

last_updated_time = soup.find('span', id='bkTimestamp0')
last_updated_datetime = datetime.now().strftime('%Y-%m-%d') + " " + last_updated_time.text

# TODO - Create loop to get data permanently from the site
current_datetime = datetime.strptime(last_updated_datetime, '%Y-%m-%d %H:%M:%S')
if last_datetime is None and current_datetime is not None:
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
	
if current_datetime > last_datetime:
	last_datetime = current_datetime	
	
top_shares_formatted = []	
top_prices_formatted = []	
last_10_times_formatted = []	
last_10_prices_formatted = []	
last_10_shares_formatted = []		

for i in range(len(last_10_times)):
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
	
df = pd.DataFrame({'Top Shares':top_shares_formatted,'Top Prices':top_prices_formatted,'Last 10 Times':last_10_times_formatted,'Last 10 Prices':last_10_prices_formatted,'Last 10 Shares':last_10_shares_formatted}) 
df.to_csv('products.csv', index=False, encoding='utf-8')	
	
'''			
print('ASKS Shares:')
print(ask_shares)
print('\n')
print('ASKS Price:')
print(ask_prices)
print('\n')
print('BIDS Shares:')
print(bid_shares)
print('\n')
print('BIDS Price:')
print(bid_prices)
print('\n')
print('Last 10 Time Trades:')
print(last_10_times)
print('\n')
print('Last 10 Price Trades:')
print(last_10_prices)
print('\n')
print('Last 10 Shares Trades:')
print(last_10_shares)
print('\n')
print('Last updated:')
print(last_datetime)
'''	



