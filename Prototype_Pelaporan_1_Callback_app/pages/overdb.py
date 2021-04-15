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
df_murni = pd.read_csv(DATA_PATH.joinpath("Data Murni.csv"))
data_RR = pd.read_csv(DATA_PATH.joinpath("datades.csv"))
df_hujan = pd.read_csv(DATA_PATH.joinpath("Data Curah Hujan Kelembapan.csv"))
df_kecamatan = pd.read_csv(DATA_PATH.joinpath("Data Kecamatan 2012-2018.csv"))
df_test = pd.read_csv(DATA_PATH.joinpath("Data Test Prediksi Prototype 3a .csv"))
df_test = df_test.dropna()

tabel1 = dash_table.DataTable(
    columns=[{'id': c, 'name': c} for c in df_murni.columns],
    data=df_murni.to_dict('records'),
    style_cell={'textAlign': 'left'},
    style_table={
        'maxHeight': '300px',
        'overflowY': 'scroll'
    })
    

grafik1 = dcc.Graph(id = 'plot_db',figure = {'data': [
    go.Bar(x = df_hujan['Tahun'], y = df_hujan['Jumlah_Penderita'], name='Jumlah Penderita',marker=dict(color='#BE350B')),
    ], 'layout':  go.Layout(title='Jumlah Penderita Demam Berdarah 2012-2018')
     })    

grafik2 = dcc.Graph(id = 'plot_kec',figure = {'data': [
    go.Bar(x = df_kecamatan['Kecamatan'], y = df_kecamatan['Jumlah_Penderita'], name='Jumlah Penderita',marker=dict(color='#FDCC44')),
    ], 'layout':  go.Layout(title='Jumlah Penderita Demam Berdarah 2012-2018')
     })   

grafik_pie = dcc.Graph(id = 'penderitadb_plot', figure = {'data':[go.Pie(labels=df_kecamatan['Kecamatan'],
values=df_kecamatan['Jumlah_Penderita'],name='Jumlah Penderita')],
'layout':go.Layout(title='Penderita Demam Berdarah Per Kecamatan')})     


def create_layout(app):
    return html.Div(
        [ Header(app),html.Div([
        html.Div([
            html.Div([
                html.H6("Demam Berdarah di Banyumas", className="subtitle padded"),
                                    html.Br([]),
                                    html.Div(
                                        [
                                            html.Li(
                                                "Demam berdarah merupakan ancaman yang nyata di Indonesia."),
                                            html.Li(
                                                "Penyakit demam berdarah banyak ditemukan di daerah tropis dan sub-tropis seperti Indonesia."),    
                                            html.Li(
                                                "Di Kabupaten Banyumas sendiri, pada awal Januari 2019, terjadi demam massal di Desa Pandak. "
                                            ),
                                            html.Li(
                                                "Jumlah penderita terbanyak tercatat pada tahun 2016."
                                            ),
                                            html.Li(
                                                "Jumlah penderita selama tahun 2012 hingga 2018 adalah 2329 orang."
                                            ),
                                        ],
                                        id="reviews-bullet-pts",
                                    ),
            ],className="six columns"),
            html.Div([html.H6(["Grafik Penderita DB Banyumas"],className = "subtitle padded"),
            grafik1,],className = "six columns"),
        ],className = "row"),# Tambah row di sini
        html.Div([html.H6("Jumlah Korban Demam Berdarah Per Kecamatan", className="subtitle padded"),grafik2,],className = "row"),
        html.Div([html.H6("Presentase Korban Demam Berdarah Per Kecamatan", className="subtitle padded"),grafik_pie,],className = "row"),
        
    ],className = "sub_page"),],className="page",)