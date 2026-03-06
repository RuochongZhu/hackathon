# Plumber API Demo (Hackathon)

A minimal R Plumber API starter for the AI Systems Hackathon.

## What This App Does

This API includes:
- `GET /echo` - Echo a message parameter
- `GET /plot` - Return a histogram image
- `POST /sum` - Add two numbers

The API uses JSON serialization for clean API responses.

## File Structure

- **`plumber.R`** - API routes and handlers
- **`Dockerfile`** - Container setup for DigitalOcean App Platform
- **`testme.R`** - Local run helper
- **`manifestme.R`** - Posit deployment manifest helper

## Local Test

Run:

```r
source("testme.R")
```

Or manually:

```r
library(plumber)
pr = plumber::plumb("plumber.R")
pr$run(host = "0.0.0.0", port = 8000)
```

Then test:
- `http://localhost:8000/echo?msg=hello`
- `http://localhost:8000/plot`

## Deployment Paths

- **DigitalOcean App Platform**: use this folder with the included `Dockerfile`.
- **Posit Connect / Posit Connect Cloud**: run `Rscript manifestme.R` to generate `manifest.json`, then publish from this folder.

## Notes

- Keep credentials and API keys in deployment environment variables, not in committed files.
