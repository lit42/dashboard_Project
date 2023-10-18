from dash import dash_table
import plotly.express as px
import plotly.graph_objects as go

from data_processing import map_salary_to_range


def create_histograms(df_processed):
    fig = px.histogram(
        df_processed,
        x="avg_salary",
        color="des_category_level",
        title="Salary Distribution by Job Level",
        labels={"avg_salary": "Average Salary", "des_category_level": "Level"},
        category_orders={
            "des_category_level": [
                "Junior Data Analysts",
                "Senior Data Analysts",
                "Lead Data Analysts",
            ]
        },
        barmode="overlay",
    )
    fig.update_traces(opacity=0.8)

    fig_domain = px.histogram(
        df_processed,
        x="avg_salary",
        color="des_category_domain",
        title="Salary Distribution by Job Domain",
        labels={"avg_salary": "Average Salary", "des_category_domain": "Domain"},
        barmode="overlay",
    )
    fig_domain.update_traces(opacity=0.8)

    fig.update_layout(
        paper_bgcolor="#282c31",  # Background outside the plot
        plot_bgcolor="#282c31",  # Background inside the plot
        font=dict(color="#e9ecef"),  # Font color
        # ... other layout properties ...
    )
    fig_domain.update_layout(
        paper_bgcolor="#282c31",
        plot_bgcolor="#282c31",
        font=dict(color="#e9ecef"),
    )

    return fig, fig_domain


def create_platform_pie(df):
    top_N = 6
    top_platforms = df['platform'].value_counts().index[:top_N]
    df.loc[:, 'grouped_platform'] = df['platform'].apply(lambda x: x if x in top_platforms else 'Others')
    grouped_platform_counts = df['grouped_platform'].value_counts().reset_index()
    grouped_platform_counts.columns = ['Platform', 'Count']

    fig_platform = px.pie(
        grouped_platform_counts,
        values='Count',
        names='Platform',
        title='Distribution of Job Listings by Platform',
        hole=0.3
    )
    fig_platform.update_traces(
        textinfo='percent+label',
        pull=[0.1 if platform == 'Others' else 0 for platform in grouped_platform_counts['Platform']]
        # adjust this value to control the pie size
    )

    return fig_platform


def create_job_title_bar_chart(df, column, selected_category, categories):
    if selected_category:
        filtered_df = df[df[column] == selected_category]
        title_counts = filtered_df['title'].value_counts().reset_index()
        title_counts.columns = ['Job Title', 'Count']
        title_counts.sort_values(by='Count', ascending=False, inplace=True)

        # Limit to top N job titles and group the rest into 'Others'
        top_N = 10  # Adjust this number based on your preference
        if len(title_counts) > top_N:
            other_count = title_counts[top_N:]['Count'].sum()
            title_counts = title_counts[:top_N]
            title_counts.loc[len(title_counts)] = ['Others', other_count]  # Using loc to add a new row

        fig = px.bar(title_counts, y='Job Title', x='Count', orientation='h',
                     labels={'y': 'Job Title', 'x': 'Count'})
        fig.update_layout(title_text=f"Top Job Titles in Category: {selected_category}")
    else:
        title_category_counts = df[column].value_counts().reset_index()
        title_category_counts.columns = ['Job Title Category', 'Count']
        title_category_counts.sort_values(by='Count', ascending=False, inplace=True)

        fig = px.bar(title_category_counts, x='Job Title Category', y='Count',
                     labels={'x': 'Job Title Category', 'y': 'Count'})
        fig.update_layout(title_text="Job Title Category Distribution")

    fig.update_traces(
        # marker_color="#e9ecef",  # light color for bars
        opacity=0.8
    )

    fig.update_layout(
        title_text=f"Top Job Titles in Category: {selected_category}",
        title_font_color="#e9ecef",  # light color for title
        plot_bgcolor="#282c31",  # dark background color
        paper_bgcolor="#282c31",  # dark paper color
        yaxis=dict(
            title_font_color="#e9ecef",  # light color for y-axis title
            tickfont_color="#e9ecef",  # light color for y-axis ticks
            gridcolor="#4f545a",  # Lighter than the plot background, but darker than text
            zerolinecolor="#4f545a"
        ),
        xaxis=dict(
            title_font_color="#e9ecef",  # light color for x-axis title
            tickfont_color="#e9ecef",  # light color for x-axis ticks
            gridcolor="#4f545a",  # Lighter than the plot background, but darker than text
            zerolinecolor="#4f545a"
        ),
        barmode="overlay",
        bargap=0.5
    )

    return fig


