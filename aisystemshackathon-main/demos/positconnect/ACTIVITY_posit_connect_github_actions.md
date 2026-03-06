# 📌 ACTIVITY

## Deploy to Posit Connect via GitHub Actions

🕒 *Estimated Time: 10-15 minutes*

---

## ✅ Your Task

Set up GitHub Actions to deploy your app/API to Posit Connect.

### 🧱 Stage 1: Generate `manifest.json`

Run the manifest helper in the app folder you want to deploy:

- Shiny R: [`../shinyr/manifestme.R`](../shinyr/manifestme.R)
- Plumber: [`../plumber/manifestme.R`](../plumber/manifestme.R)
- Shiny Python: [`../shinypy/manifestme.sh`](../shinypy/manifestme.sh)
- FastAPI: [`../fastapi/manifestme.sh`](../fastapi/manifestme.sh)

Example screenshots:

![](../../docs/images/pc_manifest_shinypy.png)
![](../../docs/images/pc_manifest_shinypy_json.png)

---

### 🧱 Stage 2: Create Posit Connect API Key

- [ ] In Posit Connect, open your account settings and create a **Publisher** API key.
- [ ] Copy and store the API key safely.

Reference screenshots:

![](../../docs/images/pc_keys_where.png)
![](../../docs/images/pc_keys_view.png)
![](../../docs/images/pc_keys_new.png)
![](../../docs/images/pc_keys_copy.png)

---

### 🧱 Stage 3: Configure GitHub Secrets

In your GitHub repository, add:

- [ ] `CONNECT_SERVER` (your Posit Connect server URL)
- [ ] `CONNECT_API_KEY` (publisher API key)

Reference screenshots:

![](../../docs/images/pc_github_settings.png)
![](../../docs/images/pc_github_secrets.png)
![](../../docs/images/pc_github_secrets_CONNECT_SERVER.png)
![](../../docs/images/pc_keys_list.png)

---

### 🧱 Stage 4: Add Workflow Template

Use templates in this folder:

- Shiny R: [`workflows/deploy-shinyr.yml`](workflows/deploy-shinyr.yml)
- Shiny Python: [`workflows/deploy-shinypy.yml`](workflows/deploy-shinypy.yml)
- Plumber: [`workflows/deploy-plumber.yml`](workflows/deploy-plumber.yml)

FastAPI can be deployed directly via:

- [`../fastapi/deployme.sh`](../fastapi/deployme.sh)

After copying a template into your repo’s `.github/workflows/`, update `paths` and `dir` so they match your project structure.

![](../../docs/images/pc_deploy_shinypy.png)

---

### 🧱 Stage 5: Test Deployment

- [ ] Push to `main` or run workflow manually in GitHub Actions.
- [ ] Confirm successful run in Actions tab.
- [ ] Open your Posit Connect dashboard and verify the app/API is deployed.

Reference screenshots:

![](../../docs/images/pc_actions_list.png)
![](../../docs/images/pc_deployed_list.png)
![](../../docs/images/pc_deployed_access.png)
![](../../docs/images/pc_deployed_env.png)
![](../../docs/images/pc_deployed_info.png)

---

## Related Demo Folders

- [`../github/`](../github/)
- [`../fastapi/`](../fastapi/)
- [`../plumber/`](../plumber/)
- [`../shinypy/`](../shinypy/)
- [`../shinyr/`](../shinyr/)
- [`../supabase/`](../supabase/)

---

![](../../docs/images/icons.png)

---

← 🏠 [Back to Top](#ACTIVITY)
