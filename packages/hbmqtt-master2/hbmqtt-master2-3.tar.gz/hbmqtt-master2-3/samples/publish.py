import logging
import asyncio

from hbmqtt.client import MQTTClient, ConnectException
from hbmqtt.mqtt.constants import QOS_1, QOS_2


#
# This sample shows how to publish messages to broker using different QOS
# Debug outputs shows the message flows
#

logger = logging.getLogger(__name__)

config = {
    'will': {
        'topic': '/will/client',
        'message': b'Dead or alive',
        'qos': 0x01,
        'retain': True
    }
}


@asyncio.coroutine
def coro2():
    try:
        C = MQTTClient()
        yield from C.connect('mqtt://127.0.0.1:1883/')
        for i in range(1,10):
            yield from C.publish('a/b', b'TEST MESSAGE WITH QOS_0', qos=0x00)

        logger.info("messages published")
        yield from C.disconnect()
    except ConnectException as ce:
        logger.error("Connection failed: %s" % ce)
        asyncio.get_event_loop().stop()


if __name__ == '__main__':
    formatter = "[%(asctime)s] %(name)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    #formatter = "%(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)
    #asyncio.get_event_loop().run_until_complete(test_coro())
    asyncio.get_event_loop().run_until_complete(coro2())
