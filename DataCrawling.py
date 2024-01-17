import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def get_articles_from_url(url, keyword, max_age_hours=24):
    articles = []

    # Get the current date and time
    current_datetime = datetime.now()

    # Fetch the webpage content
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all articles on the page
    articles_list = soup.find_all('li', class_='gs-c-promo')

    for article in articles_list:
        # Extract title and link
        title_element = article.find('h3', class_='gs-c-promo-heading__title')
        link_element = article.find('a', class_='gs-c-promo-heading')

        if title_element and link_element:
            title = title_element.text.strip()
            link = link_element['href']

            # Check if the keyword is present in the title
            if keyword.lower() in title.lower():
                # Extract and parse publication date
                try:
                    publication_date = article.find('time')['data-datetime']
                    article_date = datetime.strptime(publication_date, '%Y-%m-%dT%H:%M:%SZ')

                    # Check if the article was published in the last 24 hours
                    if current_datetime - timedelta(hours=max_age_hours) <= article_date <= current_datetime:
                        articles.append({'title': title, 'link': link})
                except Exception as e:
                    print(f"Error parsing date for article: {title}")
                    print(f"Publication date string: {publication_date}")

    return articles

# Replace this URL with the actual URL you want to scrape
sample_url = 'https://www.bbc.com/news'
keyword = 'accident'

articles = get_articles_from_url(sample_url, keyword)

for article in articles:
    print(f"Title: {article['title']}\nLink: {article['link']}\n")
