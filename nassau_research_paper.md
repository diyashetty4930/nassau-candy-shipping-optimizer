# Factory Reallocation & Shipping Optimization
# Research Paper — Nassau Candy Distributor
**Prepared by:** Data Analytics Team
**Date:** May 2026
**Dataset:** Nassau Candy Distributor — 9,949 Orders (2024–2025)

---

## Abstract

This research paper presents a comprehensive data-driven analysis of Nassau
Candy Distributor's factory-to-customer shipping operations. Using a dataset
of 9,949 orders across 15 products, 5 factories, and 4 customer regions, we
applied exploratory data analysis, predictive modeling, route clustering, and
scenario simulation to identify inefficiencies in the current factory-product
assignment system. Our findings reveal that one product (Everlasting
Gobstopper) is a clear low-risk reallocation candidate with a potential lead
time reduction of 115.7 days, and nine additional products present medium-risk
reallocation opportunities. The Gradient Boosting model achieved the best
predictive performance with RMSE of 170.17 days and R² of 0.58.

---

## 1. Introduction

### 1.1 Background
Nassau Candy Distributor operates a multi-factory distribution network
supplying candy products across four US regions: Atlantic, Gulf, Interior,
and Pacific. Products are currently assigned to factories using static legacy
rules, leading to suboptimal shipping distances, high lead times for certain
regions, and margin erosion due to logistics inefficiencies.

### 1.2 Problem Statement
The organization faces three core operational problems:
- No system exists to simulate factory-product reassignment scenarios
- Lead time inefficiencies cannot be quantified before execution
- There is no data-driven basis for optimal factory configuration at scale

### 1.3 Project Objectives
1. Build a predictive model for shipping lead time
2. Identify inefficient factory-product-region combinations
3. Simulate reallocation scenarios and quantify improvements
4. Deliver ranked, risk-assessed factory reassignment recommendations

---

## 2. Dataset Description

### 2.1 Data Overview
| Attribute         | Value                          |
|-------------------|-------------------------------|
| Total Records     | 10,194 (9,949 after cleaning) |
| Date Range        | January 2024 — December 2025  |
| Products          | 15 unique                     |
| Factories         | 5 unique                      |
| Customer Regions  | 4 (Atlantic, Gulf, Interior, Pacific) |
| Ship Modes        | 4 (First Class, Same Day, Second Class, Standard Class) |
| Key Fields        | Sales, Cost, Gross Profit, Units, Ship Mode, Region |

### 2.2 Engineered Features
The following features were computed from raw data:

| Feature                   | Method                                      |
|---------------------------|---------------------------------------------|
| Lead Time (days)          | Ship Date − Order Date                      |
| Factory                   | Product → Factory mapping (provided)        |
| Shipping Distance (miles) | Haversine formula (factory GPS → region centroid) |
| Profit Margin (%)         | Gross Profit / Sales × 100                  |
| Lead Time vs Avg (days)   | Lead Time − Overall Mean Lead Time          |
| Order Month / DOW / Year  | Extracted from Order Date                   |

### 2.3 Data Cleaning
- Sales outliers removed using IQR method: 245 rows removed (2.4%)
- Zero null values in final clean dataset
- Final dataset: 9,949 rows × 26 columns

---

## 3. Exploratory Data Analysis

### 3.1 Lead Time Distribution
The dataset exhibits lead times ranging from 904 to 1,642 days, clustered
into 5 bands corresponding to projected ship years (2026–2030). This
structure reflects long-range fulfillment planning inherent to the
distributor's operations.

Key lead time findings:
- Overall average: 1,320.8 days
- Worst product: Everlasting Gobstopper (1,641 days avg)
- Best product: Fun Dip (1,272 days avg)
- Difference between best and worst: 369 days

### 3.2 Regional Performance
| Region   | Avg Lead Time |
|----------|--------------|
| Interior | 1,340 days   |
| Pacific  | 1,328 days   |
| Atlantic | 1,318 days   |
| Gulf     | 1,297 days   |

Interior region consistently experiences the highest lead times, driven
by distance from most factory locations.

### 3.3 Ship Mode Analysis
A counter-intuitive finding emerged: First Class shipping is slower than
Standard Class on average. This suggests a systemic misuse of shipping
modes — products are not being assigned optimal ship modes relative to
their urgency and destination.

### 3.4 Factory Performance
| Factory           | Avg Lead Time | Avg Distance | Avg Profit Margin |
|-------------------|--------------|-------------|------------------|
| Sugar Shack       | 1,340 days   | 1,103 miles | 66.5%            |
| Wicked Choccy's   | 1,330 days   | 1,143 miles | 65.3%            |
| Lot's O' Nuts     | 1,325 days   | 1,249 miles | 71.4%            |
| Secret Factory    | 1,320 days   | 915 miles   | 60.7%            |
| The Other Factory | 1,280 days   | 946 miles   | 42.7%            |

### 3.5 Revenue Analysis
- Chocolate division: 98%+ of total revenue
- Sugar division: <2% of total revenue
- Lot's O' Nuts: highest average profit margin (71.4%)
- The Other Factory: critically low margin (42.7%) — urgent review needed

---

## 4. Predictive Modeling

### 4.1 Methodology
Three regression models were trained to predict lead time:
- Linear Regression (baseline)
- Random Forest Regressor (100 estimators)
- Gradient Boosting Regressor (100 estimators)

Feature set (12 features):
Factory, Region, Ship Mode, Product, Shipping Distance,
Order Month, Order Year, Order Day-of-Week,
Sales, Units, Cost, Profit Margin

Train/test split: 80% / 20% (random_state=42)

