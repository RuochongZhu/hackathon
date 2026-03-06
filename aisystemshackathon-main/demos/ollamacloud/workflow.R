# workflow.R
# Ollama Cloud API Workflow Demo (R)
# Tim Fraser
#
# This script demonstrates a minimal Ollama Cloud API request using an API key
# loaded from a local .env file.

# 0. SETUP ###################################

## 0.1 Load packages #################################

library(httr2)
library(jsonlite)

## 0.2 Load environment variables ####################################

if (file.exists(".env")) {
  readRenviron(".env")
} else {
  warning(".env file not found. Create one with OLLAMA_API_KEY=your_key.")
}

ollama_api_key = Sys.getenv("OLLAMA_API_KEY")
if (ollama_api_key == "") {
  stop("OLLAMA_API_KEY not found. Add it to your .env file.")
}

# 1. Build request ###################################

url = "https://ollama.com/api/chat"
body = list(
  model = "gpt-oss:20b-cloud",
  messages = list(
    list(
      role = "user",
      content = "Hello. Reply exactly with: Model is working."
    )
  ),
  stream = FALSE
)

# 2. Send request ###################################

res = request(url) %>%
  req_headers(
    "Authorization" = paste0("Bearer ", ollama_api_key),
    "Content-Type" = "application/json"
  ) %>%
  req_body_json(body) %>%
  req_method("POST") %>%
  req_perform()

response = resp_body_json(res)

# 3. Print response ###################################

output = response$message$content
cat("\nModel response:\n\n")
cat(output)
cat("\n\nDone.\n")
