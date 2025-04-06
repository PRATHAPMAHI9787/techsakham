import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Load Sales Data
df = pd.read_csv('/home/asu/sales_data1.csv')

# Strip spaces from column names
df.columns = df.columns.str.strip()

# Convert Date column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Group sales by month
sales_trend = df.groupby(df['Date'].dt.to_period('M')).agg({'Total_Sales': 'sum'}).reset_index()
sales_trend['Date'] = sales_trend['Date'].astype(str)  # Convert period to string

# Group sales by category
category_sales = df.groupby('Category').agg({'Total_Sales': 'sum'}).reset_index()

# Initialize Dash app
app = dash.Dash(__name__)

# App Layout
app.layout = html.Div([
    html.Div([
        html.H2("Retail Sales Dashboard", style={'textAlign': 'center', 'color': 'white'}),
        html.Hr(),
        html.Label("Select Month:", style={'fontWeight': 'bold', 'color': 'white'}),
        dcc.Dropdown(
            id='month-dropdown',
            options=[{'label': month, 'value': month} for month in sales_trend['Date']],
            value=sales_trend['Date'].iloc[-1],  # Default to latest month
            clearable=False,
            style={'width': '90%', 'margin': 'auto'}
        ),
    ], style={'width': '20%', 'backgroundColor': '#003366', 'padding': '20px', 'position': 'fixed', 'height': '100vh', 'color': 'black'}),
    
    html.Div([
        html.Div([
            html.H3("Sales Trend Over Time", style={'color': '#006699'}),
            dcc.Graph(id='sales-trend')
        ], style={'backgroundColor': '#f8f9fa', 'padding': '20px', 'borderRadius': '10px', 'marginBottom': '20px'}),
        
        html.Div([
            html.H3("Sales by Product Category", style={'color': '#006699'}),
            dcc.Graph(id='category-sales')
        ], style={'backgroundColor': '#f8f9fa', 'padding': '20px', 'borderRadius': '10px'}),
    ], style={'marginLeft': '22%', 'padding': '20px'})
], style={'fontFamily': 'Arial', 'backgroundColor': '#e9ecef'})

# Callbacks to update charts
@app.callback(
    Output('sales-trend', 'figure'),
    Output('category-sales', 'figure'),
    Input('month-dropdown', 'value')
)
def update_graphs(selected_month):
    filtered_df = df[df['Date'].dt.to_period('M').astype(str) == selected_month]
    
    sales_trend_filtered = filtered_df.groupby(filtered_df['Date'].dt.date).agg({'Total_Sales': 'sum'}).reset_index()
    sales_trend_filtered['Date'] = sales_trend_filtered['Date'].astype(str)  # Convert date to string
    
    trend_fig = px.line(
        sales_trend_filtered,
        x='Date', y='Total_Sales',
        title=f"Sales Trend for {selected_month}",
        markers=True,
        color_discrete_sequence=['#FF5733']
    )
    
    category_sales_filtered = filtered_df.groupby('Category').agg({'Total_Sales': 'sum'}).reset_index()
    category_fig = px.bar(
        category_sales_filtered, x='Category', y='Total_Sales',
        title=f"Product Sales by Category for {selected_month}",
        color='Category',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    return trend_fig, category_fig

# Run server
if __name__ == '__main__':
    app.run(debug=True)
