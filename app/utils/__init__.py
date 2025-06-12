from dotenv import load_dotenv
import os

from app.utils.database import Database

load_dotenv()


db = Database(os.getenv("DATABASE_NAME"))
