from .fal_utils import ApiHandler, FalConfig, ImageUtils

# Initialize FalConfig
fal_config = FalConfig()

# ---------------------------------------------------------------------------
# Resolution presets for LTX 2.3 — all must be divisible by 32
# ---------------------------------------------------------------------------
RESOLUTION_PRESETS = [
    "custom",
    "512x512",
    "576x512",
    "512x576",
    "768x512",
    "512x768",
    "1024x576",
    "576x1024",
    "1280x720",
    "720x1280",
    "1024x768",
    "768x1024",
    "1024x1024",
]


def _parse_resolution(preset, width, height):
    """Return (width, height) from a preset string or fall through to the
    explicit width / height fields when preset == 'custom'."""
    if preset == "custom":
        return width, height
    w, h = preset.split("x")
    return int(w), int(h)


# ---------------------------------------------------------------------------
# Text-to-Video
# ---------------------------------------------------------------------------

class LTX23TextToVideoNode:
    """LTX Video 2.3 Text-to-Video via fal.ai.

    Uses the fal-ai/ltx-video/v2.3/text-to-video endpoint.
    num_frames should satisfy (N - 1) % 8 == 0, e.g. 25, 49, 97, 121, 193.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "negative_prompt": (
                    "STRING",
                    {
                        "default": (
                            "worst quality, inconsistent motion, blurry, jittery, "
                            "distorted"
                        ),
                        "multiline": True,
                    },
                ),
                "resolution": (RESOLUTION_PRESETS, {"default": "1280x720"}),
                "num_frames": (
                    "INT",
                    {
                        "default": 121,
                        "min": 9,
                        "max": 257,
                        "step": 8,
                        "tooltip": "Best values: 25, 49, 97, 121, 193 — must satisfy (N-1) % 8 == 0",
                    },
                ),
                "frame_rate": ("INT", {"default": 25, "min": 8, "max": 60}),
                "num_inference_steps": ("INT", {"default": 40, "min": 1, "max": 100}),
                "guidance_scale": (
                    "FLOAT",
                    {"default": 3.0, "min": 1.0, "max": 10.0, "step": 0.1},
                ),
                "enable_safety_checker": ("BOOLEAN", {"default": True}),
                "expand_prompt": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "seed": ("INT", {"default": -1}),
                "custom_width": (
                    "INT",
                    {
                        "default": 1280,
                        "min": 256,
                        "max": 2048,
                        "step": 32,
                        "tooltip": "Used only when resolution == 'custom'",
                    },
                ),
                "custom_height": (
                    "INT",
                    {
                        "default": 720,
                        "min": 256,
                        "max": 2048,
                        "step": 32,
                        "tooltip": "Used only when resolution == 'custom'",
                    },
                ),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("video_url",)
    FUNCTION = "generate_video"
    CATEGORY = "FAL/LTX23"

    def generate_video(
        self,
        prompt,
        negative_prompt,
        resolution,
        num_frames,
        frame_rate,
        num_inference_steps,
        guidance_scale,
        enable_safety_checker,
        expand_prompt,
        seed=-1,
        custom_width=1280,
        custom_height=720,
    ):
        try:
            width, height = _parse_resolution(resolution, custom_width, custom_height)

            arguments = {
                "prompt": prompt,
                "negative_prompt": negative_prompt,
                "num_frames": num_frames,
                "frame_rate": frame_rate,
                "width": width,
                "height": height,
                "num_inference_steps": num_inference_steps,
                "guidance_scale": guidance_scale,
                "enable_safety_checker": enable_safety_checker,
                "expand_prompt": expand_prompt,
            }

            if seed != -1:
                arguments["seed"] = seed

            result = ApiHandler.submit_and_get_result(
                "fal-ai/ltx-video/v2.3/text-to-video", arguments
            )
            return (result["video"]["url"],)
        except Exception as e:
            return ApiHandler.handle_video_generation_error("ltx-video/v2.3/t2v", str(e))


# ---------------------------------------------------------------------------
# Image-to-Video  (also handles first-last-frame when end_frame is connected)
# ---------------------------------------------------------------------------

class LTX23ImageToVideoNode:
    """LTX Video 2.3 Image-to-Video via fal.ai.

    Connect only start_frame  → fal-ai/ltx-video/v2.3/image-to-video
    Connect start_frame + end_frame → fal-ai/ltx-video/v2.3/extend-video
      (first-last-frame conditioning)
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "start_frame": ("IMAGE",),
                "negative_prompt": (
                    "STRING",
                    {
                        "default": (
                            "worst quality, inconsistent motion, blurry, jittery, "
                            "distorted"
                        ),
                        "multiline": True,
                    },
                ),
                "resolution": (RESOLUTION_PRESETS, {"default": "1280x720"}),
                "num_frames": (
                    "INT",
                    {
                        "default": 121,
                        "min": 9,
                        "max": 257,
                        "step": 8,
                        "tooltip": "Best values: 25, 49, 97, 121, 193",
                    },
                ),
                "frame_rate": ("INT", {"default": 25, "min": 8, "max": 60}),
                "num_inference_steps": ("INT", {"default": 40, "min": 1, "max": 100}),
                "guidance_scale": (
                    "FLOAT",
                    {"default": 3.0, "min": 1.0, "max": 10.0, "step": 0.1},
                ),
                "enable_safety_checker": ("BOOLEAN", {"default": True}),
                "expand_prompt": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "end_frame": (
                    "IMAGE",
                    {
                        "tooltip": (
                            "Optional last-frame conditioning. When connected, "
                            "routes to the extend-video endpoint."
                        )
                    },
                ),
                "seed": ("INT", {"default": -1}),
                "custom_width": (
                    "INT",
                    {"default": 1280, "min": 256, "max": 2048, "step": 32},
                ),
                "custom_height": (
                    "INT",
                    {"default": 720, "min": 256, "max": 2048, "step": 32},
                ),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("video_url",)
    FUNCTION = "generate_video"
    CATEGORY = "FAL/LTX23"

    def generate_video(
        self,
        prompt,
        start_frame,
        negative_prompt,
        resolution,
        num_frames,
        frame_rate,
        num_inference_steps,
        guidance_scale,
        enable_safety_checker,
        expand_prompt,
        end_frame=None,
        seed=-1,
        custom_width=1280,
        custom_height=720,
    ):
        try:
            # Upload start frame
            start_url = ImageUtils.upload_image(start_frame)
            if not start_url:
                return ApiHandler.handle_video_generation_error(
                    "ltx-video/v2.3/i2v", "Failed to upload start frame"
                )

            width, height = _parse_resolution(resolution, custom_width, custom_height)

            if end_frame is not None:
                # First-last-frame route
                end_url = ImageUtils.upload_image(end_frame)
                if not end_url:
                    return ApiHandler.handle_video_generation_error(
                        "ltx-video/v2.3/i2v", "Failed to upload end frame"
                    )
                endpoint = "fal-ai/ltx-video/v2.3/extend-video"
                arguments = {
                    "prompt": prompt,
                    "negative_prompt": negative_prompt,
                    "image_url": start_url,
                    "last_image_url": end_url,
                    "num_frames": num_frames,
                    "frame_rate": frame_rate,
                    "width": width,
                    "height": height,
                    "num_inference_steps": num_inference_steps,
                    "guidance_scale": guidance_scale,
                    "enable_safety_checker": enable_safety_checker,
                    "expand_prompt": expand_prompt,
                }
            else:
                # Standard I2V route
                endpoint = "fal-ai/ltx-video/v2.3/image-to-video"
                arguments = {
                    "prompt": prompt,
                    "negative_prompt": negative_prompt,
                    "image_url": start_url,
                    "num_frames": num_frames,
                    "frame_rate": frame_rate,
                    "width": width,
                    "height": height,
                    "num_inference_steps": num_inference_steps,
                    "guidance_scale": guidance_scale,
                    "enable_safety_checker": enable_safety_checker,
                    "expand_prompt": expand_prompt,
                }

            if seed != -1:
                arguments["seed"] = seed

            result = ApiHandler.submit_and_get_result(endpoint, arguments)
            return (result["video"]["url"],)
        except Exception as e:
            return ApiHandler.handle_video_generation_error("ltx-video/v2.3/i2v", str(e))


