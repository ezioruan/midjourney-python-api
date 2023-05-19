from midjourney.Midjourney import MidjourneyClient
import pprint

import time


def process_message(message):
    pprint.pprint(message)


def main():
    client = MidjourneyClient(
        name="test",
        token="",  # your discord token
        application_id="",  # bot application_id
        guild_id="",  # your discord server id or None
        channel_id="",  # your channel_id
        message_handler=process_message,
    )
    client.run()
    time.sleep(3)

    # get info of the Client
    client.info()

    client.imagine("Imagine a world where you can do this")

    client.interact(message_id="", label="U1")


if __name__ == "__main__":
    main()
