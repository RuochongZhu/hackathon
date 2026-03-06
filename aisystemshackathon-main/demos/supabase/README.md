# Supabase Demo (Hackathon)

This folder contains Supabase database workflows for the AI Systems Hackathon in both R and Python.

## Purpose

Use these scripts to validate your Supabase PostgreSQL connection and practice basic table operations:
- list tables
- write a test table
- query rows
- append new rows

## Files

- `workflow.R` - R workflow using `DBI` + `RPostgres`
- `workflow.py` - Python workflow using `psycopg`

## Environment Variables

Create a `.env` file with:

```bash
SUPABASE_HOST=db.your-project-ref.supabase.co
SUPABASE_PORT=5432
SUPABASE_DB=postgres
SUPABASE_USER=postgres
SUPABASE_PASSWORD=your_database_password
```

Required:
- `SUPABASE_HOST`
- `SUPABASE_PASSWORD`

## Run the R workflow

Install packages first if needed:

```r
install.packages(c("DBI", "RPostgres", "dplyr", "dbplyr", "readr"))
```

Run:

```r
source("workflow.R")
```

## Run the Python workflow

Install packages first:

```bash
pip install psycopg[binary] pandas python-dotenv
```

Run:

```bash
python workflow.py
```

## Notes

- Supabase runs on PostgreSQL, so standard PostgreSQL clients apply.
- Do not commit `.env` files or database passwords.
- The Python script recreates `public.test_table` on each run for a repeatable demo.
