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
from data_processing import load_data, preprocess_data
raw_data = load_data()
tectonic_plates, data, merged_data, humanAct_sb, humanAct_1 = preprocess_data(raw_data)



################################################################
# defining sunburst
################################################################
sunburst = px.sunburst(humanAct_sb, path=['Earthquake cause (main class)', 'Country'],
                                values='Number of recorded earthquakes', 
                                template="plotly_dark",
                                color='Rank',
                                color_continuous_scale='Purples_r',
                                color_continuous_midpoint=5,
                                custom_data=['Number of recorded earthquakes'])

sunburst.update_traces(textinfo='label+percent parent', 
                                hovertemplate='%{label}<br>Number of recorded earthquakes: %{value}<extra></extra>' if '%{children}' else '',
                                branchvalues='total'
                                )

sunburst.update_layout(hoverlabel=dict(bgcolor="white", font_size=12, font_family="Arial"))


################################################################
# defining number of earthquakes histogram
################################################################
num_earthquakes = px.histogram(data[data.Year >= 0], x="Year", nbins=len(data[data.Year >= 0].Year.unique()))

# Customize the layout of the plot
num_earthquakes.update_layout(
    title={'text': 'Recorded Earthquakes', 'x':0.5, 'xanchor':'center'},
    xaxis_title='Year',
    yaxis_title='Count',
    # font=dict(
    #     family='Arial',
    #     size=14,
    #     color='white'
    # ),
    plot_bgcolor='black',
    hovermode='closest',
    showlegend=False,
    template="plotly_dark"
)


################################################################
# defining stacked bar chart
################################################################

# Create a stacked bar chart
stacked_bar = px.bar(humanAct_1, x='Year', y='Number of recorded earthquakes', color='Earthquake cause (main class)', 
                     template="plotly_dark", barmode='stack')

# Customizing the axis labels and adding a title
stacked_bar.update_xaxes(title='Year')
stacked_bar.update_yaxes(title='Cumulative Number of recorded human induced earthquakes')
stacked_bar.update_layout(title='Human-induced Earthquakes by Year and Cause (Stacked Bar Chart)')






  



# def create_dashboard_layout():
#     # Define countries of interest
#     countries = ['CHINA', 'INDONESIA', 'IRAN', 'JAPAN', 'TURKEY', 'CHILE', 'USA', 'GREECE', 'PHILIPPINES', 'ITALY', 'PERU', 'PAKISTAN', 'INDIA', 'RUSSIA', 'PAPUA NEW GUINEA', 'MEXICO', 'COLOMBIA', 'TAIWAN', 'ALGERIA', 'GUATEMALA']
#     country_options = [{'label': country.title(), 'value': country} for country in countries]

#     # Create the layout
#     layout = html.Div(
#         style={'backgroundColor': '#212121'},
#         children=[
#             html.H1('Shaking Up the World: Exploring Natural and Human-Induced Earthquakes', style={'background-color': '#212121', 'font-weight': 'bold'}),
#             dcc.Markdown(id='intro',
#                         children='''This dashboard provides a panoramic view of seismic activities worldwide, juxtaposed with the multifarious facets of human impact on our planet. From the disquieting depths of geological disturbances like tectonic plates, to the disruptive influence of human activities, the dashboard encapsulates an all-encompassing perspective on the intricacies of our planet's seismic history.''',
#                         style={
#                             'font-size': '24px',
#                             'font-weight': 'bold',
#                             'text-align': 'center',
#                             'padding': '0 50px',  # 50px padding on left and right
#                             'border-bottom': '1px solid #ccc'
#                             }
#                         ),
#             html.Div([
#                 dcc.RadioItems(
#                     id='layer-select',
#                     options=[
#                         {'label': 'Tectonic Plates', 'value': 'plates'},
#                         {'label': 'Earthquakes', 'value': 'quakes'},
#                         {'label': 'Both', 'value': 'both'}
#                     ],
#                     value='both',
#                     labelStyle={'display': 'inline-block', 'margin-right': '10px'}
#                 ),
#                     dcc.Graph(id='earthquake-graph'),
#             ], style={'border-bottom': '1px solid #ccc'}),
        
