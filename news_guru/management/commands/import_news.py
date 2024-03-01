"""import csv
from django.core.management.base import BaseCommand
from news_guru.models import News

class Command(BaseCommand):
    help = 'Import news data from CSV file'

    def handle(self, *args, **kwargs):
        csv_file_path = "C:/Users/kms10/OneDrive - 경희대학교/지식경영학회/news_content_processed_data.csv"  # CSV 파일 경로 설정
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # 첫 번째 행은 헤더이므로 스킵
            for row in reader:
                news_id, create_date, press, title, url, content, gpt_background = row
                News.objects.create(id=news_id, title=title, content=content, create_date=create_date, press=press, gpt_background=gpt_background)

        self.stdout.write(self.style.SUCCESS('Successfully imported news data'))
"""