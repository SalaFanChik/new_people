from aiogram import Bot, Dispatcher, types
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from handlers import start, admin_commands  # Импортируем ваши обработчики команд из модуля handlers
from middlewares import DbSessionMiddleware, ThrottlingMiddleware
from fastapi import FastAPI, Request
import logging
from contextlib import asynccontextmanager
from db.db_helper import db_helper
from admin.views import router as admin_router
from fastapi.staticfiles import StaticFiles


TOKEN = "5223424400:AAFAhZrmU_uuk9409pZkccBTuaRYuRait3U"

WEBHOOK_PATH = f"/bot/{TOKEN}"
NGROK_URL = "https://a0e2-212-96-80-141.ngrok-free.app"
WEBHOOK_URL = NGROK_URL + WEBHOOK_PATH




logging.basicConfig(filemode='a', level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

@asynccontextmanager
async def lifespan(app: FastAPI):
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(
            url=WEBHOOK_URL
        )
    yield 
    await bot.delete_webhook()

app = FastAPI(lifespan=lifespan)

app.include_router(admin_router)


dp.update.middleware(DbSessionMiddleware(session_pool=db_helper.session_factory))

dp.message.middleware(ThrottlingMiddleware())

dp.callback_query.middleware(CallbackAnswerMiddleware())


dp.include_router(start.router)
dp.include_router(admin_commands.router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.post(WEBHOOK_PATH)
async def bot_webhook(Update: types.Update, request: Request):
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot=bot, update=update)

@app.get("/")
def main_web_handler():
    return "Everything ok!"



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)