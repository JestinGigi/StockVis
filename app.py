from dash import Dash, dcc, html, Input, Output, State, callback
from datetime import datetime as dt

#Imports for plotting
import yfinance as yf 
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Importing Model
from model import forecastPrices

# Dash Instance
app = Dash(__name__, meta_tags=[{'name': 'viewport','content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}])

# Server Property
server = app.server


# Side Navigation
item1 = html.Div(
    [
        html.Div([
            html.P("StockVis Navigation", className="start"),
        html.Div([
            #Link for stock codes
            html.P([html.A("Click Me for Stock Code", href='https://stockanalysis.com/stocks/', target='_blank')]),
            #Stock code input
            dcc.Input(
                id='stock',
                type='text',
                placeholder='Stock Code',
                className='btn',
                required=True,
            ),
            html.Button('Submit', id='btn-submit', n_clicks=0, className='btn'),
        ], className='stock-text'), 
        html.Div([
            # Date range picker input
            dcc.DatePickerRange(
            id='my-date-picker-range',
            start_date=dt(2017,1, 21),
            end_date=dt.now(),
            max_date_allowed=dt.now(),
            initial_visible_month=dt.now(),
    ),
        ]),
        html.Div([
            #Stock price button
            html.Div([
                html.Button('Stock Price', id='btn-stock', className='btn btn-lower'),
            #Indicator button
                html.Button('Indicator', id='btn-indicator', className='btn btn-lower'),
            ], className='price'),
            #Days
            html.Div([
                dcc.Input(
                id='days',
                placeholder='Days',
                type='number',
                className='btn btn-lower',
                min=5,
                max=60,
            ),
            #Forecast button
            html.Button('Forecast', id='btn-forecast', className='btn btn-lower')], className='forecast'),
            
        ], className='fields')
    ], className='inputs')
    ],
    className='nav')


# Right Main Content
item2 = html.Div(
    [  html.Div([
            html.Div([
                #Company Name
                html.Div(
                    [
                        html.H2(children='Stocks', id='company-header')
                    ],className='header'),
                #Company Description
                html.Div([''], id='Description', className='description_ticker'),
                
                #Historical Stock Price Plot
                html.Div(
                 id='graph-content'),
                
                #Exponential Moving Curve Plot
                html.Div(
                 id='indicator-content'),
                
                #Forecast Plot
                html.Div(
                id='forecast-content')
            ], className='main-content')
        ], className='inner-content')
    ], className='content')

# App Layouting
app.layout = html.Div([item1, item2], className='container')


# Updating stock name and description 
@callback(Output('company-header', 'children'),
    Output('Description', 'children'),
    Input('btn-submit', 'n_clicks'),
    State('stock', 'value'))
def update_data(n_clicks, input1):
    # your function here
    if (n_clicks != 0):
        try:
            ticker = yf.Ticker(input1)
            inf = ticker.info
            df = pd.DataFrame().from_dict(inf, orient="index").T
            shortname = df['shortName'][0]
            summary = df['longBusinessSummary'][0]
            return shortname, summary
        except:
            return 'Something went Wrong', 'Stock Code Incorrect/Required'
    return 'Stocks', ''


# Historical Stock Price Functions
def get_stock_price_fig(df):
    fig = px.line(df,
                    x= 'Date',
                    y= ['Open', 'Close'],
                    template='plotly_dark',
                    title="Closing and Opening Price vs Date",
                    labels={
                        'value':'Price','variable':'Price Type'})
    return fig

@callback(Output('graph-content', 'children'),
          Input('btn-stock', 'n_clicks'),
          State('stock', 'value'),
          State('my-date-picker-range', 'start_date'),
          State('my-date-picker-range', 'end_date'))
def plot_data(n_clicks, input1, start_date, end_date):
    if (n_clicks is not None):
        try:
            df = yf.download(input1, dt.fromisoformat(start_date), dt.fromisoformat(end_date))
            df.reset_index(inplace=True)
            fig = get_stock_price_fig(df)
            return dcc.Graph(responsive=True, figure=fig, config={'scrollZoom': True}, )
        except:
            return 'Stock Code is required/Incorrect'
    return ''


# Exponential Moving curve functions
def get_more(df):
    df['EWA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
    fig = px.scatter(df,
                    x= 'Date',
                    y= 'EWA_20',
                    template='plotly_dark',
                    title="Exponential Moving Average vs Date")
    fig.update_traces(mode='lines')
    return fig
    
@callback(Output('indicator-content', 'children'),
          Input('btn-indicator', 'n_clicks'),
          State('stock', 'value'),
          State('my-date-picker-range', 'start_date'),
          State('my-date-picker-range', 'end_date'))
def get_indicator(n_clicks, input1, start_date, end_date):
    if (n_clicks is not None):
        try:
            df = yf.download(input1, dt.fromisoformat(start_date), dt.fromisoformat(end_date))
            df.reset_index(inplace=True)
            fig = get_more(df)
            return dcc.Graph(responsive=True, figure=fig, config={'scrollZoom': True})
        except:
            return 'Stock Code is required/Incorrect'
    return ''

# Forcast Plotting functions
def plotprices(df, days):
    fig = px.line(df, 
                  x='Date', 
                  y='Close',
                  template='plotly_dark',
                  title=f"Predicted prices for {days} days",
                  labels={
                      'Close':'Close Price'
                  })
    return fig
@callback(Output('forecast-content', 'children'),
          Input('btn-forecast', 'n_clicks'),
          State('days', 'value'),
          State('stock', 'value'))
def Predict_Prices(n_clicks, input1, code):
    if (n_clicks is not None):
        if (type(input1) is not int):
            return 'Number of Days required and should be greater than 4'
        else:
            try:
                df = forecastPrices(input1, code)
                fig = plotprices(df, input1)
                return dcc.Graph(responsive=True, figure=fig, config={'scrollZoom': True})
            except:
                return 'Stock Code is required/Incorrect'
    return ''

if __name__ == "__main__":
    app.run_server(debug=True)