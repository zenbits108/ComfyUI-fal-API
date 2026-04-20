from .fal_utils import ApiHandler, FalConfig, ImageUtils

# Initialize FalConfig
fal_config = FalConfig()

# ---------------------------------------------------------------------------
# Shared enum values from fal.ai schema
# ---------------------------------------------------------------------------
DURATION_STANDARD = ["6", "8", "10"]
DURATION_FAST     = ["6", "8", "10", "12", "14", "16", "18", "20"]
RESOLUTION        = ["1080p", "1440p", "2160p"]
ASPECT_RATIO      = ["16:9", "9:16"]
ASPECT_RATIO_AUTO = ["auto", "16:9", "9:16"]
FPS               = ["24", "25", "48", "50"]


# ---------------------------------------------------------------------------
# 1. Text-to-Video (standard)
#    endpoint: fal-ai/ltx-2.3/text-to-video
# ---------------------------------------------------------------------------

class LTX23TextToVideoNode:
    """LTX 2.3 Text-to-Video — standard quality via fal.ai."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "duration": (DURATION_STANDARD, {"default": "6"}),
                "resolution": (RESOLUTION, {"default": "1080p"}),
                "aspect_ratio": (ASPECT_RATIO, {"default": "16:9"}),
                "fps": (FPS, {"default": "25"}),
                "generate_audio": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("video_url",)
    FUNCTION = "generate_video"
    CATEGORY = "FAL/LTX23"

    def generate_video(self, prompt, duration, resolution, aspect_ratio, fps, generate_audio):
        try:
            arguments = {
                "prompt": prompt,
                "duration": int(duration),
                "resolution": resolution,
                "aspect_ratio": aspect_ratio,
                "fps": int(fps),
                "generate_audio": generate_audio,
            }
            result = ApiHandler.submit_and_get_result(
                "fal-ai/ltx-2.3/text-to-video", arguments
            )
            return (result["video"]["url"],)
        except Exception as e:
            return ApiHandler.handle_video_generation_error("ltx-2.3/text-to-video", str(e))


# ---------------------------------------------------------------------------
# 2. Text-to-Video (fast)
#    endpoint: fal-ai/ltx-2.3/text-to-video/fast
#    Supports longer durations (up to 20s).
#    Note: durations > 10s only supported at 25fps + 1080p.
# ---------------------------------------------------------------------------

class LTX23TextToVideoFastNode:
    """LTX 2.3 Text-to-Video — fast model via fal.ai.

    Supports up to 20 seconds. Durations > 10s require 25 FPS + 1080p.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "duration": (DURATION_FAST, {"default": "6"}),
                "resolution": (RESOLUTION, {"default": "1080p"}),
                "aspect_ratio": (ASPECT_RATIO, {"default": "16:9"}),
                "fps": (FPS, {"default": "25"}),
                "generate_audio": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("video_url",)
    FUNCTION = "generate_video"
    CATEGORY = "FAL/LTX23"

    def generate_video(self, prompt, duration, resolution, aspect_ratio, fps, generate_audio):
        try:
            arguments = {
                "prompt": prompt,
                "duration": int(duration),
                "resolution": resolution,
                "aspect_ratio": aspect_ratio,
                "fps": int(fps),
                "generate_audio": generate_audio,
            }
            result = ApiHandler.submit_and_get_result(
                "fal-ai/ltx-2.3/text-to-video/fast", arguments
            )
            return (result["video"]["url"],)
        except Exception as e:
            return ApiHandler.handle_video_generation_error("ltx-2.3/text-to-video/fast", str(e))


# ---------------------------------------------------------------------------
# 3. Image-to-Video (standard)
#    endpoint: fal-ai/ltx-2.3/image-to-video
#    Connect end_frame for start->end transition generation.
# ---------------------------------------------------------------------------

