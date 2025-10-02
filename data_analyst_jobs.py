#Import libraries
import ast 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datasets import load_dataset # type: ignore

#import data from hugging face 
data = load_dataset("lukebarousse/data_jobs")
jobsData = data['train'].to_pandas()

#Convert job_posted_date column from string to date
jobsData['job_posted_date'] = pd.to_datetime(jobsData['job_posted_date'])

#Convert job_skills column from string to list
jobsData['job_skills'] = jobsData['job_skills'].apply(lambda skill: ast.literal_eval(skill) if pd.notna(skill) else skill)

#Filter data to get Data Analyst jobs and country USA
USA_DA_jobs = jobsData[(jobsData['job_title_short'] == 'Data Analyst') & (jobsData['job_country'] == 'United States')]

#get the top 10 work locations
DA_locations = USA_DA_jobs['job_location'].value_counts().head(10).to_frame()

#use seaborn librarry to plot the top 10 locations 
sns.set_theme(style='ticks')
sns.barplot(data=DA_locations, x='count', y='job_location', hue='count', palette='dark:b_r', legend=False)
sns.despine()
plt.title('Count of job locations for Data Analsyt in USA')
plt.xlabel('Number of jobs')
plt.ylabel('Job locations')

#Plot pie chart
dict_columns = {
    'job_work_from_home': 'Work from Home Offered',
    'job_no_degree_mention': 'Degree Requirment',
    'job_health_insurance': 'Health Insurance Offered'
}

fig, ax = plt.subplots(1,3)
fig.set_size_inches(12,5)

for i, (column, title) in enumerate(dict_columns.items()):
    ax[i].pie(USA_DA_jobs[column].value_counts(), labels=['True', 'False'], autopct='%1.1f%%', startangle=90)
    ax[i].set_title(title)


#get the top 10  companies
DA_companies = USA_DA_jobs['company_name'].value_counts().head(10).to_frame()

#use seaborn librarry to plot the top 10 companies 
sns.set_theme(style='ticks')
sns.barplot(data=DA_companies, x='count', y='company_name', hue='count', palette='dark:b_r', legend=False)
sns.despine()
plt.title('Count of Companies for Data Analsyt in USA')
plt.xlabel('Number of jobs')
plt.ylabel('Job Company')


#plt.show()
