from observer.usage_observer import UsageObserver
from observer.litter_service_client import LitterServiceClient
from observer.video_buffer import VideoBuffer
from observer.models import LitterBoxObserverConfig, LitterUsageMetadata

class LitterBoxObserver:

    def __init__(
        self,
        observer_config: LitterBoxObserverConfig):
        self._usage_observer = UsageObserver(observer_config.usage_observer_config)
        self._litter_service_client = LitterServiceClient(observer_config.litter_service_client_config)
        # self._video_buffer = VideoBuffer(observer_config.video_buffer_config)

    async def begin_observing(self):
        await self._usage_observer.init()
        await self._usage_observer.begin_observing(self.on_litterbox_used)

    def on_litterbox_used(self, usage_metadata: LitterUsageMetadata):
        print(f"Litter box used! Metadata: {usage_metadata}")
        # Store usage metadata and receive usage ID
        usage_id = self._litter_service_client.store_usage(usage_metadata)
        print(f"Stored with id {usage_id}")
        # TODO: Grab video buffer
        # TODO: Store video
        # TODO: Store video metadata associated with usage ID