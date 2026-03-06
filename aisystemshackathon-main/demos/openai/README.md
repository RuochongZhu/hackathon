# OpenAI Demo (Hackathon)

This folder contains lightweight OpenAI API workflow demos for the AI Systems Hackathon in both Python and R.

## Purpose

Use these scripts to verify your `OPENAI_API_KEY`, send a simple prompt, and inspect the response payload structure before integrating model calls into APIs or apps.

## Files

- `workflow.py` - Primary Python workflow script
- `workflow.R` - Primary R workflow script
- `04_openai.py` - Original numbered variant (kept for continuity)
- `04_openai.R` - Original numbered variant (kept for continuity)
- `ACTIVITY_openai_api_key.md` - Setup activity for OpenAI credentials

## Environment Variables

Create a `.env` file in the project root (or current working directory) with:

```bash
OPENAI_API_KEY=your_api_key_here
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
install.packages(c("httr2", "jsonlite", "purrr"))
source("workflow.R")
```

## Deployment Notes

When you deploy apps/APIs that call OpenAI:
- Set `OPENAI_API_KEY` in DigitalOcean App Platform environment variables.
- Set `OPENAI_API_KEY` in Posit Connect / Posit Connect Cloud environment variables.
