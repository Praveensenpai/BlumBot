from typing import Optional
import httpx
from blum.endpoints import Endpoints
from utils.dt import current_dt_ms
from utils.loggy import logger


class FarmingActions:
    def __init__(self, session: httpx.AsyncClient):
        self.session = session

    async def start(self) -> Optional[bool]:
        resp = await self.session.post(Endpoints.Farming.START)
        match resp.status_code:
            case 200:
                is_started = (
                    abs((resp.json().get("startTime") - current_dt_ms()) / 1000) < 60
                )
                logger.success(
                    "Farming started successfully"
                    if is_started
                    else "Farming is already started"
                )
                return is_started
            case _:
                logger.error(
                    f"Failed to start farming. Status Code : {resp.status_code}"
                )

    async def claim(self):
        resp = await self.session.post(Endpoints.Farming.CLAIM)
        match resp.status_code:
            case 425:
                logger.warning("Farming is already claimed.")
            case 200:
                logger.success("Successfully claimed.")
                logger.success(
                    f"Available Balance: {resp.json().get('availableBalance')}",
                )
            case 412:
                logger.warning("Farming is not started yet.")
