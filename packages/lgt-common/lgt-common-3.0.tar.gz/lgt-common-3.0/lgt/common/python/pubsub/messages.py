import datetime
import env
import json
import time
from google.cloud import pubsub_v1
from loguru import logger
from bson import ObjectId

project_id = os.environ.get('PUBSUB_PROJECT_ID')
bot_manager_pubsub_topic = os.environ.get('BOT_MANAGER_TOPIC')
smtp_pubsub_topic = os.environ.get('SMTP_PUBSUB_TOPIC')
analytics_pubsub_topic = os.environ.get('ANALYTICS_PUBSUB_TOPIC')

def _publish_message2_pubsub(topic_name, message_json):
    def callback(message_future):
        try:
            pubsub_result = message_future.result()
            # When timeout is unspecified, the exception method waits indefinitely.
            if message_future.exception(timeout=60):
                logger.error(f'Publishing message on {topic_name} threw an Exception {message_future.exception()}.')
            else:
                logger.info('lgt-metric:lgt-slack-aggregator:pub-sub:message-sent')
                logger.info(pubsub_result)
        except Exception:
            logger.error(f'Error has happening during getting result of future message')

    attempt = 0
    while True:
        try:
            publisher = pubsub_v1.PublisherClient()
            topic_path = publisher.topic_path(project_id, topic_name)
            logger.info(f'Json: {message_json}')
            message = publisher.publish(topic_path, data=bytes(message_json, "utf8"))
            message.add_done_callback(callback)
            result = message.result()
            logger.info(f'Message has been sent {result}')
            return
        except:
            attempt = attempt + 1
            if attempt >= 3:
                raise
            time.sleep(3)


def _json_converter(o):
    if isinstance(o, datetime.datetime):
        return o.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
    if isinstance(o, ObjectId):
        return str(o)


class PatchBotsMessage:
    def __init__(self, bots):
        self.bots = bots

    def send(self):
        message_json = json.dumps(self.__dict__, ensure_ascii=False, default=_json_converter)
        _publish_message2_pubsub(bot_manager_pubsub_topic, message_json)


class SmtpMessage:
    def __init__(self, html, recipient, subject, sender=None):
        super().__init__()
        self.html = html
        self.recipient = recipient
        self.subject = subject
        self.sender = sender

    def send(self):
        message_json = json.dumps(self.__dict__, ensure_ascii=False, default=_json_converter)
        _publish_message2_pubsub(smtp_pubsub_topic, message_json)


class AnalyticsMessage:
    data: str
    name: str
    event: str
    attributes: [str]
    created_at: datetime.datetime

    def send(self):
        message_json = json.dumps(self.__dict__, ensure_ascii=False, default=_json_converter)
        _publish_message2_pubsub(analytics_pubsub_topic, message_json)



