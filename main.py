import asyncio
from contextlib import suppress
import datetime
from random import randint
import time
from blum import Blum
from blum.blum_models import UserBalance
from blum.errors import UserBalanceError, LoginError, FarmingTaskError
from telegram.tgClient import TGClient
from utils.loggy import logger
from utils.dt import milliseconds_to_dt, time_diff_in_seconds
from timecalculator import TimeCalculator


class BlumBot:
    def __init__(self, bot_name: str):
        self.blum = Blum(bot_name)

    async def fetch_user_balance(self) -> UserBalance:
        usr_balance = await self.blum.get_user_balance()
        if not usr_balance:
            logger.error("Failed to retrieve user balance.")
            raise UserBalanceError("Failed to retrieve user balance.")
        return usr_balance

    async def calculate_next_farming_dates(
        self, farming_end_time: int
    ) -> datetime.datetime:
        farming_enddt = milliseconds_to_dt(farming_end_time)
        farming_enddt_delayed = farming_enddt + datetime.timedelta(
            minutes=randint(10, 30)
        )
        logger.info(f"Next Farming Date: {farming_enddt}")
        logger.info(f"Next Farming Date (delayed): {farming_enddt_delayed}")
        return farming_enddt_delayed

    async def farming_task(self) -> None:
        await asyncio.sleep(5)
        await self.blum.farming.start()
        await asyncio.sleep(5)

        usr_balance = await self.fetch_user_balance()
        farming_enddt_delayed = await self.calculate_next_farming_dates(
            usr_balance.farming.endTime
        )
        sleep_till = time_diff_in_seconds(
            farming_enddt_delayed, datetime.datetime.now()
        )
        if sleep_till > TimeCalculator.HOUR * 8:
            logger.info(
                "Sleeping duration is greater than 8 hours so adjusted to 8 hours sleep"
            )
        sleep_till = min(sleep_till, TimeCalculator.HOUR * 8)
        if sleep_till > 0:
            logger.info(f"Sleeping for {sleep_till} seconds")
            await asyncio.sleep(sleep_till)
            return

        await asyncio.sleep(5)
        await self.blum.farming.claim()

    async def handle_error(self, e: Exception):
        match e:
            case LoginError():
                logger.error("Login error occurred.")
            case UserBalanceError():
                logger.error("User balance error occurred.")
            case FarmingTaskError():
                logger.error("Farming task error occurred.")
            case _:
                logger.error(f"An unexpected error occurred: {e}")

    async def main(self):
        while True:
            try:
                is_logged_in = await self.blum.login(TGClient())
                if not is_logged_in:
                    logger.error("Failed to log in.")
                    raise LoginError("Failed to log in.")
                await self.farming_task()

            except (LoginError, UserBalanceError, FarmingTaskError) as e:
                logger.error(f"An error occurred: {e}")
                await self.handle_error(e)
                logger.info(f"Sleepng for {TimeCalculator.HOUR * 1} seconds")
                await asyncio.sleep(TimeCalculator.HOUR * 1)

            except Exception as e:
                logger.error(f"An unexpected error occurred: {e}")
                await self.handle_error(e)
                logger.info(f"Sleepng for {TimeCalculator.HOUR * 1} seconds")
                await asyncio.sleep(TimeCalculator.HOUR * 1)

            logger.info(
                f"Rest Period: Sleepng for {TimeCalculator.HOUR * 0.25} seconds"
            )
            await asyncio.sleep(TimeCalculator.HOUR * 0.25)

    def run(self):
        while True:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(self.main())
            except Exception as e:
                logger.error(f"Restarting event loop due to error: {e}")
            finally:
                with suppress(Exception):
                    loop.close()
                logger.info("Restarting the main loop...")
                time.sleep(10)


if __name__ == "__main__":
    bot = BlumBot("BlumCryptoBot")
    bot.run()
