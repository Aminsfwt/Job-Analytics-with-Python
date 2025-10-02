#Import libraries
import ast 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datasets import load_dataset # type: ignore

#import data from hugging face 
jobsData = pd.read_csv('data_jobs.csv')

#Convert job_posted_date column from string to date
jobsData['job_posted_date'] = pd.to_datetime(jobsData['job_posted_date'])

#Convert job_skills column from string to list
jobsData['job_skills'] = jobsData['job_skills'].apply(lambda skill: ast.literal_eval(skill) if pd.notna(skill) else skill)

"""  WHAT ARE THE MOST DEMAND SKILLS FOR THE TOP 3 MOST POPULAR DATA RULES IN USA """

#GIT THE DATA OF USA ONLY
USA_jobs = jobsData[jobsData['job_country'] == 'United States']

#Explode skills from the list to cont them
df_skills = USA_jobs.explode('job_skills')

#Get the count of sskills for all job titles
df_skill_count = df_skills.groupby(['job_skills', 'job_title_short']).size()

#Convert the df_skill_count series to data frame
df_skill_count = df_skill_count.reset_index(name='skill_count')

#Sort the df_skill_count by count of skills descending
df_skill_count = df_skill_count.sort_values(by='skill_count', ascending=False)

#Get all the job skills and put them on list
job_titles = df_skill_count['job_title_short'].unique().tolist()

#Get top 3 titles in USA
Top3Titles = sorted(job_titles[0:3])

#Get the count of job titles posted in usa and convert this to data frame
USA_jobs_count = USA_jobs['job_title_short'].value_counts().reset_index(name='total_jobs')

#Merge the job counts & skills count into one data frame to calculate the percentege of most demanded skills to job title
df_jobs_percent = pd.merge(USA_jobs_count, df_skill_count, how='left', on='job_title_short')

#Create series of the percentege of most demanded skills to job title
df_jobs_percent['percentage_jobs'] = (df_jobs_percent['skill_count'] / df_jobs_percent['total_jobs']) * 100

#Plot the visualization of the likelhood percentge of top 5 demanded skills for top 3 job wanted in USA
fig, ax = plt.subplots(len(Top3Titles), 1)
sns.set_theme(style='ticks')
for i, job_title in enumerate(Top3Titles):
    df_plot = df_jobs_percent[df_jobs_percent['job_title_short'] == job_title].head(5)
    sns.barplot(data=df_plot, x='percentage_jobs', y='job_skills', ax=ax[i], hue='skill_count', palette='dark:b_r')
    ax[i].set_title(job_title)
    ax[i].set_xlabel('')
    ax[i].set_ylabel('')
    ax[i].get_legend().remove()
    ax[i].set_xlim(0, 80)

    #print the percentege for every skill in its bar in the chart
    for n, v in enumerate(df_plot['percentage_jobs']):
        ax[i].text(v+1, n, f'{v: .0f}%', va='center')

    #show only the last chart x axis
    if i != len(Top3Titles) - 1:
        ax[i].set_xticks([])

fig.suptitle('Likelihood of skills requested in USA job postings', fontsize=25) 
fig.tight_layout(h_pad=0.5)
plt.show()

