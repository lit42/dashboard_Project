import dash
import dash_bootstrap_components as dbc
import pandas as pd
from visualizations import (create_histograms, create_platform_pie, create_job_title_bar_chart, generate_choropleth_map,
                            create_skill_table, create_salary_bar_chart)
from data_processing import load_data, process_data_optimized, load_skill_dataset, parse_skills
from layout import get_layout
from dash.dependencies import Input, Output, State
from data_processing import des_categories_by_level, des_categories_by_domain
from dash import dcc, html
import plotly.express as px
from dash.exceptions import PreventUpdate

# Initialize the Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.LUX,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css"
    ],
    suppress_callback_exceptions=True
)

# Load and process data
df = load_data()
filtered_df = df[df['salary'] != 'Not specified']
df_processed = process_data_optimized(filtered_df.copy())
# Combine job categories for dropdown
all_jobs = list(des_categories_by_level.keys()) + list(des_categories_by_domain.keys())
unique_jobs = list(set(all_jobs))  # Remove duplicates

# Load the dataset on app initialization
top_hard_skills_by_domain = load_skill_dataset('skills_datasets/top_hard_skills_by_domain.csv')
top_hard_skills_by_level = load_skill_dataset('skills_datasets/top_hard_skills_by_level.csv')
top_soft_skills_by_domain = load_skill_dataset('skills_datasets/top_soft_skills_by_domain.csv')
top_soft_skills_by_level = load_skill_dataset('skills_datasets/top_soft_skills_by_level.csv')
hard_skill_domain_tables = create_skill_table(top_hard_skills_by_domain, "Hard Skill", "Domain")
hard_skill_level_tables = create_skill_table(top_hard_skills_by_level, "Hard Skill", "Level")
soft_skill_domain_tables = create_skill_table(top_soft_skills_by_domain, "Soft Skill", "Domain")
soft_skill_level_tables = create_skill_table(top_soft_skills_by_level, "Soft Skill", "Level")

# Home page
top_10_hard_skills = pd.read_csv('skills_datasets/top_10_hard_skills.csv')
top_10_soft_skills = pd.read_csv('skills_datasets/top_10_soft_skills.csv')

# Create visualizations
fig, fig_domain = create_histograms(df_processed)
fig_platform = create_platform_pie(df)

fig_platform.update_layout(
    paper_bgcolor="#282c31",
    plot_bgcolor="#282c31",
    font=dict(color="#e9ecef"),
)
choropleth_map = generate_choropleth_map(df)


# Callback to update the active link based on the current pathname
@app.callback(
    [
        Output("link-job-title", "className"),
        Output("link-salary", "className"),
        Output("link-platform", "className"),
        Output("link-usa-map", "className"),
        Output("link-skills", "className")
    ],
    [Input('url', 'pathname')]
)
def update_active_link(pathname):
    base_class = "sidebar-link"
    active_class = "sidebar-link active"

    if pathname == "/job-title-distributions":
        return [active_class, base_class, base_class, base_class, base_class]
    elif pathname == "/salary-distributions":
        return [base_class, active_class, base_class, base_class, base_class]
    elif pathname == "/platform-distributions":
        return [base_class, base_class, active_class, base_class, base_class]
    elif pathname == "/usa-map":
        return [base_class, base_class, base_class, active_class, base_class]
    elif pathname == "/skills-insights":
        return [base_class, base_class, base_class, base_class, active_class]
    else:
        return [base_class, base_class, base_class, base_class, base_class]


@app.callback(
    Output('job-title-level-bar-chart', 'figure'),
    [Input('job-title-category-level-dropdown', 'value')]
)
def update_job_title_level_bar_chart(selected_category):
    return create_job_title_bar_chart(df, 'des_category_level', selected_category, des_categories_by_level)


@app.callback(
    Output('job-title-domain-bar-chart', 'figure'),
    [Input('job-title-category-domain-dropdown', 'value')]
)
def update_job_title_domain_bar_chart(selected_category):
    return create_job_title_bar_chart(df, 'des_category_domain', selected_category, des_categories_by_domain)


@app.callback(
    Output('salary-histogram', 'figure'),
    [Input('level-dropdown', 'value'),
     Input('domain-dropdown', 'value')]
)
def update_histogram(selected_level, selected_domain):
    # Start with the default dataset
    filtered_df = df_processed
    title = "Salary Distribution"  # Default title

    # Filter the data and update the title based on user selection
    if selected_level:
        filtered_df = filtered_df[filtered_df['des_category_level'] == selected_level]
        title = f"Salary Distribution for {selected_level}"
    if selected_domain:
        filtered_df = filtered_df[filtered_df['des_category_domain'] == selected_domain]
        title = f"Salary Distribution for {selected_domain}"

    # If both are selected, concatenate their titles
    if selected_level and selected_domain:
        title = f"Salary Distribution for {selected_level} in {selected_domain} Domain"

        # Create the histogram based on the filtered data
    fig = px.histogram(
        filtered_df,
        x="avg_salary",
        title=title,
        labels={"avg_salary": "Average Salary"},
        color_discrete_sequence=["#e9ecef"],  # Change this to your desired color
    )

    # Update layout to match the dark theme
    fig.update_layout(
        paper_bgcolor="#282c31",
        plot_bgcolor="#282c31",
        font=dict(color="#e9ecef"),
        xaxis=dict(
            gridcolor="#4f545a",  # Lighter than the plot background, but darker than text
            zerolinecolor="#4f545a"
        ),
        yaxis=dict(
            gridcolor="#4f545a",
            zerolinecolor="#4f545a"
        ),
    )
    return fig


@app.callback(
    Output('table-hard-skill-domain', 'children'),
    [Input('dropdown-hard-skill-domain', 'value')]
)
def update_hard_skill_domain_table(selected_domain):
    if selected_domain:
        return hard_skill_domain_tables[selected_domain]
    return dash.no_update


@app.callback(
    Output('table-hard-skill-level', 'children'),
    [Input('dropdown-hard-skill-level', 'value')]
)
def update_hard_skill_level_table(selected_level):
    if selected_level:
        return hard_skill_level_tables[selected_level]
    return dash.no_update


@app.callback(
    Output('table-soft-skill-domain', 'children'),
    [Input('dropdown-soft-skill-domain', 'value')]
)
def update_soft_skill_domain_table(selected_domain):
    if selected_domain:
        return soft_skill_domain_tables[selected_domain]
    return dash.no_update


@app.callback(
    Output('table-soft-skill-level', 'children'),
    [Input('dropdown-soft-skill-level', 'value')]
)
def update_soft_skill_level_table(selected_level):
    if selected_level:
        return soft_skill_level_tables[selected_level]
    return dash.no_update


@app.callback(
    [Output('level-dropdown', 'value'),
     Output('domain-dropdown', 'value')],
    [Input('level-dropdown', 'value'),
     Input('domain-dropdown', 'value')]
)
def reset_dropdowns(level_value, domain_value):
    ctx = dash.callback_context
    if not ctx.triggered:
        default_level = list(des_categories_by_level.keys())[0]
        return default_level, None

    # Get the ID of the component that triggered the callback
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'level-dropdown' and level_value:
        return level_value, None
    elif trigger_id == 'domain-dropdown' and domain_value:
        return None, domain_value
    else:
        raise PreventUpdate


@app.callback(
    Output('search-results-content', 'children'),
    [Input('search-button', 'n_clicks')],
    [State('job-search-dropdown', 'value'),
     State('location-search-dropdown', 'value')]
)
def update_search_results(n_clicks, selected_job, selected_location):
    if not n_clicks:
        raise PreventUpdate

    # Filter the main dataframe based on selected job and location
    filtered_df = df[
        ((df['des_category_level'] == selected_job) | (df['des_category_domain'] == selected_job)) &
        (df['location'] == selected_location)
        ]

    results = []
    for _, row in filtered_df.iterrows():
        job_title = row['title']
        salary = row['salary']  # use 'salary' column instead
        top10_hard_skills = parse_skills(row['Top 10 Hard Skills'])  # 注意大小写和空格
        top10_soft_skills = parse_skills(row['Top 10 Soft Skills'])  # 注意大小写和空格

        # 创建一个卡片布局用于每个工作
        job_card = dbc.Card(
            [
                dbc.CardHeader(html.H5(job_title, className="card-title", style={"font-weight": "bold"})),
                dbc.CardBody(
                    [
                        html.P(f"Salary: {salary}", className="card-text", style={"color": "green"}),
                        dbc.Row([
                            dbc.Col([
                                html.P("Top Hard Skills:", className="card-text", style={"font-weight": "bold"}),
                                html.P(top10_hard_skills, className="card-text"),
                            ], md=6),
                            dbc.Col([
                                html.P("Top Soft Skills:", className="card-text", style={"font-weight": "bold"}),
                                html.P(top10_soft_skills, className="card-text"),
                            ], md=6)
                        ])
                    ]
                ),
            ],
            style={"margin-bottom": "20px"},
            className='search-card'
        )

        results.append(job_card)

    return results


@app.callback(
    Output('url', 'pathname'),
    [Input('search-button', 'n_clicks')],
    [State('job-search-dropdown', 'value'),
     State('location-search-dropdown', 'value')]
)
def trigger_search(n, job, location):
    if not n:
        raise PreventUpdate

    return "/search-results"  # 这会将用户重定向到搜索结果页面


@app.callback(
    [
        Output('total-jobs', 'children'),
        Output('pie-chart-hard-skills', 'figure'),
        Output('pie-chart-soft-skills', 'figure'),
        Output('bar-chart-salary-ranges', 'figure')  # 新增
    ],
    [Input('url', 'pathname')]
)
def update_homepage_contents(pathname):
    if pathname != '/':
        raise PreventUpdate

    total_jobs = f"Total Jobs: {len(df)}"
    fig_hard_skills = px.pie(top_10_hard_skills, names='Skill', values='Count', title='Top 10 Hard Skills')
    fig_soft_skills = px.pie(top_10_soft_skills, names='Skill', values='Count', title='Top 10 Soft Skills')
    fig_salary_ranges = create_salary_bar_chart(df)  # 新增

    return total_jobs, fig_hard_skills, fig_soft_skills, fig_salary_ranges  # 更新返回值


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == "/job-title-distributions":
        return html.Div([
            dcc.Dropdown(
                id='job-title-category-level-dropdown',
                options=[{'label': category, 'value': category} for category in des_categories_by_level.keys()],
                placeholder="Select Job Title Category"
            ),
            dcc.Graph(id='job-title-level-bar-chart'),
            dcc.Dropdown(
                id='job-title-category-domain-dropdown',
                options=[{'label': category, 'value': category} for category in des_categories_by_domain.keys()],
                placeholder="Select Job Title Category"
            ),
            dcc.Graph(id='job-title-domain-bar-chart'),
        ])
    elif pathname == "/salary-distributions":
        return html.Div([
            dcc.Dropdown(
                id='level-dropdown',
                options=[{'label': level, 'value': level} for level in des_categories_by_level.keys()],
                placeholder="Select Job Level",
                value=None
            ),
            dcc.Dropdown(
                id='domain-dropdown',
                options=[{'label': domain, 'value': domain} for domain in des_categories_by_domain.keys()],
                placeholder="Select Job Domain",
                value=None
            ),
            dcc.Graph(id='salary-histogram'),
        ])
    elif pathname == "/platform-distributions":
        return html.Div([
            dcc.Graph(figure=fig_platform),
        ])
    elif pathname == "/usa-map":  # Handling the new route
        return html.Div([
            dcc.Graph(figure=choropleth_map)
        ])
    elif pathname == "/skills-insights":
        return dcc.Tabs(id='skills-tabs', children=[
            dcc.Tab(label='Hard Skills by Domain', children=[
                dcc.Dropdown(
                    id='dropdown-hard-skill-domain',
                    options=[{'label': domain, 'value': domain} for domain in hard_skill_domain_tables],
                    placeholder="Select a Job",
                    value=list(hard_skill_domain_tables.keys())[0]
                ),
                html.Div(id='table-hard-skill-domain')
            ]),
            dcc.Tab(label='Hard Skills by Level', children=[
                dcc.Dropdown(
                    id='dropdown-hard-skill-level',
                    options=[{'label': level, 'value': level} for level in hard_skill_level_tables],
                    placeholder="Select a Job",
                    value=list(hard_skill_level_tables.keys())[0]
                ),
                html.Div(id='table-hard-skill-level')
            ]),
            dcc.Tab(label='Soft Skills by Domain', children=[
                dcc.Dropdown(
                    id='dropdown-soft-skill-domain',
                    options=[{'label': domain, 'value': domain} for domain in soft_skill_domain_tables],
                    placeholder="Select a Job",
                    value=list(soft_skill_domain_tables.keys())[0]
                ),
                html.Div(id='table-soft-skill-domain')
            ]),
            dcc.Tab(label='Soft Skills by Level', children=[
                dcc.Dropdown(
                    id='dropdown-soft-skill-level',
                    options=[{'label': level, 'value': level} for level in soft_skill_level_tables],
                    placeholder="Select a Job",
                    value=list(soft_skill_level_tables.keys())[0]
                ),
                html.Div(id='table-soft-skill-level')
            ]),
        ])
    elif pathname == "/search-results":
        return html.Div([
            html.Div(id='search-results-content')  # Placeholder for search results
        ])
    else:
        return html.Div([
            html.H2('Home Page Content'),
            html.Div(id='total-jobs', className='data-display'),
            dcc.Graph(id='pie-chart-hard-skills'),
            dcc.Graph(id='pie-chart-soft-skills'),
            dcc.Graph(id='bar-chart-salary-ranges')
        ])


# Set the layout of the app
app.layout = get_layout()

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
