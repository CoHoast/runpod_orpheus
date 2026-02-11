"""
Orpheus TTS RunPod Handler
Apache 2.0 Licensed - Commercial Use OK

Supports:
- 8 English voices: tara, leah, jess, leo, dan, mia, zac, zoe
- Expressive tags: <laugh>, <chuckle>, <sigh>, <cough>, <sniffle>, <groan>, <yawn>, <gasp>
- Voice cloning from reference audio (10-30 seconds WAV)
"""

import runpod
import os
import base64
import wave
import io
import time
import tempfile

# Initialize model globally
model = None

def initialize_model():
    global model
    if model is not None:
        return model
    
    print("Initializing Orpheus TTS 3B...")
    from orpheus_tts import OrpheusModel
    
    model = OrpheusModel(model_name="canopylabs/orpheus-tts-0.1-finetune-prod")
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
        
        # Voice cloning: base64 encoded WAV audio (10-30 seconds recommended)
        audio_prompt_base64 = input_data.get('audio_prompt_base64')
        
        # Initialize model if needed
        initialize_model()
        
        start_time = time.time()
        audio_prompt_path = None
        
        try:
            if audio_prompt_base64:
                # Voice cloning mode
                print(f"Voice cloning mode - generating: {text[:80]}...")
                
                # Save reference audio to temp file
                with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
                    tmp.write(base64.b64decode(audio_prompt_base64))
                    audio_prompt_path = tmp.name
                
                # Format prompt with voice prefix for cloning
                prompt = f"{voice}: {text}"
                
                # Generate with voice cloning
                audio_chunks = list(model.generate_with_voice_clone(
                    prompt=prompt,
                    audio_ref=audio_prompt_path
                ))
            else:
                # Standard voice mode
                print(f"Generating with voice '{voice}': {text[:80]}...")
                
                # Generate speech
                audio_chunks = list(model.generate_speech(
                    prompt=text,
                    voice=voice,
                    temperature=temperature,
                    top_p=top_p,
                    repetition_penalty=repetition_penalty
                ))
        finally:
            # Clean up temp file
            if audio_prompt_path and os.path.exists(audio_prompt_path):
                os.unlink(audio_prompt_path)
        
        generation_time = time.time() - start_time
        
        # Convert to base64
        audio_base64 = audio_to_base64(audio_chunks, sample_rate=24000)
        
        print(f"Generated in {generation_time:.2f}s")
        
        return {
            "status": "success",
            "audio_base64": audio_base64,
            "sample_rate": 24000,
            "voice": voice,
            "cloned": audio_prompt_base64 is not None,
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
