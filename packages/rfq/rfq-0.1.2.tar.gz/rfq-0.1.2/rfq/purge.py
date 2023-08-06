import rfq.redis


def purge(topic, queue, redis=None):
    r = rfq.redis.default() if redis is None else redis

    msgids = []

    while True:
        msgid = r.rpop("rfq:{topic}:{queue}".format(topic=topic, queue=queue))

        if msgid is None:
            break

        r.delete("rfq:{topic}:message:{msgid}".format(topic=topic, msgid=msgid))

        msgids.append(msgid)

    return msgids
