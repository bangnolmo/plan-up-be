from dotenv import load_dotenv
import os



load_dotenv()

SERVER_PORT = int(os.getenv("SERVER_PORT", 8000))
FRONT_URL = os.getenv("FRONT_URL", "http://localhost:3000")

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_NAME = os.getenv("DB_NAME")
DB_PASS = os.getenv("DB_PASS")
DB_PORT = int(os.getenv("DB_PORT", 3306))

CRAWL_AUTH = os.getenv("CRAWL_AUTH", 'test')

GOOGLE_OAUTH_ID = os.getenv("GOOGLE_OAUTH_ID")
GOOGLE_OAUTH_SECRET = os.getenv("GOOGLE_OAUTH_SECRET")
GOOGLE_REDIRECT = os.getenv("GOOGLE_REDIRECT")