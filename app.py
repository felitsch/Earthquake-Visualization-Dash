import dash
from chart_studio import plotly as py
from plotly.graph_objs import *
import plotly.express as px
import dash
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')



# Imports from other files
import layouts
import callbacks
from data_processing import load_data, preprocess_data
raw_data = load_data()
tectonic_plates, data, human, merged_data = preprocess_data(raw_data)




# Import the CSS stylesheet
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

external_stylesheets = [
    # Dash CSS
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    # Loading screen CSS
    'https://codepen.io/chriddyp/pen/brPBPO.css']










app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# app = dash.Dash(__name__)

# Link zu style.css hinzufügen
#app.css.append_css({"external_url": "/assets/style.css"})


# Add layout
app.layout = layouts.create_dashboard_layout()

# Register callbacks
callbacks.register_callbacks(app)

# Run app
if __name__ == '__main__':
    app.run_server(debug=True)
