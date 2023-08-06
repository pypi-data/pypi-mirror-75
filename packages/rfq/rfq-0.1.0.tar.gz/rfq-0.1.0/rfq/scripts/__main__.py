import argparse

import rfq.scripts.topics
import rfq.scripts.listq
import rfq.scripts.publish
import rfq.scripts.consume
import rfq.scripts.harvest
import rfq.scripts.purge


def main():
    parser = argparse.ArgumentParser(prog="rfq")

    subcmd = parser.add_subparsers(dest="command")
    subcmd.required = True

    Formatter = argparse.ArgumentDefaultsHelpFormatter

    topics = subcmd.add_parser("list-topics", help="lists all active message topics", formatter_class=Formatter)
    topics.set_defaults(main=rfq.scripts.topics.main)

    listq = subcmd.add_parser("list-queue", help="lists messages in a queue", formatter_class=Formatter)
    listq.add_argument("--topic", type=str, required=True, help="topic to list queue for")
    listq.add_argument("--queue", type=str, choices=("backlog", "nextlog"), default="backlog", help="queue to list")
    listq.set_defaults(main=rfq.scripts.listq.main)

    purge = subcmd.add_parser("purge-queue", help="purges messages in a queue", formatter_class=Formatter)
    purge.add_argument("--topic", type=str, required=True, help="topic to purge queue for")
    purge.add_argument("--queue", type=str, choices=("backlog", "nextlog"), default="backlog", help="queue to purge")
    purge.set_defaults(main=rfq.scripts.purge.main)

    publish = subcmd.add_parser("publish", help="publishes a message to a topic", formatter_class=Formatter)
    publish.add_argument("--topic", type=str, required=True, help="topic to publish message to")
    publish.add_argument("--message", type=str, required=True, help="message to publish")
    publish.set_defaults(main=rfq.scripts.publish.main)

    consume = subcmd.add_parser("consume", help="consumes a message from a topic", formatter_class=Formatter)
    consume.add_argument("--topic", type=str, required=True, help="topic to publish message to")
    consume.set_defaults(main=rfq.scripts.consume.main)

    harvest = subcmd.add_parser("harvest", help="moves stale messages from nextlog to backlog", formatter_class=Formatter)
    harvest.add_argument("--topic", type=str, required=True, help="topic to harvest nextlog for")
    harvest.set_defaults(main=rfq.scripts.harvest.main)

    args = parser.parse_args()
    args.main(args)


if __name__ == "__main__":
    main()
