***

# Global Fiber Route Finder
<img src="Screenshot 2026-01-04 at 01.07.27.png" alt="Application Screenshot" width="800">
An intelligent fiber-optic pathfinding web application that calculates the shortest route between any two points on Earth using a hybrid graph of terrestrial and submarine cables.

The app dynamically fetches data from the **ITU (International Telecommunication Union)** Broadband Maps for land infrastructure and the **Submarine Cable Map (SCM)** for oceanic links.

## Features

*   **Hybrid Routing:** Seamlessly chains Land $\rightarrow$ Sea $\rightarrow$ Land connections using landing station "welding" logic.
*   **Lateral Intelligence:** Incentivizes submarine routes (0.7x weight) to prefer direct sea paths over long terrestrial detours.
*   **Interactive UI:** 
    *   Visual preload of global fiber lines via WMS.
    *   Click-to-set markers for Start and End points.
    *   **Provider Filtering:** Click a network provider in the sidebar to highlight only their specific segments in purple.
    *   **Junction Markers:** Yellow markers indicate "handoff" points where cables change owners or types.
*   **Network Stats:** Calculates total distance in kilometers and provides an estimated Round Trip Time (RTT) in milliseconds.

##  Project Structure

```text
fiber-pathfinder/
├── main.py              # FastAPI Backend & Graph Engine
├── requirements.txt     # Python dependencies
├── static/
│   └── css/
│       └── styles.css   # Custom styles (placeholder)
└── templates/
    └── index.html       # Leaflet.js Frontend
```

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/fortless/fiber-pathfinder.git
cd fiber-calculator
```

### 2. Create and activate a virtual environment
Ensure you have Python 3.9+ installed.
```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell, use `python -m venv .venv` and `.venv\Scripts\Activate.ps1` instead.

### 3. Install dependencies
With the virtual environment activated:
```bash
python -m pip install -r requirements.txt
```

## Getting Started

Run the application using Uvicorn:

```bash
python main.py
```
*Or via uvicorn directly:*
```bash
python -m uvicorn main:app --reload
```

Activate the virtual environment again when opening a new terminal. By default the app listens on 127.0.0.1:8000. This is changeable in the last line of `main.py`, otherwise, you can open it in your browser by accessing:
**`http://127.0.0.1:8000`**

The app starts without fetching routing data. Route calculations require access to ITU and Submarine Cable Map; if a data service is unavailable (for example, HTTP 503), the calculation reports an error and the app remains available. Try the calculation again once the service recovers.

## How to Use

1.  **Select Points:** Click anywhere on the map to set your **Start** point. Click again to set the **End** point.
2.  **Calculate:** Click the **"Calculate Shortest Path"** button. The backend will fetch regional infrastructure and build a connectivity graph.
3.  **Explore Providers:** Once the path appears, a list of all involved network providers will show in the sidebar. Click any provider name to highlight their specific segments on the map.
4.  **Reset:** Use the **"Reset Markers"** button to clear the map and start a new search.

## Built With

*   [FastAPI](https://fastapi.tiangolo.com/) - Backend framework.
*   [NetworkX](https://networkx.org/) - Graph theory library for Dijkstra's shortest path.
*   [Leaflet.js](https://leafletjs.com/) - Interactive maps.
*   [SciPy KDTree](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.KDTree.html) - For high-speed spatial "welding" of disconnected cable segments.

## Data Sources
*   Terrestrial Data: [ITU Broadband Maps](https://bbmaps.itu.int/)
*   Submarine Data: [Submarine Cable Map](https://www.submarinecablemap.com/) via TeleGeography.

---
*Note: This tool is for educational and planning purposes. Actual fiber routing depends on BGP policies and private peering agreements.*
