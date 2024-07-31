import sys, logging, asyncio, os, random
from aiogram import Bot, Dispatcher
from aiogram.types import FSInputFile
from dotenv import load_dotenv
from app.handlers import router
from app.database import async_main
from app.repositories import UserRepository
from apscheduler.schedulers.asyncio import AsyncIOScheduler


load_dotenv()

scheduler = AsyncIOScheduler()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)

async def scheduled_broadcast():

    photo1 = FSInputFile("app/media/hello.jpg")
    photo2 = FSInputFile("app/media/have_a_nice_day.jpg")

    users = await UserRepository.get_all_users_from_sendlist()

    for user in users:
        user_id = user.user_id

        selected_post = random.choice([1, 2]) # случайным образом выбирается один пост для отправки пользователям

        if selected_post == 1:
            await bot.send_photo(chat_id=user_id, photo=photo1, caption="Привет! Это рекламный пост №1!")
        elif selected_post == 2:
            await bot.send_photo(chat_id=user_id, photo=photo2, caption="Удачного дня! Это рекламный пост №2!")

async def main():
    await async_main()

    dp = Dispatcher()
    dp.include_router(router)

    # рассылка рекламных постов через scheduler для всех людей которые есть в базе данных в таблице sendler
    scheduler.add_job(scheduled_broadcast, 'interval', hours=1) # есть вариант с параметром minutes и seconds вместо hours
    scheduler.start()

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout) # логирование
    try: asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
