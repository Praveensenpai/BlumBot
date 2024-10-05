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

    async def _claim_game(self, game_id: str) -> Optional[bool]:
        logger.info("Claiming game")
        points = random.randint(Env.MIN_POINTS, Env.MAX_POINTS)
        json_data = {
            "gameId": game_id,
            "points": points,
        }
        resp = await self.session.post(Endpoints.Game.CLAIM, json=json_data)
        match resp.status_code:
            case 200:
                logger.success(f"Successfully claimed {points} points.")
                return True

    async def _start_game(self) -> Optional[str]:
        logger.info("Starting game")
        resp = await self.session.post(Endpoints.Game.START)
        if resp.status_code == 200:
            return resp.json().get("gameId")

    async def play_game(self) -> Optional[bool]:
        game_id = await self._start_game()
        if not game_id:
            logger.error("Unable to get game ID")
            return
        sleep_time = random.randrange(35, 38)
        logger.info(f"Playing game for {sleep_time} seconds")
        await asyncio.sleep(sleep_time)
        if await self._claim_game(game_id):
            return True
