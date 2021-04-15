import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from utils import Header, make_dash_table
import pandas as pd
import dash
import dash_table
import numpy as np
import statistics as stats
import math
import pickle
from dash.dependencies import Input, Output, State
import base64
import datetime
import io
import pathlib
import dash_table_experiments as dt

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

# BUAT GRAFIK DATA NGGA BOLEH ADA NAN
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

df_fix = pd.read_csv(DATA_PATH.joinpath("3a Fix.csv"))
datades = df_fix.describe().reset_index()
df_pred1 = pd.read_csv(DATA_PATH.joinpath("percobaanTest1.csv"))
df_hujan = pd.read_csv(DATA_PATH.joinpath("Data Curah Hujan Kelembapan.csv"))
df_test = pd.read_csv(DATA_PATH.joinpath("tes_prediksi.csv"))


graf1 = dcc.Graph(id = 'plot1',figure = {'data': [
    go.Scatter(x = df_test['Tanggal'], y = df_test['RR'],mode = 'lines+markers',name='Curah Hujan Asli'),
    go.Scatter(x = df_test['Tanggal'], y = df_test['RR_pred'],mode = 'lines+markers',name='Curah Hujan Prediksi')
], 'layout':  go.Layout(title='Curah Hujan Asli vs Prediksi')
     })

def create_layout(app):
    return html.Div(
        [ Header(app),html.Div([
        html.Div([
            html.Div([html.H6("Hasil Prediksi Curah Hujan", className="subtitle padded"),graf1,],className = "row"),
        ],className = "row"),# Tambah row di sini
        html.Div([
            html.Div([html.H6("Coba Input Prediksi Curah Hujan", className="subtitle padded"),
            dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload'),],className = "row"),
        ],className = "row"),# Tambah row di sini
        
                
    ],className = "sub_page"),],className="page",)
