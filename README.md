# 🏃 Boston Marathon Data Visualization Dashboard

A professional-grade, interactive data visualization dashboard analyzing Boston Marathon winners data (Men's 1897–2024 & Women's 1966–2024). Built with **Streamlit**, **Pandas**, **Matplotlib**, and **Seaborn**.

---

## 📌 Project Overview

This dashboard presents comprehensive insights into the Boston Marathon's historical winning data, featuring:
- **13 chart types** (10 required + 3 bonus)
- **6 interactive filter types** that update all charts simultaneously
- **KPI summary cards** for quick insights
- Noon-inspired premium dark theme with amber/gold accents

---

## 📊 Features

### Charts Included
| # | Chart Type | Purpose |
|---|-----------|---------|
| 1 | Pie Chart | Winners distribution by country |
| 2 | Histogram | Frequency distribution of finishing times |
| 3 | Line Chart | Winning times trend over years |
| 4 | Bar Chart | Top 10 countries by total wins |
| 5 | Scatter Plot | Year vs finishing time relationship |
| 6 | Box Plot | Time distribution by gender |
| 7 | Heatmap | Feature correlation matrix |
| 8 | Area Chart | Cumulative wins over time |
| 9 | Count Plot | Winners per decade |
| 10 | Violin Plot | Time distribution density |
| 11 | Pair Plot *(Bonus)* | Multi-feature relationships |
| 12 | Bubble Chart *(Bonus)* | Year vs time with speed as size |
| 13 | Funnel Chart *(Bonus)* | Time bracket distribution |

### Interactive Filters
- 📅 **Year Range Slider** — Filter by year range
- 👤 **Gender Dropdown** — Filter by Male/Female
- ⏱️ **Time Range Slider** — Filter by finishing time (minutes)
- 🌍 **Country Multi-Select** — Select specific countries
- 🔍 **Search Box** — Search by winner name
- 🔄 **Reset Button** — Clear all filters to default

---

## 🛠️ Technical Stack

| Tool | Role |
|------|------|
| Python 3.x | Core language |
| Pandas | Data loading, cleaning, filtering |
| NumPy | Numerical operations |
| Matplotlib | Core plotting and chart creation |
| Seaborn | Statistical visualizations and styling |
| Streamlit | Interactive dashboard frontend |

---

## 📂 Project Structure

```
/dashboard_project/
├── data/
│   ├── Mens_Boston_Marathon_Winners_r0l7bV.csv
│   └── Womens_Boston_Marathon_Winners_8SSnWb.csv
├── notebooks/
│   └── analysis.ipynb          # Exploratory Data Analysis
├── .streamlit/
│   └── config.toml             # Streamlit server config
├── app.py                      # Main dashboard application
├── charts.py                   # Chart / visualization functions
├── filters.py                  # Filter / data processing functions
├── requirements.txt            # Python packages
├── render.yaml                 # Render deployment config
├── railway.toml                # Railway deployment config
├── nixpacks.toml               # Nixpacks build config
├── Dockerfile                  # Docker containerization
├── Procfile                    # PaaS start command
├── .env.example                # Environment variable template
├── .gitignore                  # Git exclusions
├── DEPLOYMENT_GUIDE.md         # Deployment instructions
└── README.md                   # This file
```

---

## 🚀 How to Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Dashboard
```bash
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`

---

## 📈 Key Insights

1. **Historical Dominance**: The United States has the most wins, especially in the early decades of the marathon.
2. **Kenyan & Ethiopian Rise**: From the 1990s onward, East African runners (Kenya, Ethiopia) began dominating both men's and women's categories.
3. **Improving Times**: There is a clear downward trend in winning times over the decades, showing improved athletic performance.
4. **Gender Gap Narrowing**: Women's winning times have progressively gotten closer to men's times since women were first allowed to compete officially.
5. **Distance Standardization**: The marathon distance was standardized to 26.2 miles (42.2 km) — earlier races had shorter distances.

---

## 🚀 Deployment

This project is deployment-ready for **Render** and **Railway**.

### Quick Deploy on Render
```bash
# Push to GitHub, then:
# 1. Go to render.com → New Web Service → Connect repo
# 2. Build Command: pip install -r requirements.txt
# 3. Start Command: streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true
# Or use the included render.yaml with Render Blueprints
```

### Quick Deploy on Railway
```bash
# Push to GitHub, then:
# 1. Go to railway.app → New Project → Deploy from GitHub
# 2. Railway auto-detects Python + uses railway.toml config
# 3. Generate a domain in Settings → Networking
```

### Docker
```bash
docker build -t marathon-dashboard .
docker run -p 8501:8501 marathon-dashboard
```

📖 See **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** for full step-by-step instructions.

---

## 📝 Data Description

- **Men's Data**: 126 records (1897–2024)
- **Women's Data**: 57 records (1966–2024)
- **Features**: Year, Winner, Country, Time, Distance (Miles), Distance (KM)
- **Derived Features**: Time in Minutes, Pace per Mile/KM, Speed (MPH), Decade

---

## 👤 Author

**Boston Marathon** — Exploratory Data Analysis Course Project

**Instructor**: Ali Hassan Sherazi

**Submission Date**: 05-June-2026
