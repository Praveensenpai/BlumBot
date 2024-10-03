from pyenvloadermeta import EnvLoaderMeta


class Env(metaclass=EnvLoaderMeta):
    SESSION_NAME: str
    API_ID: int
    API_HASH: str
    REF_ID: str
    # MIN_POINTS: int
    # MAX_POINTS: int
