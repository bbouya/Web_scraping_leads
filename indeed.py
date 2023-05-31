from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd

driver = webdriver.Chrome(
        '')

driver.get('https://ca.indeed.com/')


########################################## - SCRAPING THE DATA - #############################################


df = pd.DataFrame({'Link':[''], 'Job Title':[''], 'Company':[''], 'Date Posted':[''], 'Location':['']})

while True:
        
    soup = BeautifulSoup(driver.page_source, 'lxml')
    boxes = soup.find_all('div', class_ ='job_seen_beacon')
    
    for i in boxes:
        link = i.find('a').get('href')
        job_title = i.find('a', class_ = 'jcs-JobTitle css-jspxzf eu4oa1w0').text
        company = i.find('span', class_ = 'companyName').text
        location = i.find('div', class_ = 'companyLocation').text
        date_posted = i.find('span', class_ = 'date').text
        df = df.append({'Link':link, 'Job Title':job_title, 'Company':company, 'Date Posted':date_posted, 'Location':location}, ignore_index = True)
        
    next_page = soup.find('a', {'aria-label': 'Next Page'}).get('href')
    next_page = 'https://ca.indeed.com' +next_page
    driver.get(next_page)
    time.sleep(3)
    

######################################### - CLEANING THE DATA - ##########################################

    

df['Link'] = 'https://ca.indeed.com' + df['Link']

def posted(x):
    x = x.replace('PostedPosted','').strip()
    return x

df = df.iloc[1:,:]
def day(x):
    try:
        x = x.replace('days ago','').strip()
        x = x.replace('day ago','').strip()
        return float(x)
    except:
        return x

df['Date Posted'] = df['Date Posted'].apply(posted)
df['Date Posted'] = df['Date Posted'].apply(day)


################################### SEND EMAIL WITH CSV ###############################















