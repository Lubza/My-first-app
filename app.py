import pandas as pd
import plotly.express as px
import streamlit as st


#emojis: https://www.webfx.com/tools/emoji-cheat-sheet/

st.set_page_config(page_title="Portfolio overview",
                    page_icon=":bar_chart:",
                    layout="wide"
)

adress = r'C:\Users\Lubos\Dropbox\My PC (Lubos-PC1)\Desktop\python\Portfolio_dataset_1122.csv'

df = pd.read_csv(adress, engine='python')



#---- SIDEBAR -----
st.sidebar.header("Please Filter Here:")

PSize = st.sidebar.multiselect(
    "Select the position size:",
    options=df["Position_Size"].unique(),
    default=df["Position_Size"].unique()
)


sector = st.sidebar.multiselect(
    "Select the Sector:",
    options=df["Sector"].unique(),
    default=df["Sector"].unique()
)

industry = st.sidebar.multiselect(
    "Select the Industry:",
    options=df["Industry"].unique(),
    default=df["Industry"].unique()
)

REIT_sector = st.sidebar.multiselect(
    "Select the REIT Sector:",
    options=df["REIT sector"].unique(),
    default=df["REIT sector"].unique()
)

ccy = st.sidebar.multiselect(
    "Select the currency:",
    options=df["CCY"].unique(),
    default=df["CCY"].unique()
)

df_selection = df.query(
    "Position_Size == @PSize & Sector == @sector & Industry == @industry"
)


#-----MAINPAGE-----
st.title(":bar_chart: Portfolio Overview")
st.markdown('##')

#TOP KPI's
Total_net_liq = round(df_selection['% of Net Liq'].sum(), 2)
Total_MV = round(df_selection['Market Value'].sum(), 1)
Account_balance = round(((100/Total_net_liq)*Total_MV), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total_net_liq:")
    st.subheader(f"% {Total_net_liq:,}")
with middle_column:
    st.subheader("Portfolio Market Value:")
    st.subheader(f"USD {Total_MV:,}")

with right_column:
    st.subheader("Balance:")
    st.subheader(f"USD {Account_balance:,}")
    

st.markdown("---")

#st.dataframe(df_selection)
#st.dataframe(df)

# Expected Dividend by month

Expected_dividend_by_month = (

df_selection.groupby(by=["Month"]).sum()[["Next_div_receiveable"]].sort_values(by="Next_div_receiveable")

)

fig_div = px.bar(
        Expected_dividend_by_month,
        y = "Next_div_receiveable",
        x = Expected_dividend_by_month.index,
        orientation="v",
        title="<b>Expected Dividend by month<\b>",
        color_discrete_sequence=["#0083B8"] * len(Expected_dividend_by_month),
        template="plotly_white"
)

st.plotly_chart(fig_div)