#!/usr/bin/env python
# coding: utf-8


#Dependencies 
from bs4 import BeautifulSoup as bs
from splinter import Browser
from pprint import pprint
import pymongo
import pandas as pd
import requests


def scrape_info():

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    #visit NASA news URL
    mars = {}
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    browser.is_element_present_by_css('ul.item_list, li.slide', wait_time=1)
    html = browser.html
    soup = bs(html, 'html.parser')
    try:
        select_element = soup.select_one('ul.item_list li.slide')
        news_title = select_element.find('div', class_="content_title").get_text()
        news_p = select_element.find('div', class_="article_teaser_body").get_text()
        mars["news_title"] = news_title
        mars["news_p"] = news_p
    except AttributeError:
        mars["news_title"] = None
        mars["news_p"] = None

    # response = requests.get(url)
    # soup = bs(response.text, 'html.parser')

    #Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. 
    #Assign the text to variables that you can reference later.

    # titles = select_elements.find('div', class_="content_title")
    # news_title = titles.get_text()

    # paragraph = select_elements.find('div', class_="article_teaser_body").get_text()
    # news_p = paragraph.get_text()


    # print(news_title)
    # print(news_p)


    # mars["news_title"] = news_title
    # mars["news_p"] = news_p


    # # JPL Mars Space Images - Featured Image

    #Use splinter to navigate the site and find the image url for the current Featured Mars Image and 
    #assign the url string to a variable called featured_image_url.
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    find_id = browser.find_by_id('full_image')

    find_id.click()

    more_info = browser.click_link_by_partial_text('more info')

    #pull image
    soup = bs(browser.html, 'html.parser')
    results = soup.find('figure', class_='lede')
    pic = results.a.img['src']
    featured_image_url = 'https://www.jpl.nasa.gov' + pic
    featured_image_url
    mars["featured_image_url"] = featured_image_url

    # # Mars Facts

    #Visit the Mars Facts webpage here and 
    #use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    #Use Pandas to convert the data to a HTML table string.
    url = 'https://space-facts.com/mars/'
    info = pd.read_html(url)
    info

    info_df = info[0]
    info_df.columns = ['Description', 'Values']
    info_df

    html_table = info_df.to_html()
    html_table
    mars["facts"] = html_table

    # # Mars Hemispheres

    #Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.
    #open the page
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    #Brows HTML and open it with bs
    html = browser.html
    soup = bs(html, 'html.parser')
    print(soup.prettify())

    #Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.

    #Create list for image urls
    hemisphere_image_urls = []

    #Extract base url from webpage url
    base_url= (url.split('/search'))[0]

    #Retrieve all items with hemisphere info
    hemispheres = soup.find_all('div', class_='description')

    for hemisphere in hemispheres:
        
        #Create a dictionary
        hemisphere_info = {}
        
        #extract hemisphere title
        hem_title = hemisphere.find('h3').text
        
        #Add only hemisphere title into dictionary by splitting text 
        hemisphere_info['title'] = hem_title.split(' Enhanced')[0]
        
        #extract the path of hemisphere webpage
        hem_route = hemisphere.find('a', class_='itemLink product-item')['href']
        
        #Connect base url with path
        hemisphere_path = base_url + hem_route
        
        #Open new url with splinter
        browser.visit(hemisphere_path)
        
        #find HTML browser
        html = browser.html
        
        #Parse HTML object with BeautifulSoup
        soup = bs(html, 'html.parser')
        
        #Extract route to full resolution image
        image_url = soup.find('div', class_='downloads').find('ul').find('li').find('a')['href']
        
        #Add image url into dictionary
        hemisphere_info['img_url'] = image_url
        
        

    #Append the dictionary with the image url string and the hemisphere title to a list. 
    #This list will contain one dictionary for each hemisphere.
        hemisphere_image_urls.append(hemisphere_info)

    hemisphere_image_urls

    mars["hemispheres"] = hemisphere_image_urls

    return mars

if __name__ == "__main__":
    print(scrape_info())






