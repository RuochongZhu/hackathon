# DigitalOcean Deployment Guide (From Scratch)

This guide resets deployment to a clean baseline and deploys only the dashboard web app first.

## What Was Cleaned

- Removed old DigitalOcean app spec at `.do/app.yaml`
- Removed old Render config at `render.yaml`
- Removed old GitHub auto-deploy workflow at `.github/workflows/deploy.yml`
- Removed `.env` hard dependency from both Dockerfiles so cloud build won't fail when `.env` is not committed

## Current Deployment Files

- App spec: `deploy/digitalocean/app-dashboard.yaml`
- Dashboard container: `dashboard/Dockerfile`

## 0. Prerequisites

1. Push this repo to GitHub.
2. Have a DigitalOcean account with App Platform enabled.
3. Install doctl (optional but recommended):

```bash
brew install doctl
```

4. Authenticate:

```bash
doctl auth init
```

## 1. Fill App Spec

Edit `deploy/digitalocean/app-dashboard.yaml` and replace:

- `YOUR_GITHUB_USERNAME/YOUR_REPO_NAME`
- `YOUR_OPENAI_API_KEY`
- `YOUR_DATABASE_URL`
- `YOUR_SUPABASE_URL`
- `YOUR_SUPABASE_ANON_KEY`
- `YOUR_SUPABASE_SERVICE_ROLE_KEY`

If you prefer not to put secrets in file, create app in DigitalOcean UI and add env vars there.

## 2. Create App (CLI)

```bash
doctl apps create --spec deploy/digitalocean/app-dashboard.yaml
```

Save returned `app_id`.

## 3. Check Deployment

```bash
doctl apps list
doctl apps get <app_id>
doctl apps logs <app_id> --type build --follow
doctl apps logs <app_id> --type run --follow
```

When deployment is healthy, open the app URL from `doctl apps get`.

## 4. Redeploy After Code Change

If `deploy_on_push: true`, pushing `main` triggers deploy automatically.

Manual redeploy:

```bash
doctl apps create-deployment <app_id>
```

## 5. Optional: Add API as Second Service Later

After dashboard is stable, add backend API as another service. Keep dashboard-only deployment first to reduce routing complexity.
