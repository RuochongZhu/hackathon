# workflow.py
# Supabase PostgreSQL Workflow Demo (Python)
# Tim Fraser
#
# This script mirrors workflow.R:
# 1) Load environment variables
# 2) Connect to Supabase (PostgreSQL)
# 3) List tables
# 4) Write/read/append test_table

import os
from contextlib import closing

import pandas as pd
import psycopg
from dotenv import load_dotenv


# 0. Setup #################################

## 0.1 Load environment variables ############################

load_dotenv()

SUPABASE_HOST = os.getenv("SUPABASE_HOST", "")
SUPABASE_PORT = int(os.getenv("SUPABASE_PORT", "5432"))
SUPABASE_DB = os.getenv("SUPABASE_DB", "postgres")
SUPABASE_USER = os.getenv("SUPABASE_USER", "postgres")
SUPABASE_PASSWORD = os.getenv("SUPABASE_PASSWORD", "")

if not SUPABASE_HOST or not SUPABASE_PASSWORD:
    raise ValueError(
        "Missing required env vars. Set SUPABASE_HOST and SUPABASE_PASSWORD in your .env file."
    )


def connect():
    """Create a PostgreSQL connection to Supabase."""
    return psycopg.connect(
        host=SUPABASE_HOST,
        port=SUPABASE_PORT,
        dbname=SUPABASE_DB,
        user=SUPABASE_USER,
        password=SUPABASE_PASSWORD,
    )


# 1. Connect and list tables #################################

with closing(connect()) as conn:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public' ORDER BY tablename;"
        )
        tables = [row[0] for row in cur.fetchall()]
        print("\nTables in public schema:")
        print(tables if tables else "No tables found.")

    # 2. Create and write data #################################
    mydata = pd.DataFrame(
        {
            "name": ["Tim", "Kate", "Jon", "Courtney", "David", "Sameera", "Melanie"],
            "age": [30, 25, 35, 30, 35, 30, 25],
            "city": [
                "Boston",
                "New York",
                "Chicago",
                "Los Angeles",
                "San Francisco",
                "Seattle",
                "Austin",
            ],
        }
    )

    # Overwrite table each run to keep this workflow deterministic.
    with conn.cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS public.test_table;")
        cur.execute(
            """
            CREATE TABLE public.test_table (
                name TEXT,
                age INTEGER,
                city TEXT
            );
            """
        )
        conn.commit()

    with conn.cursor() as cur:
        cur.executemany(
            "INSERT INTO public.test_table (name, age, city) VALUES (%s, %s, %s);",
            mydata.itertuples(index=False, name=None),
        )
        conn.commit()

    # 3. Query data #################################
    with conn.cursor() as cur:
        cur.execute("SELECT name, age, city FROM public.test_table ORDER BY name;")
        rows = cur.fetchall()
        print("\nRows after initial insert:")
        for row in rows:
            print(row)

    # 4. Append one row #################################
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO public.test_table (name, age, city) VALUES (%s, %s, %s);",
            ("John", 30, "Boston"),
        )
        conn.commit()

    with conn.cursor() as cur:
        cur.execute("SELECT name, age, city FROM public.test_table ORDER BY name;")
        rows = cur.fetchall()
        print("\nRows after append:")
        for row in rows:
            print(row)

print("\nDone.")
