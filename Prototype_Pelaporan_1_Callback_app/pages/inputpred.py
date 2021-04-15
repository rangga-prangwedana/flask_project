import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_table
from utils import Header, make_dash_table
from keras.models import model_from_json 
import pandas as pd
import numpy as np
import statistics as stats
import math
import pickle
from sklearn import linear_model
import pathlib


# BUAT GRAFIK DATA NGGA BOLEH ADA NAN
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()
MODEL_PATH = PATH.joinpath("../model").resolve()