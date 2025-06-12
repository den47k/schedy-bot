from dotenv import load_dotenv
import os

from app.factory import create_bot, create_dispatcher, create_app

load_dotenv()

bot = create_bot(token=os.getenv("TOKEN"))
dispatcher = create_dispatcher()
create_app(bot=bot, dispatcher=dispatcher)
