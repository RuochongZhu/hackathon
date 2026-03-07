# Deployment Guide

## Automation Approach

This project uses:

- `Dockerfile` for containerized runtime
- `.do/app.yaml` for DigitalOcean App Platform spec
- `.github/workflows/ci.yml` for test checks
- `.github/workflows/deploy.yml` for automatic deployment after passing tests on `main`

## Required GitHub Secrets

Add these repository secrets before deployment:

- `DIGITALOCEAN_ACCESS_TOKEN`: DigitalOcean personal access token for App Platform deployment automation
- `OPENAI_API_KEY`: server-side OpenAI key
- `DATABASE_URL`: Supabase PostgreSQL connection string

## Optional GitHub Variables

If you want a different app name or branch later, update `.github/workflows/deploy.yml`.

## First-Time Human Steps

1. Push this repository to GitHub.
2. In GitHub repository settings, add the three secrets above.
3. In DigitalOcean, ensure your account has App Platform access.
4. Complete the one-time GitHub authorization in App Platform by creating any sample app or connecting GitHub once in the control panel.
5. Run the GitHub Actions workflow `Deploy to DigitalOcean App Platform` once.
6. Confirm the deployed app responds on `/health`.

## Important Security Note

- Do not commit `API.md` or `.env`.
- Rotate any OpenAI or Supabase service-role keys that were previously shared in plain text.
- Keep `service_role` keys out of browsers and client-side code.
