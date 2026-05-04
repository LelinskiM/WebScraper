# Inports
import os
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup

# get product page / code
product_code = input("Input product code: ")
page = 1

next =True
headers ={
    "Host":"www.ceneo.pl",
    "Cookie":"rc=igdamb4ThOR9TJV1wnnHj0peFsMflKvy5/lp9BN0GICfk5H4KXZZ6cJnqS0eypifqC3MZeoTduSk6rO+Dotsr41HXVTMsgurVnSzz257svLLQS2sjY9sN6gtzGXqE3bkpOqzvg6LbK+NR11UzLILq1Z0s89ue7Lyo3PdJGdIi2GJEbcwQDURfTI9fGwGMD364+NrKUZBiCscG0vEN/6qtg==; domain=.ceneo.pl; expires=Sun, 19-Jul-2026 13:21:44 GMT; path=/; secure; HttpOnly; SameSite=Lax",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
    "Accept-Language": "pl-PL,pl;q=0.9"
}

all_opinions =[]

##### start of while loop to repeat for all pages of opinions
while next: 

    url = f"https://www.ceneo.pl/{product_code}/opinie-{page}"
    print(url)

    # prepselenium
    path_to_driver = "D:\\selenium\\chromedriver-win64\\chromedriver.exe"
    s = Service(path_to_driver)
    driver = webdriver.Chrome(service=s)
    driver.get(url)
    driver.maximize_window()
    driver.find_element(by="xpath", value='//*[@id="js_cookie-consent-general"]/div/div[2]/button[1]').click()

    # sent request to url
    response = requests.get(url)
    print(response)

    #fetch product name
    #print(response.status_code)
    #print(response.text[:2000])
    #response = requests.get(url, headers=headers)

    page_dom = BeautifulSoup(response.text, "html.parser")

    Product_Name = page_dom.select_one('h1').get_text() ###ERROR ON THIS LINE- Need to use solenium

    Product_Name = page_dom.find('h1').get_text()

    #fetch all opinions
    Opinions = page_dom.select("div.js_product-review:not(.user-post--highlight)")
    print(len(Opinions))

    #parse opinions / get requiered data 
    for opinion in Opinions:
        single_opinion = {
            'opinion_id': opinion.get("data-entry-id"),
            'author': opinion.select_one("span.user-post__author-name").get_text().strip(),
            'recomendations': opinion.select_one('span.user-post__author-recomendation > em').get_text().strip() if opinion.select_one('span.user-post__author-recomendation > em') else None,
            'score': opinion.select_one('span.user-post__score-count').get_text().strip(),
            'content': opinion.select_one('div.user-post__text').get_text().strip(),
            'pros': [p.get_text() for p in opinion.select('div.review-feature__item--positive')],
            'cons': [c.get_text() for c in opinion.select('div.review-feature__item--negative')],
            'helpfull': opinion.select_one('button.vote.yes > span').get_text().strip() if opinion.select_one('button.vote.yes > span') else None,
            'unhelpfull': opinion.select_one('button.vote.no > span').get_text().strip() if opinion.select_one('button.vote.no > span') else None,
            'publishing_date': opinion.select_one('span.user-post__published > time:nth-child(1)[datetime]').get('datetime').strip(),
            'purchese_date': opinion.select_one('span.user-post__published > time:nth-child(2)[datetime]').get('datetime').strip() if opinion.select_one('span.user-post__published > time:nth-child(2)[datetime]') else None,
        }
        all_opinions.append(single_opinion)

    # check for page
    next = True if page_dom.select_one("button.pagination__next") else False
    if next: 
        page += 1 
        driver.find_element (by="xpath", value = '//*[@id="reviews"]/div/div[6]/button[4]').click()

##### end of while loop
print(all_opinions)
#save opinions
if not os.path.exists("./opinions"):
    os.mkdir("./opinions")

with open(f"./opinions/{product_code}.json", "w", encoding="UTF-8") as jf:
    json.dump(all_opinions, jf, indent=4, ensure_ascii=False)


print("done !!!")