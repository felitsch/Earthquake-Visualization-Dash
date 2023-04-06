from plotly.graph_objs import *
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)
import plotly.io as pio
import plotly.graph_objects as go
from plotly.graph_objs import *
import plotly.tools as tls
import plotly.express as px
import dash
from dash import dcc
import plotly.express as px
import pandas as pd

import warnings
warnings.filterwarnings('ignore')



# # defining sunburst
# from data_processing import load_data, preprocess_data
# raw_data = load_data()
# tectonic_plates, data, merged_data, humanAct_sb = preprocess_data(raw_data)
# sunburst = px.sunburst(humanAct_sb, path=['Earthquake cause (main class)', 'Country'],
#                                 values='Number of recorded earthquakes', 
#                                 template="plotly_dark",
#                                 color='Rank',
#                                 color_continuous_scale='Purples_r',
#                                 color_continuous_midpoint=5,
#                                 custom_data=['Number of recorded earthquakes'])

# sunburst.update_traces(textinfo='label+percent parent', 
#                                 hovertemplate='%{label}<br>Number of recorded earthquakes: %{value}<extra></extra>' if '%{children}' else '',
#                                 branchvalues='total'
#                                 )

# sunburst.update_layout(hoverlabel=dict(bgcolor="white", font_size=12, font_family="Arial"))

  



def create_dashboard_layout():
    # Define countries of interest
    countries = ['CHINA', 'INDONESIA', 'IRAN', 'JAPAN', 'TURKEY', 'CHILE', 'USA', 'GREECE', 'PHILIPPINES', 'ITALY', 'PERU', 'PAKISTAN', 'INDIA', 'RUSSIA', 'PAPUA NEW GUINEA', 'MEXICO', 'COLOMBIA', 'TAIWAN', 'ALGERIA', 'GUATEMALA']
    country_options = [{'label': country.title(), 'value': country} for country in countries]

    # Create the layout
    layout = html.Div(
        style={'backgroundColor': '#212121'},
        children=[
            html.H1('Shaking Up the World: Exploring Natural and Human-Induced Earthquakes', style={'background-color': '#212121'}),
            dcc.Markdown(id='intro', children=''' Here will be an introductory sentence. 
                            '''),
            html.Div([
                dcc.RadioItems(
                    id='layer-select',
                    options=[
                        {'label': 'Tectonic Plates', 'value': 'plates'},
                        {'label': 'Earthquakes', 'value': 'quakes'},
                        {'label': 'Both', 'value': 'both'}
                    ],
                    value='both',
                    labelStyle={'display': 'inline-block', 'margin-right': '10px'}
                ),
                dcc.Graph(id='earthquake-graph'),
            ]),
            
            html.Div([
                #dcc.Markdown(id='markdown', style={'display': 'inline-block', 'width': '15%'}),
                dcc.Dropdown(
                    id='country-dropdown',
                    options=country_options,
                    value=countries[:5],
                    multi=True,
                    style={
                        'width': '70%',
                        'margin': '10px',
                        'background-color': '#212121',
                        'color': '#212121',
                        'border': '1px solid #ccc',
                        'border-radius': '5px', 
                        'padding': '5px' 
                    }
                ),
            ]),
            html.Div([
                dcc.Graph(id='depth-graph', style={'display': 'inline-block', 'width': '80%'}),
                dcc.Markdown(
                    id='markdown-1',
                    style={'display': 'inline-block', 'background-color': '#212121', 'width': '20%'},
                    children='''Here we will write something about
                            the causes of earthquakes in the
                            past 50-100 years.
                            '''
                )
            ]),
            html.Div([
                dcc.Graph(id='damage-graph', style={'display': 'inline-block', 'width': '33.3%'}),
                dcc.Graph(id='houses-graph', style={'display': 'inline-block', 'width': '33.3%'}),
                dcc.Graph(id='deaths-graph', style={'display': 'inline-block', 'width': '33.3%'}),
            ]),
            dcc.Graph(figure=sunburst),
            dcc.Markdown(id='conclusion', children=''' We're all well aware of climate change, but seeing how our collective actions impact even the geological processes, don't you think it's important to also consider this path alongside the others in order to address the challenges we face?
                            ''')
        ]
    )

    return layout






