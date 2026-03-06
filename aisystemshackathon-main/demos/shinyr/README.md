# Shiny for R Demo (Hackathon)

A minimal Shiny for R starter app for the AI Systems Hackathon.

## What This App Does

This app shows a histogram of the built-in `faithful` dataset with:
- A slider for the number of bins
- A reactive histogram plot
- A text output showing current bin count

## File Structure

- **`app.R`** - Shiny app UI and server logic
- **`workflow.R`** - Optional local workflow/testing script
- **`Dockerfile`** - Container setup for DigitalOcean App Platform
- **`testme.sh`** - Local run helper
- **`manifestme.R`** - Posit deployment manifest helper

## Local Test

```bash
./testme.sh
```

Or manually from this folder:

```bash
Rscript -e "shiny::runApp('app.R', host='0.0.0.0', port=3838)"
```

Open `http://localhost:3838`.

## Deployment Paths

- **DigitalOcean App Platform**: deploy this folder with the included `Dockerfile`.
- **Posit Connect / Posit Connect Cloud**: run `Rscript manifestme.R` to generate `manifest.json`, then deploy from this folder.

## Notes

- Configure sensitive values through deployment environment variables.