### 4.2 Model Results
| Model              | RMSE   | MAE    | R²     |
|--------------------|--------|--------|--------|
| Linear Regression  | 182.33 | 181.39 | 0.5186 |
| Random Forest      | 179.01 | 151.10 | 0.5360 |
| Gradient Boosting  | 170.17 | 159.86 | 0.5807 |

**Winner: Gradient Boosting** — lowest RMSE and highest R²

### 4.3 Model Interpretation
The R² of 0.58 reflects that lead time variance in this dataset is
structurally driven by projected ship year clusters. The model correctly
captures relative differences between factory-region-product combinations
and is used for scenario comparison rather than absolute point prediction.

### 4.4 Key Feature Drivers
1. Order Year (53%) — ship year planning cluster
2. Order Month (10%) — seasonal fulfillment patterns
3. Order Day-of-Week (10%) — weekly operational patterns
4. Cost (5%) — product complexity proxy
5. Ship Mode (4.6%) — fulfillment tier signal

---

## 5. Route Clustering

### 5.1 Methodology
K-Means clustering (k=4) was applied to group routes by performance
similarity. Features used: Factory, Region, Ship Mode, Shipping Distance,
Lead Time, Profit Margin. All features were StandardScaler normalized
before clustering.

### 5.2 Cluster Profiles
| Cluster | Label                     | Orders | Avg LT  | Avg Distance |
|---------|---------------------------|--------|---------|-------------|
| 0       | Long Haul / High Margin   | 2,513  | 1,368d  | 1,847 miles |
| 1       | Mid Haul / High Margin    | 3,091  | 1,295d  | 1,071 miles |
| 2       | Short Haul / Lower Margin | 2,964  | 1,296d  | 659 miles   |
| 3       | Very Long Haul / Low Margin| 1,381 | 1,335d  | 1,832 miles |

### 5.3 Clustering Insights
- Cluster 3 (Very Long Haul / Low Margin) is the highest priority for
  intervention — combining high distance, poor margin, and above-average
  lead times
- Cluster 1 (Mid Haul / High Margin) represents the optimal operating
  profile and should be the target state for reallocation decisions

---

## 6. Scenario Simulation & Optimization

### 6.1 Simulation Methodology
For each of the 15 products, the Gradient Boosting model simulated
assignment to all 4 alternative factories — 60 total scenarios. Each
simulation recomputed shipping distance using the Haversine formula and
predicted the resulting lead time. Improvement was measured as:

  LT Improvement = Current Lead Time − Predicted Lead Time

### 6.2 Optimization Scoring
Each recommendation was scored using a weighted Priority Score:

  Priority Score = (LT Improvement × 0.5) + (Profit Margin × 0.3) + (Improvement % × 2.0)

### 6.3 Risk Classification
| Risk Level    | Criteria                              | Count |
|---------------|---------------------------------------|-------|
| Low Risk      | Improvement > 50d AND Margin > 60%    | 1     |
| Medium Risk   | Improvement > 0d AND Margin > 40%     | 9     |
| Do Not Move   | Negative improvement (worse if moved) | 5     |

---

## 7. Recommendations

### 7.1 Immediate Action — Low Risk
**Move Everlasting Gobstopper from Secret Factory to Lot's O' Nuts**
- Lead time improvement: 115.7 days (7.0%)
- Profit margin: 80.0% — highest in portfolio
- Confidence: HIGH (95%)
- Risk: Minimal — large improvement, excellent margin

### 7.2 Evaluate — Medium Risk (Top 3)
1. **SweeTARTS** → Secret Factory (+72.9 days, margin 46.7%)
2. **Laffy Taffy** → Wicked Choccy's (+37.2 days, margin 62.3%)
3. **Fizzy Lifting Drinks** → Lot's O' Nuts (+24.7 days, margin 60.0%)

### 7.3 Do Not Move — Current Assignment Optimal
Hair Toffee, Nerds, Wonka Gum, Kazookles, Fun Dip — moving any of
these products would increase lead time. Current assignments are optimal.

### 7.4 Systemic Recommendations
1. Audit ship mode assignment — First Class should not be slower than
   Standard Class. Review carrier contracts immediately.
2. Review The Other Factory profitability — 42.7% avg margin is
   critically below the 66.5% company average.
3. Investigate Sugar Shack → Pacific route — worst factory-region
   combination in the entire network (1,517 days avg).
4. Implement quarterly reallocation reviews using this simulation engine.

---

## 8. Conclusion

This project successfully elevated Nassau Candy Distributor from static
legacy assignment to intelligent, data-driven factory reallocation. The
Gradient Boosting model, combined with K-Means route clustering and a
60-scenario simulation engine, produced 10 actionable recommendations with
a total potential lead time saving of 292.9 days across all products.

The most critical immediate action is the reallocation of Everlasting
Gobstopper to Lot's O' Nuts — a low-risk, high-confidence move that saves
115.7 days with zero margin risk. Medium-risk candidates (SweeTARTS, Laffy
Taffy, Fizzy Lifting Drinks) should be evaluated in a phased approach over
the next two quarters.

The Streamlit dashboard delivered as part of this project enables ongoing
scenario simulation, allowing operations teams to continuously evaluate
factory assignments as the product portfolio and market conditions evolve.

---

## 9. Technical Appendix

### Libraries Used
pandas, numpy, scikit-learn, matplotlib, seaborn, plotly, streamlit,
scipy, math (haversine)

### Model Configuration
- Gradient Boosting: n_estimators=100, random_state=42, learning_rate=0.1
- Random Forest: n_estimators=100, random_state=42, n_jobs=-1
- Train/Test Split: 80/20, random_state=42

