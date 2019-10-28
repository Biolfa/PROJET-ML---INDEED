import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app,server
from pages import first,second,third

app.layout = html.Div([

########## NavBar ##########

    html.Header([
        html.Div([

            html.Nav([

                html.Div([
                    html.A([
                        html.H2('Yes ! Indeed')
                    ],
                    href='/',
                    ),  
                ],
                className='navbar-brand',
                ),
                              
                        html.Ul([

                            html.Li([
                                html.A([
                                    html.H5('Salaires'),
                                ],
                                href='/salary',
                                ),
                            ],
                            className='nav-item active ml-5',
                            ),

                            html.Li([
                                html.A([
                                    html.H5('Métiers et Entreprises'),
                                ],
                                href='/jobs-and-location',
                                ),
                            ],
                            className='nav-item active ml-5',
                            ),
                            html.Li([
                                html.A([
                                    html.H5('Compétences'),
                                ],
                                href='/competences-and-skills',
                                ),
                            ],
                            className='nav-item active ml-5',
                            ),
                    ],
                    className='navbar-nav d-flex flex-row justify-content-center',
                    ),

                ],
                className='navbar navbar-dark bg-dark',
                style={'color': 'white'},
                ),

        ],
        className='containers mb-5'
        ),
    ],
    ),
########## Fin NavBar ##########


    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')

########## FIN du HTML ##########

])

########## DEBUT DES FUNCTIONS  ##########

@app.callback(
    Output("page-content", "children"), 
    [
        Input("url", "pathname")
    ])
def display_page(pathname):
    if pathname == "/salary":
        return first.layout
    elif pathname == "/jobs-and-location":
        return second.layout
    elif pathname == "/competences-and-skills":
        return third.layout
    # elif pathname == "/main":
    #     return (
    #         first.create_layout,
    #         second.create_layout,
    #         third.create_layout,

    #     )

# Output : le valeur que nous affichons 
# Input : Les valeurs que nous envoyons 


########## FIN DES FUNCTIONS  ##########

if __name__ == '__main__':
    app.run_server()