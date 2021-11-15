import sys
import csv
from selenium import webdriver
import time
import json

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

# change the value inside the range to save more or less reviews
for i in range(0, num_page):
    
    # expand the review 
    time.sleep(2)
    driver.find_element_by_xpath("//span[@class='taLnk ulBlueLinks']").click()

    container = driver.find_elements_by_xpath(".//div[@class='review-container']")

    for j in range(len(container)):
        data = { 
        "title" : container[j].find_element_by_xpath(".//span[@class='noQuotes']").text,
        "date" : container[j].find_element_by_xpath(".//span[contains(@class, 'ratingDate')]").get_attribute("title"),
        "rating" : container[j].find_element_by_xpath(".//span[contains(@class, 'ui_bubble_rating bubble_')]").get_attribute("class").split("_")[3],
        "review" : container[j].find_element_by_xpath(".//p[@class='partial_entry']").text.replace("\n", " "),
        "profile" : container[j].find_element_by_xpath("//*[@id='UID_254F2CA93A21BA5B94B592FF02CF92A4-SRC_739705132']/div[1]/div/a/div/div/img.//p[@class='partial_entry']").get_attribute("src"),
        }
        # Open the file to save the review
        with open('data.json', "w") as f: 
            json.dump(data, f, indent=4)
    # change the page
    driver.find_element_by_xpath('.//a[@class="nav next ui_button primary"]').click()

driver.close()
