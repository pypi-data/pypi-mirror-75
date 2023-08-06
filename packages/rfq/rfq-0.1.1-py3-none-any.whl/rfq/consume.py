import rfq.redis


def consume(topic, redis=None):
    r = rfq.redis.default() if redis is None else redis

    msgid = r.brpoplpush("rfq:{topic}:backlog".format(topic=topic),
                         "rfq:{topic}:nextlog".format(topic=topic))

    msg = r.hgetall("rfq:{topic}:message:{msgid}".format(topic=topic, msgid=msgid))

    return msgid, msg


def commit(topic, msgid, redis=None):
    r = rfq.redis.default() if redis is None else redis

    with r.pipeline() as tx:
        tx.lrem("rfq:{topic}:nextlog".format(topic=topic), 0, msgid)
        tx.delete("rfq:{topic}:message:{msgid}".format(topic=topic, msgid=msgid))

        tx.execute()

    return msgid
