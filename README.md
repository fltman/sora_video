# Sora Video Generator

[![Support me on Patreon](https://img.shields.io/badge/Patreon-Support%20my%20work-FF424D?style=flat&logo=patreon&logoColor=white)](https://www.patreon.com/AndersBjarby)

A small command-line script that generates a video from a text prompt using OpenAI's Sora video API. It creates the job, polls until the render is complete, and downloads the resulting MP4.

## Setup

```bash
pip install openai
export OPENAI_API_KEY=sk-...
```

## Usage

```bash
python generate_video.py "a cat surfing a wave at sunset"
python generate_video.py "a city skyline timelapse" -o skyline.mp4 -i 10
```

- `prompt` — the text description of the video to generate
- `-o, --output` — output file path (default: `video.mp4`)
- `-i, --interval` — status poll interval in seconds (default: `5`)

## Tech

Python, OpenAI Python SDK (`client.videos`).
