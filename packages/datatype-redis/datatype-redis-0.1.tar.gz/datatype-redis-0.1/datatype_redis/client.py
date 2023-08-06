from .redisclient import RedisClient, Redis
import threading
import contextlib
import copy

_thread = threading.local()
_config = {}


def get_prefix():
    """Returns the current used prefix.

    If prefix is not set in config, it will executes the `configure`-method to get a prefix.

    Prefix can also be empty, but must not be unset.

    Returns:
        string: The current prefix
    """
    global _config

    if "prefix" not in _config:
        configure()

    return _config["prefix"]


def default_client():
    global _config

    try:
        _thread.client
    except AttributeError:
        if not "client" in _config or not "client_config" in _config:
            configure()

        client = _config["client"](**_config["client_config"])
        if not isinstance(client, Redis):
            raise ValueError("Given client is not a Redis-Class.")

        _thread.client = client
    return _thread.client


def configure(**kwargs):
    """
    Configure the client and everything in a central place.
    """
    global _config

    if "client" in kwargs:
        _config["client"] = kwargs["client"]
        del kwargs["client"]
    else:
        _config["client"] = RedisClient

    if "client_config" in _config:
        previous_config = copy.deepcopy(_config)
        _config["client_config"].update(kwargs)
    else:
        previous_config = None
        _config["client_config"] = kwargs

    if "prefix" not in kwargs:
        _config["prefix"] = "datatype_redis"

    if previous_config is not None:
        rename_keys(previous_config["prefix"])


def rename_keys(old_prefix):
    global _config

    """Renames all keys with old prefix, if needed.

    Args:
        old_prefix (string): The old prefix, which will be used in filter

    Returns:
        bool: True if this method rename_key_list at least one key, otherwise False
    """
    client = default_client()

    if old_prefix == _config["client_config"]["prefix"]:
        return False

    rename_key_list = []

    match = "{}/*".format(get_prefix())
    for old_key in client.scan_iter(match=old_prefix):
        new_key = str(old_key).replace(old_prefix, match, 1)
        rename_key_list.append((old_key, new_key))

    with transaction() as client:
        for old_key, new_key in rename_key_list:
            client.rename(old_key, new_key)


@contextlib.contextmanager
def transaction():
    """
    Swaps out the current client with a pipeline instance,
    so that each Redis method call inside the context will be
    pipelined. Once the context is exited, we execute the pipeline.
    """
    client = default_client()
    _thread.client = client.pipeline()
    try:
        yield
        _thread.client.execute()
    finally:
        _thread.client = client

