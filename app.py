import os, uuid, subprocess
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

DATA = Path(os.getenv("DATA_DIR", "/data"))
UPLOADS = DATA / "uploads"
OUTPUTS = DATA / "outputs"
UPLOADS.mkdir(parents=True, exist_ok=True)
OUTPUTS.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="Editing Clips Cloud API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/")
def home():
    return {"service": "Editing Clips Cloud API", "status": "running"}

@app.post("/clips")
async def create_clip(
    video: UploadFile = File(...),
    start: float = Form(0),
    duration: int = Form(30),
    caption: str = Form("")
):
    if duration not in (30, 45, 60):
        raise HTTPException(400, "duration must be 30, 45, or 60 seconds")
    job = uuid.uuid4().hex
    source = UPLOADS / f"{job}_{Path(video.filename or 'video').name}"
    output = OUTPUTS / f"{job}.mp4"
    with source.open("wb") as f:
        while chunk := await video.read(1024 * 1024):
            f.write(chunk)
    draw = "drawtext=text='" + caption.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'") + "':fontcolor=white:fontsize=42:box=1:boxcolor=black@0.5:x=(w-text_w)/2:y=h*0.78"
    vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"
    if caption.strip():
        vf += "," + draw
    cmd = ["ffmpeg", "-y", "-ss", str(max(0, start)), "-i", str(source), "-t", str(duration),
           "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
           "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(output)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode:
        raise HTTPException(500, "FFmpeg processing failed: " + result.stderr[-1200:])
    return FileResponse(output, media_type="video/mp4", filename="editing-clips.mp4")
