import requests
from bs4 import BeautifulSoup
import re
import string
import os

# Save contents to file:
def save_file(text, title, save_path):
    file = open(save_path + "\\" + title + '.txt', 'w')
    file.write(text)
    file.close()
    return  title + '.txt'
    # print(title + '.txt')


def get_article(article_url):
    r = requests.get(article_url)
    if r:
        page_content = r.content
        soup_art = BeautifulSoup(page_content, "html.parser")
        return soup_art

    else:
        print(f'The URL returned {r.status_code}')
        return ""


# print("Input the URL:")
# url = input()
pages = int(input())
article_type = input()
def scrap_page(url, page, article_type, save_path):
    saved = []
    if url.find("nature") != -1:
        dic_ = {}
        # r = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
        r = requests.get(url + "&page=" + str(page))
        if r:
            try:
                soup = BeautifulSoup(r.content, "html.parser")
                # title = soup.title
                # meta = soup.find("meta", {"name": "description"})
                # dic_["title"] = title.text
                # dic_["description"] = meta.get("content")
                # print(soup.prettify())
            except Exception:
                print("Invalid quote resource!")
            article_tags = soup.find_all("article")
            news_articles = [article for article in article_tags
                             if article.find("span", {"data-test": "article.type"}).text == article_type]
            articles_urls = [str("https://nature.com" + article.find("a", {"data-track-action": "view article"}).get("href"))
                        for article in news_articles]
            titles = [title.find("a").text for title in news_articles]
            for i, title in enumerate(titles):
                titles[i] = titles[i].translate(str.maketrans('’—‘', '   ', string.punctuation))
                titles[i] = re.sub(" +", " ", titles[i])
                titles[i] = titles[i].strip().replace(" ", "_")
            for article, title in zip(articles_urls, titles):
                article_body = get_article(article)
                full_text = article_body.find("div", {"class": "c-article-body main-content"})
                if full_text is not None:
                    article_body = full_text.text.strip()
                    article_body = re.sub("\n{2,}", "\n", article_body)
                else:
                    article_body = article_body.find("p", {"class": "article__teaser"}).text.strip()
                article_body = re.sub("\n{2,}", "\n", article_body)
                saved.append(save_file(article_body, title, save_path))
        else:
            print("Invalid page!")
    else:
        print("Invalid page!")
    return saved

for j in range(1, pages+1):
    save_path = os.getcwd() + "\\Page_" + str(j)
    if not os.path.isdir(save_path):
        os.mkdir(save_path)
    saved_files = scrap_page("https://www.nature.com/nature/articles?sort=PubDate&year=2020", j, article_type, save_path)
    print("Page ", str(j), "Saved articles:", saved_files)
print("Saved all articles.")



