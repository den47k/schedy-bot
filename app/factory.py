from dotenv import load_dotenv
import os

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from app.handlers import router

from aiohttp import web

load_dotenv()

async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(f"{os.getenv("BASE_WEBHOOK_URL")}{os.getenv("WEBHOOK_PATH")}",
                          drop_pending_updates=True)


async def on_shutdown(bot: Bot) -> None:
    await bot.delete_webhook()


def create_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher()

    dispatcher.include_router(router)
    dispatcher.startup.register(on_startup)

    return dispatcher


def create_bot(token: str) -> Bot:
    return Bot(token=token, parse_mode=ParseMode.HTML)


def create_app(bot: Bot, dispatcher: Dispatcher):

    app = web.Application()

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dispatcher,
        bot=bot
    )

    webhook_requests_handler.register(app, path=os.getenv("WEBHOOK_PATH"))

    setup_application(app, dispatcher, bot=bot)

    web.run_app(app, host=os.getenv("WEB_SERVER_HOST"), port=int(os.getenv("WEB_SERVER_PORT")))

    return app
