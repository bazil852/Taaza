import csv
import time
from collections import ChainMap
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import multiprocessing as mp


def scrape_product(item):
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    driver = webdriver.Chrome('./chromedriver', options=chrome_options)
    wait = WebDriverWait(driver, 10)
    driver.get("https://www.tridge.com/login")
    # time.sleep(2)
    dummy=wait.until(EC.presence_of_all_elements_located((By.XPATH,"//*[@class='sc-dMVFSy kkcmxE Polaris-TextField__Input']")))
    if (len(dummy) > 0):
        dummy[0].send_keys("raoali1525@gmail.com")
    else:
        print("Couldn't find input")

    # dummy=driver.find_element(By.XPATH,"//*[@class='sc-hAiVDd bbXFJJ Polaris-TextField__Input']")
    dummy[1].send_keys("Raoali1525")
    time.sleep(1)
                                        
    dummy=driver.find_elements(By.XPATH, "//*[@class='sc-gScZFl jsEqJd filled primary m symbol-before ']")
    dummy=wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[@class='sc-gScZFl jlVALW filled primary m symbol-before ']")))
    if (len(dummy)>0):
        dummy[0].click()
    else:
        print("Not Found")

    # time.sleep(2)
    wait = WebDriverWait(driver, 10)
    try:
        cookie=wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[@class='sc-gScZFl fQiJGU filled primary m symbol-before ']")))
        if (len(cookie)>0):
            cookie[0].click()
        else:
            print("Nahi mila")
    except Exception as e:
        print("Cookie not found")
        pass
    # time.sleep(2)

    # for item in my_list[0]:
    driver.get("https://www.tridge.com/prices")
    time.sleep(1)
    df = []
    wait = WebDriverWait(driver, 10)
    try:
        butt=wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[@class='sc-jVQoqC EPjsG sc-MAqyW eJQUbQ sc-cBQajf gjwVMg']")))
    except Exception as e:
        print (e)
        print('button hi ni mila')
        return
    try:
        if (len(butt)>0):
            butt[0].click()
        else:
            print("button Nahi mila")
            return
    except Exception as e:
        print(e)
        return
    try:
        dummy=wait.until(EC.presence_of_all_elements_located((By.XPATH,"//*[@class='sc-dMVFSy kkcmxE Polaris-TextField__Input']")))
    except Exception as e:
        print("input ni mili")
        return
    try:
        if (len(dummy) > 0):
            dummy[0].send_keys(item)
        else:
            print("Couldn't find input")
            return
    except Exception as e:
        print("Click ni hua")
        return
    # driver.get("https://www.tridge.com/prices?item_Product=97&entryIds=40860843%2C40880642%2C40862338%2C40861318%2C40860234")
    time.sleep(1)
    
    # sc-gScZFl hVfWEN filled white m symbol-before sc-tKebc dkbZPP
    wait = WebDriverWait(driver, 10)
    
    try:
        prodIndex=wait.until(EC.presence_of_all_elements_located((By.XPATH,"//*[@class='sc-dDPqvT abMMF']")))
    except:
        print (e)
        print("type k baad click nahi hua")
        return
    
    if (len(prodIndex) > 0):
        prodIndex[0].click()
    else:
        print("Couldn't find click")
    time.sleep(1)

    query_string = "&item_Type=w&item_OriginType=d&interval=w&dateRange=3y&startDate=2020-03-01&endDate=2023-03-17&currency=USD&unit=kg&includeEstimatedPrices=true&includeForecastedPrices=false&"
    driver.get(str(driver.current_url)+query_string)
    time.sleep(3)
    actions = ActionChains(driver)
    actions.send_keys(Keys.PAGE_DOWN).perform()
    actions.send_keys(Keys.PAGE_DOWN).perform()
    iterate=0
    # try:c
    count=0
    pageCheck=True
    while (True):
        if (count>1000):
            break
        try:
            notLoaded=False
            try:
                table=wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[@class='simplebar-content']")))
                table=wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "table")))
            except Exception as e:
                print("Table not found")
                return
            if (len(table)>0):
                table[0].click()
            else:
                print("Table is not a list")
            actions.send_keys(Keys.PAGE_DOWN).perform()
            actions.send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(1.5)
            # print (table[0].get_attribute("outerHTML"))
            headings = table[0].find_elements(By.TAG_NAME,"th")
            # print(headings.text)
            # for head in headings:
            #     print(head.text)
            # print(headings[len(headings)-1].text)
            # exit()
            try:
                rows = table[0].find_elements(By.TAG_NAME,"tr")
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
                    print(item,'\t',cells[2].text,'\t',cells[3].text,'\t',cells[4].text,'\t',cells[6].text)
                    data = {
                        "CountryName":cells[2].text,
                        "CityName":cells[3].text,
                        "ProductName":item,
                        "variety":cells[4].text,
                        "Currency/Unit":cells[5].text
                    }

                    for i in range(6, len(headings)):
                        data[headings[i].text] = cells[i].text
                    
                    df.append(data)
                
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
        except Exception as e:
            print (e)
            print("As far as i can go.")
            break
    # except:
    #     pass
    dataOut=pd.DataFrame(df)

    print("Yahan end ho gya")
    print(dataOut.head())
    dataOut.to_excel(item+".xlsx")


def main():
    my_list = []
    with open('my_file.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            my_list.append(row)

    # Set up a process pool with the number of processes equal to the number of available CPU cores
    with mp.Pool(3) as pool:
        # Use the pool.map() function to run the scrape_product function for each product in parallel
        pool.map(scrape_product, my_list[0])

    # Any post-processing or saving of the data here
    


if __name__ == "__main__":
    main()