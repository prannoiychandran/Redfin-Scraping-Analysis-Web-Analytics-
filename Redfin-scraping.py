import requests # to get the website
import time     # to force our code to wait a little before re-trying to grab a webpage
import re       # to grab the exact element we need
from bs4 import BeautifulSoup # to grab the html elements we need
import pandas as pd # to create dataframe
from selenium import webdriver #use selenium to avoid website’s anti-scraping
from selenium.common.exceptions import NoSuchElementException
path = 'C:\\Users\\prannoiychandran\\webdrivers\\chromedriver.exe'
browser = webdriver.Chrome(path)
#In this data, we mainly focus on data in New York State
browser.get('https://www.redfin.com/state/New-York')
def check_exists_by_xpath(xpath):
    try:
        browser.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True
data = []
page_source = browser.page_source
soup = BeautifulSoup(page_source, 'lxml')
cities = 'NA'
avg_price = 'NA'
avg_ppersqr = 'NA'
avg_day = 'NA'
cities_link = 'NA'
if (check_exists_by_xpath('//a[@class="ui_button nav next primary "]')):
        browser.find_element_by_xpath('//a[@class="ui_button nav next primary "]').click()
        time.sleep(4)
table = soup.find('table')
tbody = table.find('tbody')
trs = tbody.find_all('tr')
for tr in trs:
    lnk = tr.find_all('a')
    lnk = lnk[0]
    link = lnk.get('href')
    cities_link = "https://www.redfin.com" + link
    cities = lnk.text.strip()
    td1 = tr.find_all('td',{'class':'c1'})
    td1 = td1[0]
    avg_price = td1.text.strip()
    td2 = tr.find_all('td',{'class':'c2'})
    td2 = td2[0]
    avg_ppersqr = td2.text.strip()
    td3 = tr.find_all('td',{'class':'c3'})
    td3 = td3[0]
    avg_day = td3.text.strip()
    
    data.append([cities, avg_price, avg_ppersqr, avg_day, cities_link])  
#get each cities’ average price, average price/ sqr ft., average days on redfin, and link 
df = pd.DataFrame(data, columns = ['Cities', 'Avg.Price', 'Avg.price/sqr', 'Avg.days', 'link'])
 
