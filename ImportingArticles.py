import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import dateparser

def get_articles_from_url(url):
    articles = []

    # Get the current date and time
    current_datetime = datetime.now()

    print(f"Fetching articles from: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all div elements with class 'gs-c-promo'
    article_containers = soup.find_all('div', class_='gs-c-promo')
    
    for container in article_containers:
        # Extract title, link, and publication date
        title = container.find('h3').get_text().strip()
        link = container.find('a')['href']

        # Handle the date format, including relative time
        try:
            publication_date_str = container.find('time')['data-datetime']
            if 'ago' in publication_date_str:
                article_date = datetime.now() - dateparser.parse(publication_date_str)
            else:
                article_date = datetime.strptime(publication_date_str, '%Y-%m-%dT%H:%M:%SZ')
        except (ValueError, TypeError) as e:
            print(f"Error parsing date for article: {title}")
            print(f"Publication date string: {publication_date_str}")
            article_date = None

        # Check if the article was published in the last 24 hours
        if article_date and current_datetime - timedelta(hours=24) <= article_date <= current_datetime:
            articles.append({'title': title, 'link': link})

    return articles

# Use a sample URL with articles
sample_url = 'https://www.bbc.com/news'
articles = get_articles_from_url(sample_url)

for article in articles:
    print(f"Title: {article['title']}\nLink: {article['link']}\n")
