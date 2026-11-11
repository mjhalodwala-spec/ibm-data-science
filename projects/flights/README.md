# Flight reliability dashboard

Create a decision-oriented view of a licensed, user-supplied flight delay CSV. Expected fields: `month`, `carrier`, `origin`, `cancelled` (0/1), and `arr_delay` (minutes). Show denominators with cancellation and delay rates, filter by month/carrier/airport, and suppress comparisons below 30 flights.

```bash
pip install -r requirements.txt
streamlit run app.py -- data/flights.csv
```

The data source and license must be documented by the person supplying the file. The dashboard does not ship a dataset or claim results. Small-group comparisons are hidden to reduce misleading rankings.
