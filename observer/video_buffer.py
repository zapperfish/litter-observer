from observer.models import VideoBufferConfig
from reolinkapi import Camera
import threading
import datetime

class VideoBuffer:

    def __init__(self, video_buffer_config: VideoBufferConfig):
        self._config = video_buffer_config
        self._camera = Camera(self._config.reolink_camera_ip, self._config.reolink_camera_username, self._config.reolink_camera_password)
        self._image_buffer = [] # (timestamp, img) tuples
        self._image_buffer_mutex = threading.Lock()

    def _evict_stale_images(self):
        staleness_threshold_timestamp = datetime.datetime.now() - datetime.timedelta(seconds=self._config.buffer_history_duration_s)
        while len(self._image_buffer) > 0 and self._image_buffer[0][0] < staleness_threshold_timestamp:
            self._image_buffer.pop(0)

    def _begin_buffering(self):
        def image_callback(img):
            capture_timestamp = datetime.datetime.now()
            with self._image_buffer_mutex:
                self._evict_stale_images()
                assert len(self._image_buffer) == 0 or self._image_buffer[-1][0] < capture_timestamp
                self._image_buffer.append((capture_timestamp, img))

        self._camera.open_video_stream(callback=image_callback)

    def _timestamp_within_current_buffer(self, timestamp):
        return len(self._image_buffer) > 0 and timestamp >= self._image_buffer[0][0] and timestamp <= self._image_buffer[-1][0]

    def _has_footage_in_buffer(self, video_start_datetime, video_end_datetime, allow_partial_overlap=False) -> bool:
        video_start_in_buffer = self._timestamp_within_current_buffer(video_start_datetime)
        video_end_in_buffer = self._timestamp_within_current_buffer(video_end_datetime)
        if allow_partial_overlap:
            # We're fine just getting part of the desired timestamp range:
            return video_start_in_buffer or video_end_in_buffer
        else:
            return video_start_in_buffer and video_end_in_buffer

    def get_footage(self, video_start_datetime, video_end_datetime):
        assert video_start_datetime < video_end_datetime

        with self._image_buffer_mutex:
            if not self._has_footage_in_buffer(video_start_datetime, video_end_datetime, allow_partial_overlap=True):
                return None

            frames = []
            for capture_timestamp, frame in self._image_buffer:
                if (capture_timestamp >= video_start_datetime) and (capture_timestamp <= video_end_datetime):
                    frames.append(frame)

            # Add true start, end timestamps to the return here
            return frames