import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#plt.style.use('seaborn')
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Sales Dashboard",
                    layout="wide"
)

@st.cache
def get_data_from_csv():
    df = pd.read_csv('C:/Users/Adi Saputra/Desktop/Algo.ritma/new_household.csv', 
                 parse_dates=['purchase_time'])
    return df

df = get_data_from_csv()


#Create Side Bar for Filter Function
st.sidebar.header('Please Filter Here')

category = st.sidebar.multiselect(
    'Select the Category:',
    options=df['category'].unique(),
    default=df['category'].unique()
)

subcategory = st.sidebar.multiselect(
    'Select the Sub-Category:',
    options=df['sub_category'].unique(),
    default=df['sub_category'].unique()
)

store = st.sidebar.multiselect(
    'Select the Category:',
    options=df['format'].unique(),
    default=df['format'].unique()
)

#date = st.sidebar.date_input('Select Date',)

#Create Selection Function for Result
df_selection = df.query(
    "category == @category & sub_category == @subcategory & format == @store "  #& purchase_time == @date
)

st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

#total sales & Qty Formula
total_sales = int(df_selection['total'].sum())
total_qty = (df_selection['quantity'].sum())

#col1, col2, col3, col4 = st.columns(4)

#col2.metric('Total Sales', total_sales)
#col3.metric('Total Qty', total_qty)

#Sub Header Code
left_column, middle_column = st.columns(2)
with left_column:
    st.subheader('Total Sales:')
    st.subheader(f'RP {total_sales:,}')
    
with middle_column:
    st.subheader('Total Quantity')
    st.subheader(f'{total_qty:,}')
    
    
st.markdown("---")
    
# Sales by Category [Bar Chart]


cat_column, format_column = st.columns(2)

category_sales = (
      df_selection.groupby(['category'])[['total']].sum().round(2).sort_values('total', ascending=False)
)


fig_category_sales = px.bar(
    category_sales,
    x='total',
    y=category_sales.index,
    orientation='h',
    title='<b>Sales by Category</b>',
    color_discrete_sequence=['#0083B8'] * len(category_sales),
    template='plotly_white',
   
)

fig_category_sales.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=(dict(showgrid=False))
)


format_sales = (df_selection.groupby(['format'])[['total']].sum().reset_index())


fig_format_sales = px.pie(
    format_sales,
    values = 'total',
    names='format',
    title = '<b>Sales by Store Type<b>',
    color_discrete_sequence=px.colors.sequential.deep

)


cat_column, format_column = st.columns(2)

cat_column.plotly_chart(fig_category_sales, use_container_width=True)

format_column.plotly_chart(fig_format_sales, use_container_width=True)


# ---- Hide Streamlit Style ----

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
                """

st.markdown(hide_st_style, unsafe_allow_html=True)
