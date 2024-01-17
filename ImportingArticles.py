import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def get_articles_from_toi(keyword, num_pages):
    base_url = f'https://timesofindia.indiatimes.com/topic/{keyword}/news'
    articles = []

    # Get the current date and time
    current_datetime = datetime.now()

    for page in range(1, num_pages + 1):
        url = f'{base_url}/{page}'
        print(f"Fetching articles from: {url}")
        response = requests.get(url)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract title of the webpage
        webpage_title = soup.title.text
        print(f"Webpage title: {webpage_title}")
        
        article_elements = soup.find_all('span', class_='title')
        
        for article_element in article_elements:
            title = article_element.get_text().strip()
            link = article_element.find('a')['href']
            
            # Extracting and formatting the publication date from the article page
            article_page_url = f'https://timesofindia.indiatimes.com{link}'
            article_response = requests.get(article_page_url)
            article_soup = BeautifulSoup(article_response.text, 'html.parser')
            article_date_element = article_soup.find('div', class_='publish_on')
            print(f"Checking article: {title} - {article_page_url}")

            try:
                if article_date_element:
                    article_date_str = article_date_element.get_text().strip()
                    
                    # Parse the date string into a datetime object
                    article_date = datetime.strptime(article_date_str, '%d %b %Y, %H:%M')
                    
                    # Check if the article was published in the last 24 hours
                    if current_datetime - timedelta(hours=24) <= article_date <= current_datetime:
                        articles.append({'title': title, 'link': article_page_url})
                else:
                    print(f"Publication date not found for {title} - {article_page_url}")
            except Exception as e:
                print(f"Error processing article: {title} - {article_page_url}")
                print(f"Error details: {e}")

    return articles

# Replace 'Accident' with the actual keyword you are looking for.
keyword = 'Accident'
num_pages_to_scrape = 3  # Adjust as needed

articles = get_articles_from_toi(keyword, num_pages_to_scrape)

for article in articles:
    print(f"Title: {article['title']}\nLink: {article['link']}\n")
