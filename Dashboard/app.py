import dash
import flask 
import dash_bootstrap_components as dbc

path_stylesheets = ['./assets/template.css']
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, path_stylesheets])
server = app.server
app.config.suppress_callback_exceptions = True