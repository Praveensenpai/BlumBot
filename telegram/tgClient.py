from pyrogram.client import Client
from pyrogram.raw.types.input_bot_app_short_name import InputBotAppShortName
from pyrogram.raw.functions.messages.request_app_web_view import RequestAppWebView
from pyrogram.raw.types.input_peer_user import InputPeerUser
from pyrogram.raw.types.app_web_view_result_url import AppWebViewResultUrl
from pyrogram.errors.exceptions import UsernameNotOccupied
from urllib.parse import unquote
from result import Err, Ok, Result
from env import Env
from enum import Enum
import os
import re
from typing import Final
from utils.loggy import logger


class TGClientError(Enum):
    INVALID_PEER_ID = "Invalid peer ID"
    UNABLE_TO_RETRIEVE_QUERY = "Unable to retrieve query string"
    UNKNOWN_ERROR = "Unknown error"


class TGClient(Client):
    WORKDIR: Final[str] = "sessions/"

    def __init__(self):
        self.create_workdir()
        super().__init__(
            name=Env.SESSION_NAME,
            api_id=Env.API_ID,
            api_hash=Env.API_HASH,
            workdir=self.WORKDIR,
        )

    def create_workdir(self) -> None:
        os.makedirs(self.WORKDIR, exist_ok=True)

    async def get_query_string(
        self,
        peer_id: str,
        platform: str = "android",
        short_name: str = "app",
    ) -> Result[str, TGClientError]:
        try:
            async with self:
                user = await self.get_me()
                username = user.username
                logger.success(f"Logged in as @{username}")

                try:
                    bot_peer: InputPeerUser = await self.resolve_peer(peer_id)  # type: ignore
                except UsernameNotOccupied:
                    return Err(TGClientError.INVALID_PEER_ID)

                bot_app: InputBotAppShortName = InputBotAppShortName(
                    bot_id=bot_peer,  # type: ignore
                    short_name=short_name,
                )

                web_view_request: RequestAppWebView = RequestAppWebView(
                    peer=bot_peer,  # type: ignore
                    app=bot_app,  # type: ignore
                    platform=platform,
                    write_allowed=True,
                    start_param=Env.REF_ID,
                )

                web_view: AppWebViewResultUrl = await self.invoke(web_view_request)

                match = re.search(r"tgWebAppData=([^&]+)", web_view.url)
                query = unquote(unquote(match.group(1))) if match else None

                if not query:
                    return Err(TGClientError.UNABLE_TO_RETRIEVE_QUERY)

                return Ok(query)

        except Exception as e:
            logger.error(f"Query Retrieval Failed - Reason: {e}")
            return Err(TGClientError.UNKNOWN_ERROR)
