# StockVis Navigation

This project implements a Stock Visualization and Forecasting web dashboard using the Dash framework. It leverages the Plotly library to visualize the historical open and close stock prices. The prediction of future close stock prices is done using Support Vector Machine regression with an RBF kernel, which is optimized using GridSearchCV. The historical data is obtained from the yfinance PyPI library.

## Deployment
- http://jestingigi.pythonanywhere.com/
- https://dashboard.render.com/web/srv-cis10rp8g3n42okpb1ig/logs

**Loading can take some time**
## Features

- Historical open and close stock price visualization using Plotly
- Support Vector Machine regression with an RBF kernel for stock price prediction
- GridSearchCV optimization for model hyperparameter tuning
- Integration with the yfinance PyPI library for historical data retrieval

## Requirements

- **Python Version Used**: 3.8.6
- **Pip Version**: 20.2.1

```python
dash==2.11.1
dash-core-components==2.0.0
dash-html-components==2.0.0
dash-table==5.0.0
matplotlib==3.7.1
numpy==1.23.5
pandas==2.0.2
plotly==5.15.0
scikit_learn==1.2.2
seaborn==0.12.2
yfinance==0.2.24
Flask==2.2.5
```


## Installation

1. Clone the repository:

```shell
git clone https://github.com/JestinGigi/StockVis.git
```
## Local Deployment 

```shell
python app.py
```