#In this dataset, we only focus on NYC’s data
building_list = []
nyc = data[0][4]
webpages = 17
start = 1
for webpage in range(webpages):
    if (check_exists_by_xpath('//a[@class="ui_button nav next primary "]')):
        browser.find_element_by_xpath('//a[@class="ui_button nav next primary "]').click()
        time.sleep(4)
    pattern = '/page-'
    webpage = nyc + pattern + str(start)
    browser.get(webpage)
    page_source1 = browser.page_source
    soup1 = BeautifulSoup(page_source1, 'lxml')
    start += 1
    div = soup1.findAll('div', {'class':re.compile('HomeCardContainer')})
    for item in div:
        if (check_exists_by_xpath('//a[@class="ui_button nav next primary "]')):
            browser.find_element_by_xpath('//a[@class="ui_button nav next primary "]').click()
            time.sleep(4)
        a = item.find('a')
        if a == None:
            continue
        else:
            building_link = a.get('href')
            website_pattern = 'https://www.redfin.com'
            building_link = website_pattern + building_link
            browser.get(building_link)
            page_source2 = browser.page_source
            soup2 = BeautifulSoup(page_source2, 'lxml')
            span_address = soup2.find('span', {'class':re.compile('street-address')})
            building_name = span_address.text.strip()
            div_price = soup2.find('div', {'class':re.compile('statsValue')})
            building_price = div_price.text.strip()
            div_beds = soup2.find('div', {'data-rf-test-id':'abp-beds'})
            building_beds = div_beds.text.strip()
            if building_beds == '—Beds':
                building_beds = 'NA'
            div_baths = soup2.find('div', {'data-rf-test-id':'abp-baths'})
            building_baths = div_baths.text.strip()
            if building_baths == '—Baths':
                building_baths = 'NA'
            description_p = soup2.find('p', {'class':re.compile('text-base')})
            if description_p == None:
                building_description = 'NA'
            else:
                building_description = description_p.text.strip()
            span_estimate = soup2.find('span', {'data-rf-test-id': 'avmLdpPrice'})
            if span_estimate == None:
                redfin_estimates = 'NA'
            else:
                subspan_estimate = span_estimate.find('span', {'class':re.compile('value')})
                redfin_estimates = subspan_estimate.text.strip()
            span_location = soup2.find('span', {'class':re.compile('locality')})
            span_region = soup2.find('span', {'class':re.compile('region')})
            building_location = span_location.text.strip()
            building_region = span_region.text.strip()
            div_type = soup2.findAll('div', {'class':re.compile('table-value')})
            if len(div_type) == 0:
                property_type = 'NA'
                property_size = 'NA'
                property_story = 'NA'
            else:
                property_type = div_type[7].text.strip()
                if property_type == '—':
                    property_type = 'NA'
                property_size = div_type[4].text.strip()
                if property_size == '—':
                    property_size = 'NA'
                property_story = div_type[5].text.strip()
                if property_story == '—':
                    property_size = 'NA'
            walking_div = soup2.find('div', {'class':re.compile('transport-icon-and-percentage walkscore')})
            if walking_div == None:
                walking_score = 'NA'
            else:
                walking_span = walking_div.find('span', {'class':re.compile('value')})
                walking_score = walking_span.text.strip()
            transit_div = soup2.find('div', {'class':re.compile('transport-icon-and-percentage transitscore')})
            if transit_div == None:
                transit_score = 'NA'
            else:
                transit_span = transit_div.find('span', {'class':re.compile('value')})
                transit_score = transit_span.text.strip()
            bike_div = soup2.find('div', {'class':re.compile('transport-icon-and-percentage bikescore')})
            if bike_div == None:
                bike_score = 'NA'
            else:
                bike_span = bike_div.find('span', {'class':re.compile('value')})
                bike_score = bike_span.text.strip()
            
            building_list.append([
                building_name, building_price, building_beds, 
                building_baths, redfin_estimates, building_location, 
                property_type, property_size, property_story, 
                walking_score, transit_score, bike_score, building_description, building_link])
#create dataframe for building_list of active listing building’s information
df1 = pd.DataFrame(building_list, columns = ['building_name', 'building_price', 'building_beds', 
                'building_baths', 'redfin_estimates', 'building_location', 
                'property_type', 'property_size', 'property_story', 'walking_score', 'transit_score',
                                             'bike_score', 'building_description', 'building_website'])


