import duckdb
import os
import time

# --- Configuration Paths ---
RAW_CSV_DIR = "./data/raw_fir_csvs"
D1_OUTPUT_DIR = "./data/output/cloudflare_d1"
DB_NAME = "civicledger_d1.sqlite"

def main():
    start_time = time.time()
    os.makedirs(D1_OUTPUT_DIR, exist_ok=True)
    
    sqlite_db_path = f"{D1_OUTPUT_DIR}/{DB_NAME}"
    if os.path.exists(sqlite_db_path):
        os.remove(sqlite_db_path)

    print("Initializing DuckDB engine...")
    con = duckdb.connect(database=':memory:')
    con.execute("INSTALL sqlite; LOAD sqlite;")

    # ---------------------------------------------------------
    # STEP 1: Ingest & Normalize the 25-Year CSV Archive
    # ---------------------------------------------------------
    print(f"Ingesting raw Ontario FIR CSVs from {RAW_CSV_DIR}/*.csv...")
    
    con.execute(f"""
        CREATE TABLE raw_fir AS 
        SELECT * FROM read_csv_auto('{RAW_CSV_DIR}/*.csv', 
            types={{
                'Year': 'INTEGER', 
                'Municipality': 'VARCHAR',
                'SGC': 'VARCHAR', 
                'Schedule': 'VARCHAR', 
                'Line': 'VARCHAR', 
                'Column': 'VARCHAR', 
                'Value': 'DOUBLE'
            }},
            ignore_errors=true)
    """)

    print("Cleaning and normalizing data across accounting transitions...")
    con.execute("""
        CREATE TABLE clean_fir AS 
        SELECT 
            Year AS year,
            LPAD(CAST(SGC AS VARCHAR), 4, '0') AS sgc_code,
            Schedule AS schedule,
            Line AS line,
            "Column" AS col,
            COALESCE(Value, 0.0) AS amount
        FROM raw_fir
        WHERE SGC IS NOT NULL 
          AND Value IS NOT NULL
    """)

    # ---------------------------------------------------------
    # STEP 2: Cloudflare D1 Master SQLite Generation
    # ---------------------------------------------------------
    print(f"Generating master SQLite database for Edge D1 at {sqlite_db_path}...")
    
    con.execute(f"ATTACH '{sqlite_db_path}' AS d1_master (TYPE SQLITE);")
    
    con.execute("""
        CREATE TABLE d1_master.fir_data AS 
        SELECT year, sgc_code, schedule, line, col, amount
        FROM clean_fir 
        ORDER BY sgc_code, year DESC, schedule, line;
    """)
    
    # Create indexes optimized for Cloudflare D1 edge lookups
    print("Building analytical indexes...")
    con.execute("""
        CREATE INDEX d1_master.idx_d1_point_lookup 
        ON fir_data(sgc_code, year, schedule);
    """)
    
    con.execute("DETACH d1_master;")

    # ---------------------------------------------------------
    # STEP 3: Cloudflare D1 Batched SQL Seed Export
    # ---------------------------------------------------------
    print("Exporting raw SQL seed chunks for D1 Wrangler ingestion...")
    
    # D1 has limits on upload sizes, so we generate a raw SQL dump
    # that can be chunked by Cloudflare's wrangler CLI.
    con.execute(f"""
        COPY (SELECT * FROM clean_fir) 
        TO '{D1_OUTPUT_DIR}/seed_d1.sql' 
        (FORMAT CSV, DELIMITER ',', HEADER FALSE);
    """)

    elapsed = time.time() - start_time
    print(f"ETL Complete in {elapsed:.2f} seconds. D1 SQLite Seed and SQL dump ready.")

if __name__ == "__main__":
    main()
  
