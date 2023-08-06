import logging
from google.api_core.exceptions import AlreadyExists
from google.cloud.pubsub_v1 import PublisherClient
from django.conf import settings
from rest_framework.renderers import JSONRenderer
from google_pubsub_adapter.constants import PublisherConstants
from herbie_core.services.message_publisher.abstract_publisher import AbstractPublisher
from herbie_core.models.message_models_and_serializers import Message


class GooglePubsubPublisher(AbstractPublisher):
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._publisher = PublisherClient()

    def get_name(self) -> str:
        return PublisherConstants.GOOGLE_PUBSUB_PUBLISHER_NAME

    def send_message(self, message: Message):
        serializer = message.get_serializer()

        json_data = JSONRenderer().render(serializer.data)

        topic_path = self._publisher.topic_path(settings.GCLOUD_PUBSUB_PROJECT_ID, serializer.data["type"])
        future = self._publisher.publish(topic_path, data=json_data)
        future.add_done_callback(self._publish_callback)

    def _publish_callback(self, message_future):
        if message_future.exception(timeout=30):
            self._logger.info(f"Publishing message on {message_future.exception()} threw an Exception.")
        else:
            self._logger.info(message_future.result())

    def create_topic(self, topic: str):
        topic_path = self._publisher.topic_path(settings.GCLOUD_PUBSUB_PROJECT_ID, topic)
        try:
            self._publisher.create_topic(topic_path)
        except AlreadyExists:
            self._logger.info(f"Topic {topic} already exists.")
