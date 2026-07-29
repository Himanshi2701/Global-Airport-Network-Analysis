"""Run a reproducible summary of the airport-route network."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from graph_builder import DEFAULT_DATA_DIR, build_graph, network_summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyse the OpenFlights airport network.")
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    parser.add_argument("--top", type=int, default=10, help="Number of airports to rank.")
    parser.add_argument("--output", type=Path, help="Optional JSON report path.")
    args = parser.parse_args()

    summary = network_summary(build_graph(args.data_dir), args.top)
    report = json.dumps(summary, indent=2, allow_nan=False)
    print(report)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()



