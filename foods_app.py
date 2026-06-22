"""
Local Food Wastage Management System — Streamlit App
Tech Stack: Python · SQLite · Streamlit
"""

import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🍽️ Food Wastage Management System",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS Styling ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #2ecc71;
        text-align: center;
        padding-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #7f8c8d;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        border-left: 4px solid #2ecc71;
    }
</style>
""", unsafe_allow_html=True)


# ── Database helpers ──────────────────────────────────────────────────────────
@st.cache_resource
def get_connection():
    conn = sqlite3.connect("food_wastage.db", check_same_thread=False)
    return conn


@st.cache_data
def load_data():
    providers     = pd.read_csv("providers_data.csv")
    receivers     = pd.read_csv("receivers_data.csv")
    food_listings = pd.read_csv("food_listings_data.csv")
    claims        = pd.read_csv("claims_data.csv")
    claims["Timestamp"] = pd.to_datetime(claims["Timestamp"])
    return providers, receivers, food_listings, claims


def init_db(conn, providers, receivers, food_listings, claims):
    """Create tables and load data (idempotent)."""
    cur = conn.cursor()
    cur.executescript("""
        CREATE TABLE IF NOT EXISTS providers (
            Provider_ID INTEGER PRIMARY KEY, Name TEXT, Type TEXT,
            Address TEXT, City TEXT, Contact TEXT);
        CREATE TABLE IF NOT EXISTS receivers (
            Receiver_ID INTEGER PRIMARY KEY, Name TEXT, Type TEXT,
            City TEXT, Contact TEXT);
        CREATE TABLE IF NOT EXISTS food_listings (
            Food_ID INTEGER PRIMARY KEY, Food_Name TEXT, Quantity INTEGER,
            Expiry_Date TEXT, Provider_ID INTEGER, Provider_Type TEXT,
            Location TEXT, Food_Type TEXT, Meal_Type TEXT);
        CREATE TABLE IF NOT EXISTS claims (
            Claim_ID INTEGER PRIMARY KEY, Food_ID INTEGER,
            Receiver_ID INTEGER, Status TEXT, Timestamp TEXT);
    """)
    conn.commit()
    # Load data only if tables are empty
    if cur.execute("SELECT COUNT(*) FROM providers").fetchone()[0] == 0:
        providers.to_sql("providers",     conn, if_exists="append", index=False)
        receivers.to_sql("receivers",     conn, if_exists="append", index=False)
        food_listings.to_sql("food_listings", conn, if_exists="append", index=False)
        claims.to_sql("claims",           conn, if_exists="append", index=False)
        conn.commit()


def run_query(conn, sql):
    return pd.read_sql_query(sql, conn)


# ── Load data & init DB ───────────────────────────────────────────────────────
providers, receivers, food_listings, claims = load_data()
conn = get_connection()
init_db(conn, providers, receivers, food_listings, claims)

# ── Sidebar navigation ────────────────────────────────────────────────────────
st.sidebar.title("🍽️ Navigation")
page = st.sidebar.radio("Go to", [
    "🏠 Dashboard",
    "📋 View Data",
    "🔍 Filter Food",
    "📊 Visualizations",
    "🧮 SQL Queries",
    "✏️ CRUD Operations",
])

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
if page == "🏠 Dashboard":
    st.markdown('<p class="main-header">🍽️ Local Food Wastage Management System</p>',
                unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Connecting surplus food providers to receivers in need</p>',
                unsafe_allow_html=True)

    # KPI metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🏪 Total Providers",    f"{len(providers):,}")
    c2.metric("🏠 Total Receivers",    f"{len(receivers):,}")
    c3.metric("🍱 Food Listings",       f"{len(food_listings):,}")
    c4.metric("📋 Total Claims",        f"{len(claims):,}")

    st.divider()

    c1, c2, c3 = st.columns(3)
    c1.metric("🥦 Total Food Units",    f"{food_listings['Quantity'].sum():,}")
    c2.metric("✅ Completed Claims",    f"{(claims['Status']=='Completed').sum()}")
    c3.metric("🏙️ Cities Covered",     f"{providers['City'].nunique()}")

    st.divider()
    st.subheader("📌 Problem Statement")
    st.info("""
    Food wastage is a major global issue — restaurants, supermarkets, and households discard surplus food daily
    while millions struggle with food insecurity. This system connects **food providers** (restaurants, supermarkets,
    grocery stores, catering services) with **receivers** (NGOs, shelters, charities, individuals) to redistribute
    surplus food efficiently, reducing waste and fighting hunger.
    """)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🏪 Provider Type Distribution")
        pc = providers["Type"].value_counts()
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.pie(pc.values, labels=pc.index, autopct="%1.1f%%",
               colors=["#2ecc71","#3498db","#e74c3c","#f39c12"],
               startangle=140, wedgeprops=dict(edgecolor="white", linewidth=1.5))
        ax.set_title("Provider Types")
        st.pyplot(fig)
        plt.close()

    with col2:
        st.subheader("📋 Claim Status Distribution")
        cs = claims["Status"].value_counts()
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.pie(cs.values, labels=cs.index, autopct="%1.1f%%",
               colors=["#2ecc71","#e74c3c","#f39c12"],
               startangle=140, wedgeprops=dict(edgecolor="white", linewidth=1.5))
        ax.set_title("Claim Status")
        st.pyplot(fig)
        plt.close()

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — VIEW DATA
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📋 View Data":
    st.header("📋 Dataset Explorer")
    tab1, tab2, tab3, tab4 = st.tabs(
        ["🏪 Providers", "🏠 Receivers", "🍱 Food Listings", "📋 Claims"])

    with tab1:
        st.write(f"**{len(providers)} rows × {len(providers.columns)} columns**")
        st.dataframe(providers, use_container_width=True, height=400)

    with tab2:
        st.write(f"**{len(receivers)} rows × {len(receivers.columns)} columns**")
        st.dataframe(receivers, use_container_width=True, height=400)

    with tab3:
        st.write(f"**{len(food_listings)} rows × {len(food_listings.columns)} columns**")
        st.dataframe(food_listings, use_container_width=True, height=400)

    with tab4:
        st.write(f"**{len(claims)} rows × {len(claims.columns)} columns**")
        st.dataframe(claims, use_container_width=True, height=400)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — FILTER FOOD
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🔍 Filter Food":
    st.header("🔍 Filter Food Listings")

    col1, col2, col3, col4 = st.columns(4)
    cities     = ["All"] + sorted(food_listings["Location"].unique().tolist())
    food_types = ["All"] + sorted(food_listings["Food_Type"].unique().tolist())
    meal_types = ["All"] + sorted(food_listings["Meal_Type"].unique().tolist())
    prov_types = ["All"] + sorted(food_listings["Provider_Type"].unique().tolist())

    sel_city  = col1.selectbox("🏙️ City",          cities)
    sel_food  = col2.selectbox("🥦 Food Type",      food_types)
    sel_meal  = col3.selectbox("🍽️ Meal Type",      meal_types)
    sel_prov  = col4.selectbox("🏪 Provider Type",  prov_types)

    filtered = food_listings.copy()
    if sel_city  != "All": filtered = filtered[filtered["Location"]      == sel_city]
    if sel_food  != "All": filtered = filtered[filtered["Food_Type"]     == sel_food]
    if sel_meal  != "All": filtered = filtered[filtered["Meal_Type"]     == sel_meal]
    if sel_prov  != "All": filtered = filtered[filtered["Provider_Type"] == sel_prov]

    st.success(f"✅ Showing **{len(filtered)}** matching food listings")
    st.dataframe(filtered, use_container_width=True, height=450)

    st.subheader("📞 Provider Contact Details")
    if not filtered.empty:
        pids = filtered["Provider_ID"].unique()
        contacts = providers[providers["Provider_ID"].isin(pids)][
            ["Name","Type","City","Contact"]]
        st.dataframe(contacts.reset_index(drop=True), use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — VISUALIZATIONS
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📊 Visualizations":
    st.header("📊 Data Visualizations")

    viz = st.selectbox("Select Chart:", [
        "Provider Type Distribution",
        "Claim Status Distribution",
        "Food Type Distribution",
        "Meal Type Distribution",
        "Top 10 Food Items",
        "Receiver Type Distribution",
        "Quantity Distribution",
        "Monthly Claims by Status",
        "Food Type vs Meal Type Heatmap",
    ])

    fig, ax = plt.subplots(figsize=(9, 5))

    if viz == "Provider Type Distribution":
        pc = providers["Type"].value_counts()
        bars = ax.bar(pc.index, pc.values, color=["#2ecc71","#3498db","#e74c3c","#f39c12"])
        ax.set_title("Provider Type Distribution", fontweight="bold")
        for bar in bars:
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+1,
                    str(int(bar.get_height())), ha="center", fontweight="bold")

    elif viz == "Claim Status Distribution":
        cs = claims["Status"].value_counts()
        ax.pie(cs.values, labels=cs.index, autopct="%1.1f%%",
               colors=["#2ecc71","#e74c3c","#f39c12"], startangle=140,
               wedgeprops=dict(edgecolor="white", linewidth=2))
        ax.set_title("Claim Status Distribution", fontweight="bold")

    elif viz == "Food Type Distribution":
        ft = food_listings["Food_Type"].value_counts()
        ax.pie(ft.values, labels=ft.index, autopct="%1.1f%%",
               colors=["#27ae60","#2980b9","#8e44ad"], startangle=90,
               wedgeprops=dict(edgecolor="white", linewidth=2))
        ax.set_title("Food Type Distribution", fontweight="bold")

    elif viz == "Meal Type Distribution":
        mt = food_listings["Meal_Type"].value_counts()
        bars = ax.bar(mt.index, mt.values,
                      color=["#e74c3c","#3498db","#2ecc71","#f39c12"])
        ax.set_title("Meal Type Distribution", fontweight="bold")
        for bar in bars:
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+1,
                    str(int(bar.get_height())), ha="center", fontweight="bold")

    elif viz == "Top 10 Food Items":
        tf = food_listings["Food_Name"].value_counts().head(10)
        bars = ax.barh(tf.index[::-1], tf.values[::-1],
                       color=sns.color_palette("viridis", 10))
        ax.set_title("Top 10 Most Common Food Items", fontweight="bold")
        ax.set_xlabel("Count")
        for bar in bars:
            ax.text(bar.get_width()+0.3, bar.get_y()+bar.get_height()/2,
                    str(int(bar.get_width())), va="center", fontweight="bold")

    elif viz == "Receiver Type Distribution":
        rt = receivers["Type"].value_counts()
        bars = ax.bar(rt.index, rt.values,
                      color=["#9b59b6","#1abc9c","#e67e22","#3498db"])
        ax.set_title("Receiver Type Distribution", fontweight="bold")
        for bar in bars:
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+1,
                    str(int(bar.get_height())), ha="center", fontweight="bold")

    elif viz == "Quantity Distribution":
        ax.hist(food_listings["Quantity"], bins=20,
                color="#3498db", edgecolor="white", alpha=0.85)
        ax.axvline(food_listings["Quantity"].mean(), color="red",
                   linestyle="--", linewidth=2,
                   label=f"Mean: {food_listings['Quantity'].mean():.1f}")
        ax.axvline(food_listings["Quantity"].median(), color="green",
                   linestyle="--", linewidth=2,
                   label=f"Median: {food_listings['Quantity'].median():.1f}")
        ax.set_title("Food Quantity Distribution", fontweight="bold")
        ax.legend()

    elif viz == "Monthly Claims by Status":
        claims["Month"] = claims["Timestamp"].dt.to_period("M").astype(str)
        monthly = claims.groupby(["Month","Status"]).size().unstack(fill_value=0)
        monthly.plot(kind="bar", ax=ax,
                     color=["#e74c3c","#2ecc71","#f39c12"], edgecolor="white")
        ax.set_title("Monthly Claims by Status", fontweight="bold")
        ax.set_xlabel("Month")
        plt.xticks(rotation=45)

    elif viz == "Food Type vs Meal Type Heatmap":
        ct = pd.crosstab(food_listings["Food_Type"], food_listings["Meal_Type"])
        plt.close()
        fig, ax = plt.subplots(figsize=(9, 5))
        sns.heatmap(ct, annot=True, fmt="d", cmap="YlGnBu", ax=ax, linewidths=0.5)
        ax.set_title("Food Type vs Meal Type Heatmap", fontweight="bold")

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — SQL QUERIES
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🧮 SQL Queries":
    st.header("🧮 SQL Queries & Analysis")

    QUERIES = {
        "Q1 — Top 10 Cities by Providers": """
            SELECT City, COUNT(*) AS Provider_Count
            FROM providers GROUP BY City
            ORDER BY Provider_Count DESC LIMIT 10""",
        "Q2 — Provider Type Contribution": """
            SELECT Provider_Type, COUNT(*) AS Listings, SUM(Quantity) AS Total_Qty
            FROM food_listings GROUP BY Provider_Type ORDER BY Total_Qty DESC""",
        "Q3 — Top 10 Receivers by Claims": """
            SELECT r.Name, r.Type, r.City, COUNT(c.Claim_ID) AS Total_Claims
            FROM claims c JOIN receivers r ON c.Receiver_ID=r.Receiver_ID
            GROUP BY r.Receiver_ID ORDER BY Total_Claims DESC LIMIT 10""",
        "Q4 — Top Cities by Food Quantity": """
            SELECT Location AS City, SUM(Quantity) AS Total_Qty, COUNT(*) AS Items
            FROM food_listings GROUP BY Location ORDER BY Total_Qty DESC LIMIT 10""",
        "Q5 — Food Type Breakdown": """
            SELECT Food_Type, COUNT(*) AS Count, SUM(Quantity) AS Total_Qty
            FROM food_listings GROUP BY Food_Type ORDER BY Count DESC""",
        "Q6 — Top 10 Food Items by Claims": """
            SELECT fl.Food_Name, COUNT(c.Claim_ID) AS Claims, SUM(fl.Quantity) AS Qty
            FROM claims c JOIN food_listings fl ON c.Food_ID=fl.Food_ID
            GROUP BY fl.Food_Name ORDER BY Claims DESC LIMIT 10""",
        "Q7 — Top Providers by Completed Claims": """
            SELECT p.Name, p.Type, p.City, COUNT(c.Claim_ID) AS Completed
            FROM claims c JOIN food_listings fl ON c.Food_ID=fl.Food_ID
            JOIN providers p ON fl.Provider_ID=p.Provider_ID
            WHERE c.Status='Completed' GROUP BY p.Provider_ID ORDER BY Completed DESC LIMIT 10""",
        "Q8 — Claim Status % Breakdown": """
            SELECT Status, COUNT(*) AS Total,
            ROUND(COUNT(*)*100.0/(SELECT COUNT(*) FROM claims),2) AS Pct
            FROM claims GROUP BY Status ORDER BY Total DESC""",
        "Q9 — Avg Quantity by Receiver Type": """
            SELECT r.Type, ROUND(AVG(fl.Quantity),2) AS Avg_Qty
            FROM claims c JOIN receivers r ON c.Receiver_ID=r.Receiver_ID
            JOIN food_listings fl ON c.Food_ID=fl.Food_ID
            GROUP BY r.Type ORDER BY Avg_Qty DESC""",
        "Q10 — Most Popular Meal Types": """
            SELECT fl.Meal_Type, COUNT(*) AS Claims,
            ROUND(COUNT(*)*100.0/(SELECT COUNT(*) FROM claims),2) AS Pct
            FROM claims c JOIN food_listings fl ON c.Food_ID=fl.Food_ID
            GROUP BY fl.Meal_Type ORDER BY Claims DESC""",
        "Q11 — Top Providers by Total Donated": """
            SELECT p.Name, p.Type, p.City, SUM(fl.Quantity) AS Total_Donated
            FROM food_listings fl JOIN providers p ON fl.Provider_ID=p.Provider_ID
            GROUP BY p.Provider_ID ORDER BY Total_Donated DESC LIMIT 10""",
        "Q12 — City with Most Food Listings": """
            SELECT Location AS City, COUNT(*) AS Listings
            FROM food_listings GROUP BY Location ORDER BY Listings DESC LIMIT 1""",
        "Q13 — Food Expiring Soon": """
            SELECT Food_ID, Food_Name, Quantity, Expiry_Date, Location
            FROM food_listings WHERE DATE(Expiry_Date)<=DATE('now','+30 days')
            ORDER BY Expiry_Date ASC LIMIT 15""",
        "Q14 — Providers with No Completed Claims": """
            SELECT p.Provider_ID, p.Name, p.Type, p.City FROM providers p
            WHERE p.Provider_ID NOT IN (
                SELECT DISTINCT fl.Provider_ID FROM claims c
                JOIN food_listings fl ON c.Food_ID=fl.Food_ID WHERE c.Status='Completed')
            LIMIT 10""",
        "Q15 — Cities with Providers & Receivers": """
            SELECT p.City, COUNT(DISTINCT p.Provider_ID) AS Providers,
                   COUNT(DISTINCT r.Receiver_ID) AS Receivers
            FROM providers p JOIN receivers r ON p.City=r.City
            GROUP BY p.City ORDER BY Providers DESC LIMIT 10""",
    }

    selected_q = st.selectbox("Select a Query:", list(QUERIES.keys()))
    sql = QUERIES[selected_q].strip()
    st.code(sql, language="sql")

    if st.button("▶️ Run Query"):
        result = run_query(conn, sql)
        st.success(f"✅ {len(result)} rows returned")
        st.dataframe(result, use_container_width=True)

    st.divider()
    if st.checkbox("🔁 Run All 15 Queries at Once"):
        for q_name, q_sql in QUERIES.items():
            st.subheader(q_name)
            try:
                df = run_query(conn, q_sql.strip())
                st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.error(f"Error: {e}")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 6 — CRUD OPERATIONS
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "✏️ CRUD Operations":
    st.header("✏️ CRUD Operations")
    cur = conn.cursor()

    op = st.radio("Select Operation:", ["➕ Create", "👁️ Read", "✏️ Update", "🗑️ Delete"])

    if op == "➕ Create":
        st.subheader("Add New Food Listing")
        with st.form("create_form"):
            col1, col2 = st.columns(2)
            food_name   = col1.text_input("Food Name")
            quantity    = col2.number_input("Quantity", min_value=1, max_value=500, value=10)
            expiry_date = col1.date_input("Expiry Date")
            provider_id = col2.number_input("Provider ID", min_value=1, value=1)
            prov_type   = col1.selectbox("Provider Type",
                          ["Supermarket","Grocery Store","Restaurant","Catering Service"])
            location    = col2.text_input("Location/City")
            food_type   = col1.selectbox("Food Type",["Vegetarian","Vegan","Non-Vegetarian"])
            meal_type   = col2.selectbox("Meal Type",["Breakfast","Lunch","Dinner","Snacks"])
            submitted   = st.form_submit_button("➕ Add Food Listing")

            if submitted:
                if food_name and location:
                    max_id = run_query(conn, "SELECT MAX(Food_ID) FROM food_listings").iloc[0,0]
                    new_id = int(max_id) + 1
                    cur.execute("""
                        INSERT INTO food_listings
                        VALUES (?,?,?,?,?,?,?,?,?)
                    """, (new_id, food_name, quantity, str(expiry_date),
                          provider_id, prov_type, location, food_type, meal_type))
                    conn.commit()
                    st.success(f"✅ Food listing added! Food ID: {new_id}")
                else:
                    st.warning("Please fill in Food Name and Location.")

    elif op == "👁️ Read":
        st.subheader("View Food Listings (with Filters)")
        col1, col2 = st.columns(2)
        search_city = col1.text_input("Filter by City (leave blank for all)")
        search_food = col2.text_input("Filter by Food Name (leave blank for all)")
        sql = "SELECT * FROM food_listings WHERE 1=1"
        if search_city: sql += f" AND Location LIKE '%{search_city}%'"
        if search_food: sql += f" AND Food_Name LIKE '%{search_food}%'"
        sql += " LIMIT 50"
        df = run_query(conn, sql)
        st.info(f"Showing {len(df)} records")
        st.dataframe(df, use_container_width=True)

    elif op == "✏️ Update":
        st.subheader("Update Food Listing Quantity")
        food_id  = st.number_input("Enter Food ID to update", min_value=1, value=1)
        new_qty  = st.number_input("New Quantity", min_value=0, value=10)
        if st.button("✏️ Update Quantity"):
            cur.execute("UPDATE food_listings SET Quantity=? WHERE Food_ID=?",
                        (new_qty, food_id))
            conn.commit()
            if cur.rowcount > 0:
                st.success(f"✅ Food ID {food_id} updated to Quantity = {new_qty}")
                st.dataframe(run_query(conn, f"SELECT * FROM food_listings WHERE Food_ID={food_id}"))
            else:
                st.error(f"Food ID {food_id} not found.")

    elif op == "🗑️ Delete":
        st.subheader("Delete Food Listing")
        st.warning("⚠️ Deletion is permanent. Only delete listings added for testing.")
        food_id = st.number_input("Enter Food ID to delete", min_value=1, value=1001)
        preview = run_query(conn, f"SELECT * FROM food_listings WHERE Food_ID={food_id}")
        if not preview.empty:
            st.write("Record to delete:")
            st.dataframe(preview)
            if st.button("🗑️ Confirm Delete", type="primary"):
                cur.execute("DELETE FROM food_listings WHERE Food_ID=?", (food_id,))
                conn.commit()
                st.success(f"✅ Food ID {food_id} deleted.")
        else:
            st.info(f"Food ID {food_id} not found in database.")

# ── Footer ────────────────────────────────────────────────────────────────────
st.sidebar.divider()
st.sidebar.caption("🍽️ Local Food Wastage Management System")
st.sidebar.caption("Domain: Food Management · Waste Reduction")
