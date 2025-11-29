from observer.usage_observer import UsageObserver

class LitterBoxObserver:

    def __init__(
        self,
        observer_config: observer_config_pb2.LitterBoxObserverConfig)

    def begin_observing(self):
        callback = functools.partial(LitterBoxObserver.begin_observing, self)
        self._usage_observer.begin_observing(callback)

    def on_litterbox_used(self, usage_metadata):
        # Grab video buffer
        # Store video
        # Store metadata