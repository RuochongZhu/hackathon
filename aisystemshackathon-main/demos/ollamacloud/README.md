# Ollama Cloud Demo (Hackathon)

This folder contains lightweight Ollama Cloud API workflow demos for the AI Systems Hackathon in both Python and R.

## Purpose

Use these scripts to verify your `OLLAMA_API_KEY`, send a simple prompt, and inspect the response payload structure before integrating model calls into APIs or apps.

## Files

- `workflow.py` - Primary Python workflow script
- `workflow.R` - Primary R workflow script
- `03_ollama_cloud.py` - Original numbered variant (kept for continuity)
- `03_ollama_cloud.R` - Original numbered variant (kept for continuity)
- `ACTIVITY_ollama_api_key.md` - Setup activity for Ollama Cloud credentials

## Environment Variables

Create a `.env` file in the project root (or current working directory) with:

```bash
OLLAMA_API_KEY=your_api_key_here
```

Important:
- Do not commit `.env` to git.
- Keep API keys in local `.env` files or deployment environment settings.

## Quick Start

Python:

```bash
pip install requests python-dotenv
python workflow.py
```

R:

```r
install.packages(c("httr2", "jsonlite"))
source("workflow.R")
```

## Deployment Notes

When you deploy apps/APIs that call Ollama Cloud:
- Set `OLLAMA_API_KEY` in DigitalOcean App Platform environment variables.
- Set `OLLAMA_API_KEY` in Posit Connect / Posit Connect Cloud environment variables.
