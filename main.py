import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import re

# Load the dataset
url = "https://raw.githubusercontent.com/lit42/test/main/1.4_dataset.csv"
df = pd.read_csv(url)

# Define the keyword-based job title categories
title_categories = {
    "Junior Data Analysts": ["junior", "jr", "entry level", "entry-level", "analyst i", "analyst 1"],
    "Senior Data Analysts": ["senior", "sr", "analyst ii", "analyst 2", "analyst iii", "analyst 3", "advanced"],
    "Lead Data Analysts": ["lead", "director", "manager", "leader", "principal", "cto"],
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
    # Add more categories and keywords as needed
}


# Function to categorize job titles based on keywords
# def categorize_job_title(title):
#     title_lower = title.lower()
#     for category, keywords in title_categories.items():
#         for keyword in keywords:
#             if re.search(r'\b' + keyword + r'\b', title_lower):
#                 if keyword == "data analyst" and title_lower != "data analyst":
#                     continue  # Skip if it's not exactly "data analyst"
#                 return category
#     return "Other"
def categorize_job_title(title):
    title_lower = title.lower()
    for category, keywords in title_categories.items():
        for keyword in keywords:
            if re.search(r'\b' + keyword + r'\b', title_lower):
                return category
    return "Other"


# Apply the categorization function to the DataFrame
df['title_category'] = df['title'].apply(categorize_job_title)

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1("Job Listings Dashboard"),

    # Dropdown for selecting job title categories
    dcc.Dropdown(
        id='job-title-category-dropdown',
        options=[{'label': category, 'value': category} for category in title_categories.keys()],
        placeholder="Select Job Title Category"
    ),

    # Bar chart for job title distribution
    dcc.Graph(id='job-title-bar-chart'),

    # Button to show rows in the "Other" category
    html.Button("Show 'Other' Category Rows", id='show-other-rows-button'),

    # DataTable to display rows in the "Other" category
    html.Div(id='other-rows-table')
])


# Callback to update the job title distribution bar chart based on selected category
@app.callback(
    Output('job-title-bar-chart', 'figure'),
    [Input('job-title-category-dropdown', 'value')]
)
def update_job_title_bar_chart(selected_category):
    if selected_category:
        filtered_df = df[df['title_category'] == selected_category]
    else:
        filtered_df = df

    title_category_counts = filtered_df['title_category'].value_counts()
    title_category_counts = title_category_counts.reset_index()
    title_category_counts.columns = ['Job Title Category', 'Count']

    fig = px.bar(title_category_counts, x='Job Title Category', y='Count',
                 labels={'x': 'Job Title Category', 'y': 'Count'})
    fig.update_layout(title_text="Job Title Category Distribution")
    return fig


# Callback to display titles in the "Other" category
@app.callback(
    Output('other-rows-titles', 'children'),
    [Input('show-other-rows-button', 'n_clicks')]
)
def show_other_category_titles(n_clicks):
    if n_clicks:
        other_titles = df[df['title_category'] == 'Other']['title']

        titles = html.Div([
            html.P(title) for title in other_titles
        ])
        return titles
    return ""


# Define the layout of the dashboard
app.layout = html.Div([
    html.H1("Job Listings Dashboard"),

    html.H1("Job Listings Dashboard"),

    # Dropdown for selecting job title categories
    dcc.Dropdown(
        id='job-title-category-dropdown',
        options=[{'label': category, 'value': category} for category in title_categories.keys()],
        placeholder="Select Job Title Category"
    ),

    # Bar chart for job title distribution
    dcc.Graph(id='job-title-bar-chart'),

    # Button to show titles in "Other" category
    html.Button("Show Titles in Other Category", id='show-other-rows-button'),

    # Div to display titles in "Other" category
    html.Div(id='other-rows-titles')
])

if __name__ == '__main__':
    app.run_server(debug=True)
