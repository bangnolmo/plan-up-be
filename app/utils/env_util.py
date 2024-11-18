from dotenv import load_dotenv
import os

load_dotenv()

SERVER_PORT = int(os.getenv("SERVER_PORT", 8000))
FRONT_URL = os.getenv("FRONT_URL")