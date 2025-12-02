from observer.usage_observer import UsageObserver
from observer.models import LitterBoxObserverConfig

class LitterBoxObserver:

    def __init__(
        self,
        observer_config: LitterBoxObserverConfig):
        self._usage_observer = UsageObserver(observer_config.usage_observer_config)

    async def begin_observing(self):
        await self._usage_observer.init()
        await self._usage_observer.begin_observing(self.on_litterbox_used)

    def on_litterbox_used(self, usage_metadata):
        print(f"Litter box used! Metadata: {usage_metadata}")
        # TODO: Grab video buffer
        # TODO: Store video
        # TODO: Store metadata