# dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time
import pandas as pd
import requests
import pymongo


def scrape_mars():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    # scrape https://mars.nasa.gov/news/
    url = 'https://mars.nasa.gov/news/'
    headers = {'User-Agent': 'Mozilla/5.0'}
    html = requests.get(url, headers=headers).text
    # print(html)
    # init pymongo to work with mongodb
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)

    # define db and collection for part i
    db = client.scrape_mars_db
    collection = db.parti

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(html, 'html.parser')
    
    results = soup.find_all('div', class_='slide')
    # loop through returned results
    for result in results:
    
        # retrieve title and summary
        title = result.find('div', class_='content_title')
        summary = result.find('div',class_='rollover_description_inner')

        # access content
        news_title = title.a.text
        news_p = summary.text
        # print('[Article Title]')
        # print(news_title)
        # print('[Summary]')
        # print(news_p)
        # print('-------')
        # add document to parti collection in mongodb
        post = {
            'title': news_title,
            'summary': news_p
        }
        collection.insert_one(post)
    #browser.quit()
    # scrape https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars
    
    
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    # soup

    # define db and collection for part ii
    collection = db.partii
    html = browser.html
    soup = bs(html, 'html.parser')
    browser.links.find_by_partial_text('FULL IMAGE')
    image = soup.find('a', class_='button fancybox')
    image_url = image['data-fancybox-href']
    firstparturl = 'https://www.jpl.nasa.gov/'
    featured_image_url = firstparturl + image_url
    feat_img = {
        'url':featured_image_url
    }
    # print(featured_image_url)
    collection.insert_one(feat_img)
    #browser.quit()
    # scrape https://space-facts.com/mars/
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    # tables
    df = tables[0]
    # df_2 = tables[1]
    # df_3 = tables[2]
    df_col_rst = df.rename(columns={0:'description',1:'value'})
    # df_col_rst
    html_table = df_col_rst.to_html()
    clean_html_table = html_table.replace('\n', '')
    # add table to mongodb as an object?
    collection = db.partiii
    html_table_obj = {
        'table': clean_html_table
    }
    collection.insert_one(html_table_obj)
    
    # play around with xpath
    chromedriver_location = '/usr/local/bin/chromedriver'
    driver = webdriver.Chrome(chromedriver_location)
    driver.get('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')

    # init list hemisphere_image_urls list
    hemisphere_image_urls = []
    for i in range(4):
        time.sleep(3)
        # xpath for thumbnail
        thumb_btn = f'//*[@id="product-section"]/div[2]/div[{i+1}]/a/img'
        # print(thumb_btn)
        # click thumbnail
        driver.find_element_by_xpath(thumb_btn).click()
        # wait for page to load
        time.sleep(3)
        # extract title
        title = driver.find_element_by_class_name('title')
        # print(title.text)
        time.sleep(3)
        # xpath for full image
        sample_xpath = '//*[@id="wide-image"]/div/ul/li[1]/a'
        elem = driver.find_element_by_xpath(sample_xpath)
        # extract url of image
        link = elem.get_attribute('href')
        # print(link)
        # create dictionary & append hemisphere_image_urls list
        url = {
            'title':title.text,'img_url':link
        }
        hemisphere_image_urls.append(url)
        # extra link to tif file
        # orig_xpath = '//*[@id="wide-image"]/div/ul/li[2]/a'
        # elem_two = driver.find_element_by_xpath(orig_xpath)
        # link_two = elem.get_attribute('href')
        # print(link_two)
        time.sleep(3)
        driver.back()
        
        # add hemisphere_image_urls list to partiv collection
    collection = db.partiv
    collection.insert_many(hemisphere_image_urls)
    #browser.quit()
    # twitter stuff
    weath_xpath = '//*[@id="react-root"]/div/div/div/main/div/div/div/div[1]/div/div/div/div/div[2]/section/div/div/div/div[1]/div/article/div/div[2]/div[2]/div[2]/span'
    # play around with xpath
    chromedriver_location = '/usr/local/bin/chromedriver'
    driver = webdriver.Chrome(chromedriver_location)
    driver.get('https://twitter.com/marswxreport?lang=en')

    time.sleep(5)
    weath_elem = driver.find_element_by_xpath(weath_xpath)
    weath_elem_txt = weath_elem.text
    clean_w_elem = weath_elem_txt.replace('\n', '')
    twitter_weather = {
        'weather':clean_w_elem
    }
    
    collection = db.partv
    collection.insert_one(twitter_weather)
    browser.quit()

