import logging
import asyncio

from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_1, QOS_2,QOS_0

logger = logging.getLogger(__name__)

@asyncio.coroutine
def coro():
    C = MQTTClient()
    yield from C.connect('mqtt://127.0.0.1:1883')
    yield from C.subscribe([('a/b', QOS_0)])
    logger.info("Subscribed")
    try:
        for i in range(1, 20):
            message = yield from C.deliver_message()
            packet = message.publish_packet
            print("%d: %s => %s" % (i, packet.variable_header.topic_name, str(packet.payload.data)))
        yield from C.unsubscribe(['a/b'])
        logger.info("UnSubscribed")
        yield from C.disconnect()
    except ClientException as ce:
        logger.error("Client exception: %s" % ce)

if __name__ == '__main__':
    formatter = "[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=formatter)
    asyncio.get_event_loop().run_until_complete(coro())
