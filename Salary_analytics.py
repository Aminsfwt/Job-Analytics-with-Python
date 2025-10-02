#Import libraries
import ast 
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import seaborn as sns
from datasets import load_dataset # type: ignore

#import data from hugging face 
"""data = load_dataset("lukebarousse/data_jobs")
jobsData = data['train'].to_pandas()"""
jobsData = pd.read_csv('data_jobs.csv')

#Convert job_posted_date column from string to date
jobsData['job_posted_date'] = pd.to_datetime(jobsData['job_posted_date'])

#Convert job_skills column from string to list
jobsData['job_skills'] = jobsData['job_skills'].apply(lambda skill: ast.literal_eval(skill) if pd.notna(skill) else skill)

""" How well do jobs and skills pay for Data Analysts? """

#get the data df USA
USA_data = jobsData[jobsData['job_country'] == 'United States'].dropna(subset=['salary_year_avg'])

#get the top 6 job titles for possted jobs 
top6_job_titles = USA_data['job_title_short'].value_counts().index[:6].tolist()

#get the top 6 jobs in the data frame
USA_top6_jobs = USA_data[USA_data['job_title_short'].isin(top6_job_titles)]

#group the data by median salary
ordere_jobs = USA_top6_jobs.groupby('job_title_short')['salary_year_avg'].median().sort_values(ascending=False).index

sns.boxplot(data=USA_top6_jobs, x='salary_year_avg', y='job_title_short', order=ordere_jobs)
sns.set_theme(style='ticks')
sns.despine()

# this is all the same
plt.title('Salary Distributions of Data Jobs in the US')
plt.xlabel('Yearly Salary (USD)')
plt.ylabel('')
plt.xlim(0, 600000) 
ticks_x = plt.FuncFormatter(lambda y, pos: f'${int(y/1000)}K')
plt.gca().xaxis.set_major_formatter(ticks_x)
plt.show()

#Investigating median salary vs skill for data analsys
USA_DA = jobsData[(jobsData['job_title_short'] == 'Data Analyst') & (jobsData['job_country'] == 'United States')]

#drop null values in salary
USA_DA = USA_DA.dropna(subset='salary_year_avg')

#explode the job skills 
USA_DA = USA_DA.explode('job_skills')

#top 10 most payied job skills
USA_DA_top_pay = USA_DA.groupby('job_skills')['salary_year_avg'].agg(['count', 'median']).sort_values(by='median', ascending=False)
USA_DA_top_pay = USA_DA_top_pay.head(10)

#top 10 job skills
USA_DA_top_skills = USA_DA.groupby('job_skills')['salary_year_avg'].agg(['count', 'median']).sort_values(by='count', ascending=False)
USA_DA_top_skills = USA_DA_top_skills.head(10).sort_values(by='median', ascending=False)

#plot top 10 job skills & top 10 most payied job skills
fig, ax = plt.subplots(2,1)
sns.set_theme(style='ticks')

#plot top 10 highest payied job skills
sns.barplot(data=USA_DA_top_pay, x='median', y=USA_DA_top_pay.index, hue='median', ax=ax[0], palette='dark:b_r')
ax[0].legend().remove()

ax[0].set_title('Top 10 highest paied job skills in USA')
ax[0].set_xlabel('')
ax[0].set_ylabel('')
tick_x = plt.FuncFormatter(lambda y, pos: f'${int(y/1000)}K')
ax[0].xaxis.set_major_formatter(tick_x)

#plot  top 10  job skills
sns.barplot(data=USA_DA_top_skills, x='median', y=USA_DA_top_skills.index, hue='median', ax=ax[1], palette='light:b')
ax[1].legend().remove()

ax[1].set_title('Top 10 most demand job skills in USA')
ax[1].set_xlabel('Median Salary')
ax[1].set_ylabel('')
ax[1].set_xlim(ax[0].get_xlim())
tick_x = plt.FuncFormatter(lambda y, pos: f'${int(y/1000)}K')
ax[1].xaxis.set_major_formatter(tick_x)
sns.set_theme(style='ticks')
plt.tight_layout()
plt.show()