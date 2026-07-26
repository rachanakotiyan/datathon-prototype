import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import sqlite3
import dash_cytoscape as cyto
import joblib
from datetime import datetime

print("1. Connecting to the AI Database...")
conn = sqlite3.connect('chicago_crime_analytics.db')

# Pulling Hotspot Data
query = """
SELECT c.latitude, c.longitude, c.crime_type, c.district, h.hotspot_cluster
FROM crime_incidents c
JOIN ai_hotspot_insights h ON c.incident_id = h.incident_id
"""
df = pd.read_sql_query(query, conn)
df['hotspot_cluster'] = "Hotspot " + df['hotspot_cluster'].astype(str)

print("2. Generating AI Hotspot Map...")
# Dark theme map with blood red, stark white, and charcoal cluster colors
fig = px.scatter_mapbox(
    df, lat="latitude", lon="longitude", color="hotspot_cluster",
    hover_name="crime_type", hover_data=["district"], zoom=10,
    mapbox_style="carto-darkmatter", title="CLASSIFIED: AI CRIME CLUSTERS",
    color_discrete_sequence=['#e74c3c', '#8b0000', '#ffffff', '#bdc3c7', '#34495e', '#c0392b', '#7f8c8d', '#2c3e50']
)
fig.update_traces(marker=dict(size=7, opacity=0.85))
fig.update_layout(
    margin={"r":0,"t":50,"l":0,"b":0},
    paper_bgcolor="#0d0d0d",
    plot_bgcolor="#0d0d0d",
    font=dict(color="#ffffff", family="Courier New, monospace"), # Changed to pure white
    title_font=dict(size=18, color="#e74c3c"),
    hoverlabel=dict(
        bgcolor="#121212",
        font_size=14,
        font_color="#ffffff", # Ensures tooltips are also pure white
        bordercolor="#e74c3c"
    )
)

print("3. Generating Criminal Network Web...")
edges_query = "SELECT source, target, relationship FROM network_edges LIMIT 150"
edges_df = pd.read_sql_query(edges_query, conn)
conn.close()

network_elements = []
unique_nodes = set()
for _, row in edges_df.iterrows():
    source = row['source']
    target = row['target']
    if source not in unique_nodes:
        network_elements.append({'data': {'id': source, 'label': source}})
        unique_nodes.add(source)
    if target not in unique_nodes:
        network_elements.append({'data': {'id': target, 'label': target}})
        unique_nodes.add(target)
    network_elements.append({'data': {'source': source, 'target': target}})

print("4. Loading Predictive AI Model...")
# Load the brain we trained on Day 1
rf_model = joblib.load('predictive_risk_model.pkl')
le_district = joblib.load('district_encoder.pkl')

# Get unique districts for the dropdown menu
available_districts = sorted(df['district'].dropna().unique())

print("5. Launching Web Server...")
app = dash.Dash(__name__)
server = app.server  # <--- GUNICORN LOOKS FOR THIS EXACT VARIABLE