def generate_choropleth_map(df):
    # Remove 'Anywhere' and 'United States' rows
    df = df[~df['location'].isin(['Anywhere', 'United States'])].copy()

    # Use regex to extract state abbreviation
    df.loc[:, 'state'] = df.loc[:, 'location'].str.extract(r',\s*([A-Z]{2})$')[0]
    # Count the occurrences of each state
    state_counts = df['state'].value_counts()

    # Reset index and rename columns for clarity
    state_counts_df = state_counts.reset_index()
    state_counts_df.columns = ['state', 'count']

    # Create the choropleth map
    fig = px.choropleth(state_counts_df,
                        locations='state',
                        color='count',
                        locationmode='USA-states',
                        scope='usa',
                        title='Job Distributions across USA',
                        color_continuous_scale=px.colors.sequential.Blues,
                        labels={'count': 'Number of Listings'}
                        )

    fig.update_layout(
        title_text='Job Distributions across USA',
        title_font_color="#e9ecef",  # light color for title
        geo_bgcolor="#282c31",  # dark background for the map
        paper_bgcolor="#282c31",  # dark paper background
        geo=dict(
            lakecolor="#282c31"  # dark color for lakes
        ),
        coloraxis_colorbar=dict(
            titlefont=dict(color="#e9ecef"),  # light color for the colorbar title
            tickfont=dict(color="#e9ecef"),  # light color for the colorbar tick labels
            # removed the tickvals attribute to let Plotly decide the tick marks
        )
    )
    return fig


def create_skill_table(df, skill_type, category_column):
    tables = {}
    for _, row in df.iterrows():
        category = row[category_column]
        skills = [{'#': i + 1, 'Skill': row[f"Top {i + 1} {skill_type}"]} for i in range(10)]

        table = dash_table.DataTable(
            data=skills,
            columns=[
                {'name': '', 'id': '#', 'type': 'numeric'},
                {'name': 'Top 10 Skills', 'id': 'Skill'}
            ],
            style_header={
                'backgroundColor': '#343a40',
                'color': '#e9ecef',
                'fontWeight': 'bold',
                'fontSize': '16px',
                'padding': '10px',
                'textAlign': 'center'  # align the header to center
            },
            style_cell={
                'backgroundColor': '#282c31',
                'color': '#e9ecef',
                'padding': '10px',
                'textAlign': 'left',
                'border': '1px solid rgba(255, 255, 255, 0.1)',
                'width': '50%',  # default width
            },
            style_cell_conditional=[
                {
                    'if': {'column_id': '#'},
                    'width': '10%',  # set the width for the numeric column
                    'textAlign': 'right'
                },
                {
                    'if': {'column_id': 'Skill'},
                    'width': '90%',  # set the width for the skill column
                }
            ],
            style_table={
                'border': '1px solid #d6d6d6',
                'width': '70%',
                'margin': 'auto',
            },
            style_data_conditional=[
                {
                    'if': {'column_type': 'numeric'},
                    'textAlign': 'right'
                }
            ]
        )
        tables[category] = table
    return tables


def create_salary_bar_chart(df):
    df['salary_range'] = df['salary'].apply(map_salary_to_range)
    df_filtered = df[df['salary_range'].notna()]

    salary_order = ["<50k", "50k-75k", "75k-100k", "100k-125k", "125k-150k", "150k-175k", "175k-200k", "200k+"]

    salary_distribution = df_filtered['salary_range'].value_counts().reindex(salary_order).reset_index()
    salary_distribution.columns = ['Salary Range', 'Job Count']

    fig_salary_ranges = px.bar(salary_distribution,
                               x='Salary Range',
                               y='Job Count',
                               title='Job Count by Salary Range')

    fig_salary_ranges.update_layout(
        paper_bgcolor="#282c31",  # 主题的深色背景
        plot_bgcolor="#282c31",  # 与纸张背景颜色相同
        font=dict(color="#e9ecef"),  # 浅色字体
        title_font=dict(color="#e9ecef"),  # 标题的浅色字体
        xaxis=dict(
            title_font=dict(color="#e9ecef"),  # X轴标题的浅色字体
            tickfont=dict(color="#e9ecef"),  # X轴刻度的浅色字体
            linecolor="#e9ecef",  # X轴线条的浅色
            gridcolor="#4f5b62"  # 网格线的深灰色
        ),
        yaxis=dict(
            title_font=dict(color="#e9ecef"),  # Y轴标题的浅色字体
            tickfont=dict(color="#e9ecef"),  # Y轴刻度的浅色字体
            linecolor="#e9ecef",  # Y轴线条的浅色
            gridcolor="#4f5b62"  # 网格线的深灰色
        ),
    )
    fig_salary_ranges.update_traces(
        # marker_color="#e9ecef",  # light color for bars
        opacity=0.8
    )
    return fig_salary_ranges



