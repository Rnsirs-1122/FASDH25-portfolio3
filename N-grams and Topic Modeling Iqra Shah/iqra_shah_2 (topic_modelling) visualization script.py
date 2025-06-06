import pandas as pd
import plotly.express as px

# This code uses pd.set_option to adjust display settings so all columns and rows are fully visible when printed.
# It then selects specific columns related to the topic model and removes duplicate rows using drop_duplicates()
# to ensure only unique topic-word combinations are shown in the output.
# AI-guided: see AI_documentation for this code only
pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows', None)

# Load the CSV file
df = pd.read_csv(r'C:/Users/Haroon Traders/Downloads/FASDH25-portfolio3/data/dataframes/topic-model/topic-model.csv')
print(df[["Topic", "topic_1", "topic_2", "topic_3", "topic_4","Count"]].drop_duplicates())

# It will make a date column
df['date'] = pd.to_datetime({
    'year':df['year'],
    'month':df['month'],
    'day':1})

# Drop rows with invalid topic number
df_filtered = df[df['Topic'] != -1]

# Manually inspect the 4 topic word columns to identify relevant topics
# look for words like 'gaza', 'rocket', etc. that are related to the trigram exercise
relevant_topic_nums = [13, 24, 44, 73]

# Filter to keep only relevant topic numbers
df_filtered = df[df['Topic'].isin(relevant_topic_nums)].copy()

# Format date as "Month Year" for x-axis
df_filtered['Month-Year'] = df_filtered['date'].dt.to_period('M').astype(str)

# Group by Month-Year and Topic
topic_time_counts = df_filtered.groupby(['Month-Year', 'Topic']).size().reset_index(name='Article_Count')

topic_time_counts = topic_time_counts.sort_values(by='Month-Year')

# Create Topic_Label in df_filtered
df_filtered['Topic_Label'] = df_filtered[['topic_1', 'topic_2', 'topic_3', 'topic_4']].agg(', '.join, axis=1)

# Create a mapping from Topic number to label
topic_label_map = df_filtered[['Topic', 'Topic_Label']].drop_duplicates().set_index('Topic')['Topic_Label'].to_dict()

# Map the label to topic_time_counts
topic_time_counts['Topic_Label'] = topic_time_counts['Topic'].map(topic_label_map)


# Plot a group bar chart
fig = px.bar(
    topic_time_counts,
    x='Month-Year',
    y='Article_Count',
    color= 'Topic_Label',
    barmode= 'group',
    text='Article_Count',
    title='Frequency of the Topics Related to Trigram Themes',
    labels={'Topic': 'Topic Number', 'Article_Count': 'Number of Articles'}
)
fig.update_traces(textposition='outside')
fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')


# Show and save the chart
fig.show()
fig.write_html("Iqra_Shah_relevant_topics to trigrams_bar_chart.html")
print("Bar chart saved as Iqra_Shah_relevant_topics to trigrams_bar_chart.html")



