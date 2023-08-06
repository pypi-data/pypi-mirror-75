import json

from rfq.rfq import Queue


def main(args):
    topic = args.topic
    message = json.loads(args.message)

    q = Queue()

    msgid = q.publish(topic=topic, message=message)

    print(msgid)
