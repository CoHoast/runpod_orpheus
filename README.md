# Orpheus TTS - RunPod Serverless

High-quality text-to-speech using Orpheus TTS 3B model.

## Features

- **8 Built-in Voices:** tara, leah, jess, leo, dan, mia, zac, zoe
- **Expressive Tags:** `<laugh>`, `<chuckle>`, `<sigh>`, `<cough>`, `<sniffle>`, `<groan>`, `<yawn>`, `<gasp>`
- **Apache 2.0 License:** Commercial use OK

## API Usage

```bash
curl -X POST "https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "text": "Hello! <laugh> This is a test of Orpheus TTS.",
      "voice": "tara"
    }
  }'
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| text | string | required | Text to synthesize (supports expressive tags) |
| voice | string | "tara" | Voice: tara, leah, jess, leo, dan, mia, zac, zoe |
| temperature | float | 0.6 | Generation temperature |
| top_p | float | 0.95 | Top-p sampling |
| repetition_penalty | float | 1.1 | Repetition penalty (required for stability) |

## Expressive Tags

Insert these tags in your text for natural expressions:

- `<laugh>` - Laughter
- `<chuckle>` - Light chuckle
- `<sigh>` - Sigh
- `<cough>` - Cough
- `<sniffle>` - Sniffle
- `<groan>` - Groan
- `<yawn>` - Yawn
- `<gasp>` - Gasp

## Response

```json
{
  "status": "success",
  "audio_base64": "...",
  "sample_rate": 24000,
  "voice": "tara",
  "generation_time_ms": 1234
}
```

## Recommended GPU

- **48GB A40** or **24GB L4** for best performance
- Model requires ~16-20GB VRAM
# Trigger rebuild
