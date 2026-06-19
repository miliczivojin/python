import requests

from bs4 import BeautifulSoup
from bs4.element import Tag
from pathlib import Path

start_url = "https://ultimateclassicrock.com/search/?s=pink%20floyd"

response = requests.get(start_url, allow_redirects=False)
response_text = response.text

response_soup = BeautifulSoup(response_text, features="html.parser")


def get_soup(url: str) -> BeautifulSoup:
    response = requests.get(url, allow_redirects=True)
    response_text = response.text

    return BeautifulSoup(response_text, features="html.parser")


soup = get_soup(start_url)

html = Path.cwd() / "pandas_labs" / "data" / "soup.html"
html.write_text(str(soup), encoding="utf-8", errors="replace")

soup.find("article")
soup.find("article").find("a")
soup.find("span", {"class": "visually-hidden"})
text = soup.find("span", {"class": "visually-hidden"}).text
articles_all = soup.find_all("article")
time = soup.find("time")

from selenium import webdriver

driver = webdriver.Edge()

driver.get(start_url)
selenium_soup = BeautifulSoup(driver.page_source, features="html.parser")

html = Path.cwd() / "pandas_labs" / "data" / "selenium_soup.html"
html.write_text(str(selenium_soup), encoding="utf-8", errors="replace")


def get_soup_selenium(url: str) -> BeautifulSoup:
    driver = webdriver.Edge()
    driver.get(url)

    return BeautifulSoup(driver.page_source, features="html.parser")


soup_selenium = get_soup_selenium(start_url)

articles = soup_selenium.find_all("article")
article = soup_selenium.article.text
# klasa = soup_selenium.article["class"]
klasa = soup_selenium.article.get("class")

spanovi = soup_selenium.find("div", {"class": "rowline clearfix"}).span.find_next_siblings()

articles.pop(10)


def get_specific_page(url: str, page=1) -> str:
    return url if page == 1 else url.split("&searchpage=")[0] + "&searchpage=" + str(page)


def get_next_soup(url: str, page=1) -> BeautifulSoup:
    return get_soup_selenium(get_specific_page(url, page))


def crawl(url: str, max_pages=1):
    for page in range(1, max_pages + 1):
        yield get_next_soup(url, page)


gen = crawl(start_url, 2)
while True:
    try:
        print(next(gen))
    except StopIteration:
        break


def get_article_info(article: Tag):
    content = article.find("div", {"class": "content"})
    image = article.find("div", {"class": "article-image-wrapper"})

    title = content.a.text
    author = content.em.text.split("by")[-1].strip()
    date = content.time.text
    img = image.img.get("src")

    return title, author, date, img


def get_article_info_list(url: str, max_pages=1):
    article_info = []
    generator = crawl(url, max_pages)

    while True:
        try:
            articles = next(generator).find_all("article")[:-1]
            for article in articles:
                article_info.append(get_article_info(article))
        except StopIteration:
            break

    return article_info


article_list = get_article_info_list(start_url, 2)

import pandas as pd

pdlist = pd.DataFrame(article_list, columns=["title", "author", "date", "img_url"])
pdlist.to_csv(Path.cwd() / "pandas_labs" / "data" / "articles.csv", index=False)