# ---------------------------------------------------------------------------
# Video-to-Video  (extend / continue a rendered clip)
# ---------------------------------------------------------------------------

class LTX23VideoToVideoNode:
    """LTX Video 2.3 Video-to-Video (extend) via fal.ai.

    Accepts a video URL (e.g. the output of LTX23TextToVideoNode or
    LTX23ImageToVideoNode) and extends/modifies it with a new prompt.
    Optionally clamp the conditioning with an end_frame image.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video_url": ("STRING", {"default": ""}),
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "negative_prompt": (
                    "STRING",
                    {
                        "default": (
                            "worst quality, inconsistent motion, blurry, jittery, "
                            "distorted"
                        ),
                        "multiline": True,
                    },
                ),
                "num_frames": (
                    "INT",
                    {"default": 121, "min": 9, "max": 257, "step": 8},
                ),
                "frame_rate": ("INT", {"default": 25, "min": 8, "max": 60}),
                "num_inference_steps": ("INT", {"default": 40, "min": 1, "max": 100}),
                "guidance_scale": (
                    "FLOAT",
                    {"default": 3.0, "min": 1.0, "max": 10.0, "step": 0.1},
                ),
                "strength": (
                    "FLOAT",
                    {
                        "default": 0.85,
                        "min": 0.0,
                        "max": 1.0,
                        "step": 0.01,
                        "tooltip": "How much to transform the source video (0 = no change, 1 = full regen)",
                    },
                ),
                "enable_safety_checker": ("BOOLEAN", {"default": True}),
                "expand_prompt": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "end_frame": ("IMAGE",),
                "seed": ("INT", {"default": -1}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("video_url",)
    FUNCTION = "generate_video"
    CATEGORY = "FAL/LTX23"

    def generate_video(
        self,
        video_url,
        prompt,
        negative_prompt,
        num_frames,
        frame_rate,
        num_inference_steps,
        guidance_scale,
        strength,
        enable_safety_checker,
        expand_prompt,
        end_frame=None,
        seed=-1,
    ):
        try:
            if not video_url or video_url.strip() == "":
                return ApiHandler.handle_video_generation_error(
                    "ltx-video/v2.3/v2v", "No video_url provided"
                )

            arguments = {
                "video_url": video_url.strip(),
                "prompt": prompt,
                "negative_prompt": negative_prompt,
                "num_frames": num_frames,
                "frame_rate": frame_rate,
                "num_inference_steps": num_inference_steps,
                "guidance_scale": guidance_scale,
                "strength": strength,
                "enable_safety_checker": enable_safety_checker,
                "expand_prompt": expand_prompt,
            }

            if end_frame is not None:
                end_url = ImageUtils.upload_image(end_frame)
                if not end_url:
                    return ApiHandler.handle_video_generation_error(
                        "ltx-video/v2.3/v2v", "Failed to upload end frame"
                    )
                arguments["last_image_url"] = end_url

            if seed != -1:
                arguments["seed"] = seed

            result = ApiHandler.submit_and_get_result(
                "fal-ai/ltx-video/v2.3/video-to-video", arguments
            )
            return (result["video"]["url"],)
        except Exception as e:
            return ApiHandler.handle_video_generation_error("ltx-video/v2.3/v2v", str(e))


# ---------------------------------------------------------------------------
# Distilled (fast) Text-to-Video
# ---------------------------------------------------------------------------

class LTX23DistilledTextToVideoNode:
    """LTX Video 2.3 Distilled (fast) Text-to-Video via fal.ai.

    Uses fal-ai/ltx-video/v2.3/distilled/text-to-video — fewer steps needed
    (8-12 steps typical), much faster and cheaper than the full model.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "negative_prompt": (
                    "STRING",
                    {
                        "default": (
                            "worst quality, inconsistent motion, blurry, jittery, "
                            "distorted"
                        ),
                        "multiline": True,
                    },
                ),
                "resolution": (RESOLUTION_PRESETS, {"default": "1280x720"}),
                "num_frames": (
                    "INT",
                    {"default": 121, "min": 9, "max": 257, "step": 8},
                ),
                "frame_rate": ("INT", {"default": 25, "min": 8, "max": 60}),
                "num_inference_steps": (
                    "INT",
                    {
                        "default": 8,
                        "min": 1,
                        "max": 50,
                        "tooltip": "Distilled model works well at 4–12 steps",
                    },
                ),
                "guidance_scale": (
                    "FLOAT",
                    {"default": 1.0, "min": 1.0, "max": 5.0, "step": 0.1},
                ),
                "enable_safety_checker": ("BOOLEAN", {"default": True}),
                "expand_prompt": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "seed": ("INT", {"default": -1}),
                "custom_width": (
                    "INT",
                    {"default": 1280, "min": 256, "max": 2048, "step": 32},
                ),
                "custom_height": (
                    "INT",
                    {"default": 720, "min": 256, "max": 2048, "step": 32},
                ),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("video_url",)
    FUNCTION = "generate_video"
    CATEGORY = "FAL/LTX23"

    def generate_video(
        self,
        prompt,
        negative_prompt,
        resolution,
        num_frames,
        frame_rate,
        num_inference_steps,
        guidance_scale,
        enable_safety_checker,
        expand_prompt,
        seed=-1,
        custom_width=1280,
        custom_height=720,
    ):
        try:
            width, height = _parse_resolution(resolution, custom_width, custom_height)

            arguments = {
                "prompt": prompt,
                "negative_prompt": negative_prompt,
                "num_frames": num_frames,
                "frame_rate": frame_rate,
                "width": width,
                "height": height,
                "num_inference_steps": num_inference_steps,
                "guidance_scale": guidance_scale,
                "enable_safety_checker": enable_safety_checker,
                "expand_prompt": expand_prompt,
            }

            if seed != -1:
                arguments["seed"] = seed

            result = ApiHandler.submit_and_get_result(
                "fal-ai/ltx-video/v2.3/distilled/text-to-video", arguments
            )
            return (result["video"]["url"],)
        except Exception as e:
            return ApiHandler.handle_video_generation_error(
                "ltx-video/v2.3/distilled/t2v", str(e)
            )


