from django.apps import AppConfig


class HerbieGooglePubsubAdapterConfig(AppConfig):
    name = "google_pubsub_adapter"
    verbose_name = "HerbieGooglePubsubAdapter"

    def ready(self):
        from herbie_core.services.message_publisher.registry import Registry
        from google_pubsub_adapter.publisher.google_pubsub_publisher import GooglePubsubPublisher

        Registry.add_publisher(GooglePubsubPublisher())
