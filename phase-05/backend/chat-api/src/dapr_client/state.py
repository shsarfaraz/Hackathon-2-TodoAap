from dapr.clients import DaprClient
from typing import Dict, Any, Optional


class DaprStateClient:
    def __init__(self, dapr_client_getter):
        self.get_dapr_client = dapr_client_getter

    def save_state(self, store_name: str, key: str, value: Any):
        """Save state to a Dapr state store"""
        with self.get_dapr_client() as client:
            client.save_state(store_name, key, value)

    def get_state(self, store_name: str, key: str) -> Optional[Any]:
        """Get state from a Dapr state store"""
        with self.get_dapr_client() as client:
            response = client.get_state(store_name, key)
            return response.data.decode('utf-8') if response.data else None

    def delete_state(self, store_name: str, key: str):
        """Delete state from a Dapr state store"""
        with self.get_dapr_client() as client:
            client.delete_state(store_name, key)

    def bulk_get_state(self, store_name: str, keys: list) -> Dict[str, Any]:
        """Get multiple states from a Dapr state store"""
        with self.get_dapr_client() as client:
            responses = client.get_bulk_state(store_name, keys)
            result = {}
            for resp in responses:
                result[resp.key] = resp.data.decode('utf-8') if resp.data else None
            return result