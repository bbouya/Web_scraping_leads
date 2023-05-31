from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd


driver = webdriver.Chrome(
        '')

driver.get('https://www.airbnb.ca/')

########################################## - SCRAPING THE DATA - #############################################


df = pd.DataFrame({'Link':[''], 'Name':[''], 'Description':[''], 'Beds':[''], 'Rating':[''], 'Price':['']})

while True:
    soup = BeautifulSoup(driver.page_source, 'lxml')
    boxes = soup.find_all('div', class_ = 'c4mnd7m dir dir-ltr')
    for i in boxes:
        link = i.find('a').get('href')
        name = i.find('div', class_ = 't1jojoys dir dir-ltr').text
        description = i.find('span', class_ = 't6mzqp7 dir dir-ltr').text
        try:
            beds = i.find('span', class_ = 'dir dir-ltr').text
        except:
            beds = 'N/A'
        rating = i.find('span', class_ = 'r1dxllyb dir dir-ltr').text
        price = i.find('span', class_ = 'a8jt5op dir dir-ltr').text
        
        df = df.append({'Link':link, 'Name':name, 'Description':description, 'Beds':beds, 'Rating':rating, 'Price':price}, ignore_index = True)
            
    next_page = soup.find('a', {'aria-label': 'Next'}).get('href')    
    next_page =  'https://www.airbnb.ca'+next_page
    driver.get(next_page)
    time.sleep(10)
    
########################################## - CLEANING THE DATA - ##########################################

    
df['Link'] = 'https://www.airbnb.ca' +df['Link']

df = df.iloc[1:,:]

def price(x):
    x = x.split(' ')[0]
    x = x.replace(',','')
    return x

df['Price'] = df['Price'].apply(price)










    
    
