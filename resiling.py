from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd

driver = webdriver.Chrome(
        '')

driver.get('https://www.thebay.com/c/women?prefn1=isSale&prefv1=Sale%7CSolde')


########################################## - SCRAPING THE DATA - #############################################


df = pd.DataFrame({'Link':[''], 'Name':[''], 'Product':[''], 'Sale Price':[''], 'Full Price':['']})


while True:
    counter = 0     
    while counter == 0:    
          last = driver.execute_script('return document.body.scrollHeight') 
          driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
          time.sleep(7)
          new = driver.execute_script('return document.body.scrollHeight')  
          if new == last:
              counter = 1
    
    soup = BeautifulSoup(driver.page_source, 'lxml')
    boxes = soup.find_all('div', class_ ='col-6 col-sm-4 col-xl-3')
    len(boxes)
    
    for i in boxes:
        try:
            link = i.find('a').get('href')
            name = i.find('a', class_ ='product-brand adobelaunch__brand').text
            product = i.find('a', class_ = 'link').text
            sale_price = i.find('span', class_ = 'formatted_sale_price formatted_price js-final-sale-price').text
            full_price = i.find_all('span', class_ = 'formatted_price')[1].text
            df = df.append({'Link':link, 'Name':name, 'Product':product, 'Sale Price':sale_price, 'Full Price':full_price}, ignore_index = True)
        except:
            pass
    
    next_page = soup.find('a', {'aria-label': 'Next'}).get('href')
    driver.get(next_page)
    time.sleep(5)


###########################################- CLEANING THE DATA - ##########################################


df2 = df.iloc[1:,:]

def dollar(x):
    try:
        x = x.replace('$','')
        x = x.replace(',','')
        return float(x)
    except:
        return 0

df2['Full Price'] = df2['Full Price'].apply(dollar)
df2['Sale Price'] = df2['Sale Price'].apply(dollar)

df2['Discount Percentage'] = ((df2['Full Price'] - df2['Sale Price'])/df2['Full Price'])*100

df2['Link'] = 'https://www.thebay.com'+df2['Link']


