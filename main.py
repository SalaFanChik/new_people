import asyncio
from aiogram import Bot, Dispatcher
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from handlers import start, admin_commands  # Импортируем ваши обработчики команд из модуля handlers
from middlewares import DbSessionMiddleware


# Основная асинхронная функция, запускающая бота
async def main():
    # Создаем асинхронный движок базы данных и объект для асинхронных сессий
    engine = create_async_engine(url="postgresql+asyncpg://alik:alik2006@localhost:5432/new_people_db", echo=True)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    # Инициализируем объект бота с токеном и режимом парсинга сообщений (HTML)
    bot = Bot("6094011146:AAEll5hKivf2SyLhK7LEULzuVcwEXO24tr8", parse_mode="HTML")
    
    # Инициализируем диспетчер для обработки входящих сообщений и команд
    dp = Dispatcher()

    # Привязываем мидлвар DbSessionMiddleware к диспетчеру для работы с асинхронными сессиями базы данных
    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))

    # Привязываем мидлвар CallbackAnswerMiddleware к обработчику коллбэков для автоматического ответа на коллбэки
    dp.callback_query.middleware(CallbackAnswerMiddleware())

    # Регистрируем обработчики команд из ваших модулей (handlers)
    dp.include_router(start.router)
    dp.include_router(admin_commands.router)
    # Очищаем все ожидающие обновления перед запуском
    await bot.delete_webhook(drop_pending_updates=True)

    # Запускаем бота с использованием long polling и обрабатываем только те типы обновлений, которые обрабатываются в вашем диспетчере
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

# Проверяем, запущен ли этот скрипт напрямую (не импортирован ли он как модуль)
if __name__ == "__main__":
    # Запускаем основную асинхронную функцию main() с помощью asyncio.run()
    asyncio.run(main())
