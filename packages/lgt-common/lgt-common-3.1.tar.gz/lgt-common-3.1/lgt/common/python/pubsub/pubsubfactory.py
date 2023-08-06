import lgt.common.python.pubsub.env as env

from google.cloud import pubsub_v1
from google.api_core.exceptions import GoogleAPICallError
from google.auth.transport.grpc import *


class PubSubFactory:

    def create_publisher(self):
        return pubsub_v1.PublisherClient()

    def create_subscriber(self):
        return pubsub_v1.SubscriberClient()

    def get_topic_path(self, project_id, topic_name):
        publisher = self.create_publisher()
        return publisher.api.topic_path(project_id, f'{topic_name}')

    def get_subscription_path(self, project_id, subscriber_name, topic_name):
        subscriber = self.create_subscriber()
        return subscriber.api.subscription_path(project_id, f'{topic_name}_{subscriber_name}')

    def create_topic_if_doesnt_exist(self, project_id, topic_name):
        publisher = self.create_publisher()
        topic_path = self.get_topic_path(project_id, topic_name)
        try:
            publisher.api.get_topic(topic_path)
        except GoogleAPICallError as ex:
            if ex.grpc_status_code == grpc.StatusCode.NOT_FOUND:
                publisher.api.create_topic(name=topic_path)
            else:
                raise

    def create_subscription_if_doesnt_exist(self, project_id, subscriber_name, topic_name):
        subscriber = self.create_subscriber()

        topic_path = self.get_topic_path(project_id, topic_name)
        subscription_path = self.get_subscription_path(project_id, subscriber_name, topic_name)

        self.create_topic_if_doesnt_exist(project_id, topic_name)

        try:
            subscriber.api.get_subscription(subscription_path)
        except GoogleAPICallError as ex:
            if ex.grpc_status_code == grpc.StatusCode.NOT_FOUND:
                subscriber.api.create_subscription(name=subscription_path, topic=topic_path,
                                                   push_config=None, ack_deadline_seconds=60)
            else:
                raise
