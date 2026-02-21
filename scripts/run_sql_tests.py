import os
from pathlib import Path
import psycopg2
from dotenv import load_dotenv
import sys

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST", "localhost"),
    port=os.getenv("DB_PORT", "5432"),
    dbname=os.getenv("DB_NAME", "olist"),
    user=os.getenv("DB_USER", "postgres"),
    password=os.getenv("DB_PASSWORD", "postgres"),
)

tests_dir = Path("tests")
failed = False

with conn:
    with conn.cursor() as cur:
        for sql_file in sorted(tests_dir.glob("*.sql")):
            print(f"\n▶ Running {sql_file.name}")
            sql = sql_file.read_text()

            cur.execute(sql)
            rows = cur.fetchall()

            if rows:
                failed = True
                print(f"❌ FAILED ({len(rows)} rows returned)")
                for r in rows:
                    print("  ", r)
            else:
                print("✅ PASSED")

conn.close()

if failed:
    print("\n❌ SQL DATA QUALITY CHECKS FAILED")
    sys.exit(1)

print("\n✅ ALL SQL DATA QUALITY CHECKS PASSED")