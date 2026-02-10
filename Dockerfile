# Orpheus TTS RunPod Serverless
FROM runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    wget \
    curl \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /

# Install Python dependencies
COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install orpheus-speech with vllm
RUN pip install orpheus-speech
RUN pip install vllm==0.7.3

# Copy handler
COPY rp_handler.py /rp_handler.py

# Pre-download model weights to speed up cold starts
RUN python -c "from huggingface_hub import snapshot_download; snapshot_download('canopylabs/orpheus-tts-0.1-finetune-prod')"

CMD ["python3", "-u", "/rp_handler.py"]
