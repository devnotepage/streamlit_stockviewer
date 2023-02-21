import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st
import tempfile
from pathlib import Path

@st.cache
def get_data(days, tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f'{days}d')
        hist.index = hist.index.strftime('%d %B %Y')
        hist = hist[['Close']]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = 'Name'
        df = pd.concat([df, hist])
    return df

def main():
    st.title('株価表示')
    days = st.sidebar.slider('日数範囲', 1, 100, 50)
    ymin, ymax = st.sidebar.slider('株価範囲', 0.0, 3500.0, (0.0, 500.0))

    # upload file
    uploaded_file = st.file_uploader("Choose your .csv file", type="csv")
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            st.markdown("## Original CSV file")
            fp = Path(tmp_file.name)
            fp.write_bytes(uploaded_file.getvalue())
            df = pd.read_csv(fp, delimiter='\t', encoding='utf-8')
            st.dataframe(df)



    tickers = {
        'apple': 'AAPL',
        'google': 'GOOGL',
        'microsoft': 'MSFT',
        'netflix': 'NFLX',
        'amazon': 'AMZN',
    }



    df = get_data(days, tickers)
    companies = st.multiselect('会社選択', list(df.index), tickers.keys())
    if not companies:
        st.error('会社選択してください')
    else:
        data = df.loc[companies]
        st.write('株価(USD)', data.sort_index())
        data = data.T.reset_index()
        data = pd.melt(data, id_vars=['Date']).rename(
            columns={'value': 'Stock Prices(USD)'}
        )
        chart = (
            alt.Chart(data)
            .mark_line(opacity=0.8, clip=True)
            .encode(
                x="Date:T",
                y=alt.Y("Stock Prices(USD):Q", stack=None, scale=alt.Scale(domain=[ymin, ymax])),
                color='Name:N'
            )
        )
        st.altair_chart(chart, use_container_width=True)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(e)
