import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd 
import numpy as np
import plotly.graph_objects as go
from app import app,server
from control import DEPARTMENT, CITY, CATEGORIES, COMPANIES, JOBS

df = pd.read_csv('./data/df_final.csv', low_memory= False)

layout = html.Div([

########## First Row ##########

    html.Div([

########## Panneau de control ##########
            # Title
            html.Div([
                html.Div([           
                    html.Center(html.H6(
                        'Panneau de controle',
                        className='control_label'
                        )),
                ],
                className='card-header'
                ),

            # Body
            html.Div([
                html.Ul([
                    # Filter one
                    html.Li([
                        html.Label("Périodicité du salaire", className="control_label"),

                        dbc.RadioItems(
                            id="wage_status_selector",
                            options=[
                                {"label": "Par an", "value": "Par an"},
                                {"label": "Par mois", "value": "Par mois"},
                                {"label": "Par semaine", "value": "Par semaine"},
                            ],
                            inline=True,
                        ),
                    ],
                    className='list-group-item'
                    ),

                    # Filter second

                    html.Li([
                        html.Label("Salaire annuel (en K€)", className="control_label"),

                        dbc.RadioItems(
                            id="range_status_selector",
                            options=[
                                {"label": "20 - 40", "value": 1},
                                {"label": "40 - 48", "value": 2},
                                {"label": "48 - 100", "value": 3},
                            ],
                            inline=True,
                        ),
                    ],
                    className='list-group-item'
                    ),

                    # Filter third
                    html.Li([
                        html.Label("Département", className="control_label"),

                        dbc.Checklist(
                            id="department_status_selector",
                            options=[
                                {"label": label, "value": label} for label in DEPARTMENT
                            ],
                            inline=True,
                        ),
                    
                    ],
                    className='list-group-item'
                    ),
                    # Filter fourth
                    html.Li([
                            
                            html.Label("Domaine d'expertise", className="control_label"),

                            dbc.RadioItems(
                            id="areas_status_selector",
                            options=[
                                {"label": "All", "value": "All"},
                                {"label": 'Data', "value": 'Data'},
                                {"label": 'Développeur', "value": 'Développeur'},
                            ],
                            value="All",
                            inline=True,
                        ),
                    ],
                    className='list-group-item'
                    ),

                ],
                className='card-text'
                ),
            ],
            className='list-group list-group-flush'
            ),

        ],
        className='control card four columns'
        ),
########## FIN Panneau de control ##########

    ########## Indicators ##########

        html.Div([
            html.Div([

                html.Div([

                        dcc.Graph(id="avg_per_range"),        

                    ],
                    id="avg_salary_range",
                    className="card ml-5 five columns",
                ),

                    html.Div([

                            dcc.Graph(id="offers_per_range"), 

                        ],
                        id="offer_range",
                        className="card ml-5 five columns",
                    ),

                ],
                className=" row flex-display",
                ),

##########  FIN Indicators ##########

 
        ],
        className='seven columns'
        ),


    ],
    className="row flex-display",
    id="cross-filter-options",
    ),

########## FIN First Row ##########

########## Graphics 1 ##########

    html.Div([

            html.Div([

            dcc.Graph(
                id='distribution_salary',
            ),
        ],
        id= "graph_1",
        className="card eleven columns",
        ),

    ],
    className=" row mt-5 flex-display",
    ), 

    html.Div([
                html.H1(''),
            ],
            className='row'
        ),

########## FIN du HTML ##########
])

########## DEBUT DES FUNCTIONS  ##########

# Average per range


# Output : le valeur que nous affichons 
# Input : Les valeurs que nous envoyons 

@app.callback(
    Output("avg_per_range", "figure"),
    [
        Input("wage_status_selector", "value"),
        Input("department_status_selector", "value"),
        Input("areas_status_selector", "value"),
        Input("range_status_selector", "value"),
    ],
)

