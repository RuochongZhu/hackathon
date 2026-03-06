# FastAPI Demo (Hackathon)

A minimal FastAPI REST API starter for the AI Systems Hackathon.

## What This App Does

This API includes:
- `GET /` - Root endpoint with API information
- `GET /echo` - Echo a message parameter
- `POST /sum` - Add two numbers
- `GET /docs` - Interactive OpenAPI docs from FastAPI

## File Structure

- **`app.py`** - FastAPI routes and app object
- **`requirements.txt`** - Python dependencies
- **`Dockerfile`** - Container setup for DigitalOcean App Platform
- **`testme.sh`** - Local run helper
- **`manifestme.sh`** - Posit deployment manifest helper

## Local Test

```bash
./testme.sh
```

Or manually from this folder:

```bash
python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

Then test:
- `http://localhost:8000/`
- `http://localhost:8000/docs`
- `http://localhost:8000/echo?msg=hello`

## Deployment Paths

- **DigitalOcean App Platform**: use this folder with the included `Dockerfile`.
- **Posit Connect / Posit Connect Cloud**: run `./manifestme.sh` first to generate `manifest.json`, then publish from this folder.

## Notes

- For Posit, configure environment variables (API keys, secrets) in deployment settings rather than committing them in code.
