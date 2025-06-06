import pandas as pd


# Step 1: Load the data


# Load the article length data
length_df = pd.read_csv("C:/Users/DE/Downloads/FASDH25-portfolio3/data/dataframes/length/length.csv")

# Load the topic model data
topic_df = pd.read_csv("C:/Users/DE/Downloads/FASDH25-portfolio3/data/dataframes/topic-model/topic-model.csv")


# Step 2: Get a quick look at the data


# Check how many rows and columns the topic file has
print("Topic data shape:", topic_df.shape)

# Check the column names in each dataset
print("Length columns:", length_df.columns.tolist())
print("Topic columns:", topic_df.columns.tolist())

# See how many articles are assigned to each topic
print(topic_df["Topic"].value_counts())


# Step 3: Clean the topic data


# Remove rows with unassigned topics (marked as -1)
topic_df = topic_df[topic_df["Topic"] != -1]

# Combine topic keywords into one readable label (e.g., "conflict, war, army, soldiers")
topic_df["Topic_Label"] = topic_df[["topic_1", "topic_2", "topic_3", "topic_4"]].agg(", ".join, axis=1)


# Step 4: Merge the two datasets


# Combine length and topic data based on year, month, and day
merged = pd.merge(length_df, topic_df, on=["year", "month", "day"], how="inner")


# Step 5: Categorize article lengths


# Define a function to label articles as Short, Medium, or Long
def categorize_length(length):
    if length < 300:
        return "Short (<300)"
    elif length <= 800:
        return "Medium (300–800)"
    else:
        return "Long (>800)"

# Apply the function to create a new column
merged["length_type_v1"] = merged["length"].apply(categorize_length)


# Step 6: Create a readable date column


# Combine year and month into a date column (like "2023-01")
merged["date"] = pd.to_datetime(merged["year"].astype(str) + "-" + merged["month"].astype(str).str.zfill(2))


# Step 7: Explore topic popularity


# Count how many articles are in each topic
topic_counts = merged["Topic_Label"].value_counts().reset_index()
topic_counts.columns = ["Topic_Label", "Total_Count"]

# Print out the most common topics
print("Top topics by count:")
print(topic_counts.head(10))


# Step 8: Focus on the Top 5 topics


# Get the top 5 most frequent topic labels
top_5_topics = topic_counts["Topic_Label"].head(5).tolist()

# Filter the merged dataset to only include those top 5
merged_top = merged[merged["Topic_Label"].isin(top_5_topics)]

# Check the size of this filtered dataset
print("Filtered shape for top 5 topics:", merged_top.shape)


# Step 9: Save the cleaned & filtered data for next script


# Save the data to a CSV so we can use it in the presentation script
merged_top.to_csv("outputs/merged_top_5.csv", index=False)


