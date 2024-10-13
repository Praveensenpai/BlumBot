from blum.errors import UserBalanceError
from blum.game import GameActions
from blum.farming import FarmingActions
from blum.platform import Platform
from blum.blum_models import UserBalance, ValidationError
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
        self.game = GameActions(self.session)

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

    async def get_user_balance(self) -> UserBalance:
        resp = await self.session.get(Endpoints.User.BALANCE)
        if resp.status_code == 200:
            try:
                usr_balance = UserBalance(**resp.json())
                logger.info(f"Available Balance: {usr_balance.availableBalance}")
                logger.info(f"Play Passes Left: {usr_balance.playPasses}")
                return usr_balance
            except ValidationError as e:
                logger.error(
                    f"Error Getting User Balance - Reason: Validation error: {e}"
                )

        logger.error(f"Error getting User balance : Status Code - {resp.status_code}")
        logger.error("Failed to retrieve User balance.")
        raise UserBalanceError("Failed to retrieve User balance.")

    async def claim_daily_reward(self) -> bool:
        resp = await self.session.post(Endpoints.CLAIM_DAILY_REWARDS)
        match resp.status_code:
            case 200:
                logger.info("Successfully claimed daily reward")
                return True
            case 400:
                logger.info("Already claimed daily reward [Status]")
                return True
            case _:
                logger.error(
                    f"Failed to claim daily rewards. Status Code: {resp.status_code}"
                )
                return False
