import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd 
import numpy as np
import plotly.graph_objects as go
from app import app,server
from control import DEPARTMENT, CITY, CATEGORIES, SKILLS, QUALIFICATIONS, CONTRACTS

df = pd.read_csv('./data/df_final.csv', low_memory= False)

layout = html.Div([
    
    html.Div([
########## Panneau de control ##########
            # Title
            html.Div([
                html.Div([           
                    html.Center(html.H6(
                        'Panneau de control',
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
                                {"label": "20 - 36", "value": 1},
                                {"label": "37 - 45", "value": 4},
                                {"label": "47 - 57", "value": 2},
                                {"label": "60 - 90", "value": 3},
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
                    # Filter fifth
                    html.Li([
                        html.Label("Filtre par type de contrat", className="control_label"),

                        dbc.Checklist(
                            id="contracts_status_selector",
                            options=[
                                {"label": label, "value": label} for label in CONTRACTS
                            ],
                            inline=True,
                        ),
                    
                    ],
                    className='list-group-item'
                    ),

                    # Filter fifth
                    html.Li([
                        html.Label("Filtre par qualifications", className="control_label"),

                        dbc.Checklist(
                            id="qualifications_status_selector",
                            options=[
                                {"label": label, "value": label} for label in QUALIFICATIONS
                            ],
                            inline=True,
                        ),
                    
                    ],
                    className='list-group-item'
                    ),

                    # Filter sixth
                    html.Li([
                        html.Div([
                            html.Label("Filtre par compétences", className="control_label"),

                            dcc.Dropdown(
                                id="competences_statuses",
                                multi=True,
                                options=[
                                    {"label": label, "value": label} for label in SKILLS
                                ],
                                className="dropdown-item",
                            ),
                        ],
                        className='dropdown'
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
        className='card four columns'
        ),
########## FIN Panneau de control ##########


########## Graphics 2 & 3 ##########

            html.Div([

            dcc.Graph(
                id='skills_chart'
            ),
            
                ],
            id= "skills",
            className="card six columns",
            ),

            # html.Div([

            # dcc.Graph(
            #     id='pie2',
            # )
            # ],
            # id= "chart_pie2",
            # className="card five mt-5 columns",
            # ),

########## FIN Graphics 2 & 3 ##########

        ],
        className="row mt-5 flex-display",
        ),

    html.Div([

            html.Div([

            dcc.Graph(
                id='pie_contracts'
            ),
            
                ],
            id= "chart_pie1",
            className="card five mt-5 columns",
            ),

            html.Div([

            dcc.Graph(
                id='pie_qualifications',
            )
            ],
            id= "chart_pie2",
            className="card five mt-5 columns",
            ),

########## FIN Graphics 2 & 3 ##########

        ],
        className="row mt-5 flex-display",
        ),

    html.Div([
        html.H1(''),
        ],
        className='row'
        ),

########## FIN du HTML ##########

])


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

# Skills chart 

@app.callback(
    Output("skills_chart", "figure"),
    [
        Input("competences_statuses", "value"),
        Input("areas_status_selector", "value"),
        Input("department_status_selector", "value"),
        Input("range_status_selector", "value"),
        Input("wage_status_selector", "value"),
    ],
)

def update_skills(competences_statuses, areas_status_selector, department_status_selector, range_status_selector, wage_status_selector):
    if wage_status_selector == [] or wage_status_selector == None:
        if areas_status_selector == 'All':
            if department_status_selector == [] or department_status_selector == None:
                df_test = df[SKILLS].sum()
                if competences_statuses == None or competences_statuses == []:
                    bardata = go.Bar(x= df_test.index ,y= df_test.values)
                    return {'data': [bardata], 'layout' : {'title' : "Compétences", 'font' : {'size' : 20}}}
                else:
                    list_left = df_test.index.difference(competences_statuses)
                    df_test = df_test.drop(list_left)
                    bardata = go.Bar(x= df_test.index ,y= df_test.values)
                    return {'data': [bardata], 'layout' : {'title' : "Compétences", 'font' : {'size' : 20}}}
            else:
                df_test = filter_dataframe('Department_Search', department_status_selector,df).reset_index(drop=True)
                df_test = df_test[SKILLS].sum()
                if competences_statuses == None or competences_statuses == []:
                    bardata = go.Bar(x= df_test.index ,y= df_test.values)
                    return {'data': [bardata], 'layout' : {'title' : "Compétences", 'font' : {'size' : 20}}}
                else:
                    list_left = df_test.index.difference(competences_statuses)
                    df_test = df_test.drop(list_left)
                    bardata = go.Bar(x= df_test.index ,y= df_test.values)
                    return {'data': [bardata], 'layout' : {'title' : "Compétences", 'font' : {'size' : 20}}}
        else:
            if department_status_selector == [] or department_status_selector == None:
                df_test = filter_dataframe('Job_Search', [areas_status_selector],df).reset_index(drop=True)
                df_test = df_test[SKILLS].sum()
                if competences_statuses == None or competences_statuses == []:
                    bardata = go.Bar(x= df_test.index ,y= df_test.values)
                    return {'data': [bardata], 'layout' : {'title' : "Compétences", 'font' : {'size' : 20}}}
                else:
                    list_left = df_test.index.difference(competences_statuses)
                    df_test = df_test.drop(list_left)
                    bardata = go.Bar(x= df_test.index ,y= df_test.values)
                    return {'data': [bardata], 'layout' : {'title' : "Compétences", 'font' : {'size' : 20}}}
            else:
                df_test = filter_dataframe('Department_Search', department_status_selector,df).reset_index(drop=True)
                df_test = filter_dataframe('Job_Search', [areas_status_selector],df_test).reset_index(drop=True)
                df_test = df_test[SKILLS].sum()
                if competences_statuses == None or competences_statuses == []:
                    bardata = go.Bar(x= df_test.index ,y= df_test.values)
                    return {'data': [bardata], 'layout' : {'title' : "Compétences", 'font' : {'size' : 20}}}
                else:
                    list_left = df_test.index.difference(competences_statuses)
                    df_test = df_test.drop(list_left)
                    bardata = go.Bar(x= df_test.index ,y= df_test.values)
                    return {'data': [bardata], 'layout' : {'title' : "Compétences", 'font' : {'size' : 20}}}
    elif wage_status_selector == 'Par an':
        df_test = df[df['salary_period'] == wage_status_selector].reset_index(drop=True)
        if range_status_selector == [] or range_status_selector == None:
            if areas_status_selector == 'All':
                if department_status_selector == [] or department_status_selector == None:
                    df_test = df_test[SKILLS].sum()
                    if competences_statuses == None or competences_statuses == []:
                        bardata = go.Bar(x= df_test.index ,y= df_test.values)
                        return {'data': [bardata], 'layout' : {'title' : "Compétences", 'font' : {'size' : 20}}}
                    else:
                        list_left = df_test.index.difference(competences_statuses)
                        df_test = df_test.drop(list_left)
                        bardata = go.Bar(x= df_test.index ,y= df_test.values)
                        return {'data': [bardata], 'layout' : {'title' : "Compétences", 'font' : {'size' : 20}}}
                else:
                    df_test = filter_dataframe('Department_Search', department_status_selector,df_test).reset_index(drop=True)
                    df_test = df_test[SKILLS].sum()
                    if competences_statuses == None or competences_statuses == []:
                        bardata = go.Bar(x= df_test.index ,y= df_test.values)
                        return {'data': [bardata], 'layout' : {'title' : "Compétences", 'font' : {'size' : 20}}}
                    else:
                        list_left = df_test.index.difference(competences_statuses)
                        df_test = df_test.drop(list_left)
                        bardata = go.Bar(x= df_test.index ,y= df_test.values)
                        return {'data': [bardata], 'layout' : {'title' : "Compétences", 'font' : {'size' : 20}}}
            else:
                #df_test = filter_dataframe('salary_class', [range_status_selector],df_test).reset_index(drop=True)
                if department_status_selector == [] or department_status_selector == None:
                    df_test = filter_dataframe('Job_Search', [areas_status_selector],df_test).reset_index(drop=True)
                    df_test = df_test[SKILLS].sum()
                    if competences_statuses == None or competences_statuses == []:
                        bardata = go.Bar(x= df_test.index ,y= df_test.values)
                        return {'data': [bardata], 'layout' : {'title' : "Compétences", 'font' : {'size' : 20}}}
                    else:
                        list_left = df_test.index.difference(competences_statuses)
                        df_test = df_test.drop(list_left)
                        bardata = go.Bar(x= df_test.index ,y= df_test.values)
                        return {'data': [bardata], 'layout' : {'title' : "Compétences", 'font' : {'size' : 20}}}
                else:
                    df_test = filter_dataframe('Department_Search', department_status_selector,df_test).reset_index(drop=True)
                    df_test = filter_dataframe('Job_Search', [areas_status_selector],df_test).reset_index(drop=True)
                    df_test = df_test[SKILLS].sum()
                    if competences_statuses == None or competences_statuses == []:
                        bardata = go.Bar(x= df_test.index ,y= df_test.values)
                        return {'data': [bardata], 'layout' : {'title' : "Compétences", 'font' : {'size' : 20}}}
                    else:
                        list_left = df_test.index.difference(competences_statuses)
                        df_test = df_test.drop(list_left)
                        bardata = go.Bar(x= df_test.index ,y= df_test.values)
                        return {'data': [bardata], 'layout' : {'title' : "Compétences", 'font' : {'size' : 20}}}
        else:
            df_test = df_test[df_test['salary_class'] == range_status_selector].reset_index(drop=True)
            if areas_status_selector == 'All':
                if department_status_selector == [] or department_status_selector == None:
                    df_test = df_test[SKILLS].sum()
                    if competences_statuses == None or competences_statuses == []:
                        bardata = go.Bar(x= df_test.index ,y= df_test.values)
                        return {'data': [bardata], 'layout' : {'title' : "Compétences", 'font' : {'size' : 20}}}
                    else:
                        list_left = df_test.index.difference(competences_statuses)
                        df_test = df_test.drop(list_left)
                        bardata = go.Bar(x= df_test.index ,y= df_test.values)
                        return {'data': [bardata], 'layout' : {'title' : "Compétences", 'font' : {'size' : 20}}}
                else:
                    df_test = filter_dataframe('Department_Search', department_status_selector,df_test).reset_index(drop=True)
                    df_test = df_test[SKILLS].sum()
                    if competences_statuses == None or competences_statuses == []:
                        bardata = go.Bar(x= df_test.index ,y= df_test.values)
                        return {'data': [bardata], 'layout' : {'title' : "Compétences", 'font' : {'size' : 20}}}
                    else:
                        list_left = df_test.index.difference(competences_statuses)
                        df_test = df_test.drop(list_left)
                        bardata = go.Bar(x= df_test.index ,y= df_test.values)
                        return {'data': [bardata], 'layout' : {'title' : "Compétences", 'font' : {'size' : 20}}}
            else:
                if department_status_selector == [] or department_status_selector == None:
                    df_test = filter_dataframe('Job_Search', [areas_status_selector],df_test).reset_index(drop=True)
                    df_test = df_test[SKILLS].sum()
                    if competences_statuses == None or competences_statuses == []:
                        bardata = go.Bar(x= df_test.index ,y= df_test.values)
                        return {'data': [bardata], 'layout' : {'title' : "Compétences", 'font' : {'size' : 20}}}
                    else:
                        list_left = df_test.index.difference(competences_statuses)
                        df_test = df_test.drop(list_left)
                        bardata = go.Bar(x= df_test.index ,y= df_test.values)
                        return {'data': [bardata], 'layout' : {'title' : "Compétences", 'font' : {'size' : 20}}}
                else:
                    df_test = filter_dataframe('Department_Search', department_status_selector,df_test).reset_index(drop=True)
                    df_test = filter_dataframe('Job_Search', [areas_status_selector],df_test).reset_index(drop=True)
                    df_test = df_test[SKILLS].sum()
                    if competences_statuses == None or competences_statuses == []:
                        bardata = go.Bar(x= df_test.index ,y= df_test.values)
                        return {'data': [bardata], 'layout' : {'title' : "Compétences", 'font' : {'size' : 20}}}
                    else:
                        list_left = df_test.index.difference(competences_statuses)
                        df_test = df_test.drop(list_left)
                        bardata = go.Bar(x= df_test.index ,y= df_test.values)
                        return {'data': [bardata], 'layout' : {'title' : "Compétences", 'font' : {'size' : 20}}}
    else:
        df_test = df[df['salary_period'] == wage_status_selector].reset_index(drop=True)
        if areas_status_selector == 'All':
            if department_status_selector == [] or department_status_selector == None:
                df_test = df_test[SKILLS].sum()
                if competences_statuses == None or competences_statuses == []:
                    bardata = go.Bar(x= df_test.index ,y= df_test.values)
                    return {'data': [bardata], 'layout' : {'title' : "Compétences", 'font' : {'size' : 20}}}
                else:
                    list_left = df_test.index.difference(competences_statuses)
                    df_test = df_test.drop(list_left)
                    bardata = go.Bar(x= df_test.index ,y= df_test.values)
                    return {'data': [bardata], 'layout' : {'title' : "Compétences", 'font' : {'size' : 20}}}
            else:
                df_test = filter_dataframe('Department_Search', department_status_selector,df_test).reset_index(drop=True)
                df_test = df_test[SKILLS].sum()
                if competences_statuses == None or competences_statuses == []:
                    bardata = go.Bar(x= df_test.index ,y= df_test.values)
                    return {'data': [bardata], 'layout' : {'title' : "Compétences", 'font' : {'size' : 20}}}
                else:
                    list_left = df_test.index.difference(competences_statuses)
                    df_test = df_test.drop(list_left)
                    bardata = go.Bar(x= df_test.index ,y= df_test.values)
                    return {'data': [bardata], 'layout' : {'title' : "Compétences", 'font' : {'size' : 20}}}
        else:
            if department_status_selector == [] or department_status_selector == None:
                df_test = filter_dataframe('Job_Search', [areas_status_selector],df_test).reset_index(drop=True)
                df_test = df_test[SKILLS].sum()
                if competences_statuses == None or competences_statuses == []:
                    bardata = go.Bar(x= df_test.index ,y= df_test.values)
                    return {'data': [bardata], 'layout' : {'title' : "Compétences", 'font' : {'size' : 20}}}
                else:
                    list_left = df_test.index.difference(competences_statuses)
                    df_test = df_test.drop(list_left)
                    bardata = go.Bar(x= df_test.index ,y= df_test.values)
                    return {'data': [bardata], 'layout' : {'title' : "Compétences", 'font' : {'size' : 20}}}
            else:
                df_test = filter_dataframe('Department_Search', department_status_selector,df_test).reset_index(drop=True)
                df_test = filter_dataframe('Job_Search', [areas_status_selector],df_test).reset_index(drop=True)
                df_test = df_test[SKILLS].sum()
                if competences_statuses == None or competences_statuses == []:
                    bardata = go.Bar(x= df_test.index ,y= df_test.values)
                    return {'data': [bardata], 'layout' : {'title' : "Compétences", 'font' : {'size' : 20}}}
                else:
                    list_left = df_test.index.difference(competences_statuses)
                    df_test = df_test.drop(list_left)
                    bardata = go.Bar(x= df_test.index ,y= df_test.values)
                    return {'data': [bardata], 'layout' : {'title' : "Compétences", 'font' : {'size' : 20}}}


@app.callback(
    Output("pie_contracts", "figure"),
    [
        Input("areas_status_selector", "value"),
        Input("wage_status_selector", "value"),
        Input("range_status_selector", "value"),
        Input("department_status_selector", "value"),
        Input("contracts_status_selector", "value"),
    ],
)

def update_contracts_pie(areas_status_selector, wage_status_selector, range_status_selector, department_status_selector, contracts_status_selector):
    if areas_status_selector == 'All':
        if department_status_selector == [] or department_status_selector == None:
            if wage_status_selector == [] or wage_status_selector == None:
                df_test = df[CONTRACTS].sum()
                if contracts_status_selector == [] or contracts_status_selector == None:
                    piedata = go.Pie(values=df_test.values, labels=df_test.index)
                    return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par contrats', 'font' : {'size' : 20}}}
                else:
                    list_left = df_test.index.difference(contracts_status_selector)
                    df_test = df_test.drop(list_left)
                    piedata = go.Pie(values=df_test.values, labels=df_test.index)
                    return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par contrats', 'font' : {'size' : 20}}}

            elif wage_status_selector == 'Par an':
                df_test = df[df['salary_period'] == wage_status_selector].reset_index(drop=True)
                if range_status_selector == None or range_status_selector == []:
                    df_test = df_test[CONTRACTS].sum()
                    if contracts_status_selector == [] or contracts_status_selector == None:
                        piedata = go.Pie(values=df_test.values, labels=df_test.index)
                        return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par contrats', 'font' : {'size' : 20}}}
                    else:
                        list_left = df_test.index.difference(contracts_status_selector)
                        df_test = df_test.drop(list_left)
                        piedata = go.Pie(values=df_test.values, labels=df_test.index)
                        return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par contrats', 'font' : {'size' : 20}}}
                else:
                    dff = df_test[df_test['salary_class'] == range_status_selector]
                    df_test = dff[CONTRACTS].sum()
                    if contracts_status_selector == [] or contracts_status_selector == None:
                        piedata = go.Pie(values=df_test.values, labels=df_test.index)
                        return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par contrats', 'font' : {'size' : 20}}}
                    else:
                        list_left = df_test.index.difference(contracts_status_selector)
                        df_test = df_test.drop(list_left)
                        piedata = go.Pie(values=df_test.values, labels=df_test.index)
                        return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par contrats', 'font' : {'size' : 20}}}
            else:
                df_test = df[df['salary_period'] == wage_status_selector].reset_index(drop=True)
                df_test = df_test[CONTRACTS].sum()
                if contracts_status_selector == [] or contracts_status_selector == None:
                    piedata = go.Pie(values=df_test.values, labels=df_test.index)
                    return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par contrats', 'font' : {'size' : 20}}}
                else:
                    list_left = df_test.index.difference(contracts_status_selector)
                    df_test = df_test.drop(list_left)
                    piedata = go.Pie(values=df_test.values, labels=df_test.index)
                    return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par contrats', 'font' : {'size' : 20}}}  
        else:
            df_test = filter_dataframe('Department_Search', department_status_selector,df).reset_index(drop=True)
            if wage_status_selector == [] or wage_status_selector == None:
                    df_test = df_test[CONTRACTS].sum()
                    if contracts_status_selector == [] or contracts_status_selector == None:
                        piedata = go.Pie(values=df_test.values, labels=df_test.index)
                        return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par contrats', 'font' : {'size' : 20}}}
                    else:
                        list_left = df_test.index.difference(contracts_status_selector)
                        df_test = df_test.drop(list_left)
                        piedata = go.Pie(values=df_test.values, labels=df_test.index)
                        return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par contrats', 'font' : {'size' : 20}}}
            elif wage_status_selector == 'Par an':
                df_test = df_test[df_test['salary_period'] == wage_status_selector].reset_index(drop=True)
                if range_status_selector == None or range_status_selector == []:
                    df_test = df_test[CONTRACTS].sum()
                    if contracts_status_selector == [] or contracts_status_selector == None:
                        piedata = go.Pie(values=df_test.values, labels=df_test.index)
                        return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par contrats', 'font' : {'size' : 20}}}
                    else:
                        list_left = df_test.index.difference(contracts_status_selector)
                        df_test = df_test.drop(list_left)
                        piedata = go.Pie(values=df_test.values, labels=df_test.index)
                        return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par contrats', 'font' : {'size' : 20}}}
                else:
                    dff = df_test[df_test['salary_class'] == range_status_selector]
                    df_test = dff[CONTRACTS].sum()
                    if contracts_status_selector == [] or contracts_status_selector == None:
                        piedata = go.Pie(values=df_test.values, labels=df_test.index)
                        return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par contrats', 'font' : {'size' : 20}}}
                    else:
                        list_left = df_test.index.difference(contracts_status_selector)
                        df_test = df_test.drop(list_left)
                        piedata = go.Pie(values=df_test.values, labels=df_test.index)
                        return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par contrats', 'font' : {'size' : 20}}}
            else:
                df_test = df_test[df_test['salary_period'] == wage_status_selector].reset_index(drop=True)
                df_test = df_test[CONTRACTS].sum()
                if contracts_status_selector == [] or contracts_status_selector == None:
                    piedata = go.Pie(values=df_test.values, labels=df_test.index)
                    return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par contrats', 'font' : {'size' : 20}}}
                else:
                    list_left = df_test.index.difference(contracts_status_selector)
                    df_test = df_test.drop(list_left)
                    piedata = go.Pie(values=df_test.values, labels=df_test.index)
                    return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par contrats', 'font' : {'size' : 20}}}
    else:
        df_test = filter_dataframe('Job_Search', [areas_status_selector],df).reset_index(drop=True)
        if department_status_selector == [] or department_status_selector == None:
            if wage_status_selector == [] or wage_status_selector == None:
                    df_test = df_test[CONTRACTS].sum()
                    if contracts_status_selector == [] or contracts_status_selector == None:
                        piedata = go.Pie(values=df_test.values, labels=df_test.index)
                        return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par contrats', 'font' : {'size' : 20}}}
                    else:
                        list_left = df_test.index.difference(contracts_status_selector)
                        df_test = df_test.drop(list_left)
                        piedata = go.Pie(values=df_test.values, labels=df_test.index)
                        return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par contrats', 'font' : {'size' : 20}}}
            elif wage_status_selector == 'Par an':
                df_test = df_test[df_test['salary_period'] == wage_status_selector].reset_index(drop=True)
                if range_status_selector == None or range_status_selector == []:
                    df_test = df_test[CONTRACTS].sum()
                    if contracts_status_selector == [] or contracts_status_selector == None:
                        piedata = go.Pie(values=df_test.values, labels=df_test.index)
                        return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par contrats', 'font' : {'size' : 20}}}
                    else:
                        list_left = df_test.index.difference(contracts_status_selector)
                        df_test = df_test.drop(list_left)
                        piedata = go.Pie(values=df_test.values, labels=df_test.index)
                        return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par contrats', 'font' : {'size' : 20}}}
                else:
                    dff = df_test[df_test['salary_class'] == range_status_selector]
                    df_test = dff[CONTRACTS].sum()
                    if contracts_status_selector == [] or contracts_status_selector == None:
                        piedata = go.Pie(values=df_test.values, labels=df_test.index)
                        return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par contrats', 'font' : {'size' : 20}}}
                    else:
                        list_left = df_test.index.difference(contracts_status_selector)
                        df_test = df_test.drop(list_left)
                        piedata = go.Pie(values=df_test.values, labels=df_test.index)
                        return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par contrats', 'font' : {'size' : 20}}}
            else:
                df_test = df_test[df_test['salary_period'] == wage_status_selector].reset_index(drop=True)
                df_test = df_test[CONTRACTS].sum()
                if contracts_status_selector == [] or contracts_status_selector == None:
                    piedata = go.Pie(values=df_test.values, labels=df_test.index)
                    return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par contrats', 'font' : {'size' : 20}}}
                else:
                    list_left = df_test.index.difference(contracts_status_selector)
                    df_test = df_test.drop(list_left)
                    piedata = go.Pie(values=df_test.values, labels=df_test.index)
                    return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par contrats', 'font' : {'size' : 20}}}
        else:
            df_test = filter_dataframe('Department_Search', department_status_selector,df).reset_index(drop=True)
            if wage_status_selector == [] or wage_status_selector == None:
                    df_test = df_test[CONTRACTS].sum()
                    if contracts_status_selector == [] or contracts_status_selector == None:
                        piedata = go.Pie(values=df_test.values, labels=df_test.index)
                        return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par contrats', 'font' : {'size' : 20}}}
                    else:
                        list_left = df_test.index.difference(contracts_status_selector)
                        df_test = df_test.drop(list_left)
                        piedata = go.Pie(values=df_test.values, labels=df_test.index)
                        return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par contrats', 'font' : {'size' : 20}}}
            elif wage_status_selector == 'Par an':
                df_test = df_test[df_test['salary_period'] == wage_status_selector].reset_index(drop=True)
                if range_status_selector == None or range_status_selector == []:
                    df_test = df_test[CONTRACTS].sum()
                    if contracts_status_selector == [] or contracts_status_selector == None:
                        piedata = go.Pie(values=df_test.values, labels=df_test.index)
                        return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par contrats', 'font' : {'size' : 20}}}
                    else:
                        list_left = df_test.index.difference(contracts_status_selector)
                        df_test = df_test.drop(list_left)
                        piedata = go.Pie(values=df_test.values, labels=df_test.index)
                        return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par contrats', 'font' : {'size' : 20}}}
                else:
                    dff = df_test[df_test['salary_class'] == range_status_selector]
                    df_test = dff[CONTRACTS].sum()
                    if contracts_status_selector == [] or contracts_status_selector == None:
                        piedata = go.Pie(values=df_test.values, labels=df_test.index)
                        return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par contrats', 'font' : {'size' : 20}}}
                    else:
                        list_left = df_test.index.difference(contracts_status_selector)
                        df_test = df_test.drop(list_left)
                        piedata = go.Pie(values=df_test.values, labels=df_test.index)
                        return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par contrats', 'font' : {'size' : 20}}}
            else:
                df_test = df_test[df_test['salary_period'] == wage_status_selector].reset_index(drop=True)
                df_test = df_test[CONTRACTS].sum()
                if contracts_status_selector == [] or contracts_status_selector == None:
                    piedata = go.Pie(values=df_test.values, labels=df_test.index)
                    return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par contrats', 'font' : {'size' : 20}}}
                else:
                    list_left = df_test.index.difference(contracts_status_selector)
                    df_test = df_test.drop(list_left)
                    piedata = go.Pie(values=df_test.values, labels=df_test.index)
                    return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par contrats', 'font' : {'size' : 20}}}


@app.callback(
    Output("pie_qualifications", "figure"),
    [
        Input("areas_status_selector", "value"),
        Input("wage_status_selector", "value"),
        Input("range_status_selector", "value"),
        Input("department_status_selector", "value"),
        Input("qualifications_status_selector", "value"),
    ],
)

def update_qualifications_pie(areas_status_selector, wage_status_selector, range_status_selector, department_status_selector, qualifications_status_selector):
    if areas_status_selector == 'All':
        if department_status_selector == [] or department_status_selector == None:
            if wage_status_selector == [] or wage_status_selector == None:
                df_test = df[QUALIFICATIONS].sum()
                if qualifications_status_selector == [] or qualifications_status_selector == None:
                    piedata = go.Pie(values=df_test.values, labels=df_test.index)
                    return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par diplôme', 'font' : {'size' : 20}}}
                else:
                    list_left = df_test.index.difference(qualifications_status_selector)
                    df_test = df_test.drop(list_left)
                    piedata = go.Pie(values=df_test.values, labels=df_test.index)
                    return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par diplôme', 'font' : {'size' : 20}}}

            elif wage_status_selector == 'Par an':
                df_test = df[df['salary_period'] == wage_status_selector].reset_index(drop=True)
                if range_status_selector == None or range_status_selector == []:
                    df_test = df_test[QUALIFICATIONS].sum()
                    if qualifications_status_selector == [] or qualifications_status_selector == None:
                        piedata = go.Pie(values=df_test.values, labels=df_test.index)
                        return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par diplôme', 'font' : {'size' : 20}}}
                    else:
                        list_left = df_test.index.difference(qualifications_status_selector)
                        df_test = df_test.drop(list_left)
                        piedata = go.Pie(values=df_test.values, labels=df_test.index)
                        return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par diplôme', 'font' : {'size' : 20}}}
                else:
                    dff = df_test[df_test['salary_class'] == range_status_selector]
                    df_test = dff[QUALIFICATIONS].sum()
                    if qualifications_status_selector == [] or qualifications_status_selector == None:
                        piedata = go.Pie(values=df_test.values, labels=df_test.index)
                        return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par diplôme', 'font' : {'size' : 20}}}
                    else:
                        list_left = df_test.index.difference(qualifications_status_selector)
                        df_test = df_test.drop(list_left)
                        piedata = go.Pie(values=df_test.values, labels=df_test.index)
                        return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par diplôme', 'font' : {'size' : 20}}}
            else:
                df_test = df[df['salary_period'] == wage_status_selector].reset_index(drop=True)
                df_test = df_test[QUALIFICATIONS].sum()
                if qualifications_status_selector == [] or qualifications_status_selector == None:
                    piedata = go.Pie(values=df_test.values, labels=df_test.index)
                    return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par diplôme', 'font' : {'size' : 20}}}
                else:
                    list_left = df_test.index.difference(qualifications_status_selector)
                    df_test = df_test.drop(list_left)
                    piedata = go.Pie(values=df_test.values, labels=df_test.index)
                    return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par diplôme', 'font' : {'size' : 20}}}  
        else:
            df_test = filter_dataframe('Department_Search', department_status_selector,df).reset_index(drop=True)
            if wage_status_selector == [] or wage_status_selector == None:
                    df_test = df_test[QUALIFICATIONS].sum()
                    if qualifications_status_selector == [] or qualifications_status_selector == None:
                        piedata = go.Pie(values=df_test.values, labels=df_test.index)
                        return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par diplôme', 'font' : {'size' : 20}}}
                    else:
                        list_left = df_test.index.difference(qualifications_status_selector)
                        df_test = df_test.drop(list_left)
                        piedata = go.Pie(values=df_test.values, labels=df_test.index)
                        return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par diplôme', 'font' : {'size' : 20}}}
            elif wage_status_selector == 'Par an':
                df_test = df_test[df_test['salary_period'] == wage_status_selector].reset_index(drop=True)
                if range_status_selector == None or range_status_selector == []:
                    df_test = df_test[QUALIFICATIONS].sum()
                    if qualifications_status_selector == [] or qualifications_status_selector == None:
                        piedata = go.Pie(values=df_test.values, labels=df_test.index)
                        return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par diplôme', 'font' : {'size' : 20}}}
                    else:
                        list_left = df_test.index.difference(qualifications_status_selector)
                        df_test = df_test.drop(list_left)
                        piedata = go.Pie(values=df_test.values, labels=df_test.index)
                        return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par diplôme', 'font' : {'size' : 20}}}
                else:
                    dff = df_test[df_test['salary_class'] == range_status_selector]
                    df_test = dff[QUALIFICATIONS].sum()
                    if qualifications_status_selector == [] or qualifications_status_selector == None:
                        piedata = go.Pie(values=df_test.values, labels=df_test.index)
                        return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par diplôme', 'font' : {'size' : 20}}}
                    else:
                        list_left = df_test.index.difference(qualifications_status_selector)
                        df_test = df_test.drop(list_left)
                        piedata = go.Pie(values=df_test.values, labels=df_test.index)
                        return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par diplôme', 'font' : {'size' : 20}}}
            else:
                df_test = df_test[df_test['salary_period'] == wage_status_selector].reset_index(drop=True)
                df_test = df_test[QUALIFICATIONS].sum()
                if qualifications_status_selector == [] or qualifications_status_selector == None:
                    piedata = go.Pie(values=df_test.values, labels=df_test.index)
                    return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par diplôme', 'font' : {'size' : 20}}}
                else:
                    list_left = df_test.index.difference(qualifications_status_selector)
                    df_test = df_test.drop(list_left)
                    piedata = go.Pie(values=df_test.values, labels=df_test.index)
                    return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par diplôme', 'font' : {'size' : 20}}}
    else:
        df_test = filter_dataframe('Job_Search', [areas_status_selector],df).reset_index(drop=True)
        if department_status_selector == [] or department_status_selector == None:
            if wage_status_selector == [] or wage_status_selector == None:
                    df_test = df_test[QUALIFICATIONS].sum()
                    if qualifications_status_selector == [] or qualifications_status_selector == None:
                        piedata = go.Pie(values=df_test.values, labels=df_test.index)
                        return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par diplôme', 'font' : {'size' : 20}}}
                    else:
                        list_left = df_test.index.difference(qualifications_status_selector)
                        df_test = df_test.drop(list_left)
                        piedata = go.Pie(values=df_test.values, labels=df_test.index)
                        return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par diplôme', 'font' : {'size' : 20}}}
            elif wage_status_selector == 'Par an':
                df_test = df_test[df_test['salary_period'] == wage_status_selector].reset_index(drop=True)
                if range_status_selector == None or range_status_selector == []:
                    df_test = df_test[QUALIFICATIONS].sum()
                    if qualifications_status_selector == [] or qualifications_status_selector == None:
                        piedata = go.Pie(values=df_test.values, labels=df_test.index)
                        return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par diplôme', 'font' : {'size' : 20}}}
                    else:
                        list_left = df_test.index.difference(qualifications_status_selector)
                        df_test = df_test.drop(list_left)
                        piedata = go.Pie(values=df_test.values, labels=df_test.index)
                        return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par diplôme', 'font' : {'size' : 20}}}
                else:
                    dff = df_test[df_test['salary_class'] == range_status_selector]
                    df_test = dff[QUALIFICATIONS].sum()
                    if qualifications_status_selector == [] or qualifications_status_selector == None:
                        piedata = go.Pie(values=df_test.values, labels=df_test.index)
                        return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par diplôme', 'font' : {'size' : 20}}}
                    else:
                        list_left = df_test.index.difference(qualifications_status_selector)
                        df_test = df_test.drop(list_left)
                        piedata = go.Pie(values=df_test.values, labels=df_test.index)
                        return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par diplôme', 'font' : {'size' : 20}}}
            else:
                df_test = df_test[df_test['salary_period'] == wage_status_selector].reset_index(drop=True)
                df_test = df_test[QUALIFICATIONS].sum()
                if qualifications_status_selector == [] or qualifications_status_selector == None:
                    piedata = go.Pie(values=df_test.values, labels=df_test.index)
                    return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par diplôme', 'font' : {'size' : 20}}}
                else:
                    list_left = df_test.index.difference(qualifications_status_selector)
                    df_test = df_test.drop(list_left)
                    piedata = go.Pie(values=df_test.values, labels=df_test.index)
                    return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par diplôme', 'font' : {'size' : 20}}}
        else:
            df_test = filter_dataframe('Department_Search', department_status_selector,df).reset_index(drop=True)
            if wage_status_selector == [] or wage_status_selector == None:
                    df_test = df_test[QUALIFICATIONS].sum()
                    if qualifications_status_selector == [] or qualifications_status_selector == None:
                        piedata = go.Pie(values=df_test.values, labels=df_test.index)
                        return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par diplôme', 'font' : {'size' : 20}}}
                    else:
                        list_left = df_test.index.difference(qualifications_status_selector)
                        df_test = df_test.drop(list_left)
                        piedata = go.Pie(values=df_test.values, labels=df_test.index)
                        return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par diplôme', 'font' : {'size' : 20}}}
            elif wage_status_selector == 'Par an':
                df_test = df_test[df_test['salary_period'] == wage_status_selector].reset_index(drop=True)
                if range_status_selector == None or range_status_selector == []:
                    df_test = df_test[QUALIFICATIONS].sum()
                    if qualifications_status_selector == [] or qualifications_status_selector == None:
                        piedata = go.Pie(values=df_test.values, labels=df_test.index)
                        return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par diplôme', 'font' : {'size' : 20}}}
                    else:
                        list_left = df_test.index.difference(qualifications_status_selector)
                        df_test = df_test.drop(list_left)
                        piedata = go.Pie(values=df_test.values, labels=df_test.index)
                        return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par diplôme', 'font' : {'size' : 20}}}
                else:
                    dff = df_test[df_test['salary_class'] == range_status_selector]
                    df_test = dff[QUALIFICATIONS].sum()
                    if qualifications_status_selector == [] or qualifications_status_selector == None:
                        piedata = go.Pie(values=df_test.values, labels=df_test.index)
                        return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par diplôme', 'font' : {'size' : 20}}}
                    else:
                        list_left = df_test.index.difference(qualifications_status_selector)
                        df_test = df_test.drop(list_left)
                        piedata = go.Pie(values=df_test.values, labels=df_test.index)
                        return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par diplôme', 'font' : {'size' : 20}}}
            else:
                df_test = df_test[df_test['salary_period'] == wage_status_selector].reset_index(drop=True)
                df_test = df_test[QUALIFICATIONS].sum()
                if qualifications_status_selector == [] or qualifications_status_selector == None:
                    piedata = go.Pie(values=df_test.values, labels=df_test.index)
                    return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par diplôme', 'font' : {'size' : 20}}}
                else:
                    list_left = df_test.index.difference(qualifications_status_selector)
                    df_test = df_test.drop(list_left)
                    piedata = go.Pie(values=df_test.values, labels=df_test.index)
                    return {'data': [piedata], 'layout' : { 'title' : 'Répartition des offres par diplôme', 'font' : {'size' : 20}}}