# ---------------------------------------------------------------------------
# Distilled (fast) Image-to-Video
# ---------------------------------------------------------------------------

class LTX23DistilledImageToVideoNode:
    """LTX Video 2.3 Distilled (fast) Image-to-Video via fal.ai.

    Uses fal-ai/ltx-video/v2.3/distilled/image-to-video.
    Connect end_frame for first-last-frame conditioning.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "start_frame": ("IMAGE",),
                "negative_prompt": (
                    "STRING",
                    {
                        "default": (
                            "worst quality, inconsistent motion, blurry, jittery, "
                            "distorted"
                        ),
                        "multiline": True,
                    },
                ),
                "resolution": (RESOLUTION_PRESETS, {"default": "1280x720"}),
                "num_frames": (
                    "INT",
                    {"default": 121, "min": 9, "max": 257, "step": 8},
                ),
                "frame_rate": ("INT", {"default": 25, "min": 8, "max": 60}),
                "num_inference_steps": (
                    "INT",
                    {"default": 8, "min": 1, "max": 50},
                ),
                "guidance_scale": (
                    "FLOAT",
                    {"default": 1.0, "min": 1.0, "max": 5.0, "step": 0.1},
                ),
                "enable_safety_checker": ("BOOLEAN", {"default": True}),
                "expand_prompt": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "end_frame": ("IMAGE",),
                "seed": ("INT", {"default": -1}),
                "custom_width": (
                    "INT",
                    {"default": 1280, "min": 256, "max": 2048, "step": 32},
                ),
                "custom_height": (
                    "INT",
                    {"default": 720, "min": 256, "max": 2048, "step": 32},
                ),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("video_url",)
    FUNCTION = "generate_video"
    CATEGORY = "FAL/LTX23"

    def generate_video(
        self,
        prompt,
        start_frame,
        negative_prompt,
        resolution,
        num_frames,
        frame_rate,
        num_inference_steps,
        guidance_scale,
        enable_safety_checker,
        expand_prompt,
        end_frame=None,
        seed=-1,
        custom_width=1280,
        custom_height=720,
    ):
        try:
            start_url = ImageUtils.upload_image(start_frame)
            if not start_url:
                return ApiHandler.handle_video_generation_error(
                    "ltx-video/v2.3/distilled/i2v", "Failed to upload start frame"
                )

            width, height = _parse_resolution(resolution, custom_width, custom_height)

            if end_frame is not None:
                end_url = ImageUtils.upload_image(end_frame)
                if not end_url:
                    return ApiHandler.handle_video_generation_error(
                        "ltx-video/v2.3/distilled/i2v", "Failed to upload end frame"
                    )
                endpoint = "fal-ai/ltx-video/v2.3/distilled/extend-video"
                arguments = {
                    "prompt": prompt,
                    "negative_prompt": negative_prompt,
                    "image_url": start_url,
                    "last_image_url": end_url,
                    "num_frames": num_frames,
                    "frame_rate": frame_rate,
                    "width": width,
                    "height": height,
                    "num_inference_steps": num_inference_steps,
                    "guidance_scale": guidance_scale,
                    "enable_safety_checker": enable_safety_checker,
                    "expand_prompt": expand_prompt,
                }
            else:
                endpoint = "fal-ai/ltx-video/v2.3/distilled/image-to-video"
                arguments = {
                    "prompt": prompt,
                    "negative_prompt": negative_prompt,
                    "image_url": start_url,
                    "num_frames": num_frames,
                    "frame_rate": frame_rate,
                    "width": width,
                    "height": height,
                    "num_inference_steps": num_inference_steps,
                    "guidance_scale": guidance_scale,
                    "enable_safety_checker": enable_safety_checker,
                    "expand_prompt": expand_prompt,
                }

            if seed != -1:
                arguments["seed"] = seed

            result = ApiHandler.submit_and_get_result(endpoint, arguments)
            return (result["video"]["url"],)
        except Exception as e:
            return ApiHandler.handle_video_generation_error(
                "ltx-video/v2.3/distilled/i2v", str(e)
            )


# ---------------------------------------------------------------------------
# Node registrations
# ---------------------------------------------------------------------------

NODE_CLASS_MAPPINGS = {
    "LTX23TextToVideo_fal": LTX23TextToVideoNode,
    "LTX23ImageToVideo_fal": LTX23ImageToVideoNode,
    "LTX23VideoToVideo_fal": LTX23VideoToVideoNode,
    "LTX23DistilledTextToVideo_fal": LTX23DistilledTextToVideoNode,
    "LTX23DistilledImageToVideo_fal": LTX23DistilledImageToVideoNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LTX23TextToVideo_fal": "LTX 2.3 Text-to-Video (fal)",
    "LTX23ImageToVideo_fal": "LTX 2.3 Image-to-Video (fal)",
    "LTX23VideoToVideo_fal": "LTX 2.3 Video-to-Video / Extend (fal)",
    "LTX23DistilledTextToVideo_fal": "LTX 2.3 Distilled Text-to-Video (fal)",
    "LTX23DistilledImageToVideo_fal": "LTX 2.3 Distilled Image-to-Video (fal)",
}
