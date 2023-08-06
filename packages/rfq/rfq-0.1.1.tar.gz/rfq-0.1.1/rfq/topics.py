import rfq.redis


def topics(redis=None):
    r = rfq.redis.default() if redis is None else redis

    keys = []

    keys += [k[len("rfq:") : - len(":backlog")] for k in r.keys("rfq:*:backlog")]
    keys += [k[len("rfq:") : - len(":nextlog")] for k in r.keys("rfq:*:nextlog")]

    keys = list(set(keys))

    return keys