# THEME SETTINGS: Dark mode, Courier font, Red accents
app.layout = html.Div(style={'fontFamily': 'Courier New, monospace', 'padding': '30px', 'backgroundColor': '#050505', 'color': '#e0e0e0', 'minHeight': '100vh'}, children=[
    
    # --- HEADER ---
    html.H1("L-ARCHIVE: STRATEGIC INTELLIGENCE HUB", style={'textAlign': 'center', 'color': '#e74c3c', 'letterSpacing': '4px', 'fontWeight': 'bold', 'textShadow': '0 0 10px rgba(231, 76, 60, 0.3)'}),
    html.P("CONFIDENTIAL // Live AI Spatiotemporal Analytics & Predictive Policing", style={'textAlign': 'center', 'color': '#7F8C8D', 'letterSpacing': '2px', 'marginBottom': '40px'}),
    
    # --- Predictive AI Panel ---
    html.Div(style={'backgroundColor': '#121212', 'padding': '25px', 'borderRadius': '5px', 'border': '1px solid #333', 'boxShadow': '0 0 20px rgba(231, 76, 60, 0.1)', 'marginBottom': '40px'}, children=[
        html.H3("💀 PREDICTIVE RISK ENGINE", style={'color': '#c0392b', 'marginTop': '0', 'borderBottom': '1px solid #333', 'paddingBottom': '10px'}),
        html.P("INPUT PARAMETERS TO FORECAST HIGH-RISK INCIDENT PROBABILITY.", style={'color': '#bdc3c7', 'fontSize': '14px'}),
        
        html.Div(style={'display': 'flex', 'gap': '30px', 'marginTop': '20px'}, children=[
            html.Div(style={'flex': '1'}, children=[
                html.Label("SELECT SECTOR (DISTRICT):", style={'color': '#e74c3c', 'fontWeight': 'bold', 'marginBottom': '10px', 'display': 'block'}),
                html.Div(style={'color': '#000'}, children=[ # Keep text black inside dropdown for readability
                    dcc.Dropdown(
                        id='district-dropdown',
                        options=[{'label': f"DISTRICT {d}", 'value': d} for d in available_districts],
                        value=available_districts[0] if len(available_districts) > 0 else None
                    )
                ])
            ]),
            html.Div(style={'flex': '1'}, children=[
                html.Label("TIME OF DAY (HOUR):", style={'color': '#e74c3c', 'fontWeight': 'bold', 'marginBottom': '10px', 'display': 'block'}),
                dcc.Slider(
                    id='hour-slider', min=0, max=23, step=1, value=12,
                    marks={i: {'label': f'{i}:00', 'style': {'color': '#bdc3c7'}} for i in range(0, 24, 4)}
                )
            ])
        ]),
        
        # This is where the AI outputs its prediction
        html.Div(id='risk-output', style={'marginTop': '30px', 'fontSize': '28px', 'fontWeight': 'bold', 'textAlign': 'center', 'letterSpacing': '2px'})
    ]),
    
    # --- The Map ---
    html.Div([
        dcc.Graph(figure=fig, style={'height': '65vh', 'borderRadius': '5px', 'border': '1px solid #333', 'boxShadow': '0 0 20px rgba(0,0,0,0.5)'})
    ], style={'marginBottom': '50px'}),
    
    # --- The Network Graph ---
    html.H2("CRIMINAL NETWORK LINK ANALYSIS", style={'textAlign': 'center', 'color': '#e74c3c', 'letterSpacing': '2px'}),
    html.P("IDENTIFYING SUSPECT-VICTIM SYNDICATES", style={'textAlign': 'center', 'color': '#7F8C8D', 'letterSpacing': '1px'}),
    html.Div([
        cyto.Cytoscape(
            id='cytoscape-network',
            layout={'name': 'cose'},
            style={'width': '100%', 'height': '550px'},
            elements=network_elements,
            stylesheet=[
                {'selector': 'node', 'style': {
                    'label': 'data(label)', 
                    'background-color': '#8b0000', 
                    'color': '#ffffff', 
                    'font-family': 'Courier New, monospace',
                    'font-size': '12px',
                    'text-outline-width': 1,
                    'text-outline-color': '#000000'
                }},
                {'selector': 'edge', 'style': {
                    'line-color': '#444444', 
                    'width': 1, 
                    'opacity': 0.8
                }}
            ]
        )
    ], style={'backgroundColor': '#0d0d0d', 'borderRadius': '5px', 'border': '1px solid #333', 'boxShadow': '0 0 20px rgba(0,0,0,0.5)', 'padding': '20px', 'marginBottom': '50px', 'backgroundImage': 'radial-gradient(#1a1a1a 1px, transparent 1px)', 'backgroundSize': '20px 20px'}),
    
    # --- Model Diagnostics Panel ---
    html.H2("AI DIAGNOSTICS & TELEMETRY", style={'textAlign': 'center', 'color': '#e74c3c', 'letterSpacing': '2px', 'marginTop': '40px'}),
    html.P("RANDOM FOREST CLASSIFIER EVALUATION (TEST SPLIT: 20%)", style={'textAlign': 'center', 'color': '#7F8C8D'}),
    html.Div(style={'display': 'flex', 'justifyContent': 'space-around', 'backgroundColor': '#121212', 'padding': '30px', 'borderRadius': '5px', 'border': '1px solid #333', 'boxShadow': '0 0 20px rgba(231, 76, 60, 0.05)', 'marginBottom': '20px'}, children=[
        html.Div([html.H4("ACCURACY", style={'color': '#bdc3c7', 'letterSpacing': '1px'}), html.H2("82.4%", style={'color': '#ecf0f1', 'textShadow': '0 0 10px rgba(255,255,255,0.2)'})], style={'textAlign': 'center'}),
        html.Div([html.H4("PRECISION (HIGH RISK)", style={'color': '#bdc3c7', 'letterSpacing': '1px'}), html.H2("79.1%", style={'color': '#e74c3c', 'textShadow': '0 0 10px rgba(231, 76, 60, 0.4)'})], style={'textAlign': 'center'}),
        html.Div([html.H4("RECALL (HIGH RISK)", style={'color': '#bdc3c7', 'letterSpacing': '1px'}), html.H2("85.3%", style={'color': '#c0392b', 'textShadow': '0 0 10px rgba(192, 57, 43, 0.4)'})], style={'textAlign': 'center'}),
    ])
])

# --- The "Wiring" (Dash Callbacks) ---
@app.callback(
    Output('risk-output', 'children'),
    [Input('district-dropdown', 'value'),
     Input('hour-slider', 'value')]
)
def update_risk_prediction(district, hour):
    if district is None:
        return "AWAITING SECTOR INPUT..."
    
    try:
        # Translate the district back into the number the AI understands
        encoded_district = le_district.transform([str(district)])[0]
        
        # We use today's month and day of week to make the prediction feel live
        current_month = datetime.now().month
        current_day = datetime.now().weekday()
        
        # Create a DataFrame with the exact column names the AI was trained on to fix the warning
       # Inside your callback:
        input_data = pd.DataFrame(
        [[avg_lat, avg_lon, hour, current_month, encoded_district]], 
        columns=['latitude', 'longitude', 'hour', 'month', 'district_encoded']
        )
        
        # Ask the Random Forest model for a prediction
        risk_probability = rf_model.predict_proba(input_data)[0][1]
        risk_percentage = round(risk_probability * 100, 2)
        
        # Change color based on severity (Death note theme colors)
        color = "#ffffff" if risk_percentage < 30 else "#e67e22" if risk_percentage < 60 else "#ff0000"
        status = "LOW PRIORITY" if risk_percentage < 30 else "ELEVATED RISK" if risk_percentage < 60 else "CRITICAL THREAT DETECTED"
        
        return html.Span(f"[{status}] PROBABILITY: {risk_percentage}%", style={'color': color, 'textShadow': f'0 0 10px {color}'})
    
    except Exception as e:
        return f"SYSTEM ERROR: {str(e)}"

import os

# ... keep your app layout and callbacks ...

# Gunicorn needs to see 'server' at the module level
server = app.server 

if __name__ == '__main__':
    # You can just use the standard run_server. 
    # Render's Gunicorn command will override this anyway.
    app.run_server(debug=False)

