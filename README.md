## Early Detection on Students Failing Projects.

###Overview
This project runs an machine learning approach for early detection based on 289 course projects based on 
an Open Source System project done by graduate students 
in a 500-level computer science course in past five years.

###Files and Data Source
The script _*plot_commits_each_pr.py*_ contains helper methods,
such as interacting with GITHUB api to get the working patterns
and convert into arrays (here I took the first 20 days of the whole 35 periods)
as well as methods (Dynamic Time Wrapping) calculate similarities between arrays, which representing
time series data.

The file _*source_data.py*_ contains preprocessing of test_data, the big vector I read in
is from an [Excel sheet](https://docs.google.com/spreadsheets/d/1llczBevbH0kbtAjKD_XH6BRVRCHZFboJ1V03dG_kPmQ/edit#gid=0).
To omit some irrelevant attributes and merge the 3 decisions on projects' (fully merged, partially merged, rejected) into 2(success, failure).
And convert the Github PR link into times series cluster labels(here I predefined 3 type of time series).

The file _*multinominol_regression.py*_ contains Interfaces to extract the feature parts and label parts from both
training set (*PR_vectors.csv*) and testing set(*test_data.csv*). And trained multinomial logistic regression model
Then tested with last semesters' projects. 
