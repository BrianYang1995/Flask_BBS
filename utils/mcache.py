from memcache import Client

client = Client(['127.0.0.1:11211'], debug=True)


def set(key, val, timeout=120):

    client.set(key, val, timeout)


def get(key):
    return client.get(key)


def delete(key):
    return client.delete(key)

