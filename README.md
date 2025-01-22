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

1. `cash_flow`
2. `balance_sheet`
3. `income_statement`
4. `earnings`
5. `listing_status`

Example:

```bash
python finance_request.py --company IBM --function CASH_FLOW --api-key 8DMICRDAT5ZAQSUZ
```