#Now extract sold building information of nyc
sold_list = []
webpages = 17
filter_pattern = '/filter/include=sold-3mo'
start = 1
for webpage in range(webpages):
    if (check_exists_by_xpath('//a[@class="ui_button nav next primary "]')):
        browser.find_element_by_xpath('//a[@class="ui_button nav next primary "]').click()
        time.sleep(4)
    pattern = '/page-'
    webpage1 = nyc + filter_pattern + pattern + str(start)
    browser.get(webpage1)
    page_source3 = browser.page_source
    soup3 = BeautifulSoup(page_source3, 'lxml')
    start += 1
    divs = soup3.findAll('div', {'class':re.compile('HomeCardContainer')})
    for item in divs:
        if (check_exists_by_xpath('//a[@class="ui_button nav next primary "]')):
            browser.find_element_by_xpath('//a[@class="ui_button nav next primary "]').click()
            time.sleep(4) 
        a = item.find('a')
        if a == None:
            continue
        else:
            sold_building_link = a.get('href')
            website_pattern = 'https://www.redfin.com'
            sold_building_link = website_pattern + sold_building_link
            browser.get(sold_building_link)
            page_source4 = browser.page_source
            soup4 = BeautifulSoup(page_source4, 'lxml')
            span_address = soup4.find('span', {'class':re.compile('street-address')})
            if span_address == None:
                building_name = 'NA'
            else:
                building_name = span_address.text.strip()
            div_price = soup4.find('div', {'data-rf-test-id':'abp-price'})
            if div_price == None:
                sold_price = 'NA'
            else:
                subdiv_price = div_price.find('div')
                sold_price = subdiv_price.text.strip()
            redfin_div = soup4.find('div', {'data-rf-test-id':'avm-price'})
            if redfin_div == None:
                redfin_estimates = 'NA'
            else:
                subredfin_div = redfin_div.find('div')
                redfin_estimates = subredfin_div.text.strip()
            listed_div = soup4.find('div', {'class':re.compile('price-col number')})
            if listed_div == None:
                listed_price = 'NA'
            else:
                listed_price = listed_div.text.strip()
            div_beds = soup4.find('div', {'data-rf-test-id':'abp-beds'})
            if div_beds == None:
                building_beds = 'NA'
            else:
                building_beds = div_beds.text.strip()
            if building_beds == '—Beds':
                building_beds = 'NA'
            div_baths = soup4.find('div', {'data-rf-test-id':'abp-baths'})
            if div_baths == None:
                building_baths = 'NA'
            else:
                building_baths = div_baths.text.strip()
            if building_baths == '—Baths':
                building_baths = 'NA'
            description_p = soup4.find('p', {'class':re.compile('text-base')})
            if description_p == None:
                building_description = 'NA'
            else:
                building_description = description_p.text.strip()
                building_description = '"' + building_description + '"'
            span_location = soup4.find('span', {'class':re.compile('locality')})
            if span_location == None:
                building_location = 'NA'
            else:
                span_region = soup4.find('span', {'class':re.compile('region')})
                building_location = span_location.text.strip()
                building_region = span_region.text.strip()
                building_location = '"' + building_location + building_region + '"'
            div_type = soup4.findAll('div', {'class':re.compile('table-value')})
            if len(div_type) == 0:
                property_type = 'NA'
                property_size = 'NA'
                property_story = 'NA'
            else:
                property_type = div_type[5].text.strip()
                if property_size == '—':
                    property_size = 'NA'
                property_size = div_type[4].text.strip()
                if property_size == '—':
                    property_size = 'NA'
                property_story = div_type[5].text.strip()
                if property_story == '—':
                    property_story = 'NA'
            walking_div = soup4.find('div', {'class':re.compile('transport-icon-and-percentage walkscore')})
            if walking_div == None:
                walking_score = 'NA'
            else:
                walking_span = walking_div.find('span', {'class':re.compile('value')})
                walking_score = walking_span.text.strip()
            transit_div = soup4.find('div', {'class':re.compile('transport-icon-and-percentage transitscore')})
            if transit_div == None:
                transit_score = 'NA'
            else:
                transit_span = transit_div.find('span', {'class':re.compile('value')})
                transit_score = transit_span.text.strip()
            bike_div = soup4.find('div', {'class':re.compile('transport-icon-and-percentage bikescore')})
            if bike_div == None:
                bike_score = 'NA'
            else:
                bike_span = bike_div.find('span', {'class':re.compile('value')})
                bike_score = bike_span.text.strip()
                 
            sold_list.append([
                building_name, sold_price, building_beds, 
                building_baths, redfin_estimates, listed_price, building_location, 
                property_type, property_size, property_story, 
                walking_score, transit_score, bike_score, building_description, sold_building_link])
#create dataframe for building_list of sold building’s information
df2 = pd.DataFrame(sold_list, columns = ['building_name', 'sold_price', 'building_beds', 'building_baths',
                                         'redfin_estimates', 'listed_price','building_location', 
                'property_type', 'property_size', 'property_story', 
                                         'walking_score', 'transit_score', 'bike_score',
                                         'building_description', 'building_website'])
df2.head(10)
