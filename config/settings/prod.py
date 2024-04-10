from .base import *
import environ

ALLOWED_HOSTS = ['54.197.65.187', 'newscapes.org']
STATIC_ROOT = BASE_DIR / 'static/'
STATICFILES_DIRS = []
DEBUG = True

env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

# SERVER
DATABASES = {
    'default' : {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
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