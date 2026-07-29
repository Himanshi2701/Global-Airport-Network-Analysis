"""Utilities for constructing and analysing the OpenFlights airport network."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import networkx as nx
import pandas as pd


AIRPORT_COLUMNS = [
    "airport_id", "name", "city", "country", "iata", "icao", "latitude",
    "longitude", "altitude", "timezone", "dst", "tz_database", "type", "source",
]
ROUTE_COLUMNS = [
    "airline", "airline_id", "source_iata", "source_airport_id",
    "destination_iata", "destination_airport_id", "codeshare", "stops", "equipment",
]
DEFAULT_DATA_DIR = Path(__file__).resolve().parents[1] / "Data"


def load_data(data_dir: str | Path = DEFAULT_DATA_DIR) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load and clean the OpenFlights airport and route files.

    Invalid ``\\N`` identifiers are converted to missing values so they cannot become
    artificial nodes in the network.
    """
    data_dir = Path(data_dir)
    airports = pd.read_csv(data_dir / "airports.dat", header=None, names=AIRPORT_COLUMNS)
    routes = pd.read_csv(data_dir / "routes.dat", header=None, names=ROUTE_COLUMNS)

    airports["airport_id"] = pd.to_numeric(airports["airport_id"], errors="coerce")
    airports = airports.dropna(subset=["airport_id"]).copy()
    airports["airport_id"] = airports["airport_id"].astype(int)

    for column in ("source_airport_id", "destination_airport_id", "stops"):
        routes[column] = pd.to_numeric(routes[column], errors="coerce")
    routes = routes.dropna(subset=["source_airport_id", "destination_airport_id"]).copy()
    routes[["source_airport_id", "destination_airport_id"]] = routes[
        ["source_airport_id", "destination_airport_id"]
    ].astype(int)
    return airports, routes


def build_graph(
    data_dir: str | Path = DEFAULT_DATA_DIR,
    *,
    include_isolated: bool = False,
) -> nx.DiGraph:
    """Build a directed airport network from the bundled OpenFlights data.

    Each edge is a distinct origin-destination pair.  The ``airlines`` edge attribute
    contains every airline recorded on that pair, while ``route_count`` records how
    many source rows were collapsed into the edge.
    """
    airports, routes = load_data(data_dir)
    airport_ids = set(airports["airport_id"])
    routes = routes[
        routes["source_airport_id"].isin(airport_ids)
        & routes["destination_airport_id"].isin(airport_ids)
    ]

    graph = nx.DiGraph()
    if include_isolated:
        node_airports = airports
    else:
        used_ids = set(routes["source_airport_id"]) | set(routes["destination_airport_id"])
        node_airports = airports[airports["airport_id"].isin(used_ids)]

    for airport in node_airports.to_dict("records"):
        airport_id = airport.pop("airport_id")
        graph.add_node(airport_id, **airport)

    for route in routes.to_dict("records"):
        source, destination = route["source_airport_id"], route["destination_airport_id"]
        if graph.has_edge(source, destination):
            edge = graph[source][destination]
            edge["route_count"] += 1
            if route["airline"] not in edge["airlines"]:
                edge["airlines"].append(route["airline"])
        else:
            graph.add_edge(
                source,
                destination,
                route_count=1,
                airlines=[route["airline"]],
                stops=route["stops"],
            )
    return graph


def network_summary(graph: nx.DiGraph, top_n: int = 10) -> dict[str, Any]:
    """Return core network metrics and the busiest airports by total degree."""
    components = list(nx.weakly_connected_components(graph))
    largest_component_size = max((len(component) for component in components), default=0)
    ranked = sorted(graph.degree, key=lambda item: (-item[1], item[0]))[:top_n]
    top_airports = [
        {
            "airport_id": airport_id,
            "name": graph.nodes[airport_id].get("name", "Unknown"),
            "city": graph.nodes[airport_id].get("city", "Unknown"),
            "country": graph.nodes[airport_id].get("country", "Unknown"),
            "degree": degree,
            "in_degree": graph.in_degree(airport_id),
            "out_degree": graph.out_degree(airport_id),
        }
        for airport_id, degree in ranked
    ]
    return {
        "nodes": graph.number_of_nodes(),
        "edges": graph.number_of_edges(),
        "density": nx.density(graph),
        "weakly_connected_components": len(components),
        "largest_weak_component_size": largest_component_size,
        "reciprocity": nx.reciprocity(graph),
        "top_airports": top_airports,
    }
