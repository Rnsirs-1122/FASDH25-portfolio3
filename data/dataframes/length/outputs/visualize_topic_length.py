import pandas as pd
import plotly.express as px

# Load the cleaned and filtered dataset created during the exploration phase
merged_top = pd.read_csv("outputs/merged_top_5.csv")


# VISUALIZATION 1: Average Article Length Over Time for Top 5 Topics
# Group the data by date and topic, and calculate the average article length
topic_monthly_avg = merged_top.groupby(["date", "Topic_Label"])["length"].mean().reset_index()

# Create a line chart to show how article length changes over time for each topic
fig1 = px.line(
    topic_monthly_avg,
    x="date",
    y="length",
    color="Topic_Label",
    title="Average Article Length Over Time by Top 5 Topics",
    labels={"length": "Average Length", "date": "Date", "Topic_Label": "Topic"},
    markers=True  # Adds dots at each data point for clarity
)

# Save the chart as an interactive HTML file
fig1.write_html("outputs/Akram-avg-length-by-topic.html")
fig1.show()



# VISUALIZATION 2: Distribution of Article Length Categories by Topic
# Count how many articles fall into each length category (Short, Medium, Long) for each topic
length_dist = merged_top.groupby(["Topic_Label", "length_type_v1"]).size().reset_index(name="count")

# Create a grouped bar chart to compare length types across topics
fig2 = px.bar(
    length_dist,
    x="Topic_Label",
    y="count",
    color="length_type_v1",
    title="Distribution of Article Length Types Within Top 5 Topics",
    labels={"count": "Number of Articles", "length_type_v1": "Length Category"},
    barmode="group"  # Show bars side-by-side for comparison
)

fig2.write_html("outputs/Akram-length-distribution-by-topic.html")
fig2.show()



# VISUALIZATION 3: Article Count by Topic Over Years
# Count the number of articles for each topic, grouped by year
topic_year_counts = merged_top.groupby(["year", "Topic_Label"]).size().reset_index(name="count")

# Create a line chart to show how topic popularity (by article count) changes over time
fig3 = px.line(
    topic_year_counts,
    x="year",
    y="count",
    color="Topic_Label",
    markers=True,
    title="Article Counts by Topic Over Years (Top 5 Topics)",
    labels={"count": "Number of Articles", "year": "Year", "Topic_Label": "Topic"}
)

fig3.write_html("outputs/Akram-line-topic-year.html")
fig3.show()



# VISUALIZATION 4: Pie Chart of Length Category (Top Topics Only)
# Make a pie chart showing the overall share of each article length category
fig4 = px.pie(
    merged_top,
    names="length_type_v1",
    title="Overall Article Length Distribution (Top 5 Topics)"
)

fig4.write_html("outputs/Akram-overall-length-pie.html")
fig4.show()



# VISUALIZATION 5: Average Article Length per Topic (Top 5 Topics)
# Calculate the average article length for each topic
avg_length_topic = merged_top.groupby("Topic_Label")["length"].mean().reset_index()

# Create a bar chart to show which topics tend to have longer or shorter articles
fig5 = px.bar(
    avg_length_topic,
    x="Topic_Label",
    y="length",
    title="Average Article Length per Topic (Top 5 Topics)",
    labels={"length": "Average Length", "Topic_Label": "Topic"},
    text_auto=True  # Display exact length values on top of each bar
)

fig5.write_html("outputs/Akram-avg-length-per-topic.html")
fig5.show()

