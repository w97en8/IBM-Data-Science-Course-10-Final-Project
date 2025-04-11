import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Define dropdown options (You should dynamically load this based on your data)
dropdown_options = [{'label': 'All Sites', 'value': 'ALL'}] + [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()]

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # Dropdown for Launch Site selection
    dcc.Dropdown(id='site-dropdown',
                 options=dropdown_options,  # Dynamic dropdown options
                 value='ALL',  # Default value to show all sites
                 placeholder="Select Launch Site",
                 searchable=True),
    html.Br(),
    
    # Pie chart for success vs failure (for all sites or specific site)
    html.Div(dcc.Graph(id='success-pie-chart')),
    
    html.Br(),
    html.P("Payload range (Kg):"),
    
    # Payload range slider
    dcc.RangeSlider(id='payload-slider',
                    min=0,  # Min value for payload
                    max=10000,  # Max value for payload
                    step=1000,  # Step for slider
                    marks={i: f'{i} kg' for i in range(0, 10001, 1000)},  # Payload range marks
                    value=[min_payload, max_payload]),  # Default value: min to max payload
    
    # Scatter plot for payload vs success correlation
    html.Div(dcc.Graph(id='success-payload-scatter-chart'))
])

# TASK 2 Callback: Pie chart for success vs failure by site
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        # Filter successful launches
        all_launch_sites_df = spacex_df[spacex_df['class'] == 1]
        fig = px.pie(all_launch_sites_df, values='class',
                     names='Launch Site',
                     title='Total Successful Launches Count for all Sites')
    else:
        # Filter by specific site
        selected_site_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(selected_site_df, names='class', title='Outcomes for Selected Site')
    return fig

# TASK 4 Callback: Scatter plot for correlation between payload and success
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [
        Input(component_id='site-dropdown', component_property='value'),
        Input(component_id="payload-slider", component_property="value")
    ]
)
def get_scatter_chart(entered_site, payload_range):
    low, high = payload_range
    # Filter the dataframe based on payload range
    filtered_spacex_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & 
                                   (spacex_df['Payload Mass (kg)'] <= high)]
    
    if entered_site == 'ALL':
        # Scatter for all sites
        fig = px.scatter(filtered_spacex_df, x='Payload Mass (kg)', y='class',
                         color="Booster Version Category",
                         title='Correlation Between Payload and Launch Success for All Sites')
    else:
        # Filter for specific site
        selected_site_df = filtered_spacex_df[filtered_spacex_df['Launch Site'] == entered_site]
        fig = px.scatter(selected_site_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',
                         title="Correlation Between Payload and Launch Success for Specific Site")
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run()