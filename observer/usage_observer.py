from typing import Callable
from pylitterbot import LitterRobot, Account
from pylitterbot.enums import LitterBoxStatus
from observer.models import UsageObserverConfig, LitterUsageMetadata, CatMetadata, LitterBoxMetadata
import time

class UsageObserver:
    def __init__(self, usage_observer_config: UsageObserverConfig):
        self.config = usage_observer_config
        self._robot = None
        self._last_cat_activity_timestamp = None

    async def init(self):
        self._robot = await self._load_robot()

    async def _load_robot(self):
        # Create an account.
        self._account = Account()
        target_robot = None
        try:
            # Connect to the API and load robots.
            await self._account.connect(username=self.config.whisker_username, password=self.config.whisker_password, load_robots=True)

            # Print robots associated with account.
            print("Robots:")
            for robot in self._account.robots:
                print(robot)
                if robot.name == self.config.target_robot_name:
                    target_robot = robot

        finally:         
            if target_robot is None:
                # Disconnect from the API.
                await self._account.disconnect()
                raise ValueError(f"Could not find target robot {self.config.target_robot_name}")

        return target_robot

    async def _get_latest_cat_activity(self):
        for activity in await self._robot.get_activity_history():
            if activity.action == LitterBoxStatus.CAT_SENSOR_TIMING:
                return activity

        return None

    async def begin_observing(self, on_usage_observed_callback: Callable):
        if self._robot is None:
            raise RuntimeError("Plese init() before observing")

        try:
            while True:
                print("Polling robot")
                await self._robot.refresh()
                print("Updated data")
                latest_cat_usage = await self._get_latest_cat_activity()
                if latest_cat_usage is not None and latest_cat_usage.timestamp != self._last_cat_activity_timestamp:
                    litter_usage_metadata = LitterUsageMetadata(
                        cat_metadata=CatMetadata(cat_name="unknown", cat_weight_kg=-1),
                        litter_box_metadata=LitterBoxMetadata(litter_box_name=self.config.target_robot_name),
                        usage_timestamp=latest_cat_usage.timestamp
                    )
                    print(f"Latest cat usage: {litter_usage_metadata}")

                    # Avoid redundant updates + don't slam the API
                    time.sleep(30)
                    self._last_cat_activity_timestamp = latest_cat_usage.timestamp
                    # on_usage_observed_callback(litter_usage_metadata)
        finally:
            await self._account.disconnect()

    def _identify_cat(self, weight_kg):
        """
        OPTIONAL:
        If you have >=2 cats, implement heuristics like:
        - threshold weights
        - profile matching
        - historical averaging
        """
        return "Unknown"