def update_average_text(wage_status_selector,department_status_selector,areas_status_selector, range_status_selector):
    
    if wage_status_selector == [] or wage_status_selector == None :
        if department_status_selector == [] or department_status_selector == None:
            if areas_status_selector == 'All':
                salary_mean = int(round(df[df['salary_mean'] != 0]['salary_mean'].mean(),2))
                salary_max = int(max(df['salary_mean']))
                salary_min = int(min(df['salary_mean']))
                indicatordata = go.Indicator(mode = "gauge+number", value = salary_mean, title = {'text': "Salaire moyen"}, domain = {'x': [0, 1], 'y': [0, 1]},  gauge = {'axis': {'range': [salary_min, salary_max]}, 'steps' : [{'range': [salary_min,salary_mean], 'color': "lightgray"},{'range': [salary_mean,salary_max], 'color': "gray"}] })
                return {'data': [indicatordata], 'layout' : {'font' : {'size' : 20}, 'titlefont' : {'size' : 10}}}
            else:
                df_test = filter_dataframe('Job_Search', [areas_status_selector],df).reset_index(drop=True)
                salary_mean = int(round(df_test[df_test['salary_mean'] != 0]['salary_mean'].mean(),2))
                salary_max = int(max(df_test['salary_mean']))
                salary_min = int(min(df_test['salary_mean']))
                indicatordata = go.Indicator(mode = "gauge+number", value = salary_mean, title = {'text': "Salaire moyen"}, domain = {'x': [0, 1], 'y': [0, 1]},  gauge = {'axis': {'range': [salary_min, salary_max]}, 'steps' : [{'range': [salary_min,salary_mean], 'color': "lightgray"},{'range': [salary_mean,salary_max], 'color': "gray"}] })
                return {'data': [indicatordata], 'layout' : {'font' : {'size' : 20}, 'titlefont' : {'size' : 10}}}
        else:
            df_test = filter_dataframe('Department_Search', department_status_selector,df).reset_index(drop=True)
            if areas_status_selector == 'All':
                salary_mean = int(round(df_test[df_test['salary_mean'] != 0]['salary_mean'].mean(),2))
                salary_max = int(max(df_test['salary_mean']))
                salary_min = int(min(df_test['salary_mean']))
                indicatordata = go.Indicator(mode = "gauge+number", value = salary_mean, title = {'text': "Salaire moyen"}, domain = {'x': [0, 1], 'y': [0, 1]},  gauge = {'axis': {'range': [salary_min, salary_max]}, 'steps' : [{'range': [salary_min,salary_mean], 'color': "lightgray"},{'range': [salary_mean,salary_max], 'color': "gray"}] })
                return {'data': [indicatordata], 'layout' : {'font' : {'size' : 20}, 'titlefont' : {'size' : 10}}}
            else:
                df_test = filter_dataframe('Job_Search', [areas_status_selector],df_test).reset_index(drop=True)
                salary_mean = int(round(df_test[df_test['salary_mean'] != 0]['salary_mean'].mean(),2))
                salary_max = int(max(df_test['salary_mean']))
                salary_min = int(min(df_test['salary_mean']))
                indicatordata = go.Indicator(mode = "gauge+number", value = salary_mean, title = {'text': "Salaire moyen"}, domain = {'x': [0, 1], 'y': [0, 1]},  gauge = {'axis': {'range': [salary_min, salary_max]}, 'steps' : [{'range': [salary_min,salary_mean], 'color': "lightgray"},{'range': [salary_mean,salary_max], 'color': "gray"}] })
                return {'data': [indicatordata], 'layout' : {'font' : {'size' : 20}, 'titlefont' : {'size' : 10}}}
    elif wage_status_selector == 'Par an':
        df_test = df[df['salary_period'] == wage_status_selector]
        if range_status_selector == [] or range_status_selector == None :
            if department_status_selector == [] or department_status_selector == None:
                if areas_status_selector == 'All':
                    salary_mean = int(round(df_test[df_test['salary_mean'] != 0]['salary_mean'].mean(),2))
                    salary_max = int(max(df_test['salary_mean']))
                    salary_min = int(min(df_test['salary_mean']))
                    indicatordata = go.Indicator(mode = "gauge+number", value = salary_mean, title = {'text': "Salaire moyen"}, domain = {'x': [0, 1], 'y': [0, 1]},  gauge = {'axis': {'range': [salary_min, salary_max]}, 'steps' : [{'range': [salary_min,salary_mean], 'color': "lightgray"},{'range': [salary_mean,salary_max], 'color': "gray"}] })
                    return {'data': [indicatordata], 'layout' : {'font' : {'size' : 20}, 'titlefont' : {'size' : 10}}}
                else:
                    df_test = filter_dataframe('Job_Search', [areas_status_selector],df_test).reset_index(drop=True)
                    salary_mean = int(round(df_test[df_test['salary_mean'] != 0]['salary_mean'].mean(),2))
                    salary_max = int(max(df_test['salary_mean']))
                    salary_min = int(min(df_test['salary_mean']))
                    indicatordata = go.Indicator(mode = "gauge+number", value = salary_mean, title = {'text': "Salaire moyen"}, domain = {'x': [0, 1], 'y': [0, 1]},  gauge = {'axis': {'range': [salary_min, salary_max]}, 'steps' : [{'range': [salary_min,salary_mean], 'color': "lightgray"},{'range': [salary_mean,salary_max], 'color': "gray"}] })
                    return {'data': [indicatordata], 'layout' : {'font' : {'size' : 20}, 'titlefont' : {'size' : 10}}}
            else:
                df_test = filter_dataframe('Department_Search', department_status_selector,df_test).reset_index(drop=True)
                if areas_status_selector == 'All':
                    salary_mean = int(round(df_test[df_test['salary_mean'] != 0]['salary_mean'].mean(),2))
                    salary_max = int(max(df_test['salary_mean']))
                    salary_min = int(min(df_test['salary_mean']))
                    indicatordata = go.Indicator(mode = "gauge+number", value = salary_mean, title = {'text': "Salaire moyen"}, domain = {'x': [0, 1], 'y': [0, 1]},  gauge = {'axis': {'range': [salary_min, salary_max]}, 'steps' : [{'range': [salary_min,salary_mean], 'color': "lightgray"},{'range': [salary_mean,salary_max], 'color': "gray"}] })
                    return {'data': [indicatordata], 'layout' : {'font' : {'size' : 20}, 'titlefont' : {'size' : 10}}}
                else:
                    df_test = filter_dataframe('Job_Search', [areas_status_selector],df_test).reset_index(drop=True)
                    salary_mean = int(round(df_test[df_test['salary_mean'] != 0]['salary_mean'].mean(),2))
                    salary_max = int(max(df_test['salary_mean']))
                    salary_min = int(min(df_test['salary_mean']))
                    indicatordata = go.Indicator(mode = "gauge+number", value = salary_mean, title = {'text': "Salaire moyen"}, domain = {'x': [0, 1], 'y': [0, 1]},  gauge = {'axis': {'range': [salary_min, salary_max]}, 'steps' : [{'range': [salary_min,salary_mean], 'color': "lightgray"},{'range': [salary_mean,salary_max], 'color': "gray"}] })
                    return {'data': [indicatordata], 'layout' : {'font' : {'size' : 20}, 'titlefont' : {'size' : 10}}}
        else:
            df_test = filter_dataframe('salary_class', [range_status_selector],df_test).reset_index(drop=True)
            if department_status_selector == [] or department_status_selector == None:
                if areas_status_selector == 'All':
                    salary_mean = int(round(df_test[df_test['salary_mean'] != 0]['salary_mean'].mean(),2))
                    salary_max = int(max(df_test['salary_mean']))
                    salary_min = int(min(df_test['salary_mean']))
                    indicatordata = go.Indicator(mode = "gauge+number", value = salary_mean, title = {'text': "Salaire moyen"}, domain = {'x': [0, 1], 'y': [0, 1]},  gauge = {'axis': {'range': [salary_min, salary_max]}, 'steps' : [{'range': [salary_min,salary_mean], 'color': "lightgray"},{'range': [salary_mean,salary_max], 'color': "gray"}] })
                    return {'data': [indicatordata], 'layout' : {'font' : {'size' : 20}, 'titlefont' : {'size' : 10}}}
                else:
                    df_test = filter_dataframe('Job_Search', [areas_status_selector],df_test).reset_index(drop=True)
                    salary_mean = int(round(df_test[df_test['salary_mean'] != 0]['salary_mean'].mean(),2))
                    salary_max = int(max(df_test['salary_mean']))
                    salary_min = int(min(df_test['salary_mean']))
                    indicatordata = go.Indicator(mode = "gauge+number", value = salary_mean, title = {'text': "Salaire moyen"}, domain = {'x': [0, 1], 'y': [0, 1]},  gauge = {'axis': {'range': [salary_min, salary_max]}, 'steps' : [{'range': [salary_min,salary_mean], 'color': "lightgray"},{'range': [salary_mean,salary_max], 'color': "gray"}] })
                    return {'data': [indicatordata], 'layout' : {'font' : {'size' : 20}, 'titlefont' : {'size' : 10}}}
            else:
                df_test = filter_dataframe('Department_Search', department_status_selector,df_test).reset_index(drop=True)
                if areas_status_selector == 'All':
                    salary_mean = int(round(df_test[df_test['salary_mean'] != 0]['salary_mean'].mean(),2))
                    salary_max = int(max(df_test['salary_mean']))
                    salary_min = int(min(df_test['salary_mean']))
                    indicatordata = go.Indicator(mode = "gauge+number", value = salary_mean, title = {'text': "Salaire moyen"}, domain = {'x': [0, 1], 'y': [0, 1]},  gauge = {'axis': {'range': [salary_min, salary_max]}, 'steps' : [{'range': [salary_min,salary_mean], 'color': "lightgray"},{'range': [salary_mean,salary_max], 'color': "gray"}] })
                    return {'data': [indicatordata], 'layout' : {'font' : {'size' : 20}, 'titlefont' : {'size' : 10}}}
                else:
                    df_test = filter_dataframe('Job_Search', [areas_status_selector],df_test).reset_index(drop=True)
                    salary_mean = int(round(df_test[df_test['salary_mean'] != 0]['salary_mean'].mean(),2))
                    salary_max = int(max(df_test['salary_mean']))
                    salary_min = int(min(df_test['salary_mean']))
                    indicatordata = go.Indicator(mode = "gauge+number", value = salary_mean, title = {'text': "Salaire moyen"}, domain = {'x': [0, 1], 'y': [0, 1]},  gauge = {'axis': {'range': [salary_min, salary_max]}, 'steps' : [{'range': [salary_min,salary_mean], 'color': "lightgray"},{'range': [salary_mean,salary_max], 'color': "gray"}] })
                    return {'data': [indicatordata], 'layout' : {'font' : {'size' : 20}, 'titlefont' : {'size' : 10}}}
    else:
        df_test = df[df['salary_period'] == wage_status_selector]
        if department_status_selector == [] or department_status_selector == None:
            if areas_status_selector == 'All':
                salary_mean = int(round(df_test[df_test['salary_mean'] != 0]['salary_mean'].mean(),2))
                salary_max = int(max(df_test['salary_mean']))
                salary_min = int(min(df_test['salary_mean']))
                indicatordata = go.Indicator(mode = "gauge+number", value = salary_mean, title = {'text': "Salaire moyen"}, domain = {'x': [0, 1], 'y': [0, 1]},  gauge = {'axis': {'range': [salary_min, salary_max]}, 'steps' : [{'range': [salary_min,salary_mean], 'color': "lightgray"},{'range': [salary_mean,salary_max], 'color': "gray"}] })
                return {'data': [indicatordata], 'layout' : {'font' : {'size' : 20}, 'titlefont' : {'size' : 10}}}
            else:
                df_test = filter_dataframe('Job_Search', [areas_status_selector],df_test).reset_index(drop=True)
                salary_mean = int(round(df_test[df_test['salary_mean'] != 0]['salary_mean'].mean(),2))
                salary_max = int(max(df_test['salary_mean']))
                salary_min = int(min(df_test['salary_mean']))
                indicatordata = go.Indicator(mode = "gauge+number", value = salary_mean, title = {'text': "Salaire moyen"}, domain = {'x': [0, 1], 'y': [0, 1]},  gauge = {'axis': {'range': [salary_min, salary_max]}, 'steps' : [{'range': [salary_min,salary_mean], 'color': "lightgray"},{'range': [salary_mean,salary_max], 'color': "gray"}] })
                return {'data': [indicatordata], 'layout' : {'font' : {'size' : 20}, 'titlefont' : {'size' : 10}}}
        else:
            df_test = filter_dataframe('Department_Search', department_status_selector,df_test).reset_index(drop=True)
            if areas_status_selector == 'All':
                salary_mean = int(round(df_test[df_test['salary_mean'] != 0]['salary_mean'].mean(),2))
                salary_max = int(max(df_test['salary_mean']))
                salary_min = int(min(df_test['salary_mean']))
                indicatordata = go.Indicator(mode = "gauge+number", value = salary_mean, title = {'text': "Salaire moyen"}, domain = {'x': [0, 1], 'y': [0, 1]},  gauge = {'axis': {'range': [salary_min, salary_max]}, 'steps' : [{'range': [salary_min,salary_mean], 'color': "lightgray"},{'range': [salary_mean,salary_max], 'color': "gray"}] })
                return {'data': [indicatordata], 'layout' : {'font' : {'size' : 20}, 'titlefont' : {'size' : 10}}}
            else:
                df_test = filter_dataframe('Job_Search', [areas_status_selector],df_test).reset_index(drop=True)
                salary_mean = int(round(df_test[df_test['salary_mean'] != 0]['salary_mean'].mean(),2))
                salary_max = int(max(df_test['salary_mean']))
                salary_min = int(min(df_test['salary_mean']))
                indicatordata = go.Indicator(mode = "gauge+number", value = salary_mean, title = {'text': "Salaire moyen"}, domain = {'x': [0, 1], 'y': [0, 1]},  gauge = {'axis': {'range': [salary_min, salary_max]}, 'steps' : [{'range': [salary_min,salary_mean], 'color': "lightgray"},{'range': [salary_mean,salary_max], 'color': "gray"}] })
                return {'data': [indicatordata], 'layout' : {'font' : {'size' : 30}, 'titlefont' : {'size' : 10}}}

