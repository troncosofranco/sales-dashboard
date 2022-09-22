#Import libraries
import pandas as pd  
import plotly.express as px  
import streamlit as st  


# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Company Sales", page_icon=":bar_chart:", layout="wide")

#Load dataset with specific parameters
@st.cache
def get_data_from_excel():
    df = pd.read_excel(
        io="data.xlsx",
        engine="openpyxl",
        sheet_name="Sales",
        skiprows=3,
        usecols="B:R", #column A omitted
        nrows=1004,
    )
    
    # Add 'hour' column to dataframe with datetime format
    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df

df = get_data_from_excel()

#================================Input parameter: Sidebar==============================
st.sidebar.header("Selection parameter")
city = st.sidebar.multiselect(
    "City:",
    options=df["City"].unique(),
    default=df["City"].unique()
)

customer_type = st.sidebar.multiselect(
    "Customer Type:",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique(),
)

gender = st.sidebar.multiselect(
    "Gender:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

payment = st.sidebar.multiselect(
    "Payment Method:",
    options=df["Payment"].unique(),
    default=df["Payment"].unique()
)

df_selection = df.query(
    "City == @city & Customer_type ==@customer_type & Gender == @gender & Payment==@payment"
)

#=============================================Mainpage============================

st.title("📊 Sales Dashboard")
st.markdown("##")

#===========================================TOP KPI's section=======================

#KPI's variables
total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))
average_sale_by_transaction = round(df_selection["Total"].mean(), 2)
gross_income = round(df_selection["gross income"].mean(),1)


#Columns split
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"$ {total_sales:,}")
col2.metric("Average Rating", f"{average_rating}")
col3.metric("Average Trans. Sales", f"$ {average_sale_by_transaction}")
col4.metric("Gross Income", f"$ {gross_income}")

st.markdown("""---""")

#=========================================Plot Section==========================================

#Bar Chart: Sales by product
sales_by_product_line = (
    df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
)
fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template="plotly_white",
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

#Bar Chart: Sales by hour 
sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]
fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b>Sales by hour</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    template="plotly_white",
)
fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)


#Bar Chart: Sales by payment 
sales_by_payment = df_selection.groupby(by=["Payment"]).sum()[["Total"]]
fig_payment_sales = px.bar(
    sales_by_payment,
    x=sales_by_payment.index,
    y="Total",
    title="<b>Sales by Payment</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_payment),
    template="plotly_white",
)
fig_payment_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

#Bar Chart: Sales by rating 
sales_by_rating = df_selection.groupby(df_selection["Rating"].apply(lambda x: round(x,0))).sum()[["Total"]]
fig_rating_sales = px.bar(
    sales_by_rating,
    x=sales_by_rating.index,
    y="Total",
    title="<b>Sales by Rating</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_rating),
    template="plotly_white",
)
fig_rating_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)


left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
left_column.plotly_chart(fig_payment_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)
right_column.plotly_chart(fig_rating_sales, use_container_width=True)

st.write("**Credits:** [Sven-Bo](https://github.com/Sven-Bo)")







# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)