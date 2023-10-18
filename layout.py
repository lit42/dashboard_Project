import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

from data_processing import des_categories_by_level, des_categories_by_domain, load_data

df = load_data()
# Combine job categories for dropdown
all_jobs = list(des_categories_by_level.keys()) + list(des_categories_by_domain.keys())
unique_jobs = list(set(all_jobs))  # Remove duplicates


def get_layout():
    layout = html.Div([
        dcc.Location(id='url', refresh=False),
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Home", href="/")),
            ],
            brand="Job Insights Dashboard",
            brand_href="/",
            color="primary",
            dark=True,
            className="navbar fixed-top"
        ),
        dbc.Container(
            [
                # Search bar centered
                dbc.Row([
                    dbc.Col(width=2),  # Empty column for centering
                    dbc.Col(dcc.Dropdown(
                        id='job-search-dropdown',
                        options=[{'label': job, 'value': job} for job in unique_jobs],
                        placeholder="Select a Job",
                        className="py-0"
                    ), width=3, className="px-2"),
                    dbc.Col(dcc.Dropdown(
                        id='location-search-dropdown',
                        options=[{'label': location, 'value': location} for location in df['location'].unique()],
                        placeholder="Select a Location",
                        className="py-0"
                    ), width=3, className="px-2"),
                    dbc.Col(html.Button('Search', id='search-button', n_clicks=0,
                                        className="btn btn-primary rounded-pill py-0 align-middle"),
                            width=2, className="px-2"),
                    dbc.Col(width=2),  # Empty column for centering
                ], className="mb-4 justify-content-center align-items-center"),  # margin bottom for spacing

                dbc.Row([
                    dbc.Col([
                        dbc.Nav([
                            html.Div([
                                html.I(className="fas fa-chart-bar"),  # icon for Job Title Distributions
                                dcc.Link("Job Distributions", href="/job-title-distributions", id="link-job-title",
                                         className="sidebar-link"),
                            ], className="d-flex align-items-center mb-2"),
                            html.Div([
                                html.I(className="fas fa-hand-holding-usd"),  # icon for Salary Distributions
                                dcc.Link("Salary Distributions", href="/salary-distributions", id="link-salary",
                                         className="sidebar-link"),
                            ], className="d-flex align-items-center mb-2"),
                            html.Div([
                                html.I(className="fas fa-project-diagram"),  # Updated icon for Platform Distributions
                                dcc.Link("Platform Distributions", href="/platform-distributions", id="link-platform",
                                         className="sidebar-link"),
                            ], className="d-flex align-items-center mb-2"),
                            html.Div([
                                html.I(className="fas fa-map"),  # icon for USA Map Visualization
                                dcc.Link("Map Visualization", href="/usa-map", id="link-usa-map",
                                         className="sidebar-link"),
                            ], className="d-flex align-items-center mb-2"),
                            html.Div([
                                html.I(className="fas fa-brain"),  # icon for Skills Insights
                                dcc.Link("Top Skills", href="/skills-insights", id="link-skills",
                                         className="sidebar-link"),
                            ], className="d-flex align-items-center mb-2")
                        ], vertical=True, pills=True, className="sidebar"),
                    ], width=2, className="d-flex flex-column"),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.Div(id='page-content', className="page-content")
                            ])
                        ], className="mb-4"),
                    ], width=10),
                ]),
            ],
            fluid=True,
            className="main-container"
        ),
    ])

    return layout
