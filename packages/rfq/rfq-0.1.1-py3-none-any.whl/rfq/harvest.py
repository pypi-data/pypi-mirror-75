import rfq.redis


def harvest(topic, redis=None):
    r = rfq.redis.default() if redis is None else redis

    msgids = []

    while True:
        msgid = r.rpoplpush("rfq:{topic}:nextlog".format(topic=topic),
                            "rfq:{topic}:backlog".format(topic=topic))

        if msgid is None:
            break

        msgids.append(msgid)

    return msgids
