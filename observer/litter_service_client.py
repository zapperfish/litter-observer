import requests

from observer.models.litter_usage_metadata import LitterUsageMetadata
from observer.models.observer_configs import LitterServiceClientConfig


class LitterServiceClient:

    def __init__(self, litter_service_client_config: LitterServiceClientConfig):
        self.config = litter_service_client_config

    def store_usage(self, usage_metadata: LitterUsageMetadata) -> str:
        """Store usage and return the usage ID."""
        url = f"http://{self.config.service_address}:{self.config.service_port}/litter_usage"
        response = requests.post(url, json=usage_metadata.model_dump(mode='json'))
        response.raise_for_status()
        return response.json()['id']
