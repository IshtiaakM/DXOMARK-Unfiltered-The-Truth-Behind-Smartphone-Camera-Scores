# DXOMARK Unfiltered: The Truth Behind Smartphone Camera Scores

## 🔍 Problem Statement  
Smartphone brand loves to do marketing about big numbers such as **200MP**, **f/1.6**, **5 cameras**, **flagship chipset** . But do these specs actually translate into better photos? 
There was **no centralized, data-backed way** to objectively or visually compare camera performance across brands, price ranges, and years.

The goal of this project was to scrape DXOMARK camera test results, clean and structure the data, and understand what truly affects camera quality by visualizing through Tableau to answer questions such as:

> **Do Megapixels, Sensor Aperture, and Camera Count correlate with real-world scores??  
Which chipset and brands optimize image processing best? <br/> 
Does Image Processing score correlate with the final DXOMARK-like camera score? <br/> 
And Most asked question, Which phones deliver the best value per dollar?**

All findings were visualized in a fully interactive [Tableau dashboard](https://public.tableau.com/app/profile/ishtiak.mahmud/viz/DXOMARKUnfilteredTheTruthBehindSmartphoneCameraScores/Overview) (4 pages)  
---

## 📁 Data Source & Collection

### Website Scraped  
```

https://www.dxomark.com/smartphones/

````

### Scraping Method  
Data extraction was done using **Selenium**. The required data was not available on a single page; instead, it was distributed across multiple pages.

The scraping process followed these steps:
1. Load and scroll through the full smartphone ranking list to ensure all devices were rendered.
2. Extract the basic metadata and profile links for each phone from the main page.
3. For every phone, visit **two different detail pages**:
   - One page to collect **Chipset, Camera lense info**.
   - Another page to extract **related scores**.
4. Merge data from all pages into a single structured dataset.

This multi-step navigation approach was necessary to accurately collect complete and reliable data for all smartphones.

Data scraped from:
| Source | Fields Extracted |
|---|---|
| Smartphone Ranking Page | Rank, Device Name, Launch price, Launch year |
| Individual Device Page | Chipset, Camera lense, No. of Camera |
| Individual Device Score Page | photo score, video score, photo sub score,bokeh score |

---

## 📊 Dataset — Final Structured Fields

| Category | Fields |
|---|---|
| Device Info | Brand, Model, Launch Year, Price |
| Camera Quality | Overall Score, Photo Score, Video Score |
| Hardware Specs | Camera MP, Aperture |
| ISP Metrics | Exposure, Color, Texture, Noise, Artifacts |
| Chipset Info | Snapdragon, A-series, Exynos, MediaTek, HarmonyOS |

### Data Cleaning Highlights  
✔ Converted MP + Aperture to floats  
✔ Created and Normalized chipset naming (MediaTek, Exynos, HarmonyOS…)  
✔ Removed Null values from the data 
✔ Created calculated fields for:  
- Budget classification
- MP buckets  

Final cleaned CSV was used for Tableau dashboards.

---

## 📊 Dashboard Summary (4 Pages)

### **1️⃣ Overview**
![image alt](https://github.com/IshtiaakM/DXOMARK-Unfiltered-The-Truth-Behind-Smartphone-Camera-Scores/blob/main/dashboard%20images/dashboard%201.png?raw=true)
**Purpose:** High-level summary of smartphone camera landscape  
🔹 Total brands analyzed  
🔹 Top score achieved  
🔹 Avg camera score across market  
🔹 Brand leaderboard by avg performance  
🔹 Top 15 camera phones visual comparison  

**Insights Found:**  
- Huawei leads global camera performance  
- Apple, Google, Vivo maintain strong averages  
- Motorola & Sony remain lower tier in DXOMARK scoring

---

### **2️⃣ Hardware Impact – Do specs really matter?**  
Focus: Megapixels + Aperture vs Real Results
![image alt](https://github.com/IshtiaakM/DXOMARK-Unfiltered-The-Truth-Behind-Smartphone-Camera-Scores/blob/main/dashboard%20images/dashboard%202.png?raw=true)

Visuals Included:
- MP vs Camera Score Scatter
- MP Bucket Avg Score Bar Chart
- Aperture vs Photo Score Scatter
- Aperture vs Video Score Scatter

**Key Takeaways:**  
| Myth | Truth from Data |
|---|---|
| More megapixels = better photos | Scores peak in **50–99MP**, high MP shows no benefit |
| Wider aperture guarantees better photos | ⚠ Improved low-light slightly, but **not strongly correlated** |
| Hardware defines image quality | ❗ ISP & tuning matter far more |

---

### **3️⃣ Chipset & ISP Intelligence – Who processes images best?**  
Focus: Computational photography & post-processing impact
![image alt](https://github.com/IshtiaakM/DXOMARK-Unfiltered-The-Truth-Behind-Smartphone-Camera-Scores/blob/main/dashboard%20images/dashboard%203.png?raw=true)

Visuals Included:
- ISP Score Distribution by Chip Variant
- Subscore Heatmap (Color, AutoFocuse, Texture, Noise, Exposure, artifacts, Stabilization)
- Brand ISP Matrix
- Image Processing vs Overall Score Correlation

**Findings:**  
✔ Snapdragon & Apple lead overall ISP optimization  
✔ Huawei/HarmonyOS performs efficiently despite lower MP hardware  
✔ Strong correlation between **image processing score & final DXOMARK score** (higher than MP/aperture)

> **Conclusion:**  
> Modern smartphone photography is a * algorithmic processing war*, not a megapixel war.

---

### **4️⃣ Camera Value — Price vs Score Reality Check**  
Focus: Best value, overpriced models & yearly winners
![image alt](https://github.com/IshtiaakM/DXOMARK-Unfiltered-The-Truth-Behind-Smartphone-Camera-Scores/blob/main/dashboard%20images/dashboard%204.png?raw=true)

Visuals Included:
- **Price vs Score Quadrant Scatter per Year**
- **Best Budget Phone of Each Year (2020–2025)**

Quadrants Explained:
| Region | Meaning |
|---|---|
| High Score • Low Price | *Best Value* |
| High Score • High Price | Premium Justified |
| Low Score • Low Price | Decent Budget |
| Low Score • High Price | *Overpriced disappointments* |

📌 From 2023 onwards, affordable phones show massive score improvements → **budget cameras are catching flagship quality fast**.

---

## Build From Sources and Run the Selenium Scraper yourself

1. Clone the repo
```bash
git clone https://github.com/IshtiaakM/DXOMARK-Unfiltered-The-Truth-Behind-Smartphone-Camera-Scores.git
````

2. Setup virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
pip install -r requirements.txt
```

3. Run the scraper

```bash
python dxo_scraper.py
```

4. You will get a file named `dxomark_phones.csv` containing all the required fields. For further data transformation and you will get a file `Final_dxoMark_scores.csv` 
Alternatively, check our scraped data here: 

---