class LTX23ImageToVideoNode:
    """LTX 2.3 Image-to-Video — standard quality via fal.ai.

    Connect start_frame only for I2V.
    Connect start_frame + end_frame to generate a transition between two frames.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "start_frame": ("IMAGE",),
                "duration": (DURATION_STANDARD, {"default": "6"}),
                "resolution": (RESOLUTION, {"default": "1080p"}),
                "aspect_ratio": (ASPECT_RATIO_AUTO, {"default": "auto"}),
                "fps": (FPS, {"default": "25"}),
                "generate_audio": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "end_frame": (
                    "IMAGE",
                    {"tooltip": "Optional. When connected, generates a transition between start and end frames."},
                ),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("video_url",)
    FUNCTION = "generate_video"
    CATEGORY = "FAL/LTX23"

    def generate_video(self, prompt, start_frame, duration, resolution, aspect_ratio, fps, generate_audio, end_frame=None):
        try:
            start_url = ImageUtils.upload_image(start_frame)
            if not start_url:
                return ApiHandler.handle_video_generation_error(
                    "ltx-2.3/image-to-video", "Failed to upload start frame"
                )

            arguments = {
                "image_url": start_url,
                "prompt": prompt,
                "duration": int(duration),
                "resolution": resolution,
                "aspect_ratio": aspect_ratio,
                "fps": int(fps),
                "generate_audio": generate_audio,
            }

            if end_frame is not None:
                end_url = ImageUtils.upload_image(end_frame)
                if not end_url:
                    return ApiHandler.handle_video_generation_error(
                        "ltx-2.3/image-to-video", "Failed to upload end frame"
                    )
                arguments["end_image_url"] = end_url

            result = ApiHandler.submit_and_get_result(
                "fal-ai/ltx-2.3/image-to-video", arguments
            )
            return (result["video"]["url"],)
        except Exception as e:
            return ApiHandler.handle_video_generation_error("ltx-2.3/image-to-video", str(e))


# ---------------------------------------------------------------------------
# 4. Image-to-Video (fast)
#    endpoint: fal-ai/ltx-2.3/image-to-video/fast
#    Supports up to 20s duration.
# ---------------------------------------------------------------------------

class LTX23ImageToVideoFastNode:
    """LTX 2.3 Image-to-Video — fast model via fal.ai.

    Connect start_frame + end_frame for start->end frame transition.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "start_frame": ("IMAGE",),
                "duration": (DURATION_FAST, {"default": "6"}),
                "resolution": (RESOLUTION, {"default": "1080p"}),
                "aspect_ratio": (ASPECT_RATIO_AUTO, {"default": "auto"}),
                "fps": (FPS, {"default": "25"}),
                "generate_audio": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "end_frame": ("IMAGE",),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("video_url",)
    FUNCTION = "generate_video"
    CATEGORY = "FAL/LTX23"

    def generate_video(self, prompt, start_frame, duration, resolution, aspect_ratio, fps, generate_audio, end_frame=None):
        try:
            start_url = ImageUtils.upload_image(start_frame)
            if not start_url:
                return ApiHandler.handle_video_generation_error(
                    "ltx-2.3/image-to-video/fast", "Failed to upload start frame"
                )

            arguments = {
                "image_url": start_url,
                "prompt": prompt,
                "duration": int(duration),
                "resolution": resolution,
                "aspect_ratio": aspect_ratio,
                "fps": int(fps),
                "generate_audio": generate_audio,
            }

            if end_frame is not None:
                end_url = ImageUtils.upload_image(end_frame)
                if not end_url:
                    return ApiHandler.handle_video_generation_error(
                        "ltx-2.3/image-to-video/fast", "Failed to upload end frame"
                    )
                arguments["end_image_url"] = end_url

            result = ApiHandler.submit_and_get_result(
                "fal-ai/ltx-2.3/image-to-video/fast", arguments
            )
            return (result["video"]["url"],)
        except Exception as e:
            return ApiHandler.handle_video_generation_error("ltx-2.3/image-to-video/fast", str(e))


