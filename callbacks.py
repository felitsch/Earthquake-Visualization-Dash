import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)
import plotly.io as pio
import plotly.graph_objects as go
from chart_studio import plotly as py
import plotly.express as px
import dash
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

import warnings
warnings.filterwarnings('ignore')


# Imports from other files
from plot_utils import add_tectonic_plates_layer
from data_processing import load_data, preprocess_data
raw_data = load_data()
tectonic_plates, data, merged_data, humanAct_sb, humanAct_1 = preprocess_data(raw_data)



def register_callbacks(app):
    ################################################################
    # Callback for Earthquake Globe
    ################################################################
    @app.callback(
        Output('earthquake-graph', 'figure'),
        Input('layer-select', 'value')
    )
    def update_figure(selected_layer):
        new_fig = go.Figure()
        new_fig.update_traces(mode='none')
    
        if selected_layer == 'plates' or selected_layer == 'both':
            add_tectonic_plates_layer(new_fig, tectonic_plates)
        
        if selected_layer == 'quakes' or selected_layer == 'both':
            new_fig.add_trace(go.Scattergeo(
                lat=data['Latitude'],
                lon=data['Longitude'],
                text=data['Country'],
                customdata=list(zip(data['Focal Depth'], data['Year'], data['Magnitude'])),
                mode='markers',
                marker=dict(
                    size=(data['Magnitude']**3)/20,
                    color=data['Magnitude'],
                    colorscale='Inferno',
                    cmin=min(data['Magnitude']),
                    cmax=max(data['Magnitude']),
                    colorbar_title="Magnitude",
                    opacity=0.7
                ),
                hovertemplate='<b>%{text}</b><br>' +
                            'Focal Depth: %{customdata[0]:.2f}<br>' +
                            'Year: %{customdata[1]:}<br>' +
                            'Magnitude: %{customdata[2]:.2f}'
            ))
        
        new_fig.update_layout(
            title='Global Earthquake Overview',
            yaxis=dict(
                showgrid=False,
                showline=False,
                showticklabels=True,
                domain=[0, 0.85],
            ),
            yaxis2=dict(
                showgrid=False,
                showline=True,
                showticklabels=False,
                linecolor='rgba(102, 102, 102, 0.8)',
                linewidth=2,
                domain=[0, 0.85],
            ),
            xaxis=dict(
                zeroline=False,
                showline=False,
                showticklabels=True,
                showgrid=True,
                domain=[0.1, 0.9],
                rangeslider=dict(
                    visible=True,
                    bgcolor='white',  # set rangeslider color to white
                ),
                type='date',
                rangeselector=dict(
                    buttons=list([
                        dict(count=1, label='1y', step='year', stepmode='backward'),
                        dict(count=5, label='5y', step='year', stepmode='backward'),
                        dict(count=10, label='10y', step='year', stepmode='backward'),
                        dict(count=50, label='50y', step='year', stepmode='backward'),
                        dict(step='all')
                    ]),
                    bgcolor='white',  # set rangeselector border color to gray
                ),
            ),
            legend=dict(x=0.029, y=1.038, font_size=10), 
            margin=dict(l=100, r=60, t=60, b=50),
            xaxis_type='date',
            height=800,
            template='plotly_dark',  # set the template to plotly_dark
            geo=dict(
                projection_type='natural earth',
                showland=True,
                landcolor='RGB(180,180,180)',
                #showocean=True,
                #oceancolor='RGB(210,210,210)',
                showcountries=True,
                countrycolor='grey',
                showcoastlines=True,
                coastlinecolor='grey'
            ),
            hovermode='closest'
        )
        
        return new_fig


    ################################################################
    # Callback for bubble chart over time
    ################################################################
    @app.callback(
        Output('depth-graph', 'figure'),
        Input('country-dropdown', 'value')
    )
    def update_depth_graph(countries):
        data_specific = data[data['Country'].isin(countries)]
        
        # Create scatter plot
        data_depth = dict(type='scatter',
                    x=data_specific['Year'],
                    y=data_specific['Country'],
                    mode='markers',
                    text=data_specific['Country'],
                    marker=dict(size=data_specific['Magnitude']**2/2,
                                color=data_specific['Magnitude'],
                                colorbar=dict(title=dict(text='Magnitude')),
                                showscale=True,
                            ),
                    name='Scatter Visualization',
                    showlegend=False
                )

        layout_depth = dict(title=dict(text='Magnitude of Earthquakes by Country'),
                        xaxis=dict(title='Year'),
                        yaxis=dict(title='Country'),
                        template="plotly_dark"
                        )

        fig_depth = go.Figure(data=data_depth, layout=layout_depth)

        fig_depth.update_traces(hovertemplate='<b>%{y}</b><br>' +
                                            'Year: %{x}<br>' +
                                            'Magnitude: %{customdata:.2f}<br>' +
                                            'Focal Depth: %{marker.color:.2f}',
                                customdata=data_specific['Magnitude'],
                                hoverinfo='y')

        return fig_depth



    ########################################################################
    # Callback for three time series charts
    ########################################################################
    @app.callback(
        [Output('damage-graph', 'figure'),
         Output('houses-graph', 'figure'),
         Output('deaths-graph', 'figure')],
        [Input('depth-graph', 'hoverData'),
         Input('country-dropdown', 'value')]
    )
    def update_additional_graphs(hover_data, countries):
        if hover_data is None:
            country = countries[0]
        else:
            country = hover_data['points'][0]['y']

        data_specific = data[data['Country'] == country]

        # Create line charts for damages, houses, and deaths
        figures = []
        y_labels = ['Total Effects : Damages in million Dollars',
                    'Total Effects : Houses Damaged',
                    'Total Effects : Deaths']
        graph_ids = ['damage-graph', 'houses-graph', 'deaths-graph']

        for label, graph_id in zip(y_labels, graph_ids):
            # Sort data by year
            sorted_data = data_specific.sort_values(by='Year')

            # Calculate cumulative sum for each year
            cumulative_sum = sorted_data.groupby('Year')[label].sum().cumsum().reset_index()

            # Create line chart
            trace = go.Scatter(x=cumulative_sum['Year'],
                            y=cumulative_sum[label],
                            mode='lines+markers',
                            text=data_specific['Country'],
                            name=graph_id,
                            showlegend=False)

            layout = go.Layout(title=dict(text=f'Cumulative {label.split(":")[-1].strip()} over Time'),
                            xaxis=dict(title='Year'),
                            yaxis=dict(title=label),
                            template="plotly_dark")

            fig = go.Figure(data=[trace], layout=layout)
            figures.append(fig)

        return figures[0], figures[1], figures[2]
    





    @app.callback(
        [Output('sunburst', 'style'), Output('line_chart', 'style')],
        [Input('size-slider', 'value')]
    )
    def update_graphs_size(slider_value):
        sunburst_style = {
            'width': f'{slider_value}%', 'height': '60vh',
            'display': 'inline-block', 'border-radius': '5px'
        }
        line_chart_style = {
            'width': f'calc({100 - slider_value}% - 20px)', 'height': '60vh',
            'display': 'inline-block', 'border-radius': '5px', 'margin-left': '20px'
        }
        return sunburst_style, line_chart_style

    











