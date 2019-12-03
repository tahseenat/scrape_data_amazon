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

file_name = 'UPC_codes.csv'

upc_codes = pd.read_csv(file_name, encoding="ISO-8859-1", usecols=range(0, 1))
print(upc_codes.head())
upc = [x for x in upc_codes["UPC_codes"]]

self = webdriver.Chrome()

website_URL = "https://www.amazon.com/"
self.get(website_URL)

time.sleep(10)

csvFile = open("extracted_data.csv", 'w', newline='')
csvWriter = csv.writer(csvFile)
csvWriter.writerow(["UPC", "URL", "PRICE", "RANK", "ASIN"])

for i in range(len(upc)):
    print("Processing code num: ", i)
    self.find_element(By.ID, "twotabsearchtextbox").click()
    element = self.find_element(By.CSS_SELECTOR, ".nav-search-submit > .nav-input")
    actions = ActionChains(self)
    actions.move_to_element(element).perform()
    self.find_element(By.ID, "twotabsearchtextbox").clear()
    url = "url not found"
    price = "price_not_found"
    rank = "rank not found"
    asin = "asin code not available"
    tempupc = upc[i]
    tempupc = str(tempupc)
    tempupc = "0"*(13 - len(tempupc)) + tempupc

    try:
        self.find_element(By.ID, "twotabsearchtextbox").send_keys(tempupc)
        self.find_element(By.CSS_SELECTOR, ".nav-search-submit > .nav-input").click()

        # temp = str(upc[i])
        # temp.replace("+","%2B")

        # click on the product
        try:
            self.find_element(By.XPATH,
                              "//*[@class ='a-link-normal a-text-normal' and contains(@href,'keywords=" + tempupc +
                              "&')][1]").click()
            price = self.find_element(By.XPATH, "(//*[contains(@class, 'a-color-price')])[1]").text
            url = self.current_url
        except:
            try:
                self.find_element(By.XPATH,
                                  "//*[@class ='a-link-normal a-text-normal' and contains(@href,'keywords={}')]".
                                  format(tempupc)).click()
                price = self.find_element(By.XPATH, "(//*[contains(@class, 'a-color-price')])[1]").text
                url = self.current_url
            except:
                print("")
        time.sleep(2)

        # Paperback edition
        try:
            self.find_element(By.XPATH, "(//*[contains(text(), 'Paperback')])[2]").click()
            time.sleep(2)
        except:
            print("no paperback edition")
        # ASIN code
        try:
            asin = self.find_element(By.XPATH, "//*[contains(@id, 'productDetails')]//tr[contains(., 'ASIN')]//td").text
        except:
            print("")

        # price script
        # try:
        #     price = self.find_element(By.XPATH, "(//*[contains(@class, 'a-color-price')])[1]").text
        # except:
        #     price = "nothing"

        # rank script
        try:
            rank = self.find_element(By.XPATH,
                                     "//*[contains(@id, 'productDetails')]//tr[contains(., 'Best Sellers Rank')]//td").text
        except:
            rank = self.find_element(By.XPATH, "//*[@id='SalesRank']").text

    except:
        print("Product not found")

    rank = list(rank)

    if ":" in rank:
        tmp = rank.index(":")
        rank = rank[tmp + 2:]
    rank = ''.join(rank)
    price = list(price)

    if " " in price:
        for j in range(len(price)):
            if price[j] == ' ':
                break
        price = price[:j]

    price = ''.join(price)
    csvFile = open("extracted_data.csv", 'a', newline='')
    csvWriter = csv.writer(csvFile)
    print("\n\n", tempupc, price, rank, asin)
    csvWriter.writerow([tempupc, url, price, rank, asin])
self.close()
