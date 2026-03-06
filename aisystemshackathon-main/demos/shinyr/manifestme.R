# manifestme.R
#
# Write a Posit deployment manifest for this Shiny for R app.
# Run with: Rscript manifestme.R

if (!requireNamespace("rsconnect", quietly = TRUE)) {
  stop("Please install 'rsconnect' first: install.packages('rsconnect')")
}

# Generate manifest.json in the current app folder.
rsconnect::writeManifest(appDir = ".")

message("Done. manifest.json created in: ", normalizePath(".", winslash = "/"))
