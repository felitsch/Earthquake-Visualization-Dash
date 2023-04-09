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

sunburst.update_layout(title='Share of Human Induced Earthquakes by Cause and Country', hoverlabel=dict(bgcolor="white", font_size=12, font_family="Arial"))


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

########################################################################
# defining line chcart
########################################################################
# Create a line chart
line_chart = px.line(humanAct_1, x='Year', y='Number of recorded earthquakes', color='Earthquake cause (main class)', 
                     template="plotly_dark")

# Customizing the axis labels and adding a title
line_chart.update_xaxes(title='Year')
line_chart.update_yaxes(title='Number of recorded human-induced earthquakes')
line_chart.update_layout(title='Human-induced Earthquakes by Year and Cause')





########################################################################
# Create Dashboard layout
########################################################################

github_link = "https://github.com/felitsch/Earthquake-Visualization-Dash"





def create_dashboard_layout():
    # Define countries of interest
    countries = ['CHINA', 'INDONESIA', 'IRAN', 'JAPAN', 'TURKEY', 'CHILE', 'USA', 'GREECE', 'PHILIPPINES', 'ITALY', 'PERU', 'PAKISTAN', 'INDIA', 'RUSSIA', 'PAPUA NEW GUINEA', 'MEXICO', 'COLOMBIA', 'TAIWAN', 'ALGERIA', 'GUATEMALA']
    country_options = [{'label': country.title(), 'value': country} for country in countries]

    # Create the layout
    layout = html.Div(
        style={'backgroundColor': '#212121', 'border-radius': '5px'},
        children=[
            # Header
            html.H1('Shaking Up the World: Exploring Natural and Human-Induced Earthquakes', style={'background-color': '#212121', 'color': 'white', 'text-align': 'center', 'font-weight': 'bold'}),

            # Introduction
            dcc.Markdown(
                id='intro',
                children='''This dashboard provides a panoramic view of seismic activities worldwide, juxtaposed with the multifarious facets of human impact on our planet. From the disquieting depths of geological disturbances like tectonic plates, to the disruptive influence of human activities, the dashboard encapsulates an all-encompassing perspective on the intricacies of our planet's seismic history.''',
                style={
                    'font-size': '50px',
                    'font-weight': 'bold',
                    'text-align': 'center',
                    'padding': '0 12.5%',
                    'border-bottom': '1px solid #ccc',
                    'border-radius': '5px',
                    'display': 'block',
                    'width': '75%',
                    'margin-bottom': '10px',
                    'margin': '0 auto',  # Center the block element
                }
            ),

            # Separator
            html.Div(style={'border-bottom': '1px solid #ccc', 'margin-bottom': '10px'}),

            html.H3('Overview', style={'background-color': '#212121', 'color': 'white', 'text-align': 'center', 'font-weight': 'bold'}),


            # Layer selection and earthquake graph
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
                html.P("Choose between Tectonic Plates and/or Earthquakes.", style={'font-size': '14px', 'font-style': 'italic'}),
                dcc.Graph(id='earthquake-graph', style={'border-radius': '5px'})
                

            ], style={'border-bottom': '1px solid #ccc', 'border-radius': '5px'}),
            dcc.Markdown('', style={'border-bottom': '1px solid #ccc', 'margin-bottom': '10px', 'padding-top': '10px'}),
            
            # Country dropdown, summary text, and additional graphs
            html.Div([
                html.H3('Effects', style={'background-color': '#212121', 'color': 'white', 'text-align': 'center', 'font-weight': 'bold'}),
                    # Markdown text
                html.Div([
                    dcc.Markdown(
                        id='num_incr',
                        children='''The recorded earthquakes are increasingly becoming a cause for concern, resulting in significant losses in terms of human lives, property, and infrastructure. As such, it is imperative to address the underlying factors that contribute to this phenomenon, and identify measures to mitigate their impact.''',
                        style={
                            'font-size': '50px',
                            'font-weight': 'bold',
                            'text-align': 'center',
                            'border-bottom': '1px solid #ccc',
                            'display': 'block',
                            'width': '70%',
                            'padding': '0 15%',  # 15% padding on left and right
                            'margin': '0 auto',  # Center the block element
                        }
                    ),
                ], style={'width': '100%', 'display': 'inline-block'}),

                # Country dropdown
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
                ]),
                
                html.P("Hover over the country bubbles to display more detailed information about the respective country in the section below.", style={'font-size': '14px', 'font-style': 'italic'}),



            # Depth graph and earthquakes-by-year graph
            html.Div([
                dcc.Graph(id='depth-graph', style={'display': 'inline-block', 'width': '70%', 'border-radius': '5px'}),
                dcc.Graph(id='earthquakes-by-year', figure=num_earthquakes, style={'display': 'inline-block', 'width': '30%', 'border-radius': '5px'})
            ], style={'display': 'flex'}),


            # Damage, houses, and deaths graphs with hovering text
            html.Div([
                dcc.Graph(id='damage-graph', style={'display': 'inline-block', 'width': '23.3%', 'border-radius': '5px'}),
                dcc.Graph(id='houses-graph', style={'display': 'inline-block', 'width': '23.3%', 'border-radius': '5px'}),
                dcc.Graph(id='deaths-graph', style={'display': 'inline-block', 'width': '23.3%', 'border-radius': '5px'}),
                html.Div(
                    dcc.Markdown(id='hovering', children='''Upon examining the damages and deaths, the relationship between damages and individual earthquake events becomes apparent in the three visualizations on the left due to the abrupt fluctuations in the line graphs. This underscores the potential hazards and risks linked to such seismic occurrences.''',
                                style={'font-size': '50px', 'font-weight': 'bold', 'text-align': 'center', 'border-radius': '5px'}),
                    style={'display': 'inline-block', 'width': '30%', 'padding': '20px', 'border-left': '1px solid #ccc'}
                )
            ], style={'border-bottom': '1px solid #ccc','display': 'flex', 'align-items': 'center', 'border-radius': '5px'}),
            ]),
            
            # Separator
            dcc.Markdown('', style={'border-bottom': '1px solid #ccc', 'margin-bottom': '10px', 'padding-top': '10px'}),

            # Human Induced text
            html.H2('Humanity as Cause', style={'background-color': '#212121', 'color': 'white', 'text-align': 'center', 'font-weight': 'bold'}),
            dcc.Markdown(
                id='human_induced',
                children='''The following visualizations focus solely on earthquakes induced by human activities through various projects. They aim to depict the correlation between human activities and their seismic repercussions. By incorporating the respective countries involved, the graphic provides a level of accountability for these seismic consequences. A portion of the increase in recorded earthquakes since the 1950s can be attributed to human activity.''',
                style={
                    'font-size': '50px',
                    'font-weight': 'bold',
                    'text-align': 'center',
                    'border-bottom': '1px solid #ccc',
                    'display': 'block',
                    'width': '70%',
                    'padding': '0 15%',  # 15% padding on left and right
                    'margin': '0 auto',  # Center the block element
                    }
            ),
            


            html.Div([dcc.Graph(id='sunburst', figure=sunburst), dcc.Graph(id='line_chart', figure=line_chart),], style={
                'display': 'flex',
                'flex-direction': 'row',
                'border-right': '1px solid gray',
                'margin-right': '-1px'
            }),


            html.Div([
                html.H6('Slider', style={'background-color': '#212121', 'color': 'white', 'text-align': 'center'}),
                dcc.Slider(id='size-slider', min=0, max=100, step=1, value=50, marks={i: str(i) for i in range(0, 101, 10)}),
                html.P("Adjust the slider to obtain a more comprehensive view of the corresponding visualization.", style={'font-size': '14px', 'font-style': 'italic'}),
            ], style={'width': '100%', 'margin-top': '20px', 'border-bottom': '1px solid #ccc'}),




            # Conclusion
            html.H2('Conclusion', style={'background-color': '#212121', 'color': 'white', 'text-align': 'center', 'font-weight': 'bold'}),
            dcc.Markdown(id='conclusion', 
                         children=''' We're all well aware of climate change, but seeing how our collective actions impact even the geological processes, don't you think it's important to also consider this path alongside the others in order to address the challenges we face?''', 
                         style={
                            'font-size': '50px',
                            'font-weight': 'bold',
                            'text-align': 'center',
                            'border-bottom': '1px solid #ccc',
                            'display': 'block',
                            'width': '70%',
                            'padding': '0 15%',  # 15% padding on left and right
                            'margin': '0 auto',  # Center the block element
                            }
                        ),
                        
                        # Padding at the bottom
            html.Div(style={'padding-bottom': '100px', 'border-radius': '5px'}),

            html.Div([
                html.Br(),
                html.A("Link to GitHub repository", href=github_link)
            ]),

            # Separators
            dcc.Markdown('', style={'border-bottom': '1px solid #ccc', 'margin-bottom': '10px', 'padding-top': '10px'}),
            dcc.Markdown('', style={'border-bottom': '1px solid #ccc', 'margin-bottom': '10px', 'padding-top': '10px'}),
            html.Div(style={'padding-bottom': '30px', 'border-radius': '5px', 'border-bottom': '1px solid #ccc',}),

        ]
    )

    return layout





