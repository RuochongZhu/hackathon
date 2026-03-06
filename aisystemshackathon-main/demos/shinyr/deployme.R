# deployme.R

# Deploy Shiny for R from this folder.
# Includes Posit Connect and Connect Cloud options.

if (!requireNamespace("rsconnect", quietly = TRUE)) {
  stop("Please install 'rsconnect' first: install.packages('rsconnect')")
}

# Run this script from the `demos/shinyr` folder.

# Always regenerate manifest before deployment.
rsconnect::writeManifest(appDir = ".", appMode = "shiny")

# Option 1 (active): Deploy to Posit Connect Cloud (interactive account).
rsconnect::connectCloudUser(launch.browser = TRUE)
rsconnect::deployApp(appDir = ".")

# Option 2 (commented): Deploy to Posit Connect server.
# Requires CONNECT_SERVER and CONNECT_API_KEY in your environment.
# rsconnect::addServer(url = Sys.getenv("CONNECT_SERVER"), name = "hackathon-connect")
# rsconnect::connectApiUser(
#   server = "hackathon-connect",
#   apiKey = Sys.getenv("CONNECT_API_KEY")
# )
# rsconnect::deployApp(appDir = ".", server = "hackathon-connect")