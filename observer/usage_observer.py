from typing import Callable
from pylitterbot import LitterRobot, Account, LitterRobot3, LitterRobot4
from pylitterbot.enums import LitterBoxStatus
from observer.models import UsageObserverConfig, LitterUsageMetadata, CatMetadata, LitterBoxMetadata
import time
import re
from asyncio.exceptions import TimeoutError
from asyncio import sleep as async_sleep

class UsageObserver:
    def __init__(self, usage_observer_config: UsageObserverConfig):
        self._config = usage_observer_config
        self._robot = None
        self._last_cat_activity_timestamp = None

    async def init(self):
        self._robot = await self._load_robot()

    async def _load_robot(self):
        self._account = Account()
        target_robot = None
        try:
            # Connect to the API and load robots.
            await self._account.connect(username=self._config.whisker_username, password=self._config.whisker_password, load_robots=True)
            for robot in self._account.robots:
                if robot.name == self._config.target_robot_name:
                    target_robot = robot

        finally:         
            if target_robot is None:
                await self._account.disconnect()
                raise ValueError(f"Could not find target robot {self._config.target_robot_name}")

        return target_robot

    async def _get_latest_cat_activity(self):
        for activity in await self._robot.get_activity_history():
            # We can't get weight from LR3
            if isinstance(self._robot, LitterRobot3) and activity.action == LitterBoxStatus.CAT_SENSOR_TIMING:
                return {"weight_kg": -1, "unix_timestamp_ns": activity.timestamp.timestamp() * 1e9}
            elif isinstance(self._robot, LitterRobot4) and isinstance(activity.action, str) and "Pet Weight Recorded" in activity.action:
                match = re.search(r"(\d+(\.\d+)?)", activity.action)
                assert match
                return {"weight_kg": float(match.group(1)) * 0.453592, "unix_timestamp_ns": activity.timestamp.timestamp() * 1e9}

        return None

    async def begin_observing(self, on_usage_observed_callback: Callable):
        if self._robot is None:
            raise RuntimeError("Plese init() before observing")

        try:
            while True:
                print("Polling robot")
                await self._robot.refresh()
                try:
                    latest_cat_usage = await self._get_latest_cat_activity()
                except TimeoutError:
                    print("Received timeout. Waiting 1 minute before polling again.")
                    await async_sleep(60)
                    continue
                    
                if latest_cat_usage is not None and latest_cat_usage["unix_timestamp_ns"] != self._last_cat_activity_timestamp:
                    # TODO(liam): identify cat name/weight
                    litter_usage_metadata = LitterUsageMetadata(
                        cat_metadata=CatMetadata(cat_name="unknown", cat_weight_kg=latest_cat_usage["weight_kg"]),
                        litter_box_metadata=LitterBoxMetadata(litter_box_name=self._config.target_robot_name),
                        usage_timestamp_unix_ns=latest_cat_usage["unix_timestamp_ns"]
                    )
                    print(f"Latest cat usage: {litter_usage_metadata}")

                    self._last_cat_activity_timestamp = latest_cat_usage["unix_timestamp_ns"]
                    on_usage_observed_callback(litter_usage_metadata)

                # Avoid redundant updates + don't slam the API
                await async_sleep(30)
    
        finally:
            await self._account.disconnect()
