import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the dataset
url = "https://raw.githubusercontent.com/lit42/test/main/1.4_dataset.csv"
df = pd.read_csv(url)

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1("Job Listings Dashboard"),

    # Dropdown for selecting job titles
    dcc.Dropdown(
        id='job-title-dropdown',
        options=[{'label': title, 'value': title} for title in df['title'].unique()],
        multi=True,
        placeholder="Select Job Titles"
    ),

    # Bar chart for job title distribution
    dcc.Graph(id='job-title-bar-chart'),

    # Other visualizations and components can be added here
])


# Callback to update the job title distribution bar chart
@app.callback(
    Output('job-title-bar-chart', 'figure'),
    [Input('job-title-dropdown', 'value')]
)
def update_job_title_bar_chart(selected_titles):
    if selected_titles:
        filtered_df = df[df['title'].isin(selected_titles)]
    else:
        filtered_df = df

    title_counts = filtered_df['title'].value_counts()
    fig = px.bar(title_counts, x=title_counts.index, y=title_counts.values, labels={'x': 'Job Title', 'y': 'Count'})
    fig.update_layout(title_text="Job Title Distribution")
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
