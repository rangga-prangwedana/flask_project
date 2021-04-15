import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_table
from utils import Header, make_dash_table
import pandas as pd
import pathlib


# BUAT GRAFIK DATA NGGA BOLEH ADA NAN
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

df_fix = pd.read_csv(DATA_PATH.joinpath("3a Fix.csv"))
datades = df_fix.describe().reset_index()
df_test_fix = pd.read_csv(DATA_PATH.joinpath("train_model_fix.csv"))
df_model = pd.read_csv(DATA_PATH.joinpath("tes_model.csv"))

tabel1 = dash_table.DataTable(
    columns=[{'id': c, 'name': c} for c in df_fix.columns],
    data=df_fix.to_dict('records'),
    style_cell={'textAlign': 'left'},
    style_table={
        'maxHeight': '300px',
        'overflowY': 'scroll'
    })

graf_loss = dcc.Graph(id = 'plotloss',figure = {'data': [
    go.Scatter(x = df_test_fix['index'], y = df_test_fix['loss'],mode = 'lines',name='Nilai Loss Model'),
    go.Scatter(x = df_test_fix['index'], y = df_test_fix['valloss'],mode = 'lines',name='Nilai Acc Model')
], 'layout':  go.Layout(title='Loss vs Validation Loss')
     })

graf_val = dcc.Graph(id = 'plotval',figure = {'data': [
    go.Scatter(x = df_test_fix['index'], y = df_test_fix['acc'],mode = 'lines',name='Nilai Val Loss Model'),
    go.Scatter(x = df_test_fix['index'], y = df_test_fix['valacc'],mode = 'lines',name='Nilai Val Acc Model')
], 'layout':  go.Layout(title='Acc vs Val Acc')
     })

graf_test = dcc.Graph(id = 'plottest',figure = {'data': [
    go.Scatter(x = df_model['Nomor'], y = df_model['RR'],mode = 'lines',name='Curah Hujan Tes Asli'),
    go.Scatter(x = df_model['Nomor'], y = df_model['RR_pred'],mode = 'lines',name='Curah Hujan Tes Prediksi')
], 'layout':  go.Layout(title='Hasil Model Tes Prediksi')
     })     

def create_layout(app):
    return html.Div(
        [ Header(app),html.Div([
        html.Div([
            html.Div([html.H6("Data yang Dipakai", className="subtitle padded"),tabel1,],className = "row"),
        ],className = "row"),# Tambah row di sini
        html.Div([html.Div([html.H6("Nilai Loss dibanding Acc",className = "subtitle padded"),graf_loss,],className = "six columns"),
        html.Div([html.H6("Nilai Val Loss dibanding Vall Acc",className = "subtitle padded"),graf_val,],className = "six columns"),],className = "row"),
        html.Div([html.H6("Perbandingan Nilai Tes Model", className="subtitle padded"),graf_test,],className = "row"),
                
    ],className = "sub_page"),],className="page",)



