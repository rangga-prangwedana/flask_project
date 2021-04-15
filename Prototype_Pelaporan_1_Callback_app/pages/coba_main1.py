import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy as np
import statistics as stats
import math
import pickle
from dash.dependencies import Input, Output, State
import base64
import datetime
import io
import pandas as pd
import pathlib
import dash_table_experiments as dt
import tensorflow as tf
from keras.models import model_from_json 
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout

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

def lstm_datas(df):
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

def grafik_lstm(df):
    return dcc.Graph(id = 'plot_RR',figure = {'data': [
    go.Scatter(x = df['Tanggal'], y = df['RR'],mode = 'lines',name='Curah Hujan Asli'),
    go.Scatter(x = df['Tanggal'], y = df['RR_pred'],mode = 'lines',name='Curah Hujan Prediksi')
     ], 'layout':  go.Layout(title='Curah Hujan Berdasarkan Tanggal')
     })



app = dash.Dash(
    __name__,meta_tags=[{"name": "viewport", "content": "width=device-width"}]
    )
server = app.server



app.layout = html.Div([html.H5("Cobaaaaa prediksiiii"), dcc.Upload(
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
    html.Div(id='output-data-upload'),
    
    ],className="six column",)

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
            df = df.dropna()
            df_fix = df.drop(columns = ['ff_avg','Tanggal'])
            data_scaled = sc.fit_transform(df_fix)
            X2 = np.delete(data_scaled,19,axis=1)
            X_proTest = np.reshape(X2,(X2.shape[0],1,X2.shape[1]))
            global graph
            with graph.as_default():
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
            grafik = dcc.Graph(id = 'plot_RR',figure = {'data': [
                    go.Scatter(x = data_fixed['Tanggal'], y = data_fixed['RR'],mode = 'lines',name='Curah Hujan Asli'),
                    go.Scatter(x = data_fixed['Tanggal'], y = data_fixed['RR_pred'],mode = 'lines',name='Curah Hujan Prediksi')
                    ], 'layout':  go.Layout(title='Curah Hujan Berdasarkan Tanggal')
                    })
            
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),
        grafik,

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            style_cell={'textAlign': 'left'},
            style_table={
            'maxHeight': '300px',
            'overflowY': 'scroll'
    }
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])
    
        
    


@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children



if __name__ == "__main__":
    app.run_server(debug=True)










