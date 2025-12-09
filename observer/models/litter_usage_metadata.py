from pydantic import BaseModel
import datetime

class CatMetadata(BaseModel):
    """Metadata about a cat."""
    cat_name: str
    cat_weight_kg: float


class LitterBoxMetadata(BaseModel):
    """Metadata about a litter box."""
    litter_box_name: str


class LitterUsageMetadata(BaseModel):
    """Metadata about a litter box usage event."""
    cat_metadata: CatMetadata
    litter_box_metadata: LitterBoxMetadata
    usage_timestamp_unix_ns: int


class UsageVideoMetadata(BaseModel):
    """Metadata about a usage video recording."""
    start_timestamp_unix_ns: int
    usage_duration_s: float
    usage_video_filepath: str
    file_expiration_timestamp_ns: int
    camera_name: str

