import ast
import re

import pandas as pd

# Load the dataset
url = "https://raw.githubusercontent.com/lit42/test/main/1.9.4_dataset.csv"

des_categories_by_level = {
    "Junior Data Analysts": ["junior", "jr", "entry level", "entry-level", "analyst i", "analyst 1", "intern"],
    "Senior Data Analysts": ["senior", "sr", "analyst ii", "analyst 2", "analyst iii", "analyst 3", "advanced"],
    "Lead Data Analysts": ["lead", "director", "manager", "leader", "cto"],
}

des_categories_by_domain = {
    "BI Data Analysts": ["business intelligence"],
    "Google Analytics expert": ["google analytics", "ga4", "ga"],
    "Data Governance Analyst": ["governance"],
    "Qualitative Data Analysts": ["qualitative"],
    "Healthcare Data Analysts": ["healthcare", "clinical"],
    "Supply Chain Data Analysts": ["supply chain", "logistics"],
    "GIS Data Analysts": ["gis", "geospatial"],
    "HR Data Analysts": ["hr", "human resources"],
    "Marketing Data Analysts": ["marketing", "salesforce", "sales", "online retail", "advertising", "commercial",
                                "ecommerce"],
    "Financial Data Analysts": ["financial", "finance"],
    "Operations Data Analysts": ["operations"],
    "Technical Data Analysts": ["technical", "information technology"],
    "Data Scientists": ["scientist", "scientific"],
    "Data Engineers": ["engineer", "engineering"],
    "Risk Analysts": ["risk", "risks"],
    "Excel expert": ["excel"],
}


# Load the dataset
def load_data():
    try:
        df = pd.read_csv(url)
    except Exception as e:
        print(f"Error loading dataset: {e}")
        df = None  # Set df to None to indicate an issue
    return df


def load_skill_dataset(filepath):
    return pd.read_csv(filepath)


# Data processing function
def process_data_optimized(df):
    # Split salaries on "-"
    split_salaries = df['salary'].str.split('-', expand=True)

    # Clean and convert to float
    df.loc[:, 'lower_bound'] = split_salaries[0].str.replace("[^0-9]", "", regex=True).astype(float)
    df.loc[:, 'upper_bound'] = split_salaries[1].str.replace("[^0-9]", "", regex=True).astype(float)

    # Compute average salary
    df.loc[:, 'avg_salary'] = df[['lower_bound', 'upper_bound']].mean(axis=1)

    # Handle outliers
    Q1 = df['avg_salary'].quantile(0.25)
    Q3 = df['avg_salary'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df = df[(df['avg_salary'] >= lower_bound) & (df['avg_salary'] <= upper_bound)]

    return df


def parse_skills(skills_str):
    try:
        # 尝试将字符串解析为列表
        skills = ast.literal_eval(skills_str)
        # 如果成功，则将列表连接成一个字符串
        return ', '.join(skills)
    except ValueError:
        # 如果发生错误，返回原始字符串
        return skills_str


def map_salary_to_range(salary):
    if salary == "Not specified":
        return None  # 如果薪资未指定，返回 None
    elif "a year" in salary:
        if "-" in salary:
            low, high = salary.split("-")
            low = int(low.replace(",", ""))
            high = int(high.split()[0].replace(",", ""))
            avg = (low + high) / 2
        else:
            avg = int(salary.split()[0].replace(",", ""))

        # 定义更宽的薪资范围
        if avg < 50000:
            return "<50k"
        elif 50000 <= avg < 75000:
            return "50k-75k"
        elif 75000 <= avg < 100000:
            return "75k-100k"
        elif 100000 <= avg < 125000:
            return "100k-125k"
        elif 125000 <= avg < 150000:
            return "125k-150k"
        elif 150000 <= avg < 175000:
            return "150k-175k"
        elif 175000 <= avg < 200000:
            return "175k-200k"
        else:
            return "200k+"
    else:
        return "Other"
