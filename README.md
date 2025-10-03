# Data Jobs Dataset Analytics

# Overview
Welcome to my analysis of the data job market, focusing on data analyst roles. This project was created out of a desire to navigate and understand the job market more effectively. It delves into the top-paying and in-demand skills to help find optimal job opportunities for data analysts.

## The questions I want to answer in my project:
1- What are the skills most in demand for the top 3 most popular data roles?
2- How are in-demand skills trending for Data Analysts?
3- How well do jobs and skills pay for Data Analysts?
4- What are the optimal skills for data analysts to learn? (High Demand AND High Paying)

## What are the skills most in demand for the top 3 most popular data roles?

To find the most demanded skills for the top 3 most popular data roles. I filtered out those positions by which ones were the most popular, and got the top 5 skills for these top 3 roles. This query highlights the most popular job titles and their top skills.

# View the source code
[Top Skills.py](skills_count.py)

### Visualization code snippet
```fig, ax = plt.subplots(len(top3), 1)
sns.set_theme(style='ticks')
for i, job_title in enumerate(top3):
df_plot = df_jobs_percent[df_jobs_percent['job_title_short'] == job_title].head(5)
sns.barplot(data=df_plot, x='percentage_jobs', y='job_skills', ax=ax[i], hue='skill_count', palette='dark:b_r')
ax[i].set_title(job_title)
ax[i].set_xlabel('')
ax[i].set_ylabel('')
ax[i].get_legend().remove()
ax[i].set_xlim(0, 80)

for n, v in enumerate(df_plot['percentage_jobs']):
    ax[i].text(v+1, n, f'{v: .0f}%', va='center')

if i != len(top3) - 1:
    ax[i].set_xticks([])

fig.suptitle('Likelihood of skills requested in USA job postings', fontsize=25) 
fig.tight_layout(h_pad=0.5)
plt.show()
```
### Results

![Likelihood of skills requested in USA job postings](Images\LikelihoodofUSAjobskills.png)

### Insights

- Python is a very important skill, highly demand over the top 3 data jobs posted in USA,
most prominently for data science (72%) & data engineer (65%) roles.

- SQL is most requessted skill for data analyst (51%) & data engineer (68%) roles. 

- Data engineers require more specialized technical skills (aws, azure, spark) compare to data analyst & data science who expected to be more proficient in more general data managment and analysis tools (tableau, excel)


## How are in-demand skills trending for Data Analysts?
To find how skills are trending in 2023 for Data Analysts roles in USA, I filtered data analyst positions and grouped the skills by the month of the job postings. This got me the top 5 skills of data analysts by month.

# View the source code
[Trend Skills.py](trend_skills.py)


### Visualization code snippet
```
#get only the first 5 columns which mostly the top 5 skills
top5skills = skills_by_monthly_posted_job.iloc[:, :5]


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
```
### Results

![Likelihood of trending skills for Data Analyst role in 2023 in USA](Images\Trending_Top_Skills.png)

### Insights
- SQL remains the most consistently demanded skill throughout the year, although it shows a gradual decrease in demand.

- Excel experienced a significant increase in demand starting around September, surpassing both Python and Tableau by the end of the year.

- Both Python and Tableau show relatively stable demand throughout the year with some fluctuations but remain essential skills for data analysts. Power BI, while less demanded compared to the others, shows a slight upward trend towards the year's end.


# How well do jobs and skills pay for Data Analysts?
To identify the highest-paying roles and skills, I only got jobs in the United States and looked at their median salary. But first I looked at the salary distributions of common data jobs like Data Scientist, Data Engineer, and Data Analyst, to get an idea of which jobs are paid the most.

# View the source code
[Trend Skills.py](Salary_analytics.py)


### Visualization code snippet
```
#get the top 6 job titles for possted jobs 
top6_job_titles = USA_data['job_title_short'].value_counts().index[:6].tolist()

#get the top 6 jobs in the data frame
USA_top6_jobs = USA_data[USA_data['job_title_short'].isin(top6_job_titles)]

#group the data by median salary
ordered_top6_jobs = USA_top6_jobs.groupby('job_title_short')['salary_year_avg'].median().sort_values(ascending=False).index

#plot the data
sns.boxplot(data=USA_top6_jobs, x='salary_year_avg', y='job_title_short', order=ordered_top6_jobs)
sns.set_theme(style='ticks')

plt.title('Salary Distribution for top 6 roles in USA')
plt.xlabel('Yearly Salary (USD)')
plt.ylabel('')
plt.xlim(0, 60000)
#plt.legend().remove()
tick_x = plt.FuncFormatter(lambda y, pos: f'${int(y/1000)}K')
plt.gca().xaxis.set_major_formatter(tick_x)
plt.show()
```
### Results

![Likelihood of trending skills for Data Analyst role in 2023 in USA](Images\Salary_analytics.png)

### Insights
- There's a significant variation in salary ranges across different job titles. Senior Data Scientist positions tend to have the highest salary potential, with up to $600K, indicating the high value placed on advanced data skills and experience in the industry.

- Senior Data Engineer and Senior Data Scientist roles show a considerable number of outliers on the higher end of the salary spectrum, suggesting that exceptional skills or circumstances can lead to high pay in these roles. In contrast, Data Analyst roles demonstrate more consistency in salary, with fewer outliers.

