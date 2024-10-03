from typing import Final


class Auth:
    LOGIN: Final[str] = (
        "https://user-domain.blum.codes/api/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP"
    )


class Farming:
    START: Final[str] = "https://game-domain.blum.codes/api/v1/farming/start"
    CLAIM: Final[str] = "https://game-domain.blum.codes/api/v1/farming/claim"


class User:
    BALANCE: Final[str] = "https://game-domain.blum.codes/api/v1/user/balance"


class Game:
    CLAIM: Final[str] = "https://game-domain.blum.codes/api/v1/game/claim"
    START: Final[str] = "https://game-domain.blum.codes/api/v1/game/play"


class Endpoints:
    Auth = Auth()
    Farming = Farming()
    User = User()
    Game = Game()
