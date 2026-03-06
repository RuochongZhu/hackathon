# Posit Connect Workflow Templates

This folder contains GitHub Actions workflow templates for deploying demos to Posit Connect.

## Files

- `deploy-shinyr.yml` - Shiny for R deployment workflow
- `deploy-shinypy.yml` - Shiny for Python deployment workflow
- `deploy-plumber.yml` - Plumber API deployment workflow

## How to Use

1. Copy one of these files into your project at `.github/workflows/`.
2. Update trigger paths to match your repository structure.
3. Add required secrets in GitHub:
   - `CONNECT_SERVER`
   - `CONNECT_API_KEY`
4. Commit and push; then verify in GitHub Actions.

## Related Demo Folders

- [`../../github/`](../../github/)
- [`../../fastapi/`](../../fastapi/)
- [`../../plumber/`](../../plumber/)
- [`../../shinypy/`](../../shinypy/)
- [`../../shinyr/`](../../shinyr/)
- [`../../supabase/`](../../supabase/)
