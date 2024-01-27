#This is importing links but without time 

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_articles_from_url(url):
    articles = []

    print(f"Fetching articles from: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all div elements with class 'gs-c-promo'
    article_containers = soup.find_all('div', class_='gs-c-promo')
    
    for container in article_containers:
        # Extract title
        title = container.find('h3').get_text().strip()

        # Extract link using a more general approach
        link_element = container.find('a')
        if link_element and 'href' in link_element.attrs:
            link = urljoin(url, link_element['href'])
        else:
            link = None

        # Append to the list
        articles.append({'title': title, 'link': link})

    return articles

# Use a sample URL with articles
sample_url = 'https://www.bbc.com/news'
articles = get_articles_from_url(sample_url)

for article in articles:
    print(f"Title: {article['title']}\nLink: {article['link']}\n")
