# from blum.game import GameActions
from blum.farming import FarmingActions
from blum.platform import Platform
from blum.blum_models import UserBalance
from fake_useragent import UserAgent
import httpx
from typing import Optional
from blum.endpoints import Endpoints
from env import Env
from telegram.tgClient import TGClient
from utils.loggy import logger


class Blum:
    def __init__(
        self,
        peer_id: str,
        platform: Platform = Platform.ANDROID,
        http_timeout: float = 60 * 2,
    ) -> None:
        self.peer_id = peer_id
        self.session = httpx.AsyncClient(
            timeout=http_timeout,
            headers={
                "User-Agent": UserAgent(os=platform.value).random,
            },
        )
        self.farming = FarmingActions(self.session)
        # self.game = GameActions(self.session)

    async def login(self, tg_client: TGClient) -> bool:
        self.session.headers.pop("Authorization", None)
        query = await tg_client.get_query_string(self.peer_id)

        if query.is_err():
            logger.error(f"Query Retrieval Failed - Reason: {query.value}")
            return False

        resp = await self.session.post(
            Endpoints.Auth.LOGIN,
            json={
                "query": query.value,
                "referralToken": Env.REF_ID,
            },
        )

        if resp.status_code != 200:
            logger.error(f"Login Failed - Status Code: {resp.status_code}")
            return False

        token: dict = resp.json().get("token", {})
        access_token: Optional[str] = token.get("access")

        if not access_token:
            logger.error("Login Failed - Invalid Token")
            return False

        self.session.headers["Authorization"] = f"Bearer {access_token}"
        return True

    async def get_user_balance(self) -> Optional[UserBalance]:
        resp = await self.session.get(Endpoints.User.BALANCE)
        if resp.status_code == 200:
            return UserBalance(**resp.json())
        logger.error(f"Error getting user balance : Status Code - {resp.status_code}")
