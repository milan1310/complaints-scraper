from playwright.sync_api import sync_playwright  # webdriver for getting website content
from bs4 import BeautifulSoup # html parser
import json

def sscrap_sıkayetvar(company_name):
    with sync_playwright() as p: 
        for browser_type in [p.webkit]: # using webkit browser
            browser = browser_type.launch() 
            page = browser.new_page() 
            complains=[]
            for i in range(1): #change the range for scraping more number of pages for the same company
                page.goto("https://www.sikayetvar.com/"+company_name+"?page="+str(i))
                print('waiting for result....')
                page.wait_for_timeout(5000)
                print('getting data...')
                complain = page.content()
                print('parsing html')
                soup = BeautifulSoup(complain,'html.parser')
                list = soup.find_all('article',class_="complaint-card")
                complains.append(list)
            browser.close() 
            print('stop...')

            # preparing json array from the scrape data
            jsonArray = []
            for j in range(len(complains)):
                for k in range(len(complains[j])):
                    html = complains[j][k]
                    soup1 = BeautifulSoup(str(html),'html.parser')
                    complainObj = {
                        "person_name" : "none" if(soup1.find('span', class_='username') is None) else soup1.find('span', class_='username').get_text(),
                        "title": "none" if(soup1.find('a', class_="complaint-layer") is None) else soup1.find('a', class_="complaint-layer").get_text(),
                        "date": "none" if(soup1.find('span',class_="time") is None) else soup1.find('span',class_="time").get_text(),
                        "text_data":"none" if(soup1.find('p') is None) else soup1.find('p').get_text()                
                    }
                    jsonArray.append(complainObj)

            # print(jsonArray)
            jsonSrt = json.dumps(jsonArray)
            jsonFile = open(company_name + ".json", "w")
            jsonFile.write(jsonSrt)
            jsonFile.close()

sscrap_sıkayetvar("kia")
        
