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
df_hujan = pd.read_csv(DATA_PATH.joinpath("data_hujan.csv"))

tabel1 = dash_table.DataTable(
    columns=[{'id': c, 'name': c} for c in df_murni.columns],
    data=df_murni.to_dict('records'),
    style_cell={'textAlign': 'left'},
    style_table={
        'maxHeight': '300px',
        'overflowY': 'scroll'
    })

grafik1 = dcc.Graph(id = 'plot_RR',figure = {'data': [
    go.Scatter(x = df_murni['Tanggal'], y = df_murni['Curah_Hujan'],mode = 'lines',name='Curah Hujan'),
     ], 'layout':  go.Layout(title='Curah Hujan Berdasarkan Tanggal',xaxis={'title':'Tanggal'},yaxis={'title':'Curah Hujan dalan MM'},)
     })


def create_layout(app):
    return html.Div([html.Div([Header(app)]),html.Div([
        html.Div([
            html.Div([
                html.H5("Curah Hujan dan Penderita Demam Berdarah"),
                                    html.Br([]),
                                    html.P(
                                        "\
                                    Sebagai wabah endemik di Indonesia, demam berdarah merupakan salah satu penyakit \
                                    yang kasus penyebarannya selalu terjadi setiap tahun. Demam berdarah ditularkan \
                                    lewat virus dengue dengan perantara nyamuk Aedes Aegypti. Penyakit ini sangat \
                                    berbahaya apabila terlambat ditangani. Di Kabupaten Banyumas sendiri, pernah \
                                    terjadi kasus demam berdarah yang sangat banyak dalam setahun sehingga ditetapkan \
                                    sebagai Kejadian Luar Biasa. Melihat betapa berbahayanya demam berdarah, tentunya \
                                    diperlukan tindakan antisipasi dan pencegahan. Salah satu cara antisipasi demam \
                                    berdarah adalah dengan melakukan prediksi. Berdasarkan penelitian sebelumnya, \
                                    faktor yang dianggap berpengaruh terhadap penyebaran demam berdarah adalah cuaca. \
                                    Dengan demikian, dapat diasumsikan dengan melakukan prediksi terhadap curah hujan, \
                                    jumlah penderita demam berdarah dapat diprediksi juga.",   
                                    
                                        style={"color": "#ffffff"},
                                        className="row",
                                    ),
            ],className = "product",),
        ],className = "row"),# Tambah row di sini
        html.Div([
            html.Div([html.H6(["Tabel Keterangan Data Mentah Curah Hujan Tahun 2010-2019"],className = "subtitle padded"),
            html.Table(make_dash_table(data_RR)),],className = "six columns"),
            html.Div([
                html.H6("Deskripsi Data Curah Hujan", className="subtitle padded"),
                                    html.Br([]),
                                    html.Div(
                                        [
                                            html.Li(
                                                "Data dan pengetahuan data didapatkan dari BMKG secara online dan langsung ke kantor Cilacap."),
                                            html.Li(
                                                "Data berkisar dari tahun 2010 hingga pertengahan tahun 2019."),    
                                            html.Li(
                                                "Data curah hujan berjumlah 2993 record dari 2994 data."
                                            ),
                                            html.Li(
                                                "Rata-rata curah hujan dari tahun 2010 hingga pertengahan 2019 adalah 12.668625250040412."
                                            ),
                                            html.Li(
                                                "Curah hujan terendah adalah 0, dan yang tertinggi adalah 199,5."
                                            ),
                                            html.Li(
                                                "Curah hujan diprediksi dan dicari keterkaitannya dengan penyebaran demam berdarah."),
                                        ],
                                        id="reviews-bullet-pts",
                                    ),
            ],className="six columns"),
        ],className = "row"),
        html.Div([html.H6("Tabel Data Cuaca", className="subtitle padded"),tabel1,],className = "row"),
        html.Div([html.H6("Tabel Keterangan Curah Hujan", className="subtitle padded"),html.Table(make_dash_table(df_hujan)),],className = "row"),
        html.Div([html.H6("Grafik Curah Hujan", className="subtitle padded"),grafik1,],className = "row"),
    ],className = "sub_page"),],className="page",)

