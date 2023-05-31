from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd


driver = webdriver.Chrome()

driver.get('https://www.linkedin.com/')


########################################## - SCRAPING THE DATA - #############################################


df = pd.DataFrame({'Link':[''], 'Name':[''], 'Title':[''], 'Location':['']})

while True:      
    soup = BeautifulSoup(driver.page_source, 'lxml')
    boxes = soup.find_all('li', class_ = 'reusable-search__result-container')

    for i in boxes:
        try:
            link = i.find('a').get('href')
            name = i.find('span', {'dir': 'ltr'}).find('span', {'aria-hidden': 'true'}).text
            title = i.find('div', class_ = 'entity-result__primary-subtitle t-14 t-black t-normal').text
            location = i.find('div', class_ = 'entity-result__secondary-subtitle t-14 t-normal').text
            df = df.append({'Link':link, 'Name':name, 'Title':title, 'Location':location}, ignore_index = True)
        except:
            pass
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div[4]/div[3]/div[2]/div/div[1]/main/div/div/div/div[2]/div/button[2]').click()
    time.sleep(3)

df.drop_duplicates(inplace = True)

######################################### - CLEANING THE DATA - ##########################################


def ceo(x):
    x = x.lower()
    if ('ceo' in x) or ('founder' in x):
        return 1
    else:
        return 0
    
df['CEO'] = df['Title'].apply(ceo)   
    
df2 = df[df['CEO'] == 1]    
    
    
df2.to_csv('')   
    
    
    
    
    
    