#             html.Div([
#                 html.Div([
#                     dcc.Dropdown(
#                         id='country-dropdown',
#                         options=country_options,
#                         value=countries[:5],
#                         multi=True,
#                         style={
#                             'width': '90%',
#                             'margin': '10px',
#                             'background-color': '#212121',
#                             'color': '#212121',
#                             'border': '1px solid #ccc',
#                             'padding': '3px',
#                             'border-radius': '5px' 
#                         }
#                     ),
#                 ], style={'width': '50%', 'display': 'inline-block'}),
#                 html.Div([
#                     dcc.Markdown(id='num_incr', children='''The recorded earthquakes are increasingly becoming a cause for concern, resulting in significant losses in terms of human lives, property, and infrastructure. As such, it is imperative to address the underlying factors that contribute to this phenomenon, and identify measures to mitigate their impact.''', 
#                                 style={'font-size': '24px', 'font-weight': 'bold', 'text-align': 'center', 'padding': '0 50px', 'border-bottom': '1px solid #ccc', 'border-left': '1px solid #ccc'})
#                 ], style={'width': '50%', 'display': 'inline-block'})
#             ]),

#             html.Div([
#                 dcc.Graph(id='depth-graph', style={'display': 'inline-block', 'width': '70%'}),
#                 dcc.Graph(id='earthquakes-by-year', figure=num_earthquakes, style={'display': 'inline-block', 'width': '30%'} )
#             ]),

#             html.Div([
#                 dcc.Graph(id='damage-graph', style={'display': 'inline-block', 'width': '26.6%', 'border-bottom': '1px solid #ccc'}),
#                 dcc.Graph(id='houses-graph', style={'display': 'inline-block', 'width': '26.6%', 'border-bottom': '1px solid #ccc'}),
#                 dcc.Graph(id='deaths-graph', style={'display': 'inline-block', 'width': '26.6%', 'border-bottom': '1px solid #ccc'}),
#                 html.Div([
#                     dcc.Markdown(id='num_incr', children='''By hovering over the countries in the "Magnitude of Earthquakes by Country" visualization, the dependence of damages on individual earthquake events becomes evident in the three visualizations on the left. This highlights the potential dangers and risks associated with such seismic activities.''',
#                                 style={'font-size': '24px', 'font-weight': 'bold', 'text-align': 'center'})
#                 ], style={'display': 'inline-block', 'width': '20%'})
#             ], style={'display': 'flex', 'align-items': 'center', 'border-bottom': '1px solid #ccc'}),

#             html.Div([dcc.Graph(figure=sunburst)], style={'width': '50%', 'display': 'inline-block'}),
#             dcc.Graph(figure=stacked_bar),
            

#             dcc.Markdown(id='conclusion', 
#                          children=''' We're all well aware of climate change, but seeing how our collective actions impact even the geological processes, don't you think it's important to also consider this path alongside the others in order to address the challenges we face?''', 
#                          style={'font-size': '24px', 'font-weight': 'bold', 'text-align': 'center'}
#                         ),
#             html.Div(style={'padding-bottom': '100px'})  # Add padding to the bottom of the last element
#         ]
#     )

#     return layout




def create_dashboard_layout():
    # Define countries of interest
    countries = ['CHINA', 'INDONESIA', 'IRAN', 'JAPAN', 'TURKEY', 'CHILE', 'USA', 'GREECE', 'PHILIPPINES', 'ITALY', 'PERU', 'PAKISTAN', 'INDIA', 'RUSSIA', 'PAPUA NEW GUINEA', 'MEXICO', 'COLOMBIA', 'TAIWAN', 'ALGERIA', 'GUATEMALA']
    country_options = [{'label': country.title(), 'value': country} for country in countries]

    # Create the layout
    layout = html.Div(
        style={'backgroundColor': '#212121', 'border-radius': '5px'},
        children=[
            html.H1('Shaking Up the World: Exploring Natural and Human-Induced Earthquakes', style={'background-color': '#212121', 'font-weight': 'bold'}),
            dcc.Markdown(id='intro',
                        children='''This dashboard provides a panoramic view of seismic activities worldwide, juxtaposed with the multifarious facets of human impact on our planet. From the disquieting depths of geological disturbances like tectonic plates, to the disruptive influence of human activities, the dashboard encapsulates an all-encompassing perspective on the intricacies of our planet's seismic history.''',
                        style={
                            'font-size': '24px',
                            'font-weight': 'bold',
                            'text-align': 'center',
                            'padding': '0 50px',  # 50px padding on left and right
                            'border-bottom': '1px solid #ccc',
                            'border-radius': '5px'
                            }
                        ),
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
                    dcc.Graph(id='earthquake-graph', style={'border-radius': '5px'}),
            ], style={'border-bottom': '1px solid #ccc', 'border-radius': '5px'}),
        
            html.Div([
                html.Div([
                    dcc.Dropdown(
                        id='country-dropdown',
                        options=country_options,
                        value=countries[:5],
                        multi=True,
                        style={
                            'width': '90%',
                            'margin': '10px',
                            'background-color': '#212121',
                            'color': '#212121',
                            'border': '1px solid #ccc',
                            'padding': '3px',
                            'border-radius': '5px' 
                        }
                    ),
                ], style={'width': '50%', 'display': 'inline-block'}),
                html.Div([
                    dcc.Markdown(id='num_incr', children='''The recorded earthquakes are increasingly becoming a cause for concern, resulting in significant losses in terms of human lives, property, and infrastructure. As such, it is imperative to address the underlying factors that contribute to this phenomenon, and identify measures to mitigate their impact.''', 
                                style={'font-size': '24px', 'font-weight': 'bold', 'text-align': 'center', 'padding': '0 50px', 'border-bottom': '1px solid #ccc', 'border-left': '1px solid #ccc'}),
                ], style={'width': '50%', 'display': 'inline-block'})
            ]),

            html.Div([
                dcc.Graph(id='depth-graph', style={'display': 'inline-block', 'width': '70%', 'border-radius': '5px'}),
                dcc.Graph(id='earthquakes-by-year', figure=num_earthquakes, style={'display': 'inline-block', 'width': '30%', 'border-radius': '5px'})
            ]),

            html.Div([
                dcc.Graph(id='damage-graph', style={'display': 'inline-block', 'width': '26.6%', 'border-bottom': '1px solid #ccc', 'border-radius': '5px'}),
                dcc.Graph(id='houses-graph', style={'display': 'inline-block', 'width': '26.6%', 'border-bottom': '1px solid #ccc', 'border-radius': '5px'}),
                dcc.Graph(id='deaths-graph', style={'display': 'inline-block', 'width': '26.6%', 'border-bottom': '1px solid #ccc', 'border-radius': '5px'}),
                html.Div([
                    dcc.Markdown(id='num_incr', children='''By hovering over the countries in the "Magnitude of Earthquakes by Country" visualization, the dependence of damages on individual earthquake events becomes evident in the three visualizations on the left. This highlights the potential dangers and risks associated with such seismic activities.''',
                                style={'font-size': '24px', 'font-weight': 'bold', 'text-align': 'center', 'border-radius': '5px'})
                ], style={'display': 'inline-block', 'width': '20%'})
            ], style={'display': 'flex', 'align-items': 'center', 'border-bottom': '1px solid #ccc', 'border-radius': '5px'}),

            html.Div([dcc.Graph(figure=sunburst)], style={'width': '50%', 'display': 'inline-block', 'border-radius': '5px'}),
            dcc.Graph(figure=stacked_bar, style={'border-radius': '5px'}),
            

            dcc.Markdown(id='conclusion', 
                         children=''' We're all well aware of climate change, but seeing how our collective actions impact even the geological processes, don't you think it's important to also consider this path alongside the others in order to address the challenges we face?''', 
                         style={'font-size': '24px', 'font-weight': 'bold', 'text-align': 'center', 'border-radius': '5px'}
                        ),
            html.Div(style={'padding-bottom': '100px', 'border-radius': '5px'})  # Add padding to the bottom of the last element
        ]
    )

    return layout