# ---------------------------------------------------------------------------
# 5. Extend Video
#    endpoint: fal-ai/ltx-2.3/extend-video
#    Continues an existing video clip at start or end.
# ---------------------------------------------------------------------------

class LTX23ExtendVideoNode:
    """LTX 2.3 Extend Video via fal.ai.

    Extends an existing video clip at either the start or end.
    Pass video_url from any previous LTX 2.3 node or SaveVideoFromURL.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video_url": ("STRING", {"default": ""}),
                "prompt": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": True,
                        "tooltip": "Describe what should happen in the extended portion.",
                    },
                ),
                "duration": (
                    "FLOAT",
                    {
                        "default": 5.0,
                        "min": 1.0,
                        "max": 20.0,
                        "step": 0.5,
                        "tooltip": "Duration in seconds to extend. Max 20s.",
                    },
                ),
                "mode": (
                    ["end", "start"],
                    {
                        "default": "end",
                        "tooltip": "'end' extends after the last frame, 'start' prepends before the first.",
                    },
                ),
            },
            "optional": {
                "context": (
                    "FLOAT",
                    {
                        "default": 0.0,
                        "min": 0.0,
                        "max": 20.0,
                        "step": 0.5,
                        "tooltip": (
                            "Seconds of source video to use as context (min 1s, max 20s). "
                            "Leave at 0 to let fal.ai auto-maximize context."
                        ),
                    },
                ),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("video_url",)
    FUNCTION = "extend_video"
    CATEGORY = "FAL/LTX23"

    def extend_video(self, video_url, prompt, duration, mode, context=0.0):
        try:
            if not video_url or not video_url.startswith(("http://", "https://")):
                return ApiHandler.handle_video_generation_error(
                    "ltx-2.3/extend-video", "Invalid or missing video_url"
                )

            arguments = {
                "video_url": video_url.strip(),
                "prompt": prompt,
                "duration": duration,
                "mode": mode,
            }

            if context > 0.0:
                arguments["context"] = context

            result = ApiHandler.submit_and_get_result(
                "fal-ai/ltx-2.3/extend-video", arguments
            )
            return (result["video"]["url"],)
        except Exception as e:
            return ApiHandler.handle_video_generation_error("ltx-2.3/extend-video", str(e))


# ---------------------------------------------------------------------------
# 6. Audio-to-Video
#    endpoint: fal-ai/ltx-2.3/audio-to-video
#    Generate video driven by an audio file. Optional start image.
# ---------------------------------------------------------------------------

class LTX23AudioToVideoNode:
    """LTX 2.3 Audio-to-Video via fal.ai.

    Drives video generation from an audio URL (2-20s).
    Optionally anchor the first frame with a start_image.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "audio_url": (
                    "STRING",
                    {
                        "default": "",
                        "tooltip": "Public URL of audio file. Duration must be 2-20 seconds.",
                    },
                ),
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "aspect_ratio": (ASPECT_RATIO_AUTO, {"default": "auto"}),
            },
            "optional": {
                "start_frame": (
                    "IMAGE",
                    {"tooltip": "Optional first frame image to anchor the video."},
                ),
                "guidance_scale": (
                    "FLOAT",
                    {
                        "default": 5.0,
                        "min": 1.0,
                        "max": 20.0,
                        "step": 0.5,
                        "tooltip": "Higher = closer to prompt. Default 5 for T2V, 9 when image provided.",
                    },
                ),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("video_url",)
    FUNCTION = "generate_video"
    CATEGORY = "FAL/LTX23"

    def generate_video(self, audio_url, prompt, aspect_ratio, start_frame=None, guidance_scale=5.0):
        try:
            if not audio_url or not audio_url.startswith(("http://", "https://")):
                return ApiHandler.handle_video_generation_error(
                    "ltx-2.3/audio-to-video", "Invalid or missing audio_url"
                )

            arguments = {
                "audio_url": audio_url.strip(),
                "prompt": prompt,
                "aspect_ratio": aspect_ratio,
                "guidance_scale": guidance_scale,
            }

            if start_frame is not None:
                image_url = ImageUtils.upload_image(start_frame)
                if not image_url:
                    return ApiHandler.handle_video_generation_error(
                        "ltx-2.3/audio-to-video", "Failed to upload start frame"
                    )
                arguments["image_url"] = image_url

            result = ApiHandler.submit_and_get_result(
                "fal-ai/ltx-2.3/audio-to-video", arguments
            )
            return (result["video"]["url"],)
        except Exception as e:
            return ApiHandler.handle_video_generation_error("ltx-2.3/audio-to-video", str(e))


# ---------------------------------------------------------------------------
# 7. Retake Video
#    endpoint: fal-ai/ltx-2.3/retake-video
#    Re-generate a section of an existing video.
# ---------------------------------------------------------------------------

class LTX23RetakeVideoNode:
    """LTX 2.3 Retake Video via fal.ai.

    Re-generates a segment of an existing video clip by time range.
    Use to fix a bad section without re-rendering the whole shot.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video_url": ("STRING", {"default": ""}),
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "start_time": (
                    "FLOAT",
                    {
                        "default": 0.0,
                        "min": 0.0,
                        "max": 300.0,
                        "step": 0.1,
                        "tooltip": "Start time in seconds of the section to retake.",
                    },
                ),
                "duration": (
                    "FLOAT",
                    {
                        "default": 5.0,
                        "min": 0.5,
                        "max": 20.0,
                        "step": 0.5,
                        "tooltip": "Duration in seconds of the section to retake.",
                    },
                ),
                "retake_mode": (
                    ["replace_audio_and_video", "replace_video", "replace_audio"],
                    {"default": "replace_audio_and_video"},
                ),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("video_url",)
    FUNCTION = "retake_video"
    CATEGORY = "FAL/LTX23"

    def retake_video(self, video_url, prompt, start_time, duration, retake_mode):
        try:
            if not video_url or not video_url.startswith(("http://", "https://")):
                return ApiHandler.handle_video_generation_error(
                    "ltx-2.3/retake-video", "Invalid or missing video_url"
                )

            arguments = {
                "video_url": video_url.strip(),
                "prompt": prompt,
                "start_time": start_time,
                "duration": duration,
                "retake_mode": retake_mode,
            }

            result = ApiHandler.submit_and_get_result(
                "fal-ai/ltx-2.3/retake-video", arguments
            )
            return (result["video"]["url"],)
        except Exception as e:
            return ApiHandler.handle_video_generation_error("ltx-2.3/retake-video", str(e))


# ---------------------------------------------------------------------------
# Node registrations
# ---------------------------------------------------------------------------

NODE_CLASS_MAPPINGS = {
    "LTX23TextToVideo_fal":      LTX23TextToVideoNode,
    "LTX23TextToVideoFast_fal":  LTX23TextToVideoFastNode,
    "LTX23ImageToVideo_fal":     LTX23ImageToVideoNode,
    "LTX23ImageToVideoFast_fal": LTX23ImageToVideoFastNode,
    "LTX23ExtendVideo_fal":      LTX23ExtendVideoNode,
    "LTX23AudioToVideo_fal":     LTX23AudioToVideoNode,
    "LTX23RetakeVideo_fal":      LTX23RetakeVideoNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LTX23TextToVideo_fal":      "LTX 2.3 Text-to-Video (fal)",
    "LTX23TextToVideoFast_fal":  "LTX 2.3 Text-to-Video Fast (fal)",
    "LTX23ImageToVideo_fal":     "LTX 2.3 Image-to-Video (fal)",
    "LTX23ImageToVideoFast_fal": "LTX 2.3 Image-to-Video Fast (fal)",
    "LTX23ExtendVideo_fal":      "LTX 2.3 Extend Video (fal)",
    "LTX23AudioToVideo_fal":     "LTX 2.3 Audio-to-Video (fal)",
    "LTX23RetakeVideo_fal":      "LTX 2.3 Retake Video (fal)",
}
