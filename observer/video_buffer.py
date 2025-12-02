
class VideoBuffer:

    def _has_footage_in_buffer(self, video_start_datetime, video_end_datetime) -> bool:
        return False

    def get_video(self, video_start_datetime, video_end_datetime):
        if not self._has_footage_in_buffer(video_start_datetime, video_end_datetime):
            return None

        return None