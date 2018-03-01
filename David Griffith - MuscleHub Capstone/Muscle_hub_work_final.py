from codecademySQL import sql_query

import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from scipy.stats import chi2_contingency

df = sql_query('''
SELECT visits.first_name,
       visits.last_name,
       visits.visit_date,
       fitness_tests.fitness_test_date,
       applications.application_date,
       purchases.purchase_date
FROM visits
LEFT JOIN fitness_tests
    ON fitness_tests.first_name = visits.first_name
    AND fitness_tests.last_name = visits.last_name
    AND fitness_tests.email = visits.email
LEFT JOIN applications
    ON applications.first_name = visits.first_name
    AND applications.last_name = visits.last_name
    AND applications.email = visits.email
LEFT JOIN purchases
    ON purchases.first_name = visits.first_name
    AND purchases.last_name = visits.last_name
    AND purchases.email = visits.email
WHERE visits.visit_date >= '7-1-17'
''')

# -----------------------------------------------------------------------------------------------------------------------

##analysis of data

# initial outline of test defining a vs b
df['ab_test_group'] = df.fitness_test_date.apply(lambda x: "B" if x == None else "A")

ab_counts = df.groupby("ab_test_group").first_name.count()

# dimensions for the pie
labels = "A", "B"

# a vs b pie chart showing a nice 50/50 split
plt.pie(ab_counts, autopct='%0.1f%%')
plt.legend(labels)
plt.axis('equal')
plt.show()
# -----------------------------------------------------------------------------------------------------------------------

# 4 Who picks up an application
##applications

df['is_application'] = df.application_date.apply(lambda x: "No_Application" if x == None else "Application")

app_counts = df.groupby(['ab_test_group', 'is_application']).first_name.count().reset_index()

app_pivot = app_counts.pivot(columns='is_application', index='ab_test_group', values='first_name').reset_index()

app_pivot['total'] = app_pivot.Application + app_pivot.No_Application

app_pivot['percentage'] = (app_pivot.Application / app_pivot.total)

# is_application ab_test_group  Application  No_Application  total  percentage
# 0                          A          250            2254   2504    9.984026
# 1                          B          325            2175   2500   13.000000

test1 = [[250, 2254],
         [325, 2175]]
results_test1 = chi2_contingency(test1)

# pval - 0.000964782760072 therefore there is a signficant difference between A and B for Applications vs no

# -----------------------------------------------------------------------------------------------------------------------

## MEMBER ANALYISIS
df['is_member'] = df.purchase_date.apply(lambda x: "Not_Member" if x == None else "Member")

just_apps = df[df.is_application == 'Application']

member_counts = just_apps.groupby(['ab_test_group', 'is_member']).first_name.count().reset_index()

member_pivot = member_counts.pivot(columns='is_member', index='ab_test_group', values='first_name').reset_index()

member_pivot['total'] = member_pivot.Member + member_pivot.Not_Member

member_pivot['percentage'] = (member_pivot.Member / member_pivot.total)

###
# is_member ab_test_group  Member  Not_Member  total  percentage
# 0                     A     200          50    250   80.000000
# 1                     B     250          75    325   76.923077

test2 = [[200, 50],
         [250, 75]]
results_test2 = chi2_contingency(test2)

# pvalue 0.43258646051083327 difference is not significant

# -----------------------------------------------------------------------------------------------------------------------

##Overall member stuff

df['is_member'] = df.purchase_date.apply(lambda x: "Not_Member" if x == None else "Member")

final_member_counts = df.groupby(['ab_test_group', 'is_member']).first_name.count().reset_index()

final_member_pivot = final_member_counts.pivot(columns='is_member', index='ab_test_group',
                                                      values='first_name').reset_index()

final_member_pivot['total'] = final_member_pivot.Member + final_member_pivot.Not_Member

final_member_pivot['percentage'] = (final_member_pivot.Member / final_member_pivot.total)

# final memeber numbers
# is_member ab_test_group  Member  Not_Member  total  percentage
# 0                     A     200        2304   2504     7.98722
# 1                     B     250        2250   2500    10.00000

test3 = [[200, 2304],
         [250, 2250]]
results_test3 = chi2_contingency(test3)

##pvalue 0.014724114645783203 results are significant

# -----------------------------------------------------------------------------------------------------------------------

## GRAPH TIME!!!

# test 1 bar
plt.bar(range(len(app_pivot)), app_pivot['percentage'].values)
plt.title('% Visit -> Application')
ax = plt.subplot()
ax.set_xticks(range(len(app_pivot)))
ax.set_xticklabels(['Fitness Test', 'No Fitness Test'])
ax.set_yticks([0, 0.05, 0.10, 0.15, 0.20])
ax.set_yticklabels(['0%', '5%', '10%', '15%', '20%'])
plt.show()

plt.bar(range(len(member_pivot)), member_pivot['percentage'].values)
plt.title('% of Application -> Member')
ax = plt.subplot()
ax.set_xticks(range(len(member_pivot)))
ax.set_xticklabels(['Fitness Test', 'No Fitness Test'])
ax.set_yticks([0, 0.25, 0.50, 0.75, 1])
ax.set_yticklabels(['0%', '25%', '50%', '75%', '100%'])
plt.show()

plt.bar(range(len(final_member_pivot)), final_member_pivot['percentage'].values)
plt.title('% Total Visit -> Member')
ax = plt.subplot()
ax.set_xticks(range(len(final_member_pivot)))
ax.set_xticklabels(['Fitness Test', 'No Fitness Test'])
ax.set_yticks([0, 0.05, 0.10, 0.15, 0.20])
ax.set_yticklabels(['0%', '5%', '10%', '15%', '20%'])
plt.show()