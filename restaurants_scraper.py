from os import error
import sys
import csv
from selenium import webdriver
import time
import json
from selenium.webdriver.common.by import By

# default path to file to store data
path_to_file = "/Users/gius/Desktop/reviews.csv"

# default number of scraped pages
num_page = 10

# default tripadvisor website of restaurant
url = "https://www.tripadvisor.co.uk/Restaurant_Review-g186338-d2693472-Reviews-Flamingo-London_England.html"

# if you pass the inputs in the command line
if (len(sys.argv) == 4):
    path_to_file = sys.argv[1]
    num_page = int(sys.argv[2])
    url = sys.argv[3]

# Import the webdriver
driver = webdriver.Chrome()
driver.get(url)

time.sleep(1)
driver.find_element(By.XPATH,'//*[@id="_evidon-accept-button"]').click()

# change the value inside the range to save more or less reviews
data = []
for i in range(0, num_page):
    
    # expand the review 
    time.sleep(2)
    driver.find_element(By.XPATH, "//span[@class='taLnk ulBlueLinks']").click()
    container = driver.find_elements_by_xpath(".//div[contains(@class,'review-container')]")
    print("="*30)
    print("="*30)
    print("="*30)
    print(container, len(container))
    print("="*30)
    print("="*30)
    print("="*30)
    for j in range(len(container)):
        try: 
            json_data = { 
            "title" : container[j].find_element(By.XPATH,".//span[@class='noQuotes']").text,
            "title" : container[j].find_element(By.XPATH,".//div[@class='info_text pointer_cursor']").find_element(By.TAG_NAME, 'div').text,
            "date" : container[j].find_element(By.XPATH,".//span[contains(@class, 'ratingDate')]").get_attribute("title"),
            "rating" : container[j].find_element(By.XPATH,".//span[contains(@class, 'ui_bubble_rating bubble_')]").get_attribute("class").split("_")[3],
            "review" : container[j].find_element(By.XPATH,".//p[@class='partial_entry']").text.replace("\n", " "),
            "profile" : container[j].find_element(By.XPATH,".//img").get_attribute("src"),
            }
            data.append(json_data) 
        except: 
            continue
    # change the page
    try: 
        button = driver.find_element(By.XPATH,'.//a[@class="nav next ui_button primary"]')
        button.click()
    except:
        break
    

with open('data.json', "w") as f: 
    json.dump(data, f, indent=4)
driver.close()
