import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import re
import dash_bootstrap_components as dbc

# Load the dataset
url = "https://raw.githubusercontent.com/lit42/test/main/1.5_dataset.csv"
df = pd.read_csv(url)

title_categories_by_level = {
    "Junior Data Analysts": ["junior", "jr", "entry level", "entry-level", "analyst i", "analyst 1"],
    "Senior Data Analysts": ["senior", "sr", "analyst ii", "analyst 2", "analyst iii", "analyst 3", "advanced"],
    "Lead Data Analysts": ["lead", "director", "manager", "leader", "principal", "cto"],
}

title_categories_by_domain = {
    "Remote Data Analysts": ["remote"],
    "Business Data Analysts": ["business", "commercial", "ecommerce", "commerce"],
    "BI Data Analysts": ["business intelligence", "bi"],
    "Data Scientists": ["science", "scientist", "research", "researcher", "scientific"],
    "Marketing Data Analysts": ["marketing", "market", "salesforce", "sales", "product", "production", "online retail",
                                "trade"],
    "Financial Data Analysts": ["financial", "finance"],
    "Data Engineers": ["engineer", "engineering"],
    "Healthcare Data Analysts": ["health", "healthcare", "medical", "clinical", "patient"],
    "Quality Data Analysts": ["quality"],
    "Supply Chain Data Analysts": ["supply chain", "logistics"],
    "GIS Data Analysts": ["gis", "geospatial", "geographic"],
    "Operations Data Analysts": ["operations"],
    "Technical Data Analysts": ["technical", "tech", "technology", "it"],
    "HR Data Analysts": ["hr", "human resources"],
    "Data Analysts": ["data analyst", "data analysis", "data analyse", "data analyze", "data analytics"],
    "Risk Analysts": ["risk", "risks"],
    "Google Analytics expert": ["google", "ga4", "ga"],
    "Qualitative Data Analysts": ["qualitative"],
    "Excel expert": ["excel"],
    "Data Governance Analyst": ["governance"]
}

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX], suppress_callback_exceptions=True)


# options = [{'label': category, 'value': category} for category in title_categories_by_level.keys()]


# Callback to update the job title distribution bar chart based on selected category
@app.callback(
    Output('job-title-level-bar-chart', 'figure'),
    [Input('job-title-category-level-dropdown', 'value')]
)
def update_job_title_bar_chart(selected_category):
    if selected_category:
        filtered_df = df[df['title_category_level'] == selected_category]
        title_counts = filtered_df['title'].value_counts()
        title_counts = title_counts.reset_index()
        title_counts.columns = ['Job Title', 'Count']
        title_counts.sort_values(by='Count', ascending=False, inplace=True)

        fig = px.bar(title_counts, x='Job Title', y='Count',
                     labels={'x': 'Job Title', 'y': 'Count'})
        fig.update_layout(title_text=f"Job Titles in Category: {selected_category}")
    else:
        title_category_counts = df['title_category_level'].value_counts()
        title_category_counts = title_category_counts.reset_index()
        title_category_counts.columns = ['Job Title Category', 'Count']
        title_category_counts.sort_values(by='Count', ascending=False, inplace=True)

        fig = px.bar(title_category_counts, x='Job Title Category', y='Count',
                     labels={'x': 'Job Title Category', 'y': 'Count'})
        fig.update_layout(title_text="Job Title Category Distribution")

    return fig


@app.callback(
    Output('job-title-domain-bar-chart', 'figure'),
    [Input('job-title-category-domain-dropdown', 'value')]
)
def update_job_title_bar_chart(selected_category):
    if selected_category:
        filtered_df = df[df['title_category_domain'] == selected_category]
    else:
        filtered_df = df

    title_category_counts = filtered_df['title_category_domain'].value_counts()
    title_category_counts = title_category_counts.reset_index()
    title_category_counts.columns = ['Job Title Category', 'Count']

    fig = px.bar(title_category_counts, x='Job Title Category', y='Count',
                 labels={'x': 'Job Title Category', 'y': 'Count'})
    fig.update_layout(title_text="Job Title Category Distribution")
    return fig


# Define the layout of the dashboard
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/")),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("MenuItem 1", href="/menu-item-1"),
                    dbc.DropdownMenuItem("MenuItem 2", href="/menu-item-2"),
                ],
                nav=True,
                in_navbar=True,
                label="Menu",
            ),
        ],
        brand="Job Listings Dashboard",
        brand_href="/",
        color="primary",
        dark=True,
    ),
    dbc.Row([
        dbc.Col([
            dbc.Nav([
                dcc.Link("Link 1", href="/page-1"),
                dcc.Link("Link 2", href="/page-2"),
            ], vertical=True),
        ], width=2),
        dbc.Col([
            html.Div(id='page-content')
        ], width=10),
    ]),
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == "/page-1":
        return html.Div([
            html.H2('Page 1 Content'),
            # Add content for Page 1 here
            html.H1("Job Listings Dashboard"),
            # Dropdown for selecting job title categories
            dcc.Dropdown(
                id='job-title-category-level-dropdown',
                options=[{'label': category, 'value': category} for category in title_categories_by_level.keys()],
                placeholder="Select Job Title Category"
            ),
            # Bar chart for job title distribution
            dcc.Graph(id='job-title-level-bar-chart'),
            # Button to show titles in "Other" category
            html.Button("Show Titles in Other Category", id='show-other-rows-button'),
            # Div to display titles in "Other" category
            html.Div(id='other-rows-titles')
        ])
    elif pathname == "/page-2":
        return html.Div([
            html.H2('Page 2 Content'),
            # Add content for Page 2 here
            html.H1("Job Listings Dashboard"),
            # Dropdown for selecting job title categories
            dcc.Dropdown(
                id='job-title-category-domain-dropdown',
                options=[{'label': category, 'value': category} for category in title_categories_by_domain.keys()],
                placeholder="Select Job Title Category"
            ),
            # Bar chart for job title distribution
            dcc.Graph(id='job-title-domain-bar-chart'),
            # Button to show titles in "Other" category
            html.Button("Show Titles in Other Category", id='show-other-rows-button'),
            # Div to display titles in "Other" category
            html.Div(id='other-rows-titles')
        ])
    elif pathname == "/menu-item-1":
        return html.Div([
            html.H2('Menu Item 1 Content'),
            # Add content for Menu Item 1 here
        ])
    elif pathname == "/menu-item-2":
        return html.Div([
            html.H2('Menu Item 2 Content'),
            # Add content for Menu Item 2 here
        ])
    else:
        return html.Div([
            html.H2('Home Page Content'),
        ])


if __name__ == '__main__':
    app.run_server(debug=True)
