# Global Airport Network Resilience Analysis

This project analyses the structure, connectivity, community organisation, and resilience of the global airport network using graph theory and network analysis.

The project constructs a directed airport-route network from the OpenFlights airport and route datasets and investigates how the network responds to random and targeted airport removals.

## Research Question

**How resilient is the global airport network to airport failures, and which airports are most critical for maintaining network connectivity?**

## Objectives

- Construct a global airport-route network from real-world data.
- Analyse the structural properties of the network.
- Identify highly connected and structurally important airports.
- Detect communities within the global airport network.
- Compare network response to random and targeted airport failures.
- Examine whether airports with high degree centrality and betweenness centrality play different structural roles.

## Notebook Workflow

Run the notebooks in the following order from the `Notebooks` folder:

1. `01_Data_Exploration.ipynb` — dataset structure and data-quality checks.
2. `02_Graph_Construction.ipynb` — directed airport-route network construction and validation.
3. `03_Basic_Network_Analysis.ipynb` — network-level metrics and degree-based analysis.
4. `04_Centrality_Analysis.ipynb` — degree, PageRank, and betweenness centrality.
5. `05_Geographic_Visualization.ipynb` — geographic distribution of airports and major hubs.
6. `06_Communities_and_Resilience.ipynb` — community detection, random failures, targeted hub failures, and resilience analysis.

## Methods

The analysis uses:

- Graph construction using NetworkX
- Degree and degree centrality
- PageRank
- Betweenness centrality
- Louvain community detection
- Random airport failure simulations
- Degree-targeted airport removal
- Betweenness-targeted airport removal
- Largest connected component analysis
- Geographic visualisation

## Key Network Analysis

The constructed network contains thousands of airports and tens of thousands of route connections.

The analysis examines:

- network connectivity
- degree distribution
- highly connected hub airports
- centrality rankings
- community structure
- size of the largest connected component under airport removals

## Resilience Analysis

Two types of failure scenarios are considered.

### Random failures

Airports are removed randomly at different failure levels. The experiment is repeated across multiple trials to reduce dependence on one particular random selection.

### Targeted failures

Airports are removed according to structural importance, using:

- degree centrality
- betweenness centrality

The size of the largest connected component is then measured after each removal level.

This provides a structural comparison between random failures and targeted disruption of important network nodes.

> These simulations represent graph-theoretic failure scenarios and are not predictions of actual aviation disruptions.

## Community Detection

The Louvain algorithm is used to identify groups of airports with comparatively dense internal connectivity.

The resulting communities reveal strong geographic and regional structure in the global airport network.

## Project Structure

```text
global-airport-network-resilience/
│
├── Data/
│   ├── airports.dat
│   └── routes.dat
│
├── Notebooks/
│   ├── 01_Data_Exploration.ipynb
│   ├── 02_Graph_Construction.ipynb
│   ├── 03_Basic_Network_Analysis.ipynb
│   ├── 04_Centrality_Analysis.ipynb
│   ├── 05_Geographic_Visualization.ipynb
│   └── 06_Communities_and_Resilience.ipynb
│
├── Figures/
│
├── Reports/
│
├── src/
│   ├── graph_builder.py
│   └── run_analysis.py
│
├── README.md
├── requirements.txt
└── .gitignore
