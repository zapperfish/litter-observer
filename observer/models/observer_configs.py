from pydantic import BaseModel


class VideoBufferConfig(BaseModel):
    """Configuration for video buffer."""
    buffer_history_duration_s: float
    reolink_camera_ip: str
    reolink_camera_username: str
    reolink_camera_password: str


class VideoStorageConfig(BaseModel):
    """Configuration for video storage."""
    video_expiration_days: int
    video_length_s: float
    video_filestore_root_directory: str


class UsageObserverConfig(BaseModel):
    """Configuration for usage observer."""
    whisker_username: str
    whisker_password: str
    target_robot_name: str


class LitterServiceClientConfig(BaseModel):
    """Configuration for litter service client."""
    service_address: str
    service_port: int


class LitterBoxObserverConfig(BaseModel):
    """Configuration for litter box observer."""
    video_buffer_config: VideoBufferConfig
    video_storage_config: VideoStorageConfig
    usage_observer_config: UsageObserverConfig
    litter_service_client_config: LitterServiceClientConfig

