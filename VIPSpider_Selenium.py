import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time

def getHTMLtext(url, coding = 'utf-8'):
    try:
        r = requests.get(url)
        r.raise_for_status
        r.encoding = coding
        return r.text
    except:
        return ""
        
def parsePage(html):
    bs = BeautifulSoup(html, 'html.parser')
    categoryList = []
    for each in bs.body.find_all('li'):
        categoryList.append(each.string)
    return categoryList

class vipScrap:
    
    def __init__(self, url):
        self.browser = webdriver.Chrome()
        self.url = url
    
    def setUp(self):
        browser = self.browser
        browser.get(self.url)
        ele = browser.find_element_by_xpath('//*[@id="J-flagship-box"]/div[1]/ul/li[1]/span')
        ele.click()
        element = WebDriverWait(browser, 10).until(lambda x: x.find_element_by_xpath('//*[@id="J-flagship-choiceness"]/a[1]/img'))
        ele = browser.find_element_by_xpath('//*[@id="J-flagship-ft-open"]')
        ele.click()
    
    def crawler(self, categoryList):
        browser = self.browser
        pageDict = {}
        for i, cate in enumerate(categoryList):
            tempList = []
            # enter each category
            xpath = '//*[@id="J-flagship-box"]/div[1]/ul/li[' + str(i+2) + ']/span'
            cur_category = browser.find_element_by_xpath(xpath)
            cur_category.click()
        
            # enter each page
            page = 1
            while (True):
                element = WebDriverWait(browser, 10).until(lambda x: x.find_element_by_xpath('//*[@id="J-flagship-normal"]/a[1]/img'))
                j = 1
                while (True):
                    # test if we come to the final store of this page
                    try:
                        store_xpath = '//*[@id="J-flagship-normal"]/a[' + str(j) + ']'
                        store = browser.find_element_by_xpath(store_xpath)
                        store_url = store.get_attribute('href')
                        html = getHTMLtext(store_url)
                        try:
                            bs = BeautifulSoup(html, 'html.parser')
                            tempList.append(bs.head.title.string)
                            print(bs.head.title.string)
                        except:
                            tempList.append('Wrong Link!')
                        j += 1
                    except:
                        break  
                time.sleep(1)
                    
                # test if we come to the final page of this category
                try:
                    next_page = browser.find_element_by_xpath('//*[@id="J_next_paging"]')
                    next_page.click()
                    page += 1
                except:
                    try:
                        next_page_xpath = '//*[@id="J-flagship-page-wrap"]/a[' + str(page+1) + ']'
                        next_page = browser.find_element_by_xpath(next_page_xpath)
                        next_page.click()
                        page += 1
                    except:
                        print ("%s is done!" % cate)
                        break
        
            # store this category's stores
            pageDict[cate] = tempList
            
        return pageDict
    
if __name__ == "__main__":
    url = "http://category.vip.com/?act=brand"
    scraper = vipScrap(url)

    # get the list of store types
    print("Try to get the list of store types...")
    html = getHTMLtext(url)
    categoryList = parsePage(html)[1:]
    print(categoryList)

    # get the list of stores
    print("Setup the browser...")
    scraper.setUp()
    pageDict = scraper.crawler(categoryList)
    with open('stores.txt', 'w') as f:
        f.write(str(pageDict))
    f.close()
