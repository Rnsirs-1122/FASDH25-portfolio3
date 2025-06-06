# Import the required library
import pandas as pd

# Load the tf-idf similarity dataset
# This CSV file contains the pairwise similarty scores based on td-idf, between the documents
tfidf_path = r'tfidf\tfidf-over-0.3.csv'             
tfidf_df_data= pd.read_csv(tfidf_path)
 

# Step 1: Explore the loaded data (CSV files)
print("\nColumns in the tf-idf data:", tfidf_df_data.columns.tolist())
print("First 5 rows of tf-idf data:")
print(tfidf_df_data.head())

# Step 2: Create Nodes DataFrame
# Every node represents a document from which we extract metadata like filename
# Extract metadata for the first document in each similarity pair (filename-1, title-1, etc.)
# These columns (year-1, day-1) are necessary for pd.to_datetime to correctly interpret the date
nodes_df1 = tfidf_df_data[['filename-1', 'title-1', 'year-1', 'month-1', 'day-1']].rename(columns={
    'filename-1': 'Id',
    'title-1': 'Label',
    'year-1': 'Year',
    'month-1': 'Month',
    'day-1': 'Day'
})

# Extract the metadata for the second document in each similarity pair, these columns (year-2, day-2) are necessary for pd.to_datetime to correctly interpret the date
nodes_df2 = tfidf_df_data[['filename-2', 'title-2', 'year-2', 'month-2', 'day-2']].rename(columns={
    'filename-2': 'Id',
    'title-2': 'Label',
    'year-2': 'Year',
    'month-2': 'Month',
    'day-2': 'Day'
})

nodes = pd.concat([nodes_df1, nodes_df2]).drop_duplicates(subset=['Id'])

# This line ensures the 'Date' column in your final CSV is month-only ('%m')
nodes['Date'] = pd.to_datetime(nodes[['Year', 'Month', 'Day']]).dt.strftime('%m')

# Keep only the columns needed for Gephi such as the combined 'Date' and drop the individual date columns 
nodes = nodes[['Id', 'Label', 'Month']]

# Step 3: Create Edges DataFrame
# Each edge shows a link between two documents with a similarity score based on TF-IDF
edges =tfidf_df_data[['filename-1', 'filename-2', 'similarity']].rename(columns={
    'filename-1': 'Source',
    'filename-2': 'Target',
    'similarity': 'Weight'
})

# Optional filter to keep the similarity threshold above 0.6, to prevent Gephi from overloading with too many weak links
filtered_edges = edges[edges['Weight'] >= 0.6] # Adjust this threshold!

# Step 4: Export data for Gephi
# Save nodes and filtered edges into CSV files for Gephi import, to present the network visualization
nodes.to_csv('gephi_nodes_month.csv', index=False)
filtered_edges.to_csv('gephi_edges_month.csv', index=False) 


print(f"- gephi_nodes_month.csv")
print(f"- gephi_edges_month.csv")
