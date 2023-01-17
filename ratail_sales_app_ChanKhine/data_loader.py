# author: Chan Khine
# Updated to include multiple store level dataframe for web application

import pandas as pd

# retail sales dataset
retail_sales_df = pd.read_csv('data/retail_sales.csv', sep=',')
retail_sales_df['Date'] = pd.to_datetime(retail_sales_df['Date'], format='%Y-%m-%d')

# monthly sales
monthly_sales_df = retail_sales_df.groupby(['month', 'Month']).agg({'Weekly_Sales': 'sum'}).reset_index()

# holiday sales per month
holiday_sales = retail_sales_df[retail_sales_df['IsHoliday'] == 1].groupby(['month'])['Weekly_Sales'].sum().\
    reset_index().rename(columns={'Weekly_Sales': 'Holiday_Sales'})

# join monthly and holiday sales
monthly_sales_df = pd.merge(holiday_sales, monthly_sales_df, on='month', how='right').fillna(0)

# round sales to 1 decimal
monthly_sales_df['Weekly_Sales'] = monthly_sales_df['Weekly_Sales'].round(1)
monthly_sales_df['Holiday_Sales'] = monthly_sales_df['Holiday_Sales'].round(1)

# weekly sales
weekly_sales_df = retail_sales_df.groupby(['month', 'Month', 'Date']).agg({'Weekly_Sales': 'sum'}).reset_index()
weekly_sales_df['week_no'] = weekly_sales_df.groupby(['Month'])['Date'].rank(method='min')

# store level sales
store_df = retail_sales_df.groupby(['month', 'Month', 'Store']).agg({'Weekly_Sales': 'sum'}).reset_index()
store_df['Store'] = store_df['Store'].apply(lambda x: 'Store' + " " + str(x))
store_df['Weekly_Sales'] = store_df['Weekly_Sales'].round(1)

# dept level sales
dept_df = retail_sales_df.groupby(['month', 'Month', 'Dept']).agg({'Weekly_Sales': 'sum'}).reset_index()
dept_df['Dept'] = dept_df['Dept'].apply(lambda x: 'Dept' + " " + str(x))
dept_df['Weekly_Sales'] = dept_df['Weekly_Sales'].round(1)

# store level sales with holiday
holi_store_df = retail_sales_df[retail_sales_df['IsHoliday'] == 1].groupby(['Store', 'Month'])['Weekly_Sales']. \
            sum().reset_index().rename(columns={'Weekly_Sales': 'Holiday_Sales'})
holi_store_df['Store'] = holi_store_df['Store'].apply(lambda x: 'Store' + " " + str(x))
updated_store_df = pd.merge(holi_store_df, store_df, on=['Store', 'Month'], how='right').fillna(0)

updated_store_df['Weekly_Sales'] = updated_store_df['Weekly_Sales'].round(1)
updated_store_df['Holiday_Sales'] = updated_store_df['Holiday_Sales'].round(1)

# weekly sales for store level
weekly_store_sales_df = retail_sales_df.groupby(['month', 'Month', 'Date', 'Store']).agg(
            {'Weekly_Sales': 'sum'}).reset_index()
weekly_store_sales_df['week_no'] = weekly_store_sales_df.groupby(['Month'])['Date'].rank(method='min')
weekly_store_sales_df['Store'] = weekly_store_sales_df['Store'].apply(lambda x: 'Store' + " " + str(x))

# store level dept sales
dept_store_df = retail_sales_df.groupby(['Month', 'Store', 'Dept']).agg({'Weekly_Sales': 'sum'}).reset_index()
dept_store_df['Store'] = dept_store_df['Store'].apply(lambda x: 'Store' + " " + str(x))
dept_store_df['Dept'] = dept_store_df['Dept'].apply(lambda x: 'Dept' + " " + str(x))
dept_store_df['Weekly_Sales'] = dept_store_df['Weekly_Sales'].round(1)
