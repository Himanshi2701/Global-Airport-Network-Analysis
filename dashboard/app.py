import streamlit as st
from pathlib import Path
import pandas as pd

st.set_page_config(
    page_title="Global Airport Network Analysis",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

APP_DIR = Path(__file__).resolve().parent
BASE_DIR = APP_DIR.parent
FIGURES_DIR = BASE_DIR / "Reports" / "figures"
if not FIGURES_DIR.exists() and (BASE_DIR / "Figures").exists():
    FIGURES_DIR = BASE_DIR / "Figures"

# ============================================================
# PROFESSIONAL CSS
# ============================================================
st.markdown('''
<style>
.stApp { background:#f5f7fb; color:#172b4d; }
.main .block-container { max-width:1450px; padding-top:2rem; padding-bottom:4rem; }
section[data-testid="stSidebar"] { background:linear-gradient(180deg,#0b1f3a 0%,#102f5f 55%,#123c72 100%); }
section[data-testid="stSidebar"] * { color:#f7fbff !important; }
.hero { background:linear-gradient(135deg,#0c2850,#174a8b 58%,#2172ba); border-radius:22px; padding:2.4rem 2.6rem; margin-bottom:1.8rem; box-shadow:0 18px 45px rgba(13,43,82,.20); }
.hero-title { color:#fff; font-size:2.55rem; font-weight:800; line-height:1.15; margin:0; }
.hero-subtitle { color:#dcecff; font-size:1rem; line-height:1.65; margin-top:.7rem; max-width:950px; }
.section-title { color:#102f5f; font-size:1.62rem; font-weight:800; margin:1.7rem 0 .35rem; }
.section-subtitle { color:#64748b; font-size:.94rem; margin-bottom:1rem; }
.info-card { background:#fff; border:1px solid #e2e8f0; border-radius:16px; padding:1.2rem 1.3rem; margin:.25rem 0 1rem; box-shadow:0 7px 24px rgba(30,55,90,.065); }
.info-card h3 { color:#163d70; margin:0 0 .55rem; font-size:1.05rem; }
.info-card p { color:#475569; line-height:1.68; margin:.35rem 0; }
.research-box { background:linear-gradient(135deg,#eaf3ff,#f3f8ff); border:1px solid #cfe1f8; border-left:5px solid #2776c8; border-radius:14px; padding:1.15rem 1.35rem; color:#173d67; line-height:1.7; }
.finding { background:linear-gradient(135deg,#eff8f3,#f7fcf9); border:1px solid #cce9d8; border-left:5px solid #2f9e62; border-radius:14px; padding:1.1rem 1.3rem; color:#24583a; line-height:1.65; margin:.8rem 0 1rem; }
div[data-testid="stMetric"] { background:#fff; border:1px solid #e2e8f0; border-radius:16px; padding:1rem 1.1rem; min-height:120px; box-shadow:0 7px 24px rgba(30,55,90,.065); }
div[data-testid="stMetricLabel"] { color:#64748b !important; font-size:.82rem !important; font-weight:700 !important; }
div[data-testid="stMetricValue"] { color:#102f5f !important; font-size:2rem !important; font-weight:800 !important; }
[data-testid="stImage"] { background:#fff; border:1px solid #e2e8f0; border-radius:16px; padding:.5rem; box-shadow:0 8px 28px rgba(30,55,90,.065); }
.footer { text-align:center; color:#718096; font-size:.82rem; padding:1.5rem 0 .4rem; }
</style>
''', unsafe_allow_html=True)

# ============================================================
# VERIFIED RESULTS FROM THE PROJECT NOTEBOOKS
# ============================================================
AIRPORTS = 3214
ROUTES = 36907
RAW_AIRPORTS = 7698
RAW_ROUTES = 67663
VALID_ROUTE_RECORDS = 66771
SKIPPED_ROUTES = 892
DENSITY = 0.003574
WEAK_COMPONENTS = 7
LARGEST_COMPONENT = 3188
RECIPROCITY = 0.9780
UNDIRECTED_EDGES = 18859

# ============================================================
# HELPERS
# ============================================================
def figure_path(*names):
    for name in names:
        p = FIGURES_DIR / name
        if p.exists():
            return p
    return None


def show_figure(names, caption):
    if isinstance(names, str):
        names = [names]
    p = figure_path(*names)
    if p:
        st.image(str(p), caption=caption, use_container_width=True)
        return True
    st.warning("Figure not found: " + ", ".join(names), icon="⚠️")
    return False


def section_title(title, subtitle=None):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="section-subtitle">{subtitle}</div>', unsafe_allow_html=True)


def info_card(title, text):
    st.markdown(f'''<div class="info-card"><h3>{title}</h3><p>{text}</p></div>''', unsafe_allow_html=True)


def finding(title, text):
    st.markdown(f'''<div class="finding"><b>{title}</b><br>{text}</div>''', unsafe_allow_html=True)

# ============================================================
# NOTEBOOK 04 — CENTRALITY RESULTS
# ============================================================
degree = pd.DataFrame([
    ("Frankfurt am Main Airport","Frankfurt","Germany",477,238,239),
    ("Charles de Gaulle International Airport","Paris","France",470,233,237),
    ("Amsterdam Airport Schiphol","Amsterdam","Netherlands",463,231,232),
    ("Atatürk International Airport","Istanbul","Turkey",451,227,224),
    ("Hartsfield Jackson Atlanta International Airport","Atlanta","United States",433,216,217),
    ("Chicago O'Hare International Airport","Chicago","United States",409,203,206),
    ("Beijing Capital International Airport","Beijing","China",408,204,204),
    ("Munich Airport","Munich","Germany",380,189,191),
    ("Domodedovo International Airport","Moscow","Russia",375,188,187),
    ("Dallas Fort Worth International Airport","Dallas-Fort Worth","United States",372,185,187),
    ("Dubai International Airport","Dubai","United Arab Emirates",364,179,185),
    ("London Heathrow Airport","London","United Kingdom",340,170,170),
    ("George Bush Intercontinental Houston Airport","Houston","United States",337,168,169),
    ("Denver International Airport","Denver","United States",335,167,168),
    ("London Gatwick Airport","London","United Kingdom",330,165,165),
], columns=["Airport","City","Country","Total degree","In-degree","Out-degree"])

pagerank = pd.DataFrame([
    ("Hartsfield Jackson Atlanta International Airport","Atlanta","United States",0.004922),
    ("Chicago O'Hare International Airport","Chicago","United States",0.004512),
    ("Atatürk International Airport","Istanbul","Turkey",0.004482),
    ("Denver International Airport","Denver","United States",0.004430),
    ("Dallas Fort Worth International Airport","Dallas-Fort Worth","United States",0.004409),
    ("Domodedovo International Airport","Moscow","Russia",0.004213),
    ("Charles de Gaulle International Airport","Paris","France",0.004137),
    ("Frankfurt am Main Airport","Frankfurt","Germany",0.004018),
    ("Beijing Capital International Airport","Beijing","China",0.003951),
    ("Amsterdam Airport Schiphol","Amsterdam","Netherlands",0.003809),
    ("Dubai International Airport","Dubai","United Arab Emirates",0.003708),
    ("George Bush Intercontinental Houston Airport","Houston","United States",0.003707),
    ("Los Angeles International Airport","Los Angeles","United States",0.003461),
    ("Sydney Kingsford Smith International Airport","Sydney","Australia",0.003338),
    ("Lester B. Pearson International Airport","Toronto","Canada",0.003196),
], columns=["Airport","City","Country","PageRank"])

betweenness = pd.DataFrame([
    ("Charles de Gaulle International Airport","CDG","Paris","France",0.063563),
    ("Los Angeles International Airport","LAX","Los Angeles","United States",0.060503),
    ("Ted Stevens Anchorage International Airport","ANC","Anchorage","United States",0.058427),
    ("Dubai International Airport","DXB","Dubai","United Arab Emirates",0.055406),
    ("Frankfurt am Main Airport","FRA","Frankfurt","Germany",0.052432),
    ("Amsterdam Airport Schiphol","AMS","Amsterdam","Netherlands",0.051063),
    ("Beijing Capital International Airport","PEK","Beijing","China",0.049788),
    ("Chicago O'Hare International Airport","ORD","Chicago","United States",0.046583),
    ("Lester B. Pearson International Airport","YYZ","Toronto","Canada",0.044345),
    ("Atatürk International Airport","ISL","Istanbul","Turkey",0.042428),
    ("Guarulhos - Governador André Franco Montoro International Airport","GRU","Sao Paulo","Brazil",0.041686),
    ("London Heathrow Airport","LHR","London","United Kingdom",0.037098),
    ("Narita International Airport","NRT","Tokyo","Japan",0.035306),
    ("Sydney Kingsford Smith International Airport","SYD","Sydney","Australia",0.034768),
    ("Seattle Tacoma International Airport","SEA","Seattle","United States",0.032996),
], columns=["Airport","IATA","City","Country","Betweenness"])

# ============================================================
# NOTEBOOK 06 — COMMUNITY RESULTS
# ============================================================
communities = pd.DataFrame([
    (14,732,"United States (410), Canada (70), Mexico (56)"),
    (5,510,"France (54), United Kingdom (45), Spain (40)"),
    (4,463,"India (67), Iran (38), Turkey (35)"),
    (11,405,"Australia (113), Indonesia (63), Philippines (35)"),
    (12,322,"China (172), Japan (62), Vietnam (20)"),
    (13,212,"Brazil (122), Argentina (36), Peru (19)"),
    (22,161,"Russia (103), Kazakhstan (17), Uzbekistan (11)"),
    (15,131,"United States (131)"),
    (1,110,"Canada (110)"),
    (9,27,"French Polynesia (27)"),
    (2,26,"Norway (26)"),
    (20,23,"Canada (23)"),
    (19,21,"Greenland (17), Iceland (4)"),
    (10,10,"New Caledonia (10)"),
    (23,10,"Kenya (10)"),
], columns=["Community","Airports","Dominant countries"])

# ============================================================
# NOTEBOOK 06 — RESILIENCE RESULTS
# ============================================================
resilience = pd.DataFrame({
    "Airports removed": [0,1,5,10,20,50],
    "Random failures": [1.000000,0.999646,0.997923,0.995646,0.991368,0.978347],
    "Degree-targeted": [1.000000,0.999686,0.993413,0.981493,0.966123,0.926913],
    "Betweenness-targeted": [1.000000,0.999373,0.968005,0.962045,0.927227,0.859787],
})

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("### ✈️ Airport Network")
    st.caption("Graph Theory • Network Science")
    page = st.radio(
        "ANALYSIS MODULES",
        ["Overview","Network Structure","Airport Hubs","Communities","Resilience Analysis","Geographic Network"],
    )
    st.divider()
    st.caption("Project: Global Airport Network Analysis")
    st.caption("Methods: NetworkX • PageRank • Betweenness • Louvain • Resilience")
    st.caption("Data: OpenFlights")

# ============================================================
# HERO
# ============================================================
st.markdown('''
<div class="hero">
    <div class="hero-title">✈️ Global Airport Network Analysis</div>
    <div class="hero-subtitle">
        Graph-theoretic analysis of connectivity, centrality, community structure,
        geographic organization and resilience in the global air transportation network.
    </div>
</div>
''', unsafe_allow_html=True)

# ============================================================
# OVERVIEW
# ============================================================
if page == "Overview":
    section_title("Project Overview", "From raw OpenFlights records to a network-science analysis.")
    st.markdown('''
    <div class="info-card">
        <h3>Research problem</h3>
        <p>The global air transportation system is modelled as a <b>directed graph</b>.
        Airports are nodes and scheduled routes are directed edges.</p>
        <p>The project examines network structure, airport importance, geographic
        organization, community structure and resilience under different airport-failure strategies.</p>
    </div>
    ''', unsafe_allow_html=True)

    section_title("Research Question")
    st.markdown('''
    <div class="research-box"><b>
    How is the global airport transportation network structurally organized,
    which airports are most critical for maintaining worldwide connectivity,
    and how resilient is the network to different airport failure scenarios?
    </b></div>
    ''', unsafe_allow_html=True)

    section_title("Validated Network Statistics")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("AIRPORTS IN ANALYTICAL GRAPH",f"{AIRPORTS:,}","nodes")
    c2.metric("UNIQUE DIRECTED ROUTES",f"{ROUTES:,}","edges")
    c3.metric("LARGEST WEAK COMPONENT",f"{LARGEST_COMPONENT:,}","of 3,214 nodes")
    c4.metric("ROUTE RECIPROCITY",f"{RECIPROCITY:.3f}","very high")

    section_title("From Raw Data to Analytical Graph")
    raw = pd.DataFrame({
        "Stage":["Raw airports","Raw route records","Valid route records","Skipped route records","Unique graph edges"],
        "Count":[RAW_AIRPORTS,RAW_ROUTES,VALID_ROUTE_RECORDS,SKIPPED_ROUTES,ROUTES],
        "Meaning":["OpenFlights airport records","Original route rows","Routes with valid endpoint IDs","Invalid or missing endpoint records","Unique ordered airport pairs in the DiGraph"],
    })
    st.dataframe(raw,use_container_width=True,hide_index=True)

    section_title("Project Workflow")
    workflow = [
        "01  Data exploration & quality checks",
        "02  Directed graph construction",
        "03  Network structure & degree analysis",
        "04  Degree, PageRank & betweenness centrality",
        "05  Geographic visualization",
        "06  Louvain communities & resilience simulations",
    ]
    for item in workflow:
        st.markdown(f'<div class="info-card" style="padding:.75rem 1rem;margin:.35rem 0;"><b>{item}</b></div>', unsafe_allow_html=True)

    section_title("Global Network Visualization")
    show_figure("global_network.png","Global Airport Transportation Network")

    finding("Main structural picture", "The analytical network is sparse (density 0.003574), but almost all of its nodes lie in one dominant weakly connected component of 3,188 airports. The route reciprocity of 0.978 indicates that most unique connections are represented in both directions.")

# ============================================================
# NETWORK STRUCTURE
# ============================================================
elif page == "Network Structure":
    section_title("Network Structure", "Topology, connectivity and degree heterogeneity.")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("NODES | V |",f"{AIRPORTS:,}")
    c2.metric("EDGES | E |",f"{ROUTES:,}")
    c3.metric("WEAK COMPONENTS",WEAK_COMPONENTS)
    c4.metric("NETWORK DENSITY",f"{DENSITY:.6f}")

    section_title("Connectivity")
    info_card("Largest weak component", "The largest weakly connected component contains 3,188 of 3,214 airports. Therefore nearly the entire analytical network belongs to one dominant connected system.")

    section_title("Global Network")
    show_figure("global_network.png","Global Airport Transportation Network")

    section_title("Degree Distribution", "Most airports have relatively few direct connections, while a small number of airports have very high degree.")
    show_figure("degree_distribution.png","Degree Distribution of the Global Airport Network")

    finding("Interpretation", "The concentration of high-degree connections around a small set of hubs is important for both efficiency and vulnerability: the same airports that provide extensive connectivity can also become points of network dependence.")

# ============================================================
# AIRPORT HUBS
# ============================================================
elif page == "Airport Hubs":
    section_title("Airport Hubs & Centrality", "Three measures capture three different meanings of airport importance.")

    section_title("Top Connected Airports", "Total degree = in-degree + out-degree.")
    st.dataframe(degree,use_container_width=True,hide_index=True)

    section_title("PageRank Leaders", "PageRank rewards airports connected to other influential airports.")
    st.dataframe(pagerank,use_container_width=True,hide_index=True)

    section_title("Betweenness Leaders", "Betweenness highlights airports that lie on many shortest paths between other airports.")
    st.dataframe(betweenness,use_container_width=True,hide_index=True)

    section_title("Hub Visualization")
    show_figure(["top20_hubs.png","top_20_hubs.png"],"Top Airport Hubs by Total Degree")

    finding("Important distinction", "Frankfurt, Amsterdam Schiphol and Charles de Gaulle rank highly in both degree and betweenness, while Los Angeles and Anchorage rank particularly highly in betweenness. This demonstrates why a single centrality measure is insufficient for identifying critical infrastructure.")

# ============================================================
# COMMUNITIES
# ============================================================
elif page == "Communities":
    section_title("Community Detection", "Louvain analysis on the undirected version of the analytical network.")
    c1,c2,c3 = st.columns(3)
    c1.metric("AIRPORTS",f"{AIRPORTS:,}")
    c2.metric("UNDIRECTED EDGES",f"{18859:,}")
    c3.metric("METHOD","Louvain")

    info_card("What a community means", "Louvain groups airports that have relatively dense internal connectivity. The resulting communities provide a mesoscopic view between individual hubs and the whole network.")

    section_title("Largest Detected Communities", "The table shows the 15 largest communities reported by the notebook, with their dominant countries.")
    st.dataframe(communities,use_container_width=True,hide_index=True)

    finding("Geographic structure", "The largest groups have clear regional signatures: North America, Western Europe, South Asia/Middle East, Oceania, East Asia, South America and Russia/Central Asia. This supports the interpretation that global aviation is organized into strongly regional subnetworks connected by international gateways.")

    section_title("Why this matters for resilience")
    info_card("Community bridges", "Airports that connect communities can be important even when they are not the highest-degree hubs. Their removal can weaken inter-regional connectivity and is one reason betweenness centrality is useful in the failure analysis.")

# ============================================================
# RESILIENCE
# ============================================================
elif page == "Resilience Analysis":
    section_title("Network Resilience", "Comparison of random, degree-targeted and betweenness-targeted airport removal.")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("BASELINE LARGEST COMPONENT",f"{LARGEST_COMPONENT:,}")
    c2.metric("RANDOM @ 50 REMOVED","97.83%","remaining")
    c3.metric("DEGREE @ 50 REMOVED","92.69%","remaining")
    c4.metric("BETWEENNESS @ 50 REMOVED","85.98%","remaining")

    section_title("Interactive Failure Comparison", "Fraction of the original largest connected component remaining.")
    chart_data = resilience.set_index("Airports removed")[["Random failures","Degree-targeted","Betweenness-targeted"]]
    st.line_chart(chart_data,use_container_width=True,height=430)

    section_title("Notebook Results", "Exact values used to generate the resilience comparison.")
    display_res = resilience.copy()
    for col in ["Random failures","Degree-targeted","Betweenness-targeted"]:
        display_res[col] = (display_res[col]*100).round(3).astype(str)+"%"
    st.dataframe(display_res,use_container_width=True,hide_index=True)

    section_title("Original Resilience Figure")
    show_figure(["Random_vs_Targeted.png","_Random_vs_Targeted.png"],"Network Resilience: Random Failures vs Targeted Hub Removal")

    finding("Main finding", "The network is highly robust to random removal but substantially more sensitive to targeted structural attacks. At 50 removed airports, the largest component retains 97.83% under random removal, 92.69% after degree-targeted removal and only 85.98% after betweenness-targeted removal.")
    info_card("Why betweenness matters", "Degree targets highly connected hubs. Betweenness targets bridge airports whose position connects different parts of the network. The stronger damage from betweenness-targeted removal shows that bridge structure is a major component of network vulnerability.")
    st.caption("These are graph-theoretic simulations, not predictions of real-world aviation disruptions.")

# ============================================================
# GEOGRAPHIC NETWORK
# ============================================================
elif page == "Geographic Network":
    section_title("Geographic Network", "Spatial organization of airports and global hubs.")
    show_figure("global_network.png","Global Airport Transportation Network")

    section_title("Geographic Interpretation")
    a,b,c = st.columns(3)
    with a:
        info_card("Global coverage", "Airports are distributed across all major populated regions, but their density is highly uneven.")
    with b:
        info_card("Regional concentration", "Large communities correspond to recognizable regional aviation systems.")
    with c:
        info_card("Global gateways", "International hubs connect geographically distant communities and therefore can become structurally critical.")

    finding("Connection between geography and graph structure", "Location alone does not determine centrality. The centrality and resilience analyses show that airports become important because of how their connections position them within the network.")

# ============================================================
# FOOTER
# ============================================================
st.divider()
st.markdown('''
<div class="footer">
    <b>Global Airport Network Analysis</b><br>
    Himanshi Pandey • M.Sc. Applied Mathematics • National Institute of Technology Warangal<br>
    Graph Theory • Network Science • Centrality • Louvain Communities • Resilience
</div>
''', unsafe_allow_html=True)