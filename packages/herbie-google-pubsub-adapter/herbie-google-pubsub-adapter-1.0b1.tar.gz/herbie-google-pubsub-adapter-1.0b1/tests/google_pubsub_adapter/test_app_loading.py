from unittest import mock
from django.test import SimpleTestCase
from django.apps import apps
from google_pubsub_adapter.apps import HerbieGooglePubsubAdapterConfig


class AppLoadingTestCase(SimpleTestCase):
    def tearDown(self):
        apps.clear_cache()

    @mock.patch("google_pubsub_adapter.publisher.google_pubsub_publisher.GooglePubsubPublisher")
    def test_loading_app(self, mock_google_pubsub):
        with self.settings(
            INSTALLED_APPS=["google_pubsub_adapter.apps.HerbieGooglePubsubAdapterConfig"],
            GCLOUD_PUBSUB_PROJECT_ID="pubsub",
        ):
            mock_google_pubsub()

            self.assertIsNotNone(apps.get_app_config(HerbieGooglePubsubAdapterConfig.name))
