from .base import *

ALLOWED_HOSTS = []

DATABASES = {
    'default' : {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_SERVER_NAME'), # 조금 전 psql 접속하여 만든 Database 이름
        'USER': env('DB_SERVER_USER'), # 서버를 만들때 입력한 관리자 사용자 이름
        'PASSWORD': env('DB_ADMIN_PW'), # 관리자 비밀번호
        'HOST': 'ai-newscape.postgres.database.azure.com', # DB 배포 후 생성된 서버 이름
        'PORT': '5432', # Postgresql 포트 번호
    },
    'OPTIONS': {
        'sslmode': 'require',
    },
}