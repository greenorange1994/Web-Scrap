#install.packages(c("rvest", "dplyr", "stringr", "RSelenium")) #°²×°ËùÐèpackage
library(rvest)
library(dplyr)
library(stringr)
library(RSelenium)
library(sys)

#extract categories' names
page <- read_html("xxx")
cate_list <- page %>%
  html_nodes("li span") %>%
  html_text()

#cate_list <- unlist(str_split(cate_list, " "))[811:822] 
cate_list <- cate_list[2:13]
cate_list
cate_n <- length(cate_list)
cate_name_df <- as.data.frame(matrix("", 254, cate_n))
colnames(cate_name_df) <- cate_list

#Open the virtual browser
Sys.sleep(60)
remDr <- remoteDriver(remoteServerAddr = "127.0.0.1" 
                      , port = 4444
                      , browserName = "chrome")
remDr$open() 
remDr$navigate("xxx")
webElem <- remDr$findElement(using = 'xpath', '//*[@id="J-flagship-ft-open"]')
webElem$clickElement()

for (i in 1:cate_n) {
  cate_name_df[, i] <- as.character(levels(cate_name_df[, i]))[cate_name_df[, i]]
  
  #enter each category
  xpath <- str_c('//*[@id="J-flagship-box"]/div[1]/ul/li[', as.character(i+1), ']/span')
  webElem <- remDr$findElement(using = "xpath", xpath)
  webElem$clickElement()
  Sys.sleep(5)
  
  for (j in 1:11) {
    
    for (k in 1:24) {
      #enter each store under each page
      xpath_store <- str_c('//*[@id="J-flagship-normal"]/a[', as.character(k), ']')
      res <- try(webElem <- remDr$findElement(using = 'xpath', xpath_store))
      if (inherits(res, 'try-error')) {
        print("Final page done!")
        break
      }
      url <- unlist(webElem$getElementAttribute("href"))
      store_page <- read_html(url)
      name <- store_page %>%
        html_nodes('title') %>%
        html_text()
      #exception handling
      if (length(name) > 1) {
        name <- name[2]
      }
      print(name)
      cate_name_df[24 * (j-1) + k, i] <- name
      Sys.sleep(0.3)
    }
    
    #enter next page under each category
    if (i != 1 & i != 4) {
      xpath_page <- str_c('//*[@id="J-flagship-page-wrap"]/a[', as.character(j+1), ']')
      res <- try(webElem <- remDr$findElement(using = 'xpath', xpath_page))
      if (inherits(res, 'try-error')) {
        break
      }
    } else {
      if (j == 1) {
        webElem <- remDr$findElement(using = 'xpath', '//*[@id="J-flagship-page-wrap"]/a[2]')
      } else if (j < 5) {
        xpath_page <- str_c('//*[@id="J-flagship-page-wrap"]/a[', as.character(j+2), ']')
        webElem <- remDr$findElement(using = 'xpath', xpath_page)
      } else {
        res <- try(webElem <- remDr$findElement(using = 'xpath', '//*[@id="J-flagship-page-wrap"]/a[6]'))
        if (inherits(res, 'try-error')) {
          break
        }
      }
    }
    webElem$clickElement()
    Sys.sleep(5)
  }
}
write.csv(cate_name_df, 'temp_df.csv')

