#Import libraries
import ast 
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from adjustText import adjust_text # type: ignore
import seaborn as sns
from datasets import load_dataset # type: ignore

#import data from hugging face 
"""
data = load_dataset("lukebarousse/data_jobs")
jobsData = data['train'].to_pandas()
"""

jobsData = pd.read_csv('data_jobs.csv')

#Convert job_posted_date column from string to date
jobsData['job_posted_date'] = pd.to_datetime(jobsData['job_posted_date'])

#Convert job_skills column from string to list
jobsData['job_skills'] = jobsData['job_skills'].apply(lambda skill: ast.literal_eval(skill) if pd.notna(skill) else skill)

""" How are in-demand skills trending for Data Analysts? """

#Filter data to get Data Analyst jobs and country USA
USA_DA_jobs = jobsData[(jobsData['job_title'] == 'Data Analyst') & (jobsData['job_country'] == 'United States')].copy()

#get the data df USA
USA_DA_jobs = USA_DA_jobs.dropna(subset=['salary_year_avg'])

#explode the job skills 
USA_DA_jobs_exploded = USA_DA_jobs.explode('job_skills')

USA_DA_Top5skills = USA_DA_jobs_exploded[['job_skills', 'salary_year_avg']].head(5)

#top 10 most payied job skills
USA_DA_skills = USA_DA_jobs_exploded.groupby('job_skills')['salary_year_avg'].agg(['count', 'median']).sort_values(by='median', ascending=False)
USA_DA_skills = USA_DA_skills.rename(columns={'count': 'skill_count', 'median': 'median_salary'})

USA_DA_counts = len(USA_DA_jobs)
USA_DA_skills['skill_percent'] = (USA_DA_skills['skill_count'] / USA_DA_counts) * 100

skill_percentege = 5
high_demand_skills =  USA_DA_skills[USA_DA_skills['skill_percent'] > skill_percentege]

"""plt.scatter(high_demand_skills['skill_percent'], high_demand_skills['median_salary'])

plt.xlabel('Percent of Data Analyst Jobs')
plt.ylabel('Median Salary ($USD)')  # Assuming this is the label you want for y-axis
plt.title('Most Optimal Skills for Data Analysts in the US')

# Get current axes, set limits, and format axes
ax = plt.gca()
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, pos: f'${int(y/1000)}K'))  # Example formatting y-axis

# Add labels to points and collect them in a list
texts = []
for i, txt in enumerate(high_demand_skills.index):
    texts.append(plt.text(high_demand_skills['skill_percent'].iloc[i], high_demand_skills['median_salary'].iloc[i], " " + txt))

# Adjust text to avoid overlap and add arrows
adjust_text(texts, arrowprops=dict(arrowstyle='->', color='gray'))
"""
df_technology = jobsData['job_type_skills'].copy()

# remove duplicates
df_technology = df_technology.drop_duplicates()

# remove NaN values
df_technology = df_technology.dropna()

# combine all dictionaries into one
technology_dict = {}
for row in df_technology:
    row_dict = ast.literal_eval(row)  # convert string to dictionary
    for key, value in row_dict.items():
        if key in technology_dict:  # if key already exists in technology_dict, add value to existing value
            technology_dict[key] += value
        else:                       # if key does not exist in technology_dict, add key and value
            technology_dict[key] = value

# remove duplicates by converting values to set then back to list
for key, value in technology_dict.items():
    technology_dict[key] = list(set(value))

# turn dictionary into dataframe
df_technology = pd.DataFrame(list(technology_dict.items()), columns=['technology', 'skills'])

df_technology = df_technology.explode('skills')

# merge df_DA_skills and df_technology
df_DA_skills_tech = USA_DA_skills.merge(df_technology, left_on='job_skills', right_on='skills')

df_DA_skills_tech_high_demand = df_DA_skills_tech[df_DA_skills_tech['skill_percent'] > skill_percentege]

sns.scatterplot(
    data=df_DA_skills_tech_high_demand,
    x='skill_percent',
    y='median_salary',
    hue='technology'
)

sns.despine()
sns.set_theme(style='ticks')

# Prepare texts for adjustText
texts = []
for i, txt in enumerate(high_demand_skills.index):
    texts.append(plt.text(high_demand_skills['skill_percent'].iloc[i], high_demand_skills['median_salary'].iloc[i], txt))

# Adjust text to avoid overlap
adjust_text(texts, arrowprops=dict(arrowstyle='->', color='gray'))

# Set axis labels, title, and legend
plt.xlabel('Percent of Data Analyst Jobs')
plt.ylabel('Median Yearly Salary')
plt.title('Most Optimal Skills for Data Analysts in the US')
plt.legend(title='Technology')

ax = plt.gca()
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, pos: f'${int(y/1000)}K'))
ax.xaxis.set_major_formatter(PercentFormatter(decimals=0))

# Adjust layout and display plot 
plt.tight_layout()
plt.show()

