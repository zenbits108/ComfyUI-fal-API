# ComfyUI-fal-API

Custom nodes for using Flux models with fal API in ComfyUI with only one API Key for all.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Available Nodes](#available-nodes)
  - [Image Generation](#image-generation)
  - [Video Generation](#video-generation)
  - [LTX 2.3 Video Generation](#ltx-23-video-generation)
  - [Language Models (LLMs)](#language-models-llms)
  - [Vision Language Models (VLMs)](#vision-language-models-vlms)
  - [Training](#training)
  - [Utility](#utility)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Installation

1. Navigate to your ComfyUI custom nodes directory:
   ```
   cd custom_nodes
   ```

2. Clone this repository:
   ```
   git clone https://github.com/gokayfem/ComfyUI-fal-API.git
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configuration

1. Get your fal API key from [fal.ai](https://fal.ai/dashboard/keys)

2. Open the `config.ini` file inside `custom_nodes/ComfyUI-fal-API`

3. Replace `<your_fal_api_key_here>` with your actual fal API key:
   ```ini
   [API]
   FAL_KEY = your_actual_api_key
   ```

4. Alternatively, you can set the FAL_KEY environment variable:
   ```bash
   export FAL_KEY=your_actual_api_key
   ```

## Usage

After installation and configuration, restart ComfyUI. The new nodes will be available in the node browser under the "FAL" category.

## Available Nodes

### Image Generation

- **Flux Pro (fal)**: Generate high-quality images using the Flux Pro model
- **Flux Dev (fal)**: Use the development version of Flux for image generation
- **Flux Schnell (fal)**: Fast image generation with Flux Schnell
- **Flux Pro 1.1 (fal)**: Latest version of Flux Pro for image generation
- **Flux Pro 1 Fill (fal)**: Image-to-image generation with mask-based fill capabilities
- **Flux Ultra (fal)**: Ultra-high quality image generation with advanced controls
- **Flux General (fal)**: ControlNets, Ipadapters, Loras for Flux Dev
- **Flux LoRA (fal)**: Flux with dual LoRA support for custom styles
- **Flux Pro Kontext (fal)**: Context-aware single image-to-image generation with max_quality toggle
- **Flux Pro Kontext Multi (fal)**: Multi-image composition (2-4 images) with context awareness and max_quality toggle
- **Flux Pro Kontext Text-to-Image (fal)**: Text-to-image with aspect ratio controls and max_quality toggle
- **Recraft V3 (fal)**: Professional design generation with multiple style options
- **Sana (fal)**: High-quality image synthesis with ultra-high resolution support
- **HiDream Full (fal)**: Advanced image generation with comprehensive parameter control
- **Ideogram v3 (fal)**: Advanced text-to-image generation with typography support
- **Clarity Upscaler (fal)**: Clarity upscaler for upscaling images with high very fidelity
- **Seedvr Upscaler (fal)**: Use SeedVR2 to upscale your images
- **Imagen4 Preview (fal)**: Use Imagen4 (Preview version) to generate images
- **Qwen Image Edit (fal)**: Use Qwen to edit images
- **Qwen Image Edit Plus with LoRAs (fal)**: Use Qwen Image Edit Plus with LoRA support to edit images
- **SeedEdit 3.0 (fal)**: Use SeedEdit 3.0 to edit images
- **Seedream 4.0 Edit (fal)**: Use Seedream 4.0 to edit images
- **Nano Banana Text-to-Image (fal)**: Use Nano Banana to generate images
- **Nano Banana Edit (fal)**: Use Nano Banana to edit images
- **Nano Banana Pro (fal)**: Unified node for both text-to-image and image editing with Nano Banana Pro
- **Nano Banana 2 (fal)**: Unified node for text-to-image and image editing with Nano Banana 2 (Gemini 3.1 Flash Image) with multi-resolution (0.5K-4K) and optional web search grounding
- **Reve Text-to-Image (fal)**: Use Reve's image model to generate images
- **Dreamina v3.1 Text-to-Image (fal)**: Use Dreamina v3.1 to generate images
- **GPT-Image 1.5 (fal)**: High-fidelity text-to-image generation with strong prompt adherence
- **GPT-Image 1.5 Edit (fal)**: High-fidelity image editing with strong prompt adherence (supports up to 16 batched images and optional mask)
- **DY Wan Fun 2.2 (fal)**: Generate images using DY Wan Fun 2.2 model
- **DY Wan Upscaler (fal)**: Upscale images using DY Wan Upscaler

### Video Generation

- **Infinity Star Text-to-Video (fal)**: Generate videos using Infinity Star and text prompts
- **Kling Video Generation (fal)**: Generate videos using the Kling model
- **Kling Pro v1.0 Video Generation (fal)**: Original version of Kling Pro for video generation
- **Kling Pro v1.6 Video Generation (fal)**: Latest version of Kling Pro with improved quality
- **Kling Master v2.0 Video Generation (fal)**: Advanced video generation with Kling Master
- **Kling Pro 2.1 Video Generation (fal)**: Video Generation with Kling Pro with First Frame Last Frame support
- **Kling v2.5 Turbo Pro Image-to-Video (fal)**: Video Generation with Kling Turbo with First Frame Last Frame support
- **Kling Omni Image-to-Video (fal)**: Kling Omni image-to-video generation with start/end image support
- **Kling Omni Reference-to-Video (fal)**: Generate videos with reference images and elements
- **Kling Omni Video-to-Video Edit (fal)**: Edit videos with prompts and reference images
- **Kling Omni Video-to-Video Reference (fal)**: Video-to-video with reference image control
- **Kling v2.6 Pro Video Generation (fal)**: Unified T2V/I2V with native audio generation
- **Kling V3 Standard Video Generation (fal)**: Kling 3.0 Standard unified T2V/I2V with 1080p, 3-15s duration, native audio, and end frame control
- **Kling V3 Pro Video Generation (fal)**: Kling 3.0 Pro unified T2V/I2V with higher quality cinematic output (3-15s)
- **Kling V3 Standard Motion Control (fal)**: Character animation via motion transfer from reference video
- **Kling V3 Pro Motion Control (fal)**: Pro-quality character animation via motion transfer from reference video
- **Kling O3 Standard Video Generation (fal)**: Kling O3 Standard unified T2V/I2V with 3-15s duration and native audio
- **Kling O3 Pro Video Generation (fal)**: Kling O3 Pro unified T2V/I2V with highest quality output (3-15s)
- **Krea Wan 14b Video-to-Video (fal)**: Video-to-Video generation using Krea Wan 14b model
- **Runway Gen3 Image-to-Video (fal)**: Convert images to videos using Runway Gen3
- **Luma Dream Machine (fal)**: Create videos with Luma Dream Machine
- **MiniMax Video Generation (fal)**: Generate videos using MiniMax model
- **MiniMax Text-to-Video (fal)**: Create videos from text prompts using MiniMax
- **MiniMax Subject Reference (fal)**: Generate videos with subject reference using MiniMax
- **Pixverse Swap (fal)**: Swap a person, object, or background in a video using Pixverse Swap
- **Google Veo2 Image-to-Video (fal)**: Convert images to videos using Google's Veo2 model
- **Veo3 Video Generation (fal)**: Text-to-video generation with Google Veo3 model
- **Veo 3.1 First-Last-Frame-to-Video (fal)**: First Frame - Last Frame (Optional) video generation using the full VEO 3.1 model
- **Veo 3.1 Fast First-Last-Frame-to-Video (fal)**: First Frame - Last Frame (Optional) video generation using the fast VEO 3.1 model
- **Wan Pro Image-to-Video (fal)**: High-quality video generation with Wan Pro model
- **Wan 2.5 Preview Image-to-Video (fal)**: Image-to-video generation with the latest Wan 2.5 preview model
- **Wan VACE Video Edit (fal)**: Video + Reference Images to video generation with Wan VACE
- **Wan 2.2 VACE Fun 14b (fal)**: Video editing with Wan 2.2 VACE Fun 14b model for pose and depth control
- **Wan 2.2 14b Animate: Replace Character (fal)**: Animate video content by replacing the foreground character with a new or augmented character using Wan 2.2 14b
- **Wan 2.2 14b Animate: Move Character (fal)**: Animate video content by moving the foreground character within the scene using Wan 2.2 14b
- **Wan 2.6 Video Generation (fal)**: Unified T2V/I2V node - generates video from text, or from image if provided
- **Wan 2.6 Reference-to-Video (fal)**: Generate videos with subject consistency using up to 3 reference videos (@Video1, @Video2, @Video3 in prompt)
- **Seedance Image-to-Video (fal)**: Convert images to videos using Seedance Lite model
- **Seedance Text-to-Video (fal)**: Generate videos from text prompts using Seedance Lite model
- **Seedance Pro Image-to-Video (fal)**: Convert images to videos using Seedance Pro model with advanced controls
- **Sora 2 Pro Image-to-Video (fal)**: Generate Videos from an image input using OpenAI Sora 2 Pro
- **Video Upscaler (fal)**: Upscale video quality using AI
- **Seedvr Upscale Video (fal)**: Upscale video quality using Seedvr
- **Bria Video Increase Resolution (fal)**: Increase video resolution using Bria
- **Topaz Upscale Video (fal)**: Upscale video quality using Topaz
- **Combined Video Generation (fal)**: Generate videos using multiple services simultaneously
  - Supports Kling Pro v1.6, Kling Master v2.0, MiniMax, Luma, Veo2, and Wan Pro
  - Each service can be individually enabled/disabled
  - Wan Pro runs with safety checker enabled and automatic seed selection
- **Load Video from URL**: Load and process videos from a given URL

### LTX 2.3 Video Generation

Open-source 4K video generation by Lightricks. Pay-per-second, no minimums. All nodes are found under the `FAL/LTX23` category.

#### Pricing (fal.ai, April 2026)

| Endpoint | 1080p | 1440p | 2160p |
|---|---|---|---|
| Text-to-Video (standard) | $0.08/s | $0.16/s | $0.32/s |
| Image-to-Video (standard) | $0.06/s | $0.12/s | $0.24/s |
| Text-to-Video (fast) | $0.04/s | $0.08/s | $0.16/s |
| Image-to-Video (fast) | $0.04/s | $0.08/s | $0.16/s |
| Audio-to-Video | $0.10/s | flat rate | — |
| Extend Video | $0.10/s | flat rate | — |
| Retake Video | $0.10/s | flat rate | — |

#### Nodes

- **LTX 2.3 Text-to-Video (fal)**: Generate video from a text prompt. Supports 6/8/10s duration, 1080p–2160p resolution, 16:9 or 9:16 aspect ratio, 24/25/48/50 FPS, and native audio generation.

- **LTX 2.3 Text-to-Video Fast (fal)**: Speed-optimised text-to-video. Supports up to 20s duration. Durations over 10s require 25 FPS + 1080p.

- **LTX 2.3 Image-to-Video (fal)**: Animate a start frame image. Connect an optional `end_frame` to generate a transition between two frames (first-last-frame conditioning).

- **LTX 2.3 Image-to-Video Fast (fal)**: Speed-optimised image-to-video with the same start/end frame support. Supports up to 20s duration.

- **LTX 2.3 Extend Video (fal)**: Extend an existing video clip at the start or end. Takes a `video_url` string from any generation node. Control extension duration (up to 20s), mode (`start`/`end`), and context window.

- **LTX 2.3 Audio-to-Video (fal)**: Drive video generation from an audio file URL (2–20s). Optionally anchor the first frame with a start image. Useful for music-synced or dialogue-driven shots.

- **LTX 2.3 Retake Video (fal)**: Re-generate a specific time segment of an existing video without re-rendering the whole clip. Set `start_time`, `duration`, and `retake_mode` (`replace_video`, `replace_audio`, or `replace_audio_and_video`).

#### Typical Workflow

```
[Load Image] ──► [LTX 2.3 Image-to-Video (fal)]
                          │ video_url
                          ▼
               [LTX 2.3 Extend Video (fal)]
                          │ video_url
                          ▼
               [Preview Video from URL (fal)]
                          │ video_url
                          ▼
               [Save Video from URL (fal)]
```

---

### Language Models (LLMs)

- **LLM (fal)**: Large Language Model for text generation and processing via OpenRouter endpoint
  - Available models:
    - google/gemini-2.5-flash
    - anthropic/claude-sonnet-4.5
    - openai/gpt-4.1
    - openai/gpt-oss-120b
    - meta-llama/llama-4-maverick
    - Custom (get model name from OpenRouter)

### Vision Language Models (VLMs)

- **VLM (fal)**: Vision Language Model for image understanding and text generation via OpenRouter endpoint
  - Available models:
    - google/gemini-2.5-flash
    - anthropic/claude-sonnet-4.5
    - openai/gpt-4o
    - qwen/qwen3-vl-235b-a22b-instruct
    - x-ai/grok-4-fast
    - Custom (get model name from OpenRouter)
  - Supports image captioning, visual question answering, and more

### Training

- **Flux LoRA Trainer (fal)**: Train a custom LoRA on Flux using your own images
- **Hunyuan Video LoRA Trainer (fal)**: Train a LoRA for Hunyuan Video generation
- **WAN LoRA Trainer (fal)**: Train a LoRA for WAN video generation
- **LTX Video LoRA Trainer (fal)**: Train a LoRA for LTX Video generation with scene splitting and validation options

### Utility

Utility nodes are found under the `FAL/Utility` category and work with **any** node that outputs a `video_url` STRING — not just LTX 2.3.

- **Save Video from URL (fal)**: Download a video from a URL and save it to ComfyUI's output directory.
  - Auto-increments filenames (`prefix_00001.mp4`, `prefix_00002.mp4`, ...)
  - Optional subfolder for organisation (e.g. `aphelion/s1/e03`)
  - Format auto-detection from URL, or force `mp4`/`webm`/`mov`/`gif`
  - Optional sidecar `.txt` file embedding the generation prompt and source URL
  - Outputs `saved_path`, `filename`, and passes `video_url` through for chaining
  - `overwrite` mode for fast iteration loops

- **Preview Video from URL (fal)**: Download a video and display a thumbnail preview inside the ComfyUI node panel.
  - Extracts the first frame as a PNG for native ComfyUI image preview
  - Full video saved to `output/fal_previews/` for local playback
  - Install [ComfyUI-VideoHelperSuite](https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite) for full inline video playback with audio

- **Passthrough Video URL (fal)**: Route a `video_url` string through a labelled node for workflow clarity. No processing — purely organisational.

- **LTX 2.3 Cost Estimator (fal)**: Estimate fal.ai rendering cost before committing to a generation.
  - Covers all 7 LTX 2.3 endpoints with verified pricing
  - `num_renders` multiplier for batch/episode cost planning
  - Outputs formatted cost summary string, raw USD float, and rate per second

## Troubleshooting

If you encounter any errors during installation or usage, try the following:

1. Ensure you have the latest version of ComfyUI installed
2. Update this custom node package:
   ```
   cd custom_nodes/ComfyUI-fal-API
   git pull
   pip install -r requirements.txt
   ```
3. If you're using ComfyUI Windows Portable, you may need to install fal-client manually:
   ```
   ComfyUI_windows_portable>.\python_embeded\python.exe -m pip install fal-client
   ```
4. **FAL_KEY not found**: Ensure your `config.ini` uses `[API]` as the section header and `FAL_KEY` as the key name. Environment variable `FAL_KEY` takes priority if set.
5. **Video preview not playing**: Install [ComfyUI-VideoHelperSuite](https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite) via ComfyUI Manager for full inline video playback.

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any issues or have questions, please open an issue on the [GitHub repository](https://github.com/gokayfem/ComfyUI-fal-API/issues).
