import dash_html_components as html 
import dash_core_components as dcc 

def Header(app):
    return html.Div([get_header(app), html.Br([]), get_menu()])


def get_header(app):
    header=html.Div(
        [
            html.Div(
                [html.Img( src = app.get_asset_url("amikom_logoweb.png"),
                className = "logo",),
                
                ],
                className = "row",
            ),
            html.Div(
                [html.Div([html.H5("Laporan Hasil Prediksi Curah Hujan dan Penderita Demam Berdarah Kabupaten Banyumas")],
                className = "seven columns main-title",),
                html.Div(
                        [
                            dcc.Link(
                                "Full View",
                                href="/Prototype_Pelaporan_1_Callback_app/full-view",
                                className="full-view-link",
                            )
                        ],
                        className="five columns",
                    ),
                ],
                className="twelve columns",
                style={"padding-left": "0"},
            ),
        ],
        className="row",
    )
    return header

def get_menu():
    menu = html.Div(
        [
            dcc.Link(
                "Overview",
                href="/Prototype_Pelaporan_1_Callback_app/overview",
                className="tab first",
            ),
            dcc.Link(
                "Demam Berdarah",
                href="/Prototype_Pelaporan_1_Callback_app/overdb",
                className="tab first",
            ),
            dcc.Link(
                "Model",
                href="/Prototype_Pelaporan_1_Callback_app/model",
                className="tab",
            ),
            dcc.Link(
                "Prediksi Curah Hujan",
                href="/Prototype_Pelaporan_1_Callback_app/prediksi",
                className="tab",
            ),
            dcc.Link(
                "Prediksi Penderita DB",
                href="/Prototype_Pelaporan_1_Callback_app/prediksidb",
                className="tab",
            ),
            
        ],
        className="row all-tabs",
    )
    return menu


def make_dash_table(df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table