# Import required libraries
import pandas as pd
import plotly.express as px

# Step 1: Load the 3-gram dataset from CSV file
file_path = 'C:/Users/Haroon Traders/Downloads/FASDH25-portfolio3/data/dataframes/n-grams/3-gram/3-gram-year.csv'
# Read the CSV into a pandas dataframe
data = pd.read_csv(file_path)
# Printing the 30 most frequent trigrams.
print(data.head(30))


# Step 2: Define specific target trigrams to analyze
# These are the selected phrases relevant to war and humanitarian discourse. 
focus_trigrams = [
    'war on gaza', 
    'the israeli army', 
    'hamas rocket attacks',
    'have been killed',
    'told al jazeera',
]
focus_trigrams = [t.lower() for t in focus_trigrams]

# Convert trigram column to lowercase for consistent matching.
data['3-gram'] = data['3-gram'].str.lower()

# Step 3: Filter for selected trigrams only
filtered = data[data['3-gram'].isin(focus_trigrams)].copy()

# Step 4: Normalize counts within each year to prevent misleading treands and to compute count-sum of selected trigrams.
yearly_totals = filtered.groupby('year')['count-sum'].sum().rename('total_year_mentions')
filtered = filtered.merge(yearly_totals, on='year')
filtered['relative_freq'] = (filtered['count-sum'] / filtered['total_year_mentions']) * 100

# Step 5: Rename columns for clarity in the chart
filtered.rename(columns={'3-gram': 'trigram', 'relative_freq': 'percentage'}, inplace=True)
#Filter only years from 2021 onwards
filtered = filtered[filtered['year'] >= 2021]

# Step 6: Create grouped bar chart
fig = px.bar(
    filtered,
    x='year',
    y='percentage',
    color='trigram',
    barmode='group',
    title='Relative Frequency of Selected 3-Grams by Year (%)',
    labels={'percentage': 'Share of Mentions (%)', 'year': 'Year'},
    color_discrete_sequence=px.colors.qualitative.Vivid
)

# Step 7: Setting the layout of the chart
fig.update_layout(
    xaxis=dict(dtick=1),
    font=dict(size=12),
    title_font=dict(size=18),
    legend_title='3-Gram Themes',
    plot_bgcolor='rgba(255,255,255,1)'
)

# Show and save
fig.show()
fig.write_html("Iqra_Shah_3gram_normalized_grouped_bar.html")
print("Iqra_Shah_3gram_normalized_grouped_bar.html")
