import argparse
import json
import pandas as pd
import requests
from loguru import logger
from datetime import datetime
from pathlib import Path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get financial data for a company")
    parser.add_argument("--company", type=str, required=True, help="Company symbol (e.g. IBM)")
    parser.add_argument("--api-key", type=str, required=True, help="Alpha Vantage API key", default="8DMICRDAT5ZAQSUZ")
    args = parser.parse_args()

    date_suffix = datetime.now().strftime("%Y%m%d")
    report_dir = Path(f"reports_{date_suffix}")
    json_dir = report_dir / "jsons"
    
    report_dir.mkdir(exist_ok=True)
    json_dir.mkdir(exist_ok=True)
    
    functions = ["CASH_FLOW", "BALANCE_SHEET", "INCOME_STATEMENT", "EARNINGS"]
    
    dfs = {}
    for function in functions:
        json_path = json_dir / f"{args.company}_{function.lower()}.json"
        
        # Check if report already exists
        if json_path.exists():
            with json_path.open("r") as f:
                data = json.load(f)
            logger.info(f"Loaded existing {function} report for {args.company} from {json_path}")
        else:
            # Make API call if report doesn"t exist
            url = f"https://www.alphavantage.co/query?function={function}&symbol={args.company}&apikey={args.api_key}"
            r = requests.get(url)
            data = r.json()
            
            # Save raw JSON
            with json_path.open("w") as f:
                json.dump(data, f)
            logger.info(f"Downloaded and saved {function} report for {args.company} to {json_path}")
            
        # Create dataframe and add to dictionary
        if "quarterlyReports" in data:
            df = pd.DataFrame(data["quarterlyReports"])
            dfs[function] = df
        elif "quarterlyEarnings" in data:  # Special case for earnings
            df = pd.DataFrame(data["quarterlyEarnings"])
            dfs[function] = df
        else:
            logger.error(f"No quarterly reports found for {args.company} in {function} data")

    # Get all unique fiscal dates across all dataframes
    all_fiscal_dates = set()
    for df in dfs.values():
        all_fiscal_dates.update(df["fiscalDateEnding"].values)
    all_fiscal_dates = sorted(list(all_fiscal_dates), reverse=True)

    # Create a base dataframe with all fiscal dates
    final_df = pd.DataFrame({"fiscalDateEnding": all_fiscal_dates})

    # Merge each dataframe with the base dataframe
    for function, df in dfs.items():
        # Add suffix to avoid column name conflicts
        df = df.add_suffix(f"_{function.lower()}")
        # Rename fiscalDateEnding back to original for merging
        if f"fiscalDateEnding_{function.lower()}" in df.columns:
            df = df.rename(columns={f"fiscalDateEnding_{function.lower()}": "fiscalDateEnding"})
        # Merge with final_df
        final_df = pd.merge(final_df, df, on="fiscalDateEnding", how="left")

    output_path = report_dir / f"financial_report_{args.company}.csv"
    final_df.to_csv(output_path, index=False)
    logger.info(f"Saved combined report to {output_path}")