# Offers per range

@app.callback(
    Output("offers_per_range", "figure"),
    [
        Input("wage_status_selector", "value"),
        Input("department_status_selector", "value"),
        Input("areas_status_selector", "value"),
        Input("range_status_selector", "value"),
    ],
)

def update_offers_text(wage_status_selector,department_status_selector,areas_status_selector, range_status_selector):
    if wage_status_selector == [] or wage_status_selector == None:
        if department_status_selector == [] or department_status_selector == None:
            if areas_status_selector == 'All':
                indicatordata = go.Indicator(mode = "gauge+number", value = df.shape[0], title = {'text': "Nombre d'offres"}, domain = {'x': [0, 1], 'y': [0, 1]},  gauge = {'axis': {'range': [None, df.shape[0]]}, 'steps' : [{'range': [0, (df.shape[0]/2)], 'color': "lightgray"},{'range': [(df.shape[0]/2), df.shape[0]], 'color': "gray"}] })
                return {'data': [indicatordata], 'layout' : {'font' : {'size' : 15}}}
            else:
                df_test = filter_dataframe('Job_Search', [areas_status_selector],df).reset_index(drop=True)
                indicatordata = go.Indicator(mode = "gauge+number", value = df_test.shape[0], title = {'text': "Nombre d'offres"}, domain = {'x': [0, 1], 'y': [0, 1]},  gauge = {'axis': {'range': [None, df.shape[0]]}, 'steps' : [{'range': [0, (df.shape[0]/2)], 'color': "lightgray"},{'range': [(df.shape[0]/2), df.shape[0]], 'color': "gray"}] })
                return {'data': [indicatordata], 'layout' : {'font' : {'size' : 15}}}
        else:
            df_test = filter_dataframe('Department_Search', department_status_selector,df).reset_index(drop=True)
            if areas_status_selector == 'All':
                indicatordata = go.Indicator(mode = "gauge+number", value = df_test.shape[0], title = {'text': "Nombre d'offres"}, domain = {'x': [0, 1], 'y': [0, 1]},  gauge = {'axis': {'range': [None, df.shape[0]]}, 'steps' : [{'range': [0, (df.shape[0]/2)], 'color': "lightgray"},{'range': [(df.shape[0]/2), df.shape[0]], 'color': "gray"}] })
                return {'data': [indicatordata], 'layout' : {'font' : {'size' : 15}}}
            else:
                df_test = filter_dataframe('Job_Search', [areas_status_selector],df_test).reset_index(drop=True)
                indicatordata = go.Indicator(mode = "gauge+number", value = df_test.shape[0], title = {'text': "Nombre d'offres"}, domain = {'x': [0, 1], 'y': [0, 1]},  gauge = {'axis': {'range': [None, df.shape[0]]}, 'steps' : [{'range': [0, (df.shape[0]/2)], 'color': "lightgray"},{'range': [(df.shape[0]/2), df.shape[0]], 'color': "gray"}] })
                return {'data': [indicatordata], 'layout' : {'font' : {'size' : 15}}}
    elif wage_status_selector == 'Par an':
        df_test = df[df['salary_period'] == wage_status_selector]
        if range_status_selector == [] or range_status_selector == None :
            if department_status_selector == [] or department_status_selector == None:
                if areas_status_selector == 'All':
                    indicatordata = go.Indicator(mode = "gauge+number", value = df_test.shape[0], title = {'text': "Nombre d'offres"}, domain = {'x': [0, 1], 'y': [0, 1]},  gauge = {'axis': {'range': [None, df.shape[0]]}, 'steps' : [{'range': [0, (df.shape[0]/2)], 'color': "lightgray"},{'range': [(df.shape[0]/2), df.shape[0]], 'color': "gray"}] })
                    return {'data': [indicatordata], 'layout' : {'font' : {'size' : 15}}}
                else:
                    df_test = filter_dataframe('Job_Search', [areas_status_selector],df_test).reset_index(drop=True)
                    indicatordata = go.Indicator(mode = "gauge+number", value = df_test.shape[0], title = {'text': "Nombre d'offres"}, domain = {'x': [0, 1], 'y': [0, 1]},  gauge = {'axis': {'range': [None, df.shape[0]]}, 'steps' : [{'range': [0, (df.shape[0]/2)], 'color': "lightgray"},{'range': [(df.shape[0]/2), df.shape[0]], 'color': "gray"}] })
                    return {'data': [indicatordata], 'layout' : {'font' : {'size' : 15}}}
            else:
                df_test = filter_dataframe('Department_Search', department_status_selector,df_test).reset_index(drop=True)
                if areas_status_selector == 'All':
                    indicatordata = go.Indicator(mode = "gauge+number", value = df_test.shape[0], title = {'text': "Nombre d'offres"}, domain = {'x': [0, 1], 'y': [0, 1]},  gauge = {'axis': {'range': [None, df.shape[0]]}, 'steps' : [{'range': [0, (df.shape[0]/2)], 'color': "lightgray"},{'range': [(df.shape[0]/2), df.shape[0]], 'color': "gray"}] })
                    return {'data': [indicatordata], 'layout' : {'font' : {'size' : 15}}}
                else:
                    df_test = filter_dataframe('Job_Search', [areas_status_selector],df_test).reset_index(drop=True)
                    indicatordata = go.Indicator(mode = "gauge+number", value = df_test.shape[0], title = {'text': "Nombre d'offres"}, domain = {'x': [0, 1], 'y': [0, 1]},  gauge = {'axis': {'range': [None, df.shape[0]]}, 'steps' : [{'range': [0, (df.shape[0]/2)], 'color': "lightgray"},{'range': [(df.shape[0]/2), df.shape[0]], 'color': "gray"}] })
                    return {'data': [indicatordata], 'layout' : {'font' : {'size' : 15}}}
        else:
            df_test = filter_dataframe('salary_class', [range_status_selector],df_test).reset_index(drop=True)
            if department_status_selector == [] or department_status_selector == None:
                if areas_status_selector == 'All':
                    indicatordata = go.Indicator(mode = "gauge+number", value = df_test.shape[0], title = {'text': "Nombre d'offres"}, domain = {'x': [0, 1], 'y': [0, 1]},  gauge = {'axis': {'range': [None, df.shape[0]]}, 'steps' : [{'range': [0, (df.shape[0]/2)], 'color': "lightgray"},{'range': [(df.shape[0]/2), df.shape[0]], 'color': "gray"}] })
                    return {'data': [indicatordata], 'layout' : {'font' : {'size' : 15}}}
                else:
                    df_test = filter_dataframe('Job_Search', [areas_status_selector],df_test).reset_index(drop=True)
                    indicatordata = go.Indicator(mode = "gauge+number", value = df_test.shape[0], title = {'text': "Nombre d'offres"}, domain = {'x': [0, 1], 'y': [0, 1]},  gauge = {'axis': {'range': [None, df.shape[0]]}, 'steps' : [{'range': [0, (df.shape[0]/2)], 'color': "lightgray"},{'range': [(df.shape[0]/2), df.shape[0]], 'color': "gray"}] })
                    return {'data': [indicatordata], 'layout' : {'font' : {'size' : 15}}}
            else:
                df_test = filter_dataframe('Department_Search', department_status_selector,df_test).reset_index(drop=True)
                if areas_status_selector == 'All':
                    indicatordata = go.Indicator(mode = "gauge+number", value = df_test.shape[0], title = {'text': "Nombre d'offres"}, domain = {'x': [0, 1], 'y': [0, 1]},  gauge = {'axis': {'range': [None, df.shape[0]]}, 'steps' : [{'range': [0, (df.shape[0]/2)], 'color': "lightgray"},{'range': [(df.shape[0]/2), df.shape[0]], 'color': "gray"}] })
                    return {'data': [indicatordata], 'layout' : {'font' : {'size' : 15}}}
                else:
                    df_test = filter_dataframe('Job_Search', [areas_status_selector],df_test).reset_index(drop=True)
                    indicatordata = go.Indicator(mode = "gauge+number", value = df_test.shape[0], title = {'text': "Nombre d'offres"}, domain = {'x': [0, 1], 'y': [0, 1]},  gauge = {'axis': {'range': [None, df.shape[0]]}, 'steps' : [{'range': [0, (df.shape[0]/2)], 'color': "lightgray"},{'range': [(df.shape[0]/2), df.shape[0]], 'color': "gray"}] })
                    return {'data': [indicatordata], 'layout' : {'font' : {'size' : 15}}}

    else:
        df_test = df[df['salary_period'] == wage_status_selector].reset_index(drop=True).reset_index(drop=True)
        if department_status_selector == [] or department_status_selector == None:
            if areas_status_selector == 'All':
                indicatordata = go.Indicator(mode = "gauge+number", value = df_test.shape[0], title = {'text': "Nombre d'offres"}, domain = {'x': [0, 1], 'y': [0, 1]},  gauge = {'axis': {'range': [None, df.shape[0]]}, 'steps' : [{'range': [0, (df.shape[0]/2)], 'color': "lightgray"},{'range': [(df.shape[0]/2), df.shape[0]], 'color': "gray"}] })
                return {'data': [indicatordata], 'layout' : {'font' : {'size' : 15}}}
            else:
                df_test = filter_dataframe('Job_Search', [areas_status_selector],df_test).reset_index(drop=True)
                indicatordata = go.Indicator(mode = "gauge+number", value = df_test.shape[0], title = {'text': "Nombre d'offres"}, domain = {'x': [0, 1], 'y': [0, 1]},  gauge = {'axis': {'range': [None, df.shape[0]]}, 'steps' : [{'range': [0, (df.shape[0]/2)], 'color': "lightgray"},{'range': [(df.shape[0]/2), df.shape[0]], 'color': "gray"}] })
                return {'data': [indicatordata], 'layout' : {'font' : {'size' : 15}}}
        else:
            df_test = filter_dataframe('Department_Search', department_status_selector,df_test).reset_index(drop=True)
            if areas_status_selector == 'All':
                indicatordata = go.Indicator(mode = "gauge+number", value = df_test.shape[0], title = {'text': "Nombre d'offres"}, domain = {'x': [0, 1], 'y': [0, 1]},  gauge = {'axis': {'range': [None, df.shape[0]]}, 'steps' : [{'range': [0, (df.shape[0]/2)], 'color': "lightgray"},{'range': [(df.shape[0]/2), df.shape[0]], 'color': "gray"}] })
                return {'data': [indicatordata], 'layout' : {'font' : {'size' : 15}}}
            else:
                df_test = filter_dataframe('Job_Search', [areas_status_selector],df_test).reset_index(drop=True)
                indicatordata = go.Indicator(mode = "gauge+number", value = df_test.shape[0], title = {'text': "Nombre d'offres"}, domain = {'x': [0, 1], 'y': [0, 1]},  gauge = {'axis': {'range': [None, df.shape[0]]}, 'steps' : [{'range': [0, (df.shape[0]/2)], 'color': "lightgray"},{'range': [(df.shape[0]/2), df.shape[0]], 'color': "gray"}] })
                return {'data': [indicatordata], 'layout' : {'font' : {'size' : 15}}}


