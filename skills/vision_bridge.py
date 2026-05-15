#!/usr/bin/env python3
"""Vision bridge skill - describe images using multiple vision APIs."""

import os
import sys
import base64
import json
import urllib.request
import urllib.error

DEFAULT_NVIDIA_MODEL = "google/paligemma"  # phi-4 degraded, using paligemma

# Other good NVIDIA vision models:
# microsoft/phi-4-multimodal-instruct - better descriptions
# nvidia/llama-3.1-nemotron-nano-4b-vl-4k - NVIDIA's own model

def get_api_key(provider='google'):
    """Get API key from environment or file."""
    if provider == 'google':
        key = os.environ.get('GOOGLE_API_KEY') or os.environ.get('GOOGLE_GENERATIVE_AI_API_KEY')
        env_key = 'GOOGLE_API_KEY'
    elif provider == 'nvidia':
        key = os.environ.get('NVIDIA_API_KEY')
        env_key = 'NVIDIA_API_KEY'
    else:
        env_key = f'{provider.upper()}_API_KEY'
        key = os.environ.get(env_key)

    if not key:
        env_path = r'D:\Olympus\MASTER_API_KEYS.env'
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                for line in f:
                    if line.startswith(f'{env_key}='):
                        key = line.strip().split('=', 1)[1]
                        break
    return key

def describe_image_google(image_data, mime_type, prompt, api_key):
    """Call Google Gemini API to describe an image."""
    url = "https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key=" + api_key
    payload = {
        "contents": [{
            "role": "user",
            "parts": [
                {"text": prompt},
                {"inline_data": {"mime_type": mime_type, "data": image_data}}
            ]
        }],
        "generationConfig": {"maxOutputTokens": 1024, "temperature": 0.4}
    }
    try:
        req = urllib.request.Request(
            url, data=json.dumps(payload).encode(),
            headers={'Content-Type': 'application/json'}, method='POST'
        )
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            if 'candidates' in result and len(result['candidates']) > 0:
                parts = result['candidates'][0].get('content', {}).get('parts', [])
                return {"description": ' '.join(p.get('text', '') for p in parts)}
            return {"error": "No description in response", "raw": result}
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.read().decode()}"}
    except Exception as e:
        return {"error": str(e)}

def describe_image_nvidia(image_data, mime_type, prompt, api_key, model=None):
    """Call NVIDIA API to describe an image."""
    model = model or DEFAULT_NVIDIA_MODEL
    url = f"https://ai.api.nvidia.com/v1/vlm/{model}"
    # Special handling for phi-4 which uses chat/completions endpoint
    if 'phi-4' in model:
        url = "https://integrate.api.nvidia.com/v1/chat/completions"
        payload = {
            "model": model,
            "messages": [{
                "role": "user",
                "content": f'{prompt} <img src="data:{mime_type};base64,{image_data}" />'
            }],
            "max_tokens": 512,
            "temperature": 0.7,
            "top_p": 0.70,
            "stream": False
        }
    else:
        payload = {
            "messages": [{
                "role": "user",
                "content": f'{prompt} <img src="data:{mime_type};base64,{image_data}" />'
            }],
            "max_tokens": 512,
            "temperature": 0.7,
            "top_p": 0.70,
            "stream": False
        }
    try:
        req = urllib.request.Request(
            url, data=json.dumps(payload).encode(),
            headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {api_key}'},
            method='POST'
        )
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            desc = result.get('choices', [{}])[0].get('message', {}).get('content', '')
            return {"description": desc or "No description", "model": model}
    except urllib.error.HTTPError as e:
        try:
            err = json.loads(e.read().decode())
        except:
            err = {"error": e.read().decode()}
        return {"error": f"HTTP {e.code}", "details": err, "model": model}
    except Exception as e:
        return {"error": str(e), "model": model}

def describe_image(image_path=None, image_url=None, prompt=None, provider='nvidia', nvidia_model=None):
    """Call vision API to describe an image."""
    if provider == 'nvidia':
        api_key = get_api_key('nvidia')
        if not api_key:
            return {"error": "No NVIDIA_API_KEY found"}
    else:
        api_key = get_api_key('google')
        if not api_key:
            return {"error": "No GOOGLE_API_KEY found in environment or MASTER_API_KEYS.env"}

    if not image_path and not image_url:
        return {"error": "No image path or URL provided"}

    image_data = None
    mime_type = "image/jpeg"

    if image_path and os.path.exists(image_path):
        with open(image_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode()
        ext = os.path.splitext(image_path)[1].lower()
        mime_map = {'.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.gif': 'image/gif', '.webp': 'image/webp'}
        mime_type = mime_map.get(ext, 'image/jpeg')
    elif image_url:
        try:
            req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as resp:
                image_data = base64.b64encode(resp.read()).decode()
                content_type = resp.headers.get('Content-Type', 'image/jpeg')
                if content_type.startswith('image/'):
                    mime_type = content_type
        except Exception as e:
            return {"error": f"Failed to download image: {e}"}
    else:
        return {"error": "Image file not found"}

    user_prompt = prompt or "What is in this image?"

    if provider == 'nvidia':
        return describe_image_nvidia(image_data, mime_type, user_prompt, api_key, nvidia_model)
    else:
        return describe_image_google(image_data, mime_type, user_prompt, api_key)

if __name__ == "__main__":
    args = sys.argv[1:]
    image_path = None
    image_url = None
    prompt = None
    provider = 'google'
    nvidia_model = None

    i = 0
    while i < len(args):
        if args[i] == '--path' and i + 1 < len(args):
            image_path = args[i + 1]
            i += 2
        elif args[i] == '--url' and i + 1 < len(args):
            image_url = args[i + 1]
            i += 2
        elif args[i] == '--prompt' and i + 1 < len(args):
            prompt = args[i + 1]
            i += 2
        elif args[i] == '--nvidia':
            provider = 'nvidia'
            i += 1
        elif args[i] == '--model-nvidia' and i + 1 < len(args):
            nvidia_model = args[i + 1]
            i += 2
        elif args[i].startswith('http'):
            image_url = args[i]
            i += 1
        elif not args[i].startswith('--'):
            image_path = args[i]
            i += 1
        else:
            i += 1

    result = describe_image(image_path=image_path, image_url=image_url, prompt=prompt, provider=provider, nvidia_model=nvidia_model)
    print(json.dumps(result, indent=2))