from datetime import timedelta

import streamlit as st
import plotly.express as px
import pandas as pd
import os
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Load the data
df = pd.read_csv('Amazon.csv')

# Convert Date to datetime and set as index
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# Dashboard title with colorful styling
st.title(" :bar_chart: Amazon Stock Analysis Dashboard")
st.markdown('<style>div.block-container{padding-top:2rem;} color: #ff0000;</style>', unsafe_allow_html=True)

# Sidebar for filters
st.sidebar.header('Filters')

# Quick time range selector
time_range = st.sidebar.selectbox('Select Time Range', ['All', '1 Week', '1 Month', '1 Year', '5 Years'])

# Calculate start and end dates based on selection
max_date = df.index.max().date()
min_date = df.index.min().date()

if time_range == '1 Week':
    start_date = max_date - timedelta(weeks=1)
elif time_range == '1 Month':
    start_date = max_date - timedelta(days=30)
elif time_range == '1 Year':
    start_date = max_date - timedelta(days=365)
elif time_range == '5 Years':
    start_date = max_date - timedelta(days=365*5)
else:
    start_date = min_date

# Date inputs (override if needed)
start_date = st.sidebar.date_input('Start Date', start_date)
end_date = st.sidebar.date_input('End Date', max_date)

# Filter the dataframe
filtered_df = df.loc[start_date:end_date]

# Display key metrics in colorful boxes
col1, col2, col3 = st.columns(3)
with col1:
    latest_close = filtered_df['Close'].iloc[-1] if not filtered_df.empty else 0
    st.markdown(f"<div style='background-color: #FFD700; padding: 10px; border-radius: 5px;'><h3 style='color: #333;'>Latest Close: ${latest_close:.2f}</h3></div>", unsafe_allow_html=True)
with col2:
    avg_volume = filtered_df['Volume'].mean() if not filtered_df.empty else 0
    st.markdown(f"<div style='background-color: #ADFF2F; padding: 10px; border-radius: 5px;'><h3 style='color: #333;'>Avg Volume: {avg_volume:,.0f}</h3></div>", unsafe_allow_html=True)
with col3:
    total_return = filtered_df['Daily_Return'].sum() if not filtered_df.empty else 0
    color = '#32CD32' if total_return > 0 else '#FF0000'
    st.markdown(f"<div style='background-color: {color}; padding: 10px; border-radius: 5px;'><h3 style='color: #333;'>Total Return: {total_return:.2f}%</h3></div>", unsafe_allow_html=True)
# Raw data expander
with st.expander("View Raw Data"):
    st.dataframe(filtered_df.style.background_gradient(cmap='viridis'))

# Graph 1: Closing Price Line Chart
st.subheader('Graph 1: Closing Price Over Time (Line Chart)')
fig_close = px.line(filtered_df, x=filtered_df.index, y='Close', title='Closing Price',
                    color_discrete_sequence=px.colors.qualitative.Set1)
fig_close.update_layout(template='plotly_dark')
st.plotly_chart(fig_close, use_container_width=True)
with st.expander('Dataset for Closing Price Chart'):
    st.dataframe(filtered_df.style.background_gradient(cmap='Oranges'))

# Graph 2: Daily Return Line Chart
st.subheader('Graph 2: Daily Return Over Time (Line Chart)')
fig_return = px.line(filtered_df, x=filtered_df.index, y='Daily_Return', title='Daily Return',
                     color_discrete_sequence=px.colors.qualitative.Set2)
fig_return.update_layout(template='plotly_dark')
st.plotly_chart(fig_return, use_container_width=True)
with st.expander('Dataset for Daily Return Chart'):
    st.dataframe(filtered_df.style.background_gradient(cmap='Blues'))

# Graph 3: Price Range Line Chart
st.subheader('Graph 3: Price Range Over Time (Line Chart)')
fig_range = px.line(filtered_df, x=filtered_df.index, y='Price_Range', title='Price Range',
                    color_discrete_sequence=px.colors.qualitative.Set3)
fig_range.update_layout(template='plotly_dark')
st.plotly_chart(fig_range, use_container_width=True)
with st.expander('Dataset for Price Range Chart'):
    st.dataframe(filtered_df.style.background_gradient(cmap='Purples'))

# Graph 4: Trading Volume Bar Chart
st.subheader('Graph 4: Trading Volume (Bar Chart)')
fig_volume = px.bar(filtered_df, x=filtered_df.index, y='Volume', title='Trading Volume',
                    color='Volume', color_continuous_scale='plasma')
fig_volume.update_layout(template='plotly_dark')
st.plotly_chart(fig_volume, use_container_width=True)
with st.expander('Dataset for Trading Volume Chart'):
    st.dataframe(filtered_df.style.background_gradient(cmap='Greens'))

# Graph 5: Combined Close Price Line and Volume Bar Chart
st.subheader('Graph 5: Combined Closing Price (Line) and Volume (Bar) Chart')
fig_combined = go.Figure()

# Add Close Price Line
fig_combined.add_trace(go.Scatter(x=filtered_df.index, y=filtered_df['Close'], mode='lines', name='Close Price', yaxis='y1', line=dict(color='orange')))

# Add Volume Bar
fig_combined.add_trace(go.Bar(x=filtered_df.index, y=filtered_df['Volume'], name='Volume', yaxis='y2', marker_color='blue', opacity=0.5))

# Update layout for dual y-axes
fig_combined.update_layout(
    title='Combined Close Price and Volume',
    xaxis_title='Date',
    yaxis_title='Close Price',
    yaxis2=dict(title='Volume', overlaying='y', side='right'),
    template='plotly_dark',
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
)
st.plotly_chart(fig_combined, use_container_width=True)
with st.expander('Dataset for Combined Chart'):
    st.dataframe(filtered_df[['Close', 'Volume']].style.background_gradient(cmap='RdYlGn'))

# Interactive Scatter Plot for Daily Return vs Price Change
st.subheader('Bonus Graph: Daily Return vs Price Change (Scatter Plot)')
fig_scatter = px.scatter(filtered_df, x='Daily_Return', y='Price_Change', color='Volume',
                         size='Volume', hover_data=['Open', 'Close'],
                         title='Daily Return vs Price Change',
                         color_continuous_scale='plasma')
fig_scatter.update_layout(template='plotly_dark')
st.plotly_chart(fig_scatter, use_container_width=True)
with st.expander('Dataset for Scatter Plot'):
    st.dataframe(filtered_df[['Daily_Return', 'Price_Change', 'Volume']].style.background_gradient(cmap='plasma'))

# Data Statistics
with st.expander('Data Statistics'):
    st.write(filtered_df.describe().style.background_gradient(cmap='coolwarm'))

# Footer
st.markdown("<p style='text-align: center; color: #808080;'>Built with Streamlit & Plotly - Hover over charts for data details! Authentic Stock Analysis Dashboard</p>", unsafe_allow_html=True)