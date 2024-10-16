from app.factory import create_bot, create_dispatcher, create_app
from app.secret import *

bot = create_bot(token=TOKEN)
dispatcher = create_dispatcher()
create_app(bot=bot, dispatcher=dispatcher)
