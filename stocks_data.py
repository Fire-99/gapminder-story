
    
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Big Tech Stock Race | Data Story", layout="wide")

@st.cache_data
def load_data():
    data = px.data.stocks().copy()
    data["date"] = pd.to_datetime(data["date"])
    return data

df = load_data()
companies = [c for c in df.columns if c != "date"]
long_df = df.melt(id_vars="date", var_name="Company", value_name="Normalized value")
start = df.iloc[0]
end = df.iloc[-1]
returns = pd.DataFrame({
    "Company": companies,
    "Growth (%)": [(end[c] / start[c] - 1) * 100 for c in companies]
}).sort_values("Growth (%)", ascending=False)
leader = returns.iloc[0]
laggard = returns.iloc[-1]

st.title("Big Tech's Stock Race: Microsoft Rose 78.8% in 2018-2019")
st.write("A business journalist's look at six technology stocks, using normalized price series.")

# Sidebar controls apply to the Explore tab; the Story tab shows the full dataset.
with st.sidebar:
    st.header("Explore stock data")
    st.caption("Change these filters, then open the Explore it yourself tab.")
    selected = st.multiselect(
        "Choose stocks", companies, default=companies, key="sidebar_companies"
    )
    date_range = st.slider(
        "Date range",
        min_value=df["date"].min().to_pydatetime(),
        max_value=df["date"].max().to_pydatetime(),
        value=(df["date"].min().to_pydatetime(), df["date"].max().to_pydatetime()),
        format="MMM YYYY",
        key="sidebar_dates",
    )
    st.divider()
    st.caption("Source: Plotly Express stocks dataset (2018-2019)")

story, explore = st.tabs(["The story", "Explore it yourself"])

with story:
    st.header(f"{leader['Company']} led the six stocks with {leader['Growth (%)']:.1f}% growth")
    fig = px.bar(
        returns.sort_values("Growth (%)"),
        x="Growth (%)", y="Company", orientation="h",
        color="Company", text="Growth (%)",
        title="Start-to-end growth, Jan 2018-Dec 2019"
    )
    fig.update_traces(texttemplate="%{x:.1f}%", textposition="outside")
    fig.update_layout(showlegend=False, xaxis_title="Growth from first to last observation (%)")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
        f"Between **{df['date'].min():%b %d, %Y}** and **{df['date'].max():%b %d, %Y}**, "
        f"**{leader['Company']} grew {leader['Growth (%)']:.1f}%**, compared with "
        f"**{laggard['Company']} at {laggard['Growth (%)']:.1f}%**. "
        "The gap between their starting-point-normalized performances widened over the period; "
        "these are descriptive historical comparisons, not evidence of what caused the moves."
    )
    st.caption("Source: Plotly Express sample dataset, px.data.stocks(); values normalized to 1.0 at the first observation. Growth = (last/first - 1) x 100. No dividends included in this calculation.")

    st.subheader("When did the leaders pull apart?")
    fig_time = px.line(long_df, x="date", y="Normalized value", color="Company",
                       title="Relative stock performance, January 2018-December 2019")
    fig_time.update_layout(yaxis_title="Value (first observation = 1.0)", xaxis_title="Date")
    st.plotly_chart(fig_time, use_container_width=True)
    st.caption("The time series reveals the timing of divergence; the bar chart above establishes the overall winner.")

with explore:
    left, right = st.columns([1, 3])
    left.info("Use the sidebar to choose companies and dates.")
    if not selected:
        right.warning("Select at least one stock to explore its performance.")
    else:
        mask = df["date"].between(pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1]))
        filtered = df.loc[mask, ["date"] + selected].copy()
        if len(filtered) < 2:
            right.warning("Choose a wider date range with at least two observations.")
        else:
            selected_returns = pd.Series({
                c: (filtered[c].iloc[-1] / filtered[c].iloc[0] - 1) * 100
                for c in selected
            }).sort_values(ascending=False)
            best = selected_returns.index[0]
            left.metric("Top selected stock", best)
            left.metric("Growth in selection", f"{selected_returns.iloc[0]:+.1f}%")
            left.metric("Stocks selected", len(selected))
            right.markdown(
                f"From **{filtered['date'].iloc[0]:%b %d, %Y}** to "
                f"**{filtered['date'].iloc[-1]:%b %d, %Y}**, **{best}** grew "
                f"**{selected_returns.iloc[0]:.1f}%**, the most among your "
                f"**{len(selected)} selected stocks**."
            )
            chart_data = filtered.melt(id_vars="date", var_name="Company", value_name="Normalized value")
            chart_data["Rebased value"] = chart_data.groupby("Company")["Normalized value"].transform(lambda s: s / s.iloc[0])
            chart = px.line(chart_data, x="date", y="Rebased value", color="Company",
                            title="Relative performance rebased to selected start date")
            chart.update_layout(yaxis_title="Value (selected start = 1.0)", xaxis_title="Date")
            right.plotly_chart(chart, use_container_width=True)
            with right.expander("See the data behind this chart"):
                st.dataframe(filtered, hide_index=True, use_container_width=True)
                st.download_button("Download as CSV", data=filtered.to_csv(index=False).encode("utf-8"),
                                   file_name="selected_tech_stocks.csv", mime="text/csv",
                                   key="explore_csv")

