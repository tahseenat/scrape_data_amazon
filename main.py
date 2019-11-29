# Generated by Selenium IDE
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pandas as pd
import csv

file_name = 'UPC_Codes.csv'

upc_codes = pd.read_csv(file_name, encoding="ISO-8859-1", usecols=range(0, 1))
print(upc_codes.head())
upc = [x for x in upc_codes["UPS_codes"]]

self = webdriver.Chrome()

website_URL = "https://www.amazon.com/"
self.get(website_URL)

time.sleep(10)

csvFile = open("extracted_data.csv", 'w', newline='')
csvWriter = csv.writer(csvFile)
csvWriter.writerow(["UPC", "URL", "PRICE", "RANK"])

for i in range(78, 92):
    print("Processing code num: ", i)
    self.find_element(By.ID, "twotabsearchtextbox").click()
    element = self.find_element(By.CSS_SELECTOR, ".nav-search-submit > .nav-input")
    actions = ActionChains(self)
    actions.move_to_element(element).perform()
    self.find_element(By.ID, "twotabsearchtextbox").clear()
    url = "item not found"
    price = "item not found"
    rank = "item not found"
    try:
        self.find_element(By.ID, "twotabsearchtextbox").send_keys(upc[i])
        self.find_element(By.CSS_SELECTOR, ".nav-search-submit > .nav-input").click()
        # temp = str(upc[i])
        # temp.replace("+","%2B")
        self.find_element(By.XPATH,
                          "//*[@class ='a-link-normal a-text-normal' and contains(@href,'keywords=" + upc[
                              i] + "&')][1]").click()
        time.sleep(2)
        url = self.current_url
        print(url)
        price = self.find_element(By.ID, "priceblock_ourprice").text
        print(price)
        rank = self.find_element(By.XPATH,
                                 "//*[@id='prodDetails']//tr[contains(., 'Best Sellers Rank')]//td").text
        print(rank)
    except:
        print("Product not found")
    csvFile = open("extracted_data.csv", 'a', newline='')
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow([upc[i], url, price, rank])
self.close()
