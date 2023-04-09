# Shaking Up the World: Exploring Natural and Human-Induced Earthquakes - Dashboard

This repository contains the source code and data for the Earthquake Dashboard web application.
The Dashboard can be viewed under this [link](https://shaking-up-the-world-exploring-natural.onrender.com/).


## Files and Folders

- `assets`: This folder contains static files, such as images and stylesheets, used by the application.
- `premade_assets`: This folder contains additional static files for reference, but not actively used by the application.
- `Procfile`: Configuration file used for deploying the application to a hosting platform, such as render.
- `README.md`: This file provides an overview of the project and its components.
- `Tectonic.csv`: A dataset containing information about tectonic plates and their location.
- `The_Human_Induced_Earthquake_Database_v2023.03.27.xlsx`: A dataset containing information about human-induced earthquakes.
- `app.py`: The main file for the Dash web application. It initializes the app, sets the layout, and runs the server.
- `callbacks.py`: Contains callback functions for updating the application's components based on user interactions.
- `data_processing.py`: Contains functions for processing and cleaning the datasets used in the application.
- `generate_requirements.py`: A script to generate the `requirements.txt` file based on the project's dependencies.
- `layouts.py`: Contains the layout functions and components used to build the application's user interface.
- `plot_utils.py`: Contains utility functions for generating plots and visualizations used in the application.
- `requirements.txt`: Lists the Python packages required to run the application.
- `significant-earthquake-database.csv`: A dataset containing information about significant earthquakes.

To get started, follow the instructions below:

1. Clone the repository to your local machine.
2. Install the required packages using `pip install -r requirements.txt`.
3. Run the application using `python app.py`.
