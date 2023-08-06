from redis import Redis


class RedisClient(Redis):
    """
    A Redis client wrapper
    """

    def __init__(self, *args, **kwargs):
        #kwargs.setdefault("decode_responses", True)
        kwargs.setdefault("encoding", 'utf-8')
        super().__init__(*args, **kwargs)
