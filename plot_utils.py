import plotly.graph_objects as go

def add_tectonic_plates_layer(fig, tectonic_plates):
  """
  Adds a layer with tectonic plates to a plotly figure object.
  The tectonic_plates argument should be a pandas DataFrame containing
  columns for 'plate', 'lat', 'lon', and 'Plate Name'.
  """
  for plate_name in tectonic_plates['Plate Name'].unique():
    plate_vals = tectonic_plates[tectonic_plates['Plate Name'] == plate_name]
    fig.add_trace(go.Scattergeo(
    lon=plate_vals['lon'].values,
    lat=plate_vals['lat'].values,
    marker=dict(
        size=2.5,  # set marker size to 2
        color='grey',
        opacity=0.7
    ),
    name=plate_name,
    hovertemplate=None,
    showlegend=False
    )) 