- The median salaries increase with the seniority and specialization of the roles. Senior roles (Senior Data Scientist, Senior Data Engineer) not only have higher median salaries but also larger differences in typical salaries, reflecting greater variance in compensation as responsibilities increase.

# Highest Paid & Most Demanded Skills for Data Analysts
Next, I narrowed my analysis and focused only on data analyst roles. I looked at the highest-paid skills and the most in-demand skills. I used two bar charts to showcase these.

# View the source code
[Trend Skills.py](Salary_analytics.py)


### Visualization code snippet
```
#top 10 most payied job skills
USA_DA_top_pay = USA_DA.groupby('job_skills')['salary_year_avg'].agg(['count', 'median']).sort_values(by='median', ascending=False)
USA_DA_top_pay = USA_DA_top_pay.head(10)

#top 10 job skills
USA_DA_top_skills = USA_DA.groupby('job_skills')['salary_year_avg'].agg(['count', 'median']).sort_values(by='count', ascending=False)
USA_DA_top_skills = USA_DA_top_skills.head(10).sort_values(by='median', ascending=False)

#plot top 10 job skills & top 10 most payied job skills
fig, ax = plt.subplots(2,1)
sns.set_theme(style='ticks')

#plot  top 10 highest payied job skills
sns.barplot(data=USA_DA_top_pay, x='median', y=USA_DA_top_pay.index, hue='median', ax=ax[0], palette='dark:b_r')
ax[0].legend().remove()

ax[0].set_title('Top 10 highest payied job skills in USA')
ax[0].set_xlabel('')
ax[0].set_ylabel('')
tick_x = plt.FuncFormatter(lambda y, pos: f'${int(y/1000)}K')
plt.gca().xaxis.set_major_formatter(tick_x)

#plot  top 10  job skills
sns.barplot(data=USA_DA_top_skills, x='median', y=USA_DA_top_skills.index, hue='median', ax=ax[1], palette='dark:b_r')
ax[0].legend().remove()

ax[0].set_title('Top 10 most demand job skills in USA')
ax[0].set_xlabel('')
ax[0].set_ylabel('')
tick_x = plt.FuncFormatter(lambda y, pos: f'${int(y/1000)}K')
plt.gca().xaxis.set_major_formatter(tick_x)

plt.show()
```
### Results

![Likelihood of trending skills for Data Analyst role in 2023 in USA](Images\Highest_PaidMost_Demanded_Skills.png)

# Insights:
- The top graph shows specialized technical skills like dplyr, Bitbucket, and Gitlab are associated with higher salaries, some reaching up to $200K, suggesting that advanced technical proficiency can increase earning potential.

- The bottom graph highlights that foundational skills like Excel, PowerPoint, and SQL are the most in-demand, even though they may not offer the highest salaries. This demonstrates the importance of these core skills for employability in data analysis roles.

- There's a clear distinction between the skills that are highest paid and those that are most in-demand. Data analysts aiming to maximize their career potential should consider developing a diverse skill set that includes both high-paying specialized skills and widely demanded foundational skills.

# What are the most optimal skills to learn for Data Analysts?
To identify the most optimal skills to learn ( the ones that are the highest paid and highest in demand) I calculated the percent of skill demand and the median salary of these skills. To easily identify which are the most optimal skills to learn.

# View the source code
[Optimal Skills.py](optimal_skills.py)


### Visualization code snippet
```
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
```
### Results

![Most Optimal Skills for Data Analysts in the US](Images\Most_Optimal_Skill.png)

# Insights:
- The scatter plot shows that most of the programming skills (colored blue) tend to cluster at higher salary levels compared to other categories, indicating that programming expertise might offer greater salary benefits within the data analytics field.

- The database skills (colored orange), such as Oracle and SQL Server, are associated with some of the highest salaries among data analyst tools. This indicates a significant demand and valuation for data management and manipulation expertise in the industry.

- Analyst tools (colored green), including Tableau and Power BI, are prevalent in job postings and offer competitive salaries, showing that visualization and data analysis software are crucial for current data roles. This category not only has good salaries but is also versatile across different types of data tasks.

# Tools I Used
For my deep dive into the data analyst job market, I harnessed the power of several key tools:

- Python: The backbone of my analysis, allowing me to analyze the data and find critical insights.I also used the following Python libraries:
    - Pandas Library: This was used to analyze the data.
    - Matplotlib Library: I visualized the data.
    - Seaborn Library: Helped me create more advanced visuals.
    - Visual Studio Code: My go-to for executing my Python scripts.
    - Git & GitHub: Essential for version control and sharing my Python code and analysis, ensuring collaboration and project tracking.

# Insights
This project provided several general insights into the data job market for analysts:

Skill Demand and Salary Correlation: There is a clear correlation between the demand for specific skills and the salaries these skills command. Advanced and specialized skills like Python and Oracle often lead to higher salaries.
Market Trends: There are changing trends in skill demand, highlighting the dynamic nature of the data job market. Keeping up with these trends is essential for career growth in data analytics.
Economic Value of Skills: Understanding which skills are both in-demand and well-compensated can guide data analysts in prioritizing learning to maximize their economic returns. 

# Conclusion
This exploration into the data analyst job market has been incredibly informative, highlighting the critical skills and trends that shape this evolving field. The insights I got enhance my understanding and provide actionable guidance for anyone looking to advance their career in data analytics. As the market continues to change, ongoing analysis will be essential to stay ahead in data analytics. This project is a good foundation for future explorations and underscores the importance of continuous learning and adaptation in the data field.