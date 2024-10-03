from datetime import datetime


def milliseconds_to_dt(ms: int) -> datetime:
    return datetime.fromtimestamp(ms / 1000)


def time_diff_in_seconds(dt2: datetime, dt1: datetime) -> float:
    return (dt2 - dt1).total_seconds()


def current_dt_ms() -> float:
    return datetime.now().timestamp() * 1000
