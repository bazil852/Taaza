import csv
import time
#pyopenxl
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

def scrape_product(args):
    item, account, login_inputs, login_button, cookie_button,Table_click, Table_input, Table_first_element = args
    email, password=account
    print(email,password)
    chrome_options = Options()
    chrome_options.add_argument('--window-size=1280,720')
    # chrome_options.add_argument('--headless')
    driver = webdriver.Chrome('./chromedriver', options=chrome_options)
    wait = WebDriverWait(driver, 10)
    driver.get("https://www.tridge.com/login")
    dummy=wait.until(EC.presence_of_all_elements_located((By.XPATH,"//*[@class='"+login_inputs+"']")))
    if (len(dummy) > 0):
        dummy[0].send_keys(email)
        print('passed')

    else:
        print("Couldn't find input email or password. Try changing Input XPATH")

    dummy[1].send_keys(password)

                                        
    dummy=driver.find_elements(By.XPATH, "//*[@class='"+login_button+"']")

    dummy=wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[@class='"+login_button+"']")))
    if (len(dummy)>0):
        dummy[0].click()
        time.sleep(5)
        try:
            dummy[0].click()
        except Exception as e:
            print("Couldn't find Login Button. Try changing Login Button XPATH")
        
    else:
        print("Couldn't find Login Button. Try changing Login Button XPATH")
    time.sleep(1)

    wait = WebDriverWait(driver, 10)
    try:
        cookie=wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[@class='"+cookie_button+"']")))
        if (len(cookie)>0):
            cookie[0].click()
        else:
            print("Couldn't find Cookie Button (Might cause error later on). Try changing Cookie XPATH")
    except Exception as e:
        print("Couldn't find Cookie Button (Might cause error later on). Try changing Cookie XPATH")
        pass

    driver.get("https://www.tridge.com/prices")
    wait.until(EC.url_contains('https://www.tridge.com/prices'))
    df = []
    wait = WebDriverWait(driver, 10)

    try:
        butt=wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[@class='"+Table_click+"']")))
    except Exception as e:
        print (e)
        print("Couldn't find Product Search Dropdown. Try changing XPATH")

        return
    try:
        if (len(butt)>0):
            butt[0].click()
        else:
            print("Couldn't find Product Search Dropdown. Try changing XPATH")
            return
    except Exception as e:
        print(e)
        return
    try:
        dummy=wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[@class='"+Table_input+"']")))
    except Exception as e:
        print("Couldn't find Product Search Input. Try changing XPATH")
        return

    try:
        if (len(dummy) > 0):
            dummy[0].send_keys(item)
        else:
            print("Couldn't find Product Search Input. Try changing XPATH")
            return
    except Exception as e:
        print("Click ni hua")
        return
    
    wait = WebDriverWait(driver, 10)
    
    try:
        prodIndex=wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[@class='"+Table_first_element+"']")))
    except:
        print (e)
        print("Couldn't find Searched Product. Try changing XPATH")
        return
    if (len(prodIndex) > 0):
        prodIndex[0].click()
    else:
        print("Couldn't find Searched Product. Try changing XPATH")

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

        try:
            notLoaded=False
            try:
                table=wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[@class='simplebar-content']")))
                table=wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "table")))
            except Exception as e:
                print("Couldn't Find table in element, Please check your internet connection")
                return
            if (len(table)>0):
                table[0].click()
            else:
                print("Table is not a list")
            actions.send_keys(Keys.PAGE_DOWN).perform()
            actions.send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(1.5)
            headings = table[0].find_elements(By.TAG_NAME,"th")
            try:
                rows = table[0].find_elements(By.TAG_NAME,"tr")
            except NoSuchElementException:
                print ("Unexpected error please debug")
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
            print(len(rows))
            print("Sr\tCountry\tRegion\tVariety\tPrice")
            for row in rows:
                cells = row.find_elements(By.TAG_NAME,"td")
                if (len(cells)>6):
                    print(count,'\t')
                    count+=1
                    print(item,'\t',cells[2].text,'\t',cells[3].text,'\t',cells[4].text,'\t',cells[6].text)
                    for i in range(6, len(headings)):
                        data = {
                            "CountryName": cells[2].text,
                            "CityName": cells[3].text,
                            "ProductName": item,
                            "variety": cells[4].text,
                            "Currency/Unit": cells[5].text
                        }
                        data['Price Date']=headings[i].text
                        data['Price'] = cells[i].text
                        df.append(data)
            if (count>1000):
                break
            actions.send_keys(Keys.PAGE_DOWN).perform()
            next=wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[@class='sc-ftTHYK bFoDHH toned secondary s ']")))
            if (len(next)>0):
                if (pageCheck==True):
                    next[0].click()
                    pageCheck=False
                else:
                    if (len(next)>1):
                        next[1].click()
                    else:
                        print(item, "Scraping ended")
                        break
            else:
                print ("Next Button Not found, Try changing XPATH")
                break
            time.sleep(1)
            iterate+=1
        except Exception as e:
            print (e)
            print("Scarping Finished")
            break
    dataOut=pd.DataFrame(df)
    print(dataOut.head())
    dataOut.to_excel(item+".xlsx")


def main():
    accounts=[("daud.shafqat@tazahtech.com","15531635"),("raoali1525@gmail.com","Raoali1525"),("bazilsb7@gmail.com","Bazil123")]
    login_inputs="sc-juxSYv daeEXU Polaris-TextField__Input"
    login_button="sc-gScZFl jlVALW filled primary m symbol-before "
    Table_click="sc-doKvHv cFuPeG sc-hixjlP lfUcaI sc-jYECHi fOhYPt"
    Table_input="sc-juxSYv daeEXU Polaris-TextField__Input"
    Table_first_element="sc-eZceyY eavIQf"
    cookie_button="sc-gScZFl fQiJGU filled primary m symbol-before "

    my_list = []
    with open('my_file.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            my_list.append(row)

    # input_tuples = [(item, accounts, login_inputs, login_button, cookie_button, Table_click, Table_input, Table_first_element) for item in my_list[0]]
    # Set up a process pool with the number of processes equal to the number of available CPU cores
    input_tuples = [(item, account, login_inputs, login_button, cookie_button, Table_click, Table_input, Table_first_element) 
                    for item in my_list[0] for account in accounts]
    # To use max cpu available mp.Pool(1) - > mo.Pool(mp.cpu_count())
    with mp.Pool(1) as pool:
        # Use the pool.map() function to run the scrape_product function for each product in parallel
        pool.map(scrape_product, input_tuples)

    # Any post-processing or saving of the data here
    


if __name__ == "__main__":
    main()