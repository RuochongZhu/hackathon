# Shiny for Python Demo (Hackathon)

A minimal Shiny for Python starter app for the AI Systems Hackathon.

## What This App Does

This interactive app includes:
- A sidebar slider for number of points
- A text input for custom labels
- Reactive output that updates immediately

## File Structure

- **`app.py`** - Shiny app UI and server logic
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
python -m shiny run app.py --host 0.0.0.0 --port 8000
```

Open `http://localhost:8000` and test reactivity.

## Deployment Paths

- **DigitalOcean App Platform**: deploy this folder using the included `Dockerfile`.
- **Posit Connect / Posit Connect Cloud**: run `./manifestme.sh` to generate `manifest.json`, then deploy from this folder.

## Notes

- Put API keys and other secrets in deployment environment variables.
