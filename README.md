# 🍽️ Local Food Wastage Management System

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![SQL](https://img.shields.io/badge/SQL-SQLite-orange?logo=sqlite)](https://www.sqlite.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-GPL--3.0-green)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Completed-brightgreen)](https://github.com/pardeep0011/food-waste-Management)

**A full-stack data analytics project connecting surplus food providers to receivers in need, powered by Python, SQLite, and Streamlit.**

---

## 📑 Table of Contents

1. [Problem Statement](#-problem-statement)
2. [Project Objectives](#-project-objectives)
3. [Tech Stack](#-tech-stack)
4. [Dataset Description](#-dataset-description)
5. [Project Architecture](#-project-architecture)
6. [Exploratory Data Analysis](#-exploratory-data-analysis)
7. [Data Visualizations](#-data-visualizations)
8. [SQL Queries & Insights](#-sql-queries--insights-15-queries)
9. [CRUD Operations](#-crud-operations)
10. [Streamlit Application](#-streamlit-application)
11. [Key Insights](#-key-insights)
12. [Project Structure](#-project-structure)
13. [Getting Started (Clone & Run)](#-getting-started-clone--run)
14. [Evaluation Metrics](#-evaluation-metrics)
15. [Future Enhancements](#-future-enhancements)

---

## 🚨 Problem Statement

Food wastage is one of the most critical global challenges:

- **1.3 billion tonnes** of food is wasted globally every year.
- Restaurants, supermarkets, and households discard surplus food daily.
- Simultaneously, millions of people struggle with food insecurity.

This project builds a **Local Food Wastage Management System** where:

- 🏪 Restaurants and grocery stores can **list surplus food**.
- 🏠 NGOs, shelters, charities, and individuals can **claim available food**.
- 🗄️ An **SQLite database** stores all food listings, providers, and claims.
- 📊 A **Streamlit application** enables filtering, CRUD, and visualization.
- 🔍 **15+ SQL queries** provide data-driven insights into food donation trends.

---

## 🎯 Project Objectives

| # | Objective |
|---|-----------|
| 1 | Load and clean 4 CSV datasets (Providers, Receivers, Food Listings, Claims) |
| 2 | Perform Exploratory Data Analysis (EDA) |
| 3 | Store data in a structured SQLite relational database |
| 4 | Execute 15+ SQL queries for trend analysis |
| 5 | Implement full CRUD operations |
| 6 | Build a Streamlit app for interactive filtering and visualization |
| 7 | Extract actionable business insights from the data |

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.10+** | Core programming language |
| **Pandas** | Data loading, cleaning, manipulation |
| **NumPy** | Numerical computations |
| **Matplotlib** | Static data visualizations |
| **Seaborn** | Statistical data visualizations |
| **SQLite3** | Relational database storage |
| **Streamlit** | Interactive web application |
| **Jupyter Notebook** | Exploratory analysis & documentation |

---

## 📦 Dataset Description

The project uses **4 CSV datasets** with 1,000 rows each:

### 1. Providers Dataset (`providers_data.csv`)

Food providers who donate surplus food to the system.

| Column | Type | Description |
|--------|------|-------------|
| Provider_ID | Integer | Unique identifier |
| Name | String | Provider name |
| Type | String | Supermarket / Restaurant / Grocery Store / Catering Service |
| Address | String | Physical address |
| City | String | City of the provider |
| Contact | String | Phone number |

**Provider Types:**
- 🏪 Supermarket: 262 (26.2%)
- 🛒 Grocery Store: 256 (25.6%)
- 🍽️ Restaurant: 246 (24.6%)
- 🍱 Catering Service: 236 (23.6%)

---

### 2. Receivers Dataset (`receivers_data.csv`)

Individuals and organizations that claim donated food.

| Column | Type | Description |
|--------|------|-------------|
| Receiver_ID | Integer | Unique identifier |
| Name | String | Receiver name |
| Type | String | NGO / Charity / Shelter / Individual |
| City | String | City of the receiver |
| Contact | String | Phone number |

**Receiver Types:**
- 🏢 NGO: 274 (27.4%)
- ❤️ Charity: 263 (26.3%)
- 🏠 Shelter: 246 (24.6%)
- 👤 Individual: 217 (21.7%)

---

### 3. Food Listings Dataset (`food_listings_data.csv`)

Available food items ready to be claimed.

| Column | Type | Description |
|--------|------|-------------|
| Food_ID | Integer | Unique identifier |
| Food_Name | String | Name of the food item |
| Quantity | Integer | Units available (1–50) |
| Expiry_Date | Date | Expiry date of food |
| Provider_ID | Integer | FK → providers |
| Provider_Type | String | Type of provider |
| Location | String | City where food is available |
| Food_Type | String | Vegetarian / Vegan / Non-Vegetarian |
| Meal_Type | String | Breakfast / Lunch / Dinner / Snacks |

**Summary Statistics — Quantity:**

| Metric | Value |
|--------|-------|
| Mean | 25.79 |
| Median | 26.00 |
| Min | 1 |
| Max | 50 |
| Std Dev | 14.61 |

---

### 4. Claims Dataset (`claims_data.csv`)

Records of food claims made by receivers.

| Column | Type | Description |
|--------|------|-------------|
| Claim_ID | Integer | Unique identifier |
| Food_ID | Integer | FK → food_listings |
| Receiver_ID | Integer | FK → receivers |
| Status | String | Completed / Pending / Cancelled |
| Timestamp | DateTime | Date and time of claim |

**Claim Status Breakdown:**

| Status | Count | Percentage |
|--------|-------|------------|
| Completed | 339 | 33.9% |
| Cancelled | 336 | 33.6% |
| Pending | 325 | 32.5% |

---

## 🏗️ Project Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   DATA SOURCES (CSV Files)                   │
│  providers_data.csv | receivers_data.csv | claims_data.csv  │
│                    food_listings_data.csv                    │
└────────────────────────┬────────────────────────────────────┘
                         │ pandas.read_csv()
                         ▼
┌─────────────────────────────────────────────────────────────┐
│               PYTHON DATA PROCESSING LAYER                   │
│   EDA · Cleaning · Type Conversion · Feature Engineering    │
└────────────────────────┬────────────────────────────────────┘
                         │ df.to_sql()
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                SQLite RELATIONAL DATABASE                    │
│   providers | receivers | food_listings | claims            │
│   15+ SQL Queries · CRUD Operations · JOINs · Aggregations  │
└────────────────────────┬────────────────────────────────────┘
                         │
          ┌──────────────┴──────────────┐
          ▼                             ▼
┌─────────────────┐         ┌──────────────────────┐
│  VISUALIZATIONS │         │   STREAMLIT APP       │
│  Matplotlib     │         │   Filtering · CRUD    │
│  Seaborn        │         │   Charts · Queries    │
└─────────────────┘         └──────────────────────┘
```

### Database Schema (ERD)

```
providers (Provider_ID PK, Name, Type, Address, City, Contact)
      │
      │ 1:N
      ▼
food_listings (Food_ID PK, Food_Name, Quantity, Expiry_Date,
               Provider_ID FK, Provider_Type, Location,
               Food_Type, Meal_Type)
      │
      │ 1:N
      ▼
claims (Claim_ID PK, Food_ID FK, Receiver_ID FK, Status, Timestamp)
                                       │
                                  1:N  │
                                       ▼
                         receivers (Receiver_ID PK, Name, Type, City, Contact)
```

---

## 🔍 Exploratory Data Analysis

### Data Quality Check

| Dataset | Rows | Columns | Missing Values | Duplicates |
|---------|------|---------|----------------|------------|
| providers | 1,000 | 6 | 0 | 0 |
| receivers | 1,000 | 5 | 0 | 0 |
| food_listings | 1,000 | 9 | 0 | 0 |
| claims | 1,000 | 5 | 0 | 0 |

✅ All datasets are **complete, clean, and ready** for analysis.

### EDA Questions Answered

1. **Basic characteristics** — 4 tables, 4,000 total rows, 25 total columns
2. **Structure** — Mix of categorical and numerical; dates converted to datetime
3. **Patterns** — Rice, Soup, Salad are the top donated foods
4. **Outliers** — Quantity ranges 1–50 (uniform); no extreme outliers
5. **Missing values** — Zero missing values across all datasets
6. **Data correctness** — Verified primary/foreign key integrity
7. **Correlations** — Food Type and Meal Type analyzed via heatmap
8. **Claims trends** — Explored by month using timestamp data
9. **Variability** — Quantity std dev = 14.61 on a mean of 25.79
10. **Subsets** — Analyzed by city, provider type, receiver type

---

## 📊 Data Visualizations

### Graph 1 — Provider Type Distribution

![Provider Type Distribution](g1_provider_type.png)

> **Insight:** Supermarkets (26.2%) are the most common food providers, closely followed by Grocery Stores (25.6%). All four provider types are roughly equally distributed.

---

### Graph 2 — Claim Status Distribution

![Claim Status](g2_claim_status.png)

> **Insight:** Claims are nearly equally split — 33.9% Completed, 33.6% Cancelled, 32.5% Pending. The high cancellation rate highlights a significant opportunity to improve the claim process.

---

### Graph 3 — Food Type Distribution

![Food Type](g3_food_type.png)

> **Insight:** Listings are nearly equally split between Vegetarian (33.6%), Vegan (33.4%), and Non-Vegetarian (33.0%).

---

### Graph 4 — Meal Type Distribution

![Meal Type](g4_meal_type.png)

> **Insight:** Breakfast (254) has the highest representation, followed closely by Snacks (253), Lunch (248), and Dinner (245).

---

### Graph 5 — Top 10 Most Common Food Items

![Top Foods](g5_top_foods.png)

> **Insight:** Rice (114 listings) is the most donated food item, followed by Soup (111) and Salad (105).

---

### Graph 6 — Receiver Type Distribution

![Receiver Type](g6_receiver_type.png)

> **Insight:** NGOs (274) are the largest category of food receivers, followed by Charities (263) and Shelters (246).

---

### Graph 7 — Food Quantity Distribution

![Quantity Distribution](g7_quantity_dist.png)

> **Insight:** Food quantities are fairly uniformly distributed between 1 and 50 units, with a mean of 25.79.

---

### Graph 8 — Monthly Claims by Status

![Monthly Claims](g8_monthly_claims.png)

> **Insight:** Claims activity is concentrated in March 2025. Completed, cancelled, and pending claims are evenly distributed throughout the month.

---

### Graph 9 — Top 10 Cities by Providers

![Top Cities](g9_top_cities.png)

> **Insight:** Provider distribution across cities is highly diverse — no single city dominates, indicating a wide geographic reach.

---

### Graph 10 — Food Type vs Meal Type Heatmap

![Heatmap](g10_heatmap.png)

> **Insight:** Vegetarian Breakfast (89) and Vegan Snacks (92) appear slightly more frequently, suggesting morning and snack donations skew plant-based.

---

## 🧮 SQL Queries & Insights (15 Queries)

### Q1 — Top 10 Cities by Number of Food Providers

```sql
SELECT City, COUNT(*) AS Provider_Count
FROM providers
GROUP BY City
ORDER BY Provider_Count DESC
LIMIT 10;
```

### Q2 — Provider Type Contribution (Food Quantity)

```sql
SELECT Provider_Type,
       COUNT(*)        AS Total_Listings,
       SUM(Quantity)   AS Total_Quantity
FROM food_listings
GROUP BY Provider_Type
ORDER BY Total_Quantity DESC;
```

### Q3 — Top 10 Receivers by Number of Claims

```sql
SELECT r.Name, r.Type, r.City, COUNT(c.Claim_ID) AS Total_Claims
FROM claims c
JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
GROUP BY r.Receiver_ID
ORDER BY Total_Claims DESC
LIMIT 10;
```

### Q4 — Total Food Quantity Available per City

```sql
SELECT Location AS City,
       SUM(Quantity) AS Total_Quantity,
       COUNT(Food_ID) AS Total_Items
FROM food_listings
GROUP BY Location
ORDER BY Total_Quantity DESC
LIMIT 10;
```

### Q5 — Most Common Food Types

```sql
SELECT Food_Type,
       COUNT(*) AS Count,
       SUM(Quantity) AS Total_Quantity
FROM food_listings
GROUP BY Food_Type
ORDER BY Count DESC;
```

### Q6 — Top 10 Food Items by Number of Claims

```sql
SELECT fl.Food_Name,
       COUNT(c.Claim_ID) AS Total_Claims,
       SUM(fl.Quantity)  AS Total_Quantity
FROM claims c
JOIN food_listings fl ON c.Food_ID = fl.Food_ID
GROUP BY fl.Food_Name
ORDER BY Total_Claims DESC
LIMIT 10;
```

### Q7 — Top 10 Providers by Successful Claims

```sql
SELECT p.Name, p.Type, p.City,
       COUNT(c.Claim_ID) AS Completed_Claims
FROM claims c
JOIN food_listings fl ON c.Food_ID = fl.Food_ID
JOIN providers p ON fl.Provider_ID = p.Provider_ID
WHERE c.Status = 'Completed'
GROUP BY p.Provider_ID
ORDER BY Completed_Claims DESC
LIMIT 10;
```

### Q8 — Claim Status Breakdown (%)

```sql
SELECT Status,
       COUNT(*) AS Total,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims), 2) AS Percentage
FROM claims
GROUP BY Status
ORDER BY Total DESC;
```

### Q9 — Average Quantity Claimed per Receiver Type

```sql
SELECT r.Type AS Receiver_Type,
       ROUND(AVG(fl.Quantity), 2) AS Avg_Quantity_Claimed
FROM claims c
JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
JOIN food_listings fl ON c.Food_ID = fl.Food_ID
GROUP BY r.Type
ORDER BY Avg_Quantity_Claimed DESC;
```

### Q10 — Most Popular Meal Types in Claims

```sql
SELECT fl.Meal_Type,
       COUNT(c.Claim_ID) AS Total_Claims,
       ROUND(COUNT(c.Claim_ID) * 100.0 / (SELECT COUNT(*) FROM claims), 2) AS Percentage
FROM claims c
JOIN food_listings fl ON c.Food_ID = fl.Food_ID
GROUP BY fl.Meal_Type
ORDER BY Total_Claims DESC;
```

### Q11 — Top 10 Providers by Total Food Donated

```sql
SELECT p.Name, p.Type, p.City,
       SUM(fl.Quantity) AS Total_Donated,
       COUNT(fl.Food_ID) AS Total_Listings
FROM food_listings fl
JOIN providers p ON fl.Provider_ID = p.Provider_ID
GROUP BY p.Provider_ID
ORDER BY Total_Donated DESC
LIMIT 10;
```

### Q12 — City with Highest Number of Food Listings

```sql
SELECT Location AS City, COUNT(Food_ID) AS Listing_Count
FROM food_listings
GROUP BY Location
ORDER BY Listing_Count DESC
LIMIT 1;
```

### Q13 — Food Items Expiring Within 7 Days

```sql
SELECT Food_ID, Food_Name, Quantity, Expiry_Date, Location
FROM food_listings
WHERE DATE(Expiry_Date) <= DATE('now', '+7 days')
ORDER BY Expiry_Date ASC
LIMIT 15;
```

### Q14 — Providers with No Completed Claims

```sql
SELECT p.Provider_ID, p.Name, p.Type, p.City
FROM providers p
WHERE p.Provider_ID NOT IN (
    SELECT DISTINCT fl.Provider_ID
    FROM claims c
    JOIN food_listings fl ON c.Food_ID = fl.Food_ID
    WHERE c.Status = 'Completed'
);
```

### Q15 — Cities with Both Providers and Receivers

```sql
SELECT p.City,
       COUNT(DISTINCT p.Provider_ID) AS Providers,
       COUNT(DISTINCT r.Receiver_ID) AS Receivers
FROM providers p
JOIN receivers r ON p.City = r.City
GROUP BY p.City
ORDER BY Providers DESC
LIMIT 10;
```

---

## 🔄 CRUD Operations

All four CRUD operations are demonstrated in the notebook:

| Operation | SQL Statement | Description |
|-----------|--------------|-------------|
| **CREATE** | `INSERT INTO food_listings ...` | Add a new food donation listing |
| **READ** | `SELECT * FROM food_listings WHERE ...` | Retrieve a specific record |
| **UPDATE** | `UPDATE food_listings SET Quantity = 50 ...` | Modify existing listing data |
| **DELETE** | `DELETE FROM food_listings WHERE ...` | Remove a food listing |

---

## 🌐 Streamlit Application

The Streamlit app (`foods_app.py`) provides an interactive interface:

### Features

- 📋 **Data Display** — View all 4 datasets in tabular format
- 🔍 **Filtering** — Filter by City, Provider Type, Food Type, Meal Type
- 📊 **Visualizations** — Embedded charts and graphs
- 🗄️ **SQL Query Results** — Display outputs of all 15 SQL queries
- ✏️ **CRUD Panel** — Add, update, and delete food listings through UI
- 📞 **Contact Details** — View provider and receiver contact info

### Run the App

```bash
streamlit run foods_app.py
```

---

## 💡 Key Insights

| # | Insight |
|---|---------|
| 1 | **25,794 total food units** are available across all listings |
| 2 | **33.9% of claims are successfully completed** — leaving room for improvement |
| 3 | **Supermarkets** are the leading provider type by count |
| 4 | **Rice** is the most frequently donated food item (114 listings) |
| 5 | **NGOs** handle the most food claims among receiver categories |
| 6 | **No missing values** — dataset is clean and reliable |
| 7 | **Claim cancellations (33.6%)** indicate a logistical gap worth addressing |
| 8 | Food is distributed across **diverse city locations** — no single hotspot |
| 9 | **Vegetarian and Vegan** foods slightly outnumber Non-Vegetarian listings |
| 10 | **Breakfast items** are donated most frequently across all meal types |

---

## 📁 Project Structure

```
food-waste-Management/
│
├── 📓 food_wastage_analysis.ipynb   # Main Jupyter Notebook (EDA + SQL + CRUD)
├── 🐍 foods_app.py                  # Streamlit Web Application
├── 📖 README.md                     # This file
│
├── 📊 CSV Data Files/
│   ├── providers_data.csv
│   ├── receivers_data.csv
│   ├── food_listings_data.csv
│   └── claims_data.csv
│
├── 📈 Graph Images/
│   ├── g1_provider_type.png
│   ├── g2_claim_status.png
│   ├── g3_food_type.png
│   ├── g4_meal_type.png
│   ├── g5_top_foods.png
│   ├── g6_receiver_type.png
│   ├── g7_quantity_dist.png
│   ├── g8_monthly_claims.png
│   ├── g9_top_cities.png
│   └── g10_heatmap.png
│
└── 🗄️ food_wastage.db               # SQLite database (auto-generated by notebook)
```

---

## 🚀 Getting Started (Clone & Run)

Follow these steps to clone and run this project on your local machine.

### Prerequisites

Make sure you have the following installed:

- **Python 3.10 or higher** → [Download Python](https://www.python.org/downloads/)
- **pip** (comes with Python)
- **Git** → [Download Git](https://git-scm.com/downloads)

### Step 1 — Clone the Repository

```bash
git clone https://github.com/pardeep0011/food-waste-Management.git
cd food-waste-Management
```

### Step 2 — Install Required Libraries

```bash
pip install pandas numpy matplotlib seaborn streamlit jupyter
```

> **Optional:** Create a virtual environment first to keep dependencies isolated:
> ```bash
> python -m venv venv
> # On Windows:
> venv\Scripts\activate
> # On Mac/Linux:
> source venv/bin/activate
> ```

### Step 3 — Run the Jupyter Notebook

This will perform EDA, generate the graphs, and create the SQLite database:

```bash
jupyter notebook food_wastage_analysis.ipynb
```

Once Jupyter opens in your browser, click **"Run All Cells"** (Kernel → Restart & Run All).

### Step 4 — Launch the Streamlit App

```bash
streamlit run foods_app.py
```

The app will automatically open at `http://localhost:8501` in your browser.

---

### 🔁 Quick Reference — All Commands

```bash
# 1. Clone the repo
git clone https://github.com/pardeep0011/food-waste-Management.git

# 2. Enter the project folder
cd food-waste-Management

# 3. Install dependencies
pip install pandas numpy matplotlib seaborn streamlit jupyter

# 4. Run the Jupyter Notebook (for EDA + database generation)
jupyter notebook food_wastage_analysis.ipynb

# 5. Run the Streamlit App
streamlit run foods_app.py
```

---

## 📏 Evaluation Metrics

| Metric | Description | Marks |
|--------|-------------|-------|
| Code Quality / Data Transformations | Clean, well-commented code with proper EDA | 10 |
| Documentation / README / Insights | Comprehensive README + notebook documentation | 10 |
| Code Reusability / Modular Programming | Helper functions (`run_query`), reusable sections | 10 |
| Presentation | Clear visualizations, structured notebook flow | 10 |
| Task Accomplishment | 15+ queries, CRUD, EDA, Streamlit app | 10 |
| Mock Questions | SQL, Python, Streamlit, Data Analysis concepts | 10 |
| **Total** | | **60** |

---

## 🚀 Future Enhancements

- [ ] **Real-time notifications** — Alert receivers when matching food is listed
- [ ] **Geolocation mapping** — Show providers and receivers on an interactive map
- [ ] **ML demand prediction** — Forecast which food types will be claimed fastest
- [ ] **Expiry alerts** — Automated reminders for food nearing expiry
- [ ] **Mobile app** — React Native frontend for field workers
- [ ] **Rating system** — Providers and receivers rate each other post-claim
- [ ] **Route optimization** — Suggest pickup routes for volunteer drivers
- [ ] **Multi-language support** — Local language UI for wider accessibility

---

## 📚 References

- [Streamlit Documentation](https://docs.streamlit.io)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Seaborn Documentation](https://seaborn.pydata.org)
- [Matplotlib Documentation](https://matplotlib.org/stable/contents.html)

---

## 👤 Author

**Pardeep** — [@pardeep0011](https://github.com/pardeep0011)  
Domain: Food Management · Waste Reduction · Social Good  
Tech Stack: Python · SQL · Streamlit · Data Analysis

---

*"Every meal saved is a life nourished."* 🌱

**Made with ❤️ to reduce food wastage and fight hunger**
