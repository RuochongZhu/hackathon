# workflow.R
# OpenAI API Workflow Demo (R)
# Tim Fraser
#
# This script demonstrates a minimal OpenAI API request using an API key
# loaded from a local .env file.

# 0. SETUP ###################################

## 0.1 Load packages #################################

library(httr2)
library(jsonlite)
library(purrr)

## 0.2 Load environment variables ####################################

if (file.exists(".env")) {
  readRenviron(".env")
} else {
  warning(".env file not found. Create one with OPENAI_API_KEY=your_key.")
}

openai_api_key = Sys.getenv("OPENAI_API_KEY")
if (openai_api_key == "") {
  stop("OPENAI_API_KEY not found. Add it to your .env file.")
}

# 1. Build request ###################################

url = "https://api.openai.com/v1/responses"
body = list(
  model = "gpt-4o-mini",
  input = "Hello. Reply exactly with: Model is working."
)

# 2. Send request ###################################

res = request(url) %>%
  req_headers(
    "Authorization" = paste0("Bearer ", openai_api_key),
    "Content-Type" = "application/json"
  ) %>%
  req_body_json(body) %>%
  req_method("POST") %>%
  req_perform()

response = resp_body_json(res)

# 3. Print response ###################################

output = response %>% pluck("output", 1, "content", 1, "text")
cat("\nModel response:\n\n")
cat(output)
cat("\n\nDone.\n")
