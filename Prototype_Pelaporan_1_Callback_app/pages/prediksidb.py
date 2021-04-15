import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_table
from utils import Header, make_dash_table
import pandas as pd
import numpy as np
import statistics as stats
import math
import pickle
from sklearn import linear_model
import pathlib
from dash.dependencies import Input, Output



# BUAT GRAFIK DATA NGGA BOLEH ADA NAN
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()
MODEL_PATH = PATH.joinpath("../model").resolve()

df_hujan = pd.read_csv(DATA_PATH.joinpath("Data Curah Hujan Kelembapan.csv"))
df_tes_asli = pd.read_csv(DATA_PATH.joinpath("Data Test Curah Hujan Kelembapan Asli.csv"))
df_tes_pred = pd.read_csv(DATA_PATH.joinpath("Data Test Curah Hujan Kelembapan Prediksi.csv"))
reg_model1 = pickle.load(open(MODEL_PATH.joinpath("regmodel1.sav"),'rb')) 
reg_model2 = pickle.load(open(MODEL_PATH.joinpath("regmodel2.sav"),'rb'))

def reg_pred1(df):
    test_d = df.Curah_Hujan
    test_data = np.asarray(test_d)
    test_data1 = np.reshape(test_data,(-1,1))
    pred_model1 = reg_model1.predict(test_data1)
    return pred_model1

def reg_pred2(df):
    pred_model2 = reg_model2.predict(df[['Curah_Hujan','Kelembapan']])
    return pred_model2

reg1_asli = reg_pred1(df_tes_asli)
reg1_pred = reg_pred1(df_tes_pred)

reg2_asli = reg_pred2(df_tes_asli)
reg2_pred = reg_pred2(df_tes_pred)

Curah_HujanRR = df_hujan.Curah_Hujan
Curah_HujanRR = Curah_HujanRR.values.reshape(-1,1)
Jml_Penderita = df_hujan.Jumlah_Penderita

reg1_score = reg_model1.score(Curah_HujanRR,Jml_Penderita)
reg2_score = reg_model2.score(df_hujan[['Curah_Hujan','Kelembapan']],df_hujan.Jumlah_Penderita)

def create_layout(app):
    return html.Div(
        [ Header(app),html.Div([
        html.Div([
            html.Div([
                html.H6("Hasil Regresi 1 Variabel dengan Curah Hujan Asli", className="subtitle padded"),reg1_asli[0], ],className="six columns"),
            html.Div([html.H6(["Hasil Regresi 1 Variabel dengan Curah Hujan Prediksi"],className = "subtitle padded"),reg1_pred[0], ],className = "six columns"),
        ],className = "row"),# Tambah row di sini
         html.Div([
            html.Div([
                html.H6("Hasil Regresi 2 Variabel dengan Curah Hujan Asli", className="subtitle padded"),reg2_asli[0], ],className="six columns"),
            html.Div([html.H6(["Hasil Regresi 2 Variabel dengan Curah Hujan Prediksi"],className = "subtitle padded"),reg2_pred[0], ],className = "six columns"),
        ],className = "row"),# Tambah row di sini
         html.Div([
            html.Div([
                html.H6("Score Regresi 1 Variabel", className="subtitle padded"),reg1_score, ],className="six columns"),
            html.Div([html.H6(["Score Regresi 2 Variabel"],className = "subtitle padded"),reg2_score, ],className = "six columns"),
        ],className = "row"),# Tambah row di sini        
        html.Div([
            html.Div([html.H6("Prediksi Penderita Demam Berdarah dari Curah Hujan", className="subtitle padded"),
           dcc.Input(id="input-1", type="number", value =1,debounce=True, min=1),html.Div(id="number-output"),
            ],className = "row"),
        ],className = "row"),# Tambah row di sini
        
    ],className = "sub_page"),],className="page",)


