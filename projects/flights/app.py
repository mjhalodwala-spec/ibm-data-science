import sys
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Flight reliability", page_icon="✈️", layout="wide")
st.title("Flight reliability")
st.caption("Course-aligned retrospective dashboard · use a licensed dataset and record its source")
path = sys.argv[1] if len(sys.argv) > 1 else "data/flights.csv"
try:
    df = pd.read_csv(path)
except (FileNotFoundError, pd.errors.ParserError):
    st.info("Provide a CSV path: `streamlit run app.py -- path/to/flights.csv`.")
    st.stop()
required = {"month", "carrier", "origin", "cancelled", "arr_delay"}
missing = required.difference(df.columns)
if missing:
    st.error("Missing required columns: " + ", ".join(sorted(missing)))
    st.stop()
df = df.dropna(subset=["month", "carrier", "origin", "cancelled"])
df["cancelled"] = df["cancelled"].astype(bool)
months = st.multiselect("Month", sorted(df.month.astype(str).unique()), default=sorted(df.month.astype(str).unique()))
carriers = st.multiselect("Carrier", sorted(df.carrier.astype(str).unique()), default=sorted(df.carrier.astype(str).unique()))
view = df[df.month.astype(str).isin(months) & df.carrier.astype(str).isin(carriers)]
if view.empty:
    st.warning("No records match those filters.")
    st.stop()
summary = view.groupby(["origin", "carrier"], as_index=False).agg(flights=("cancelled", "size"), cancellations=("cancelled", "sum"), mean_arrival_delay=("arr_delay", "mean"))
summary["cancellation_rate"] = summary.cancellations / summary.flights
summary.loc[summary.flights < 30, ["cancellation_rate", "mean_arrival_delay"]] = float("nan")
a,b,c=st.columns(3)
a.metric("Flights in view", f"{len(view):,}")
b.metric("Overall cancellation rate", f"{view.cancelled.mean():.1%}")
c.metric("Mean arrival delay (min)", f"{view.arr_delay.mean():.1f}")
large=summary[summary.flights>=30]
if large.empty:
    st.info("No carrier-airport group has 30 or more records. Broaden the filters.")
else:
    st.subheader("Cancellation rate by airport and carrier (groups under 30 hidden)")
    st.plotly_chart(px.bar(large, x="origin", y="cancellation_rate", color="carrier", hover_data=["flights"], barmode="group", labels={"origin":"Airport","cancellation_rate":"Cancellation rate"}), use_container_width=True)
    st.subheader("Group detail")
    st.dataframe(summary.sort_values("flights", ascending=False), use_container_width=True)
