"""
Orpheus TTS RunPod Handler
Apache 2.0 Licensed - Commercial Use OK

Supports:
- 8 English voices: tara, leah, jess, leo, dan, mia, zac, zoe
- Expressive tags: <laugh>, <chuckle>, <sigh>, <cough>, <sniffle>, <groan>, <yawn>, <gasp>
- Voice cloning from reference audio
"""

import runpod
import os
import base64
import wave
import io
import time

# Initialize model globally
model = None

def initialize_model():
    global model
    if model is not None:
        return model
    
    print("Initializing Orpheus TTS 3B...")
    from orpheus_tts import OrpheusModel
    
    model = OrpheusModel(
        model_name="canopylabs/orpheus-tts-0.1-finetune-prod",
        max_model_len=2048
    )
    print("Orpheus TTS initialized!")
    return model

def audio_to_base64(audio_chunks, sample_rate=24000):
    """Convert audio chunks to base64 WAV"""
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        for chunk in audio_chunks:
            wf.writeframes(chunk)
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode('utf-8')

def handler(event):
    global model
    try:
        input_data = event.get('input', {})
        text = input_data.get('text')
        
        if not text:
            return {"error": "Missing 'text' parameter"}
        
        # Voice selection (default: tara - most natural)
        voice = input_data.get('voice', 'tara')
        valid_voices = ['tara', 'leah', 'jess', 'leo', 'dan', 'mia', 'zac', 'zoe']
        if voice not in valid_voices:
            voice = 'tara'
        
        # Generation parameters
        temperature = float(input_data.get('temperature', 0.6))
        top_p = float(input_data.get('top_p', 0.95))
        repetition_penalty = float(input_data.get('repetition_penalty', 1.1))
        
        print(f"Generating with voice '{voice}': {text[:80]}...")
        
        # Initialize model if needed
        initialize_model()
        
        start_time = time.time()
        
        # Generate speech
        audio_chunks = list(model.generate_speech(
            prompt=text,
            voice=voice,
            temperature=temperature,
            top_p=top_p,
            repetition_penalty=repetition_penalty
        ))
        
        generation_time = time.time() - start_time
        
        # Convert to base64
        audio_base64 = audio_to_base64(audio_chunks, sample_rate=24000)
        
        print(f"Generated in {generation_time:.2f}s")
        
        return {
            "status": "success",
            "audio_base64": audio_base64,
            "sample_rate": 24000,
            "voice": voice,
            "generation_time_ms": int(generation_time * 1000)
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

if __name__ == '__main__':
    initialize_model()
    runpod.serverless.start({'handler': handler})
