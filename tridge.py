from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd
from collections import ChainMap
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import csv

my_list = []
chrome_options = Options()
chrome_options.add_argument('--headless')

with open('my_file.csv', mode='r') as file:
    reader = csv.reader(file)
    for row in reader:
        my_list.append(row)

# Salmon,Lamb,Fresh Whole Beef,Frozen Pork Ham & Shoulder,Fresh Banana,
# dataF=pd.DataFrame(columns=['Date','Country Name','City Name','category','Product Name','variety','Price/Unit'])

 
driver = webdriver.Chrome('./chromedriver',options=chrome_options)

driver.get("https://www.tridge.com/login?next=%252Fsellers/browse")
time.sleep(2)
dummy=driver.find_elements(By.XPATH,"//*[@class='sc-eYulFz bLYEsy Polaris-TextField__Input']")
if (len(dummy) > 0):
    dummy[0].send_keys("bazilsb7@gmail.com")
else:
    print("Couldn't find input")

# dummy=driver.find_element(By.XPATH,"//*[@class='sc-hAiVDd bbXFJJ Polaris-TextField__Input']")
dummy[1].send_keys("Bazil123")
time.sleep(1)
                                    
dummy=driver.find_elements(By.XPATH, "//*[@class='sc-gScZFl jsEqJd filled primary m symbol-before ']")
dummy=driver.find_elements(By.XPATH, "//*[@class='sc-gScZFl jlVALW filled primary m symbol-before ']")
if (len(dummy)>0):
    dummy[0].click()
else:
    print("Not Found")

time.sleep(2)

cookie=driver.find_elements(By.XPATH, "//*[@class='sc-gScZFl fQiJGU filled primary m symbol-before ']")
if (len(cookie)>0):
    cookie[0].click()
else:
    print("Nahi mila")
time.sleep(2)

for item in my_list[0]:
    driver.get("https://www.tridge.com/prices")
    time.sleep(1)
    df = []
    butt=driver.find_elements(By.XPATH, "//*[@class='sc-fCBrnK gxBBRa soso-selector-button soso-selector-button text-align-start']")
    if (len(butt)>0):
        butt[0].click()
    else:
        print("button Nahi mila")
    dummy=driver.find_elements(By.XPATH,"//*[@class='sc-eYulFz bLYEsy Polaris-TextField__Input']")
    if (len(dummy) > 0):
        dummy[0].send_keys(item)
    else:
        print("Couldn't find input")
    # driver.get("https://www.tridge.com/prices?item_Product=97&entryIds=40860843%2C40880642%2C40862338%2C40861318%2C40860234")
    time.sleep(1)
    
    prodIndex=driver.find_elements(By.XPATH,"//*[@class='sc-doKvHv cxNgbi']")
    
    if (len(prodIndex) > 0):
        prodIndex[0].click()
    else:
        print("Couldn't find input")
    time.sleep(1)
    actions = ActionChains(driver)
    actions.send_keys(Keys.PAGE_DOWN).perform()
    actions.send_keys(Keys.PAGE_DOWN).perform()
    iterate=0
    # try:c
    count=0
    pageCheck=True
    while (True):
        notLoaded=False
        try:
            table=driver.find_element(By.XPATH, "//*[@class='simplebar-content']")
            table=driver.find_element(By.TAG_NAME, "table")
        except Exception as e:
            print("Table not found")
            break
        
        table.click()
        actions.send_keys(Keys.PAGE_DOWN).perform()
        actions.send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(1.5)
        # print (table[0].get_attribute("outerHTML"))
        headings = table.find_elements(By.TAG_NAME,"th")
        # print(headings.text)
        # for head in headings:
        #     print(head.text)
        # print(headings[len(headings)-1].text)
        # exit()
        try:
            rows = table.find_elements(By.TAG_NAME,"tr")
        except NoSuchElementException:
            print ("Handling Exception")
            continue
        for row in rows:
            cells = row.find_elements(By.TAG_NAME,"td")
            if (len(cells)>6):
                if (len(cells[2].text)<=0):
                    notLoaded=True
        if (notLoaded==True):
            continue
        else:
            pass
            #     print(cell.text,end='  ')
        print(len(rows))
        print("Sr\tCountry\tRegion\tVariety\tPrice")
        for row in rows:
            cells = row.find_elements(By.TAG_NAME,"td")
            # for cell in cells:
            #     print(cell.text,end='  ')
            if (len(cells)>6):
                print(count,'\t')
                count+=1
                print(cells[2].text,'\t',cells[3].text,'\t',cells[4].text,'\t',cells[6].text)
                df.append({
                    "Date":headings[len(headings)-1].text,
                    "CountryName":cells[2].text,
                    "CityName":cells[3].text,
                    "category":"Fruit",
                    "ProductName":item,
                    "variety":cells[4].text,
                    "Currency/Unit":cells[5].text,
                    headings[6].text:cells[6].text,
                    headings[7].text:cells[7].text,
                    headings[8].text:cells[8].text,
                    headings[9].text:cells[9].text,
                    headings[10].text:cells[10].text,
                    headings[11].text:cells[11].text,
                    headings[12].text:cells[12].text,
                    headings[13].text:cells[13].text,
                    headings[14].text:cells[14].text,
                    headings[15].text:cells[15].text,
                    headings[16].text:cells[16].text,
                    headings[17].text:cells[17].text,
                    headings[18].text:cells[18].text,
                    headings[19].text:cells[19].text,

                })
            # print ()
        # sc-ftTHYK cOLBMg toned secondary s 
        actions.send_keys(Keys.PAGE_DOWN).perform()
        # time.sleep(300)
        next=driver.find_elements(By.XPATH, "//*[@class='sc-ftTHYK bFoDHH toned secondary s ']")
        if (len(next)>0):
            if (pageCheck==True):
                next[0].click()
                pageCheck=False
            else:
                if (len(next)>1):
                    next[1].click()
                else:
                    print("Scraping ended")
                    break
        else:
            print ("Nahi mila")
            break
        time.sleep(1)
        iterate+=1
    # except:
    #     pass
    dataOut=pd.DataFrame(df)

    print("Yahan end ho gya")
    print(dataOut.head())
    dataOut.to_excel(item+".xlsx")
exit()