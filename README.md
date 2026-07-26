# **L-Archive: Strategic Intelligence Hub 🚨**

**L-Archive** is an AI-driven spatiotemporal analytics and predictive policing platform built as a hackathon prototype. It transforms raw, static crime data into an interactive intelligence dashboard. By combining geospatial analysis, network theory, Natural Language Processing (NLP), and machine learning, this platform demonstrates how crime incidents can be analyzed from multiple angles to shift law enforcement strategies from *reactive* to *proactive*.

## **The Problem Statement**

Current law enforcement data systems often act merely as digital filing cabinets. Because crime data is overwhelmingly raw, unstructured, and siloed, analysts struggle to interpret it quickly. This makes it incredibly difficult to:

* See the "big picture" regarding where crimes are clustering.  
* Uncover hidden relationships between repeat offenders, victims, and operational territories.  
* Extract actionable patterns from messy, unstructured incident narratives.  
* Anticipate and deploy resources *before* high-risk crimes occur.

## **What This Solution Does**

L-Archive acts as a 4-pillar predictive intelligence pipeline that solves these issues:

1. **Spatial AI (Automated Hotspot Detection):** Uses the *K-Means Clustering* algorithm to automatically group thousands of GPS coordinates, drawing boundaries around high-density crime zones.  
2. **Network Link Analysis (Syndicate Mapping):** Leverages *Graph Theory* to visually map out relationships, instantly exposing hidden connections between suspects, victims, and specific districts.  
3. **NLP Modus Operandi (MO) Extraction:** Implements *TF-IDF* vectorization to read through unstructured police report narratives and automatically extract key terms that define the criminal's Modus Operandi.  
4. **Predictive Risk Engine (Forecasting):** Powered by a *Random Forest Classifier*, this engine allows officers to input specific parameters (time/location) to estimate the probability of a high-risk violent incident occurring.

## 

## **Key Features & Functionalities**

* **Interactive Command Dashboard:** A sleek, dark-themed UI built for exploring macro-level crime patterns seamlessly.  
* **Dynamic Geospatial Mapping:** High-contrast hotspot maps providing clustered geographic insights for optimized patrol routing.  
* **Relational "Spider Web" Graphs:** Interactive network visualization uncovering suspect-victim-district syndicates.  
* **Real-Time Predictive Forecasting:** Instant risk probability scoring based on historical spatiotemporal factors.  
* **Unified SQLite Architecture:** A robust backend workflow ensuring analysis can be queried and reused easily, completely eliminating data silos.

## **Tech Stack**

The platform was engineered as an integrated, full-stack Python ecosystem:

* **Backend & Data Engineering:** Python, Pandas, SQLite  
* **Machine Learning & AI:** Scikit-Learn, NetworkX, Natural Language Toolkit (NLTK/TF-IDF)  
* **Frontend & Visualization:** Plotly, Dash, Dash-Cytoscape  
* **Deployment & Serialization:** Joblib, Gunicorn

## **Project Structure**

* dashboard.py – The main controller; launches the Plotly Dash UI and displays visual outputs.  
* hotspot\_clustering.py – Executes the spatial AI hotspot detection model.  
* network\_analysis.py – Builds and saves the criminal network centrality graph.  
* nlp\_mo\_extraction.py – Extracts MO keywords from unstructured narratives.  
* predictive\_risk\_model.py – Trains, evaluates, and saves the Random Forest prediction model.  
* chicago\_crime\_analytics.db – The unified SQLite database used by the AI engine.  
* chicago\_crimes.csv & 01\_District\_wise\_crimes\_committed\_IPC\_2001\_2012.csv – Reference data sources.  
* requirements.txt – Core Python dependencies.

## **Setup & Installation**

**1\. Create and activate a Python virtual environment:**

python \-m venv env  
source env/bin/activate  \# On Windows use: env\\Scripts\\activate

**2\. Install dependencies:**

pip install \-r requirements.txt

**3\. Database Verification:**

Ensure the chicago\_crime\_analytics.db SQLite database file is present in your root project folder.

## **Running the AI Pipeline**

Before launching the dashboard, execute the analysis scripts in this exact order to process the data, train the models, and populate the database:

python hotspot\_clustering.py  
python network\_analysis.py  
python nlp\_mo\_extraction.py  
python predictive\_risk\_model.py

## **Launching the Dashboard**

Once the AI pipeline has finished generating insights, start the web application:

python dashboard.py

Open the local URL shown in your terminal (usually http://127.0.0.1:8050/) in your browser to view the live dashboard.

## **Proposed Impact & Use Case** 

This project serves as a strong reference prototype for demonstrating how modern data science can revolutionize public safety. It showcases a complete **end-to-end data flow**:

1. **Ingestion:** Raw, messy data is ingested and structured.  
2. **Analysis:** Meaningful mathematical patterns are extracted via Machine Learning.  
3. **Visualization:** Deep insights are rendered interactively for non-technical end-users.  
4. **Actionable Intelligence:** Predictive telemetry is provided to support proactive, life-saving decision support.

*Note: This is a prototype intended for demonstration, exploration, and hackathon presentation purposes. While not currently a production-grade deployment system, it clearly and effectively showcases the core architectural approach to modern predictive policing.*