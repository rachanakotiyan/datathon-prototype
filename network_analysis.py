import sqlite3
import pandas as pd
import networkx as nx
import warnings

warnings.filterwarnings('ignore')

print("1. Connecting to the Chicago Crime Database...")
conn = sqlite3.connect('chicago_crime_analytics.db')

print("2. Fetching suspect and victim data...")
# We ignore rows where the suspect is "Unknown" because we can't link a ghost
query = """
SELECT incident_id, suspect_name, victim_name, district
FROM crime_incidents
WHERE suspect_name != 'Unknown'
"""
df = pd.read_sql_query(query, conn)
print(f"Loaded {len(df)} records for Network Analysis.")

print("3. Building the Criminal Network Graph...")
G = nx.Graph()

# Loop through the data to draw the connections (Edges)
for _, row in df.iterrows():
    suspect = row['suspect_name']
    victim = row['victim_name']
    
    # We add 'District ' as a prefix so it doesn't get confused with a person's name
    district_node = f"District {row['district']}"

    # Connect the suspect to the victim
    G.add_edge(suspect, victim, relationship='targeted')
    # Connect the suspect to the district they operated in
    G.add_edge(suspect, district_node, relationship='operated_in')

print(f"Network successfully built with {G.number_of_nodes()} unique nodes and {G.number_of_edges()} links.")

print("4. Calculating 'Kingpin' Scores (Degree Centrality)...")
# This algorithm finds the most connected nodes in the entire web
centrality = nx.degree_centrality(G)

# Sort them to find the top 5
top_kingpins = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:5]
print("\n--- Top 5 Most Connected Entities ---")
for entity, score in top_kingpins:
    print(f"{entity}: Score {score:.4f}")

print("\n5. Saving Network to Database for the Dashboard...")
# Save the Nodes (People/Places)
nodes_df = pd.DataFrame([
    {'node_id': node, 'centrality_score': score}
    for node, score in centrality.items()
])
nodes_df.to_sql('network_nodes', conn, if_exists='replace', index=False)

# Save the Edges (The links between them)
edges = []
for u, v, data in G.edges(data=True):
    edges.append({'source': u, 'target': v, 'relationship': data.get('relationship', 'unknown')})
    
edges_df = pd.DataFrame(edges)
edges_df.to_sql('network_edges', conn, if_exists='replace', index=False)

conn.close()
print("Success! Network connections saved to the database.")