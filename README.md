# Install

```bash
git clone https://github.com/reallyigor/easy_financial_report
cd easy_financial_report
```

```bash
python -m pip install -r requirements.txt
```

# Use

```bash
python finance_request.py --companies SYMBOL1,SYMBOL2,SYMBOL3,...SYMBOLN --api-key YOUR_API_KEY
```

You can use optional `output_dir` argument, for example, to cache your results.

```bash
python finance_request.py --output_dir ./cool_companies --companies SYMBOL1,SYMBOL2,SYMBOL3,...SYMBOLN --api-key YOUR_API_KE
```

Example:

```bash
python finance_request.py --companies IBM,AAPL --api-key 8DMICRDAT5ZAQSUZ
```
