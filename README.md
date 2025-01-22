Here's a README.md file for your financial data fetching project:

# Install

```bash
git clone https://github.com/reallyigor/easy_financial_report
cd easy_financial_report
```

```bash
pip install -r requirements.txt
```

# Use

```bash
python finance_request.py --company SYMBOL --function REPORT_TYPE --api-key YOUR_API_KEY
```

REPORT_TYPE could be one of:

cash_flow
balance_sheet
income_statement
earnings
listing_status

Example:

```bash
python finance_request.py --company IBM --function CASH_FLOW --api-key 8DMICRDAT5ZAQSUZ
```
