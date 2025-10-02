#Import libraries
import ast 
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import seaborn as sns
from datasets import load_dataset # type: ignore

#import data from hugging face 
data = load_dataset("lukebarousse/data_jobs")
jobsData = data['train'].to_pandas()

#Convert job_posted_date column from string to date
jobsData['job_posted_date'] = pd.to_datetime(jobsData['job_posted_date'])

#Convert job_skills column from string to list
jobsData['job_skills'] = jobsData['job_skills'].apply(lambda skill: ast.literal_eval(skill) if pd.notna(skill) else skill)

""" How are in-demand skills trending for Data Analysts? """

#Filter data to get Data Analyst jobs and country USA
USA_DA_jobs = jobsData[(jobsData['job_title'] == 'Data Analyst') & (jobsData['job_country'] == 'United States')].copy()

#Create column for months
USA_DA_jobs['job_posted_month_no'] = USA_DA_jobs['job_posted_date'].dt.month  

#Explode job skills
USA_DA_skills = USA_DA_jobs.explode('job_skills')

#Pivote USA_DA_skills to get the count of skills by each month
USA_DA_Pivotedskills = USA_DA_skills.pivot_table(
                                index='job_posted_month_no',
                                columns='job_skills',
                                aggfunc='size',
                                fill_value=0
)

#Create row to get the total skills
USA_DA_Pivotedskills.loc['Total'] = USA_DA_Pivotedskills.sum()

#sort the pivot table by total sskill counts
USA_DA_Pivotedskills = USA_DA_Pivotedskills[USA_DA_Pivotedskills.loc['Total'].sort_values(ascending=False).index]

#drop total row
USA_DA_Pivotedskills = USA_DA_Pivotedskills.drop('Total')

#get the total jobs posted by month
total_monthly_jobs = USA_DA_jobs.groupby('job_posted_month_no').size()

#get the precentege skills by total jobs posted every month
skills_by_monthly_posted_job = USA_DA_Pivotedskills.div(total_monthly_jobs / 100 , axis=0)

#convert month number to its name
skills_by_monthly_posted_job = skills_by_monthly_posted_job.reset_index()

#apply function to convert the month to date and cut the month name from it and put it in column
skills_by_monthly_posted_job['job_posted_month'] = skills_by_monthly_posted_job['job_posted_month_no'].apply(
                                                   lambda x: pd.to_datetime(x, format='%m').strftime('%b')) 
#set this column to be the index
skills_by_monthly_posted_job = skills_by_monthly_posted_job.set_index('job_posted_month')

#drop the month_no column
skills_by_monthly_posted_job = skills_by_monthly_posted_job.drop(columns='job_posted_month_no')

#get only the first 5 columns which mostly the top 5 skills
top5skills = skills_by_monthly_posted_job.iloc[:, :5]
#print(top5skills)

#plot the trending skills
sns.lineplot(data=top5skills, dashes=False, palette='tab10')
sns.set_theme(style='ticks')
sns.despine()  #to remove the frame of the plot

plt.title('Top Trending skills for Data Analyst role per month')
plt.ylabel('Liklihood in Job Posting')
plt.xlabel('2023')
plt.legend().remove()

ax = plt.gca()
ax.yaxis.set_major_formatter(PercentFormatter(decimals=0))

for i in range(5):
    plt.text(11.3, top5skills.iloc[-1, i], top5skills.columns[i], color='black')

plt.show()