# Financial time series exploration (descriptive only)
# Example: python market_history.py --ticker IBM --period 5y
import argparse
from pathlib import Path
import yfinance as yf
import matplotlib.pyplot as plt

def main():
    p=argparse.ArgumentParser(); p.add_argument("--ticker",default="IBM"); p.add_argument("--period",default="5y"); p.add_argument("--output",default="reports/market-history.png"); a=p.parse_args()
    prices=yf.download(a.ticker,period=a.period,auto_adjust=True,progress=False)
    if prices.empty: raise SystemExit("No prices returned; check ticker, provider availability and terms.")
    close=prices["Close"].squeeze().dropna(); returns=close.pct_change().dropna()
    print({"ticker":a.ticker,"observations":len(close),"start":str(close.index.min().date()),"end":str(close.index.max().date()),"mean_daily_return":float(returns.mean()),"daily_volatility":float(returns.std())})
    out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); close.plot(title=f"{a.ticker}: adjusted close (descriptive)",figsize=(10,5)); plt.ylabel("Price"); plt.tight_layout(); plt.savefig(out,dpi=150)
if __name__=="__main__":main()
