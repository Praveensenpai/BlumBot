from pydantic import BaseModel, ValidationError


class Farming(BaseModel):
    startTime: int
    endTime: int
    earningsRate: float
    balance: float


class UserBalance(BaseModel):
    availableBalance: float
    playPasses: int
    isFastFarmingEnabled: bool
    timestamp: int
    farming: Farming
