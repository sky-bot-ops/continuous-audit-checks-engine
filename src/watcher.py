import time
from pathlib import Path
import pandas as pd

# Directories
WATCH_DIR = Path("data/incoming")
OUT_DIR = Path("reports")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Audit rules
RULES = [
    {"name": "Negative Amount", "fn": lambda df: df[df["amount"] < 0]},
    {"name": "Missing Vendor", "fn": lambda df: df[df["vendor"].isna() | (df["vendor"].astype(str).str.strip() == "")]},
    {"name": "Weekend Posting", "fn": lambda df: df[pd.to_datetime(df["posting_date"]).dt.dayofweek >= 5]},
    {"name": "Duplicate Invoice", "fn": lambda df: df[df.duplicated(subset=["invoice_id"], keep=False)]},
]

def run_checks(file_path: Path) -> Path:
    df = pd.read_csv(file_path)
    df.columns = [c.strip().lower() for c in df.columns]

    # Data type handling
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
    df["posting_date"] = pd.to_datetime(df["posting_date"], errors="coerce")

    exceptions = []

    for rule in RULES:
        flagged = rule["fn"](df).copy()
        if not flagged.empty:
            flagged["rule"] = rule["name"]
            exceptions.append(flagged)

    exception_df = (
        pd.concat(exceptions, ignore_index=True)
        if exceptions
        else pd.DataFrame(columns=list(df.columns) + ["rule"])
    )

    output_file = OUT_DIR / f"exceptions_{file_path.stem}.xlsx"

    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        df.head(2000).to_excel(writer, index=False, sheet_name="sample_input")
        exception_df.to_excel(writer, index=False, sheet_name="exceptions")

        summary = (
            exception_df.groupby("rule")
            .size()
            .reset_index(name="count")
            if not exception_df.empty
            else pd.DataFrame({"rule": [], "count": []})
        )

        summary.to_excel(writer, index=False, sheet_name="summary")

    return output_file

def main():
    WATCH_DIR.mkdir(parents=True, exist_ok=True)
    processed = set()

    print(f"Monitoring folder: {WATCH_DIR.resolve()}")

    while True:
        for file in WATCH_DIR.glob("*.csv"):
            if file.name not in processed:
                print(f"Processing {file.name}")
                report = run_checks(file)
                print(f"Report generated: {report}")
                processed.add(file.name)
        time.sleep(3)

if __name__ == "__main__":
    main()
