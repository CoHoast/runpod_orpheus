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

# Model will download at runtime (first request will be slow)
# To speed up: add HF_TOKEN env var in RunPod settings

CMD ["python3", "-u", "/rp_handler.py"]