# Fonction pour filter les datasets en fonction des criteres 

def filter_dataframe(category, arguments, dataset):

    if len(arguments) < 1:
        dataset_test = dataset[dataset[category] == arguments[0]]
    else:
        dataset_test = pd.DataFrame
        for i in range(len(arguments)):
            if i < 1:
                dataset_test = dataset[dataset[category] == arguments[i]]
            else:
                dataset_partial = dataset[dataset[category] == arguments[i]]
                frame = [dataset_test, dataset_partial]
                dataset_test = pd.concat(frame)
        return dataset_test


# Distribution Salary

@app.callback(
    Output("distribution_salary", "figure"),
    [
        Input("wage_status_selector", "value"),
        Input("department_status_selector", "value"),
        Input("areas_status_selector", "value"),
        Input("range_status_selector", "value"),
    ]
)

def distribution_graph(wage_status_selector, department_status_selector, areas_status_selector, range_status_selector):
    if wage_status_selector == [] or wage_status_selector == None:
        df_test = df[df['salary_mean'] != 0].reset_index(drop=True)
        if department_status_selector == [] or department_status_selector == None:
            if areas_status_selector == 'All':
                histdata = go.Histogram(x=df_test['salary_mean'].values)
                return {'data': [histdata], 'layout' : {'title' : 'Distribution des salaires', 'bargap' : 0.2, 'font' : {'size' : 20}}}
            else:
                df_test = filter_dataframe('Job_Search', [areas_status_selector],df_test).reset_index(drop=True)
                histdata = go.Histogram(x=df_test['salary_mean'].values)
                return {'data': [histdata], 'layout' : {'title' : 'Distribution des salaires', 'bargap' : 0.2, 'font' : {'size' : 20}}}
        else:
            df_test = filter_dataframe('Department_Search', department_status_selector,df).reset_index(drop=True)
            if areas_status_selector == 'All':
                histdata = go.Histogram(x=df_test['salary_mean'].values)
                return {'data': [histdata], 'layout' : {'title' : 'Distribution des salaires', 'bargap' : 0.2, 'font' : {'size' : 20}}}
            else:
                df_test = filter_dataframe('Job_Search', [areas_status_selector],df_test).reset_index(drop=True)
                histdata = go.Histogram(x=df_test['salary_mean'].values)
                return {'data': [histdata], 'layout' : {'title' : 'Distribution des salaires', 'bargap' : 0.2, 'font' : {'size' : 20}}}
    elif wage_status_selector == 'Par an':
        df_test = df[df['salary_period'] == wage_status_selector].reset_index(drop=True)
        if range_status_selector == [] or range_status_selector == None:
            if department_status_selector == [] or department_status_selector == None:
                if areas_status_selector == 'All':
                    histdata = go.Histogram(x=df_test['salary_mean'].values)
                    return {'data': [histdata], 'layout' : {'title' : 'Distribution des salaires', 'bargap' : 0.2, 'font' : {'size' : 20}}}
                else:
                    df_test = filter_dataframe('Job_Search', [areas_status_selector],df_test).reset_index(drop=True)
                    histdata = go.Histogram(x=df_test['salary_mean'].values)
                    return {'data': [histdata], 'layout' : {'title' : 'Distribution des salaires', 'bargap' : 0.2, 'font' : {'size' : 20}}}
            else:
                df_test = filter_dataframe('Department_Search', department_status_selector,df_test).reset_index(drop=True)
                if areas_status_selector == 'All':
                    histdata = go.Histogram(x=df_test['salary_mean'].values)
                    return {'data': [histdata], 'layout' : {'title' : 'Distribution des salaires', 'bargap' : 0.2, 'font' : {'size' : 20}}}
                else:
                    df_test = filter_dataframe('Job_Search', [areas_status_selector],df_test).reset_index(drop=True)
                    histdata = go.Histogram(x=df_test['salary_mean'].values)
                    return {'data': [histdata], 'layout' : {'title' : 'Distribution des salaires', 'bargap' : 0.2, 'font' : {'size' : 20}}}
        else:
            df_test = filter_dataframe('salary_class', [range_status_selector],df_test).reset_index(drop=True)
            df_test = df_test[df_test['salary_period'] == wage_status_selector].reset_index(drop=True)
            if department_status_selector == [] or department_status_selector == None:
                if areas_status_selector == 'All':
                    histdata = go.Histogram(x=df_test['salary_mean'].values)
                    return {'data': [histdata], 'layout' : {'title' : 'Distribution des salaires', 'bargap' : 0.2, 'font' : {'size' : 20}}}
                else:
                    df_test = filter_dataframe('Job_Search', [areas_status_selector],df_test).reset_index(drop=True)
                    histdata = go.Histogram(x=df_test['salary_mean'].values)
                    return {'data': [histdata], 'layout' : {'title' : 'Distribution des salaires', 'bargap' : 0.2, 'font' : {'size' : 20}}}
            else:
                df_test = filter_dataframe('Department_Search', department_status_selector,df_test).reset_index(drop=True)
                if areas_status_selector == 'All':
                    histdata = go.Histogram(x=df_test['salary_mean'].values)
                    return {'data': [histdata], 'layout' : {'title' : 'Distribution des salaires', 'bargap' : 0.2, 'font' : {'size' : 20}}}
                else:
                    df_test = filter_dataframe('Job_Search', [areas_status_selector],df_test).reset_index(drop=True)
                    histdata = go.Histogram(x=df_test['salary_mean'].values)
                    return {'data': [histdata], 'layout' : {'title' : 'Distribution des salaires', 'bargap' : 0.2, 'font' : {'size' : 20}}}
    else:
        df_test = df[df['salary_period'] == wage_status_selector].reset_index(drop=True)
        if department_status_selector == [] or department_status_selector == None:
            if areas_status_selector == 'All':
                histdata = go.Histogram(x=df_test['salary_mean'].values)
                return {'data': [histdata], 'layout' : {'title' : 'Distribution des salaires', 'bargap' : 0.2, 'font' : {'size' : 20}}}
            else:
                df_test = filter_dataframe('Job_Search', [areas_status_selector],df_test).reset_index(drop=True)
                histdata = go.Histogram(x=df_test['salary_mean'].values)
                return {'data': [histdata], 'layout' : {'title' : 'Distribution des salaires', 'bargap' : 0.2, 'font' : {'size' : 20}}}
        else:
            df_test = filter_dataframe('Department_Search', department_status_selector,df_test).reset_index(drop=True)
            if areas_status_selector == 'All':
                histdata = go.Histogram(x=df_test['salary_mean'].values)
                return {'data': [histdata], 'layout' : {'title' : 'Distribution des salaires', 'bargap' : 0.2, 'font' : {'size' : 20}}}
            else:
                df_test = filter_dataframe('Job_Search', [areas_status_selector],df_test).reset_index(drop=True)
                histdata = go.Histogram(x=df_test['salary_mean'].values)
                return {'data': [histdata], 'layout' : {'title' : 'Distribution des salaires', 'bargap' : 0.2, 'font' : {'size' : 20}}}