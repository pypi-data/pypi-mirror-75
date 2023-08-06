import uuid

import rfq.redis


def publish(topic, message, redis=None):
    r = rfq.redis.default() if redis is None else redis

    msgid = uuid.uuid1().hex

    with r.pipeline() as tx:
        tx.hmset("rfq:{topic}:message:{msgid}".format(topic=topic, msgid=msgid), message)
        tx.lpush("rfq:{topic}:backlog".format(topic=topic), msgid)

        tx.execute()

    return msgid
