import argparse
import json
import pandas as pd
import requests
from loguru import logger
from datetime import datetime


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get financial data for a company")
    parser.add_argument("--company", type=str, required=True, help="Company symbol (e.g. IBM)")
    parser.add_argument("--function", type=str, required=True, help="Alpha Vantage function (e.g. CASH_FLOW)")
    parser.add_argument("--api-key", type=str, required=True, help="Alpha Vantage API key", default="8DMICRDAT5ZAQSUZ")
    args = parser.parse_args()

    url = f"""https://www.alphavantage.co/query?function={args.function.upper()}&symbol={args.company}&apikey={args.api_key}"""
    r = requests.get(url)
    data = r.json()

    date_suffix = datetime.now().strftime("%Y%m%d")
    
    with open(f"{args.function.lower()}_{date_suffix}.json", "w") as f:
        json.dump(data, f)

    df = pd.DataFrame(data["quarterlyReports"])
    df.to_csv(f"{args.function.lower()}_{args.company}_{date_suffix}.csv", index=False)

    logger.info("Done")
