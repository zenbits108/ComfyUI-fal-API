import os
import re
import time
import json
from pathlib import Path

import requests
import folder_paths


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_output_dir():
    """Return ComfyUI's output directory."""
    return folder_paths.get_output_directory()


def _next_filename(directory: str, prefix: str, extension: str) -> tuple[str, str]:
    """Find the next available auto-incremented filename.

    Returns (full_path, filename_only).
    """
    extension = extension.lstrip(".")
    existing = []
    pattern = re.compile(rf"^{re.escape(prefix)}_(\d+)\.{extension}$")
    if os.path.isdir(directory):
        for f in os.listdir(directory):
            m = pattern.match(f)
            if m:
                existing.append(int(m.group(1)))
    next_idx = (max(existing) + 1) if existing else 1
    filename = f"{prefix}_{next_idx:05d}.{extension}"
    return os.path.join(directory, filename), filename


def _sanitize_prefix(prefix: str) -> str:
    """Strip characters that are unsafe in filenames."""
    return re.sub(r'[\\/:*?"<>|]', "_", prefix).strip("_") or "video"


# ---------------------------------------------------------------------------
# SaveVideoFromURL
# ---------------------------------------------------------------------------

class SaveVideoFromURL:
    """Download a video from a URL and save it to ComfyUI's output directory.

    Works with any node that returns a video_url STRING — LTX 2.3, Kling,
    Veo 3.1, Seedance, Wan, MiniMax, etc.

    Outputs
    -------
    saved_path  : absolute path of the saved file (useful for ffmpeg nodes)
    filename    : just the filename (e.g. my_shot_00003.mp4)
    video_url   : passes the original URL through for chaining
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video_url": ("STRING", {"default": ""}),
                "filename_prefix": (
                    "STRING",
                    {
                        "default": "fal_video",
                        "tooltip": "Base name used for auto-incremented files, e.g. 'shot_01'",
                    },
                ),
                "subfolder": (
                    "STRING",
                    {
                        "default": "",
                        "tooltip": (
                            "Optional subfolder inside ComfyUI's output directory. "
                            "Leave blank to save directly in output/."
                        ),
                    },
                ),
                "format": (
                    ["mp4", "webm", "mov", "gif", "auto"],
                    {
                        "default": "auto",
                        "tooltip": (
                            "'auto' detects format from the URL; "
                            "choose a specific format to force the extension."
                        ),
                    },
                ),
                "timeout": (
                    "INT",
                    {
                        "default": 300,
                        "min": 10,
                        "max": 1800,
                        "tooltip": "Download timeout in seconds.",
                    },
                ),
                "overwrite": (
                    "BOOLEAN",
                    {
                        "default": False,
                        "tooltip": (
                            "If True, skip auto-increment and overwrite using just "
                            "the prefix name (useful for preview/iteration loops)."
                        ),
                    },
                ),
            },
            "optional": {
                "metadata_prompt": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": True,
                        "tooltip": (
                            "Optional: embed the generation prompt as a sidecar "
                            ".txt file next to the video."
                        ),
                    },
                ),
            },
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("saved_path", "filename", "video_url")
    FUNCTION = "save_video"
    CATEGORY = "FAL/Utility"
    OUTPUT_NODE = True

    def save_video(
        self,
        video_url,
        filename_prefix,
        subfolder,
        format,
        timeout,
        overwrite,
        metadata_prompt="",
    ):
        try:
            if not video_url or video_url.strip() == "":
                print("[SaveVideoFromURL] Error: no video_url provided.")
                return ("", "", video_url)

            video_url = video_url.strip()

            # ----------------------------------------------------------------
            # Resolve output directory
            # ----------------------------------------------------------------
            base_output = _get_output_dir()
            if subfolder.strip():
                output_dir = os.path.join(base_output, subfolder.strip())
            else:
                output_dir = base_output
            os.makedirs(output_dir, exist_ok=True)

            # ----------------------------------------------------------------
            # Determine file extension
            # ----------------------------------------------------------------
            if format == "auto":
                # Try to detect from URL (strip query params first)
                url_path = video_url.split("?")[0].rstrip("/")
                ext = Path(url_path).suffix.lstrip(".").lower()
                if ext not in ("mp4", "webm", "mov", "gif"):
                    ext = "mp4"  # safe fallback
            else:
                ext = format

            # ----------------------------------------------------------------
            # Build filename
            # ----------------------------------------------------------------
            prefix = _sanitize_prefix(filename_prefix)

            if overwrite:
                filename = f"{prefix}.{ext}"
                saved_path = os.path.join(output_dir, filename)
            else:
                saved_path, filename = _next_filename(output_dir, prefix, ext)

            # ----------------------------------------------------------------
            # Download
            # ----------------------------------------------------------------
            print(f"[SaveVideoFromURL] Downloading {video_url}")
            print(f"[SaveVideoFromURL] → {saved_path}")

            headers = {"User-Agent": "ComfyUI-fal-API/1.0"}
            response = requests.get(
                video_url, stream=True, timeout=timeout, headers=headers
            )
            response.raise_for_status()

            total_bytes = 0
            with open(saved_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024 * 256):
                    if chunk:
                        f.write(chunk)
                        total_bytes += len(chunk)

            size_mb = total_bytes / (1024 * 1024)
            print(f"[SaveVideoFromURL] Saved {filename} ({size_mb:.2f} MB)")

            # ----------------------------------------------------------------
            # Optional sidecar .txt with prompt metadata
            # ----------------------------------------------------------------
            if metadata_prompt.strip():
                sidecar_path = os.path.splitext(saved_path)[0] + ".txt"
                with open(sidecar_path, "w", encoding="utf-8") as f:
                    f.write(f"source_url: {video_url}\n")
                    f.write(f"prompt:\n{metadata_prompt.strip()}\n")
                print(f"[SaveVideoFromURL] Sidecar written → {sidecar_path}")

            return (saved_path, filename, video_url)

        except requests.exceptions.Timeout:
            print(f"[SaveVideoFromURL] Timeout after {timeout}s downloading {video_url}")
            return ("", "", video_url)
        except requests.exceptions.HTTPError as e:
            print(f"[SaveVideoFromURL] HTTP error: {e}")
            return ("", "", video_url)
        except Exception as e:
            print(f"[SaveVideoFromURL] Unexpected error: {e}")
            return ("", "", video_url)


# ---------------------------------------------------------------------------
# VideoURLToPreview  — wraps saved_path for ComfyUI's built-in video preview
# ---------------------------------------------------------------------------

class VideoURLPreview:
    """Preview a video directly in the ComfyUI UI from a video_url string.

    Downloads to a temp location in output/ and registers it for the
    ComfyUI frontend preview panel (same mechanism as VHS/VideoHelper).
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video_url": ("STRING", {"default": ""}),
                "timeout": ("INT", {"default": 300, "min": 10, "max": 1800}),
            },
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("saved_path", "video_url")
    FUNCTION = "preview_video"
    CATEGORY = "FAL/Utility"
    OUTPUT_NODE = True

    def preview_video(self, video_url, timeout):
        try:
            if not video_url or video_url.strip() == "":
                return {"ui": {"videos": []}, "result": ("", video_url)}

            video_url = video_url.strip()
            output_dir = _get_output_dir()
            preview_dir = os.path.join(output_dir, "fal_previews")
            os.makedirs(preview_dir, exist_ok=True)

            url_path = video_url.split("?")[0].rstrip("/")
            ext = Path(url_path).suffix.lstrip(".").lower()
            if ext not in ("mp4", "webm", "mov", "gif"):
                ext = "mp4"

            timestamp = int(time.time())
            filename = f"preview_{timestamp}.{ext}"
            saved_path = os.path.join(preview_dir, filename)

            headers = {"User-Agent": "ComfyUI-fal-API/1.0"}
            response = requests.get(
                video_url, stream=True, timeout=timeout, headers=headers
            )
            response.raise_for_status()

            with open(saved_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024 * 256):
                    if chunk:
                        f.write(chunk)

            print(f"[VideoURLPreview] Preview saved → {saved_path}")

            # ComfyUI preview registration — subfolder relative to output/
            return {
                "ui": {
                    "videos": [
                        {
                            "filename": filename,
                            "subfolder": "fal_previews",
                            "type": "output",
                        }
                    ]
                },
                "result": (saved_path, video_url),
            }

        except Exception as e:
            print(f"[VideoURLPreview] Error: {e}")
            return {"ui": {"videos": []}, "result": ("", video_url)}


# ---------------------------------------------------------------------------
# PassthroughVideoURL  — simple no-op relay for routing video_url strings
# ---------------------------------------------------------------------------

class PassthroughVideoURL:
    """Route a video_url through a labelled node for workflow clarity.

    Useful when you want to visually distinguish which video URL is going
    where in a complex workflow without any processing overhead.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video_url": ("STRING", {"default": ""}),
                "label": (
                    "STRING",
                    {
                        "default": "video",
                        "tooltip": "Human-readable label — has no effect on output.",
                    },
                ),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("video_url",)
    FUNCTION = "passthrough"
    CATEGORY = "FAL/Utility"

    def passthrough(self, video_url, label):
        return (video_url,)


# ---------------------------------------------------------------------------
# Node registrations
# ---------------------------------------------------------------------------

NODE_CLASS_MAPPINGS = {
    "SaveVideoFromURL_fal": SaveVideoFromURL,
    "VideoURLPreview_fal": VideoURLPreview,
    "PassthroughVideoURL_fal": PassthroughVideoURL,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveVideoFromURL_fal": "Save Video from URL (fal)",
    "VideoURLPreview_fal": "Preview Video from URL (fal)",
    "PassthroughVideoURL_fal": "Passthrough Video URL (fal)",
}
