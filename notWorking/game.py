import random
from typing import Optional
import asyncio

import httpx
from blum.endpoints import Endpoints
from env import Env
from utils.loggy import logger


class GameActions:
    def __init__(self, session: httpx.AsyncClient):
        self.session = session

    async def claim_game(self, game_id: str):
        logger.info("Claiming game")
        json_data = {
            "gameId": game_id,
            "points": random.randint(Env.MIN_POINTS, Env.MAX_POINTS),
        }
        logger.info(json_data)

        resp = await self.session.post(Endpoints.Game.CLAIM, json=json_data)
        logger.success(resp)
        logger.success(resp.text)
        logger.success(resp.json())

    async def start_game(self) -> Optional[str]:
        logger.info("Starting game")
        resp = await self.session.post(Endpoints.Game.START)
        logger.success(resp)
        logger.success(resp.json())
        if resp.status_code == 200:
            return (await resp.json()).get("gameId")

    async def play_game(self):
        game_id = await self.start_game()
        if not game_id:
            return
        sleep_time = random.randrange(35, 38)
        logger.info(f"Playing game for {sleep_time} seconds")
        await asyncio.sleep(sleep_time)
        await self.claim_game(game_id)
