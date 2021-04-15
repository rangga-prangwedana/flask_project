import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy as np
import statistics as stats
import math
import pickle
from sklearn import linear_model
import tensorflow as tf
from keras.models import model_from_json 
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout

import pandas as pd
import pathlib

from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range = (0, 1))

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()
MODEL_PATH = PATH.joinpath("../model").resolve()

df_data_murni = pd.read_csv(DATA_PATH.joinpath("Data Murni.csv"))
df_data_murni = df_data_murni.dropna()
datades = df_data_murni.describe().reset_index()
df_hujan = pd.read_csv(DATA_PATH.joinpath("Data Curah Hujan Kelembapan.csv"))
df_tes_asli = pd.read_csv(DATA_PATH.joinpath("Data Test Curah Hujan Kelembapan Asli.csv"))
df_tes_pred = pd.read_csv(DATA_PATH.joinpath("Data Test Curah Hujan Kelembapan Prediksi.csv"))
df_tes_lstm = pd.read_csv(DATA_PATH.joinpath("Data Test Prediksi Prototype 3a .csv"))
df_tes_lstm = df_tes_lstm.dropna()
reg_model1 = pickle.load(open(MODEL_PATH.joinpath("regmodel1.sav"),'rb')) 
reg_model2 = pickle.load(open(MODEL_PATH.joinpath("regmodel2.sav"),'rb'))

# load json and create model
json_file = open(MODEL_PATH.joinpath("model1.json"), 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights(MODEL_PATH.joinpath("model1.h5"))

graph = tf.get_default_graph()

def lstm_graphs(df):
    df_fix = df.drop(columns = ['ff_avg','Tanggal'])
    data_scaled = sc.fit_transform(df_fix)
    X2 = np.delete(data_scaled,19,axis=1)
    X_proTest = np.reshape(X2,(X2.shape[0],1,X2.shape[1]))
    predicted_RRTest = loaded_model.predict(X_proTest)
    predicted_RRealTest = np.hstack((X2,predicted_RRTest))
    predicted_RReal_Pred = sc.inverse_transform(predicted_RRealTest)
    datadeal = pd.DataFrame(predicted_RReal_Pred,columns = ['Tn', 'Tx', 'Tavg', 'RH_avg', 'ff_x', 'ddd_x', 'ddd_car', 'bulan',
       'RH_avg_5day', 'RH1', 'RH2', 'RH3', 'ff_x1', 'ff_x2', 'ff_x3',
       'RR_avg5_day', 'RR1', 'RR2', 'RR3', 'RR_pred'])
    RR_predict = datadeal.RR_pred
    df.reset_index(drop=True, inplace=True)
    RR_predict.reset_index(drop=True, inplace=True)
    data_fixed = pd.concat([df,RR_predict],axis=1)   
    return data_fixed

new_dataset = lstm_graphs(df_tes_lstm)
       


testdata2 = df_tes_asli[['Curah_Hujan','Kelembapan']]
predmodel_2 = reg_model2.predict(df_tes_asli[['Curah_Hujan','Kelembapan']])



tabel1=dash_table.DataTable(
    columns=[{'id': c, 'name': c} for c in datades.columns],
    data=datades.to_dict('records'),
    style_cell={'textAlign': 'left'},
    )

tabel2 = dash_table.DataTable(
    columns=[{'id': c, 'name': c} for c in df_data_murni.columns],
    data=df_data_murni.to_dict('records'),
    style_cell={'textAlign': 'left'},
    style_table={
        'maxHeight': '300px',
        'overflowY': 'scroll'
    })

 
graf2 = dcc.Graph(id='scatter2',figure={'data': [go.Scatter(
                    x = df_data_murni['Tanggal'],y = df_data_murni['RR'],mode = 'markers',
                    marker = {'size': 12,'color': 'rgb(51,204,153)','symbol': 'pentagon','line': {'width': 2} })],
            'layout': go.Layout(title = 'Scatterplot', xaxis = {'title': 'Tanggal'},
                yaxis = {'title': 'Curah Hujan'},hovermode='closest' )})


grafiklstm = dcc.Graph(id = 'plot_RR',figure = {'data': [
    go.Scatter(x = new_dataset['Tanggal'], y = new_dataset['RR'],mode = 'lines',name='Curah Hujan Asli'),
    go.Scatter(x = new_dataset['Tanggal'], y = new_dataset['RR_pred'],mode = 'lines',name='Curah Hujan Prediksi')
     ], 'layout':  go.Layout(title='Curah Hujan Berdasarkan Tanggal')
     })    


app = dash.Dash(
    __name__,meta_tags=[{"name": "viewport", "content": "width=device-width"}]
    )
server = app.server

app.layout = html.Div([html.H5("Cobaaaaa prediksiiii"),grafiklstm,],className="six column",)





if __name__ == "__main__":
    app.run_server(debug=True)
   