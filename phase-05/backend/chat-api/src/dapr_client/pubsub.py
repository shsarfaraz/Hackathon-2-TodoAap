from dapr.clients import DaprClient
import json


class DaprPubSubClient:
    def __init__(self, dapr_client_getter):
        self.get_dapr_client = dapr_client_getter

    def publish_event(self, pubsub_name: str, topic_name: str, data: dict):
        """Publish an event to a Dapr pub/sub topic"""
        with self.get_dapr_client() as client:
            # Serialize the data
            serialized_data = json.dumps(data)
            
            # Publish the event
            client.publish_event(
                pubsub_name=pubsub_name,
                topic_name=topic_name,
                data=serialized_data,
                data_content_type='application/json'
            )

    def subscribe_to_topic(self, pubsub_name: str, topic_name: str, callback):
        """Subscribe to a Dapr pub/sub topic (this would typically be handled differently in practice)"""
        # Note: In a real implementation, Dapr subscription would be handled via HTTP callbacks
        # This is a simplified representation
        pass