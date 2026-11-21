# Editing Clips Cloud (starter)

This is an early backend starter for processing a video file that you own or have permission to edit.

## Current features
- Upload a video file to the API
- Choose a start time and a 30, 45, or 60 second duration
- Crop to vertical 9:16 (1080x1920)
- Optionally add a simple text caption
- Export MP4 using FFmpeg

## Not included yet
- YouTube URL importing/downloading
- AI detection of viral moments
- Automatic speech recognition/subtitles
- Music, transitions, thumbnails, or AI-generated titles/tags
- A finished mobile-friendly user interface

## Run with Docker
```bash
docker compose up --build
```
Then open `http://localhost:8000` and API docs at `/docs`.

## Cloud deployment
Deploy this Docker project to a cloud host that supports Docker and persistent storage. Mount a persistent volume at `/data`. Keep in mind that video processing can use significant CPU, memory, and storage. Do not put API keys or passwords in this repository.

This starter is not hosted yet. A cloud provider account and deployment steps are still required. Ask a parent/guardian to help with any account setup or paid plan.
