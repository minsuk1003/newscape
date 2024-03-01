import requests
from bs4 import BeautifulSoup
import re
import datetime
from datetime import date, timedelta
import time
from tqdm import tqdm
import psycopg2
from concurrent.futures import ThreadPoolExecutor
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from requests import get
from bs4 import BeautifulSoup
from tqdm import tqdm
from news_guru.models import News


class Command(BaseCommand):
    help = 'Crawl news and store in the database'

    def handle(self, *args, **options):
        # Use your existing logic for crawling and parsing here
        
        # Connect to your PostgreSQL database
        conn = psycopg2.connect(
            dbname="news_guru", 
            user="root", 
            password="9832", 
            host="localhost", 
            port="5432"
        )
        cur = conn.cursor()

        def make_date_list(start_year):
            global conn
            global cur

            # Query for the most recent date in your articles table
            cur.execute("SELECT MAX(publish_date) FROM news_guru_news")
            result = cur.fetchone()[0]

            if result:
                start_date = datetime.datetime.strptime(result, '%Y%m%d').date() + datetime.timedelta(days=1)
            else:
                start_date = datetime.date(start_year, 1, 1)

            end_date = datetime.date.today()

            date_list = [(start_date + datetime.timedelta(days=x)).strftime('%Y%m%d') for x in range((end_date - start_date).days + 1)]

            return date_list


        def crawl_url(url):
            headers = {'user-agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
            time.sleep(0.02) # Be polite with the server
            rs = requests.get(url, headers=headers)
            if rs.status_code != 200:
                return None
            rs.encoding = 'UTF-8'
            soup = BeautifulSoup(rs.text, 'html.parser')
            title = soup.select_one('#title_area > span').get_text() # Update selector based on the actual page
            content = ' '.join([p.get_text() for p in soup.select('#newsct_article')]) # Update selector
            return title, content

        def save_news_to_db(date, press, title, url, content):
            # Create a new News instance and save it to the database
            News.objects.create(
                publish_date=datetime.datetime.strptime(date, '%Y%m%d').date(),
                press=press,
                title=title,
                url=url,
                content=content
            )

        def news_crawling_and_saving(year):
            press_list = ['032', '005', '020', '021', '081', '022', '023', '025', '028', '469']
            date_list = make_date_list(year)
            headers = {'user-agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}

            for date in tqdm(date_list):
                if date[-2:] == '15':
                    time.sleep(60)
                else:
                    time.sleep(1)
                for press in press_list:
                    url = f'https://media.naver.com/press/{press}/ranking?type=popular&date={date}'
                    rs = requests.get(url, headers=headers)
                    if rs.status_code == 200:
                        soup = BeautifulSoup(rs.text, 'html.parser')
                        links = soup.find_all('a', href=True)
                        for link in links:
                            article_url = link['href']
                            title, content = crawl_url(article_url)
                            if title and content:
                                save_news_to_db(date, press, title, article_url, content)

        # Example usage
        news_crawling_and_saving(2024)

        # Close database connection
        cur.close()
        conn.close()