# Executive Summary
# Nassau Candy Distributor — Factory Reallocation & Shipping Optimization
**For:** Senior Leadership & Operations Stakeholders
**Date:** May 2026
**Prepared by:** Data Analytics Team

---

## The Problem
Nassau Candy Distributor assigns its 15 products to 5 factories using
static legacy rules. This results in suboptimal shipping routes, excessive
lead times for certain products, and margin erosion — with no system to
quantify or simulate improvements before making changes.

---

## What We Did
We analyzed 9,949 orders from 2024–2025 using machine learning and
simulation to answer one question: **which products should move to which
factory, and is it safe to do so?**

Our approach in plain terms:
1. Cleaned and enriched the data (lead times, distances, margins)
2. Built 3 machine learning models to predict shipping lead times
3. Clustered all routes into 4 performance groups
4. Simulated 60 factory reassignment scenarios
5. Ranked every recommendation by improvement, margin, and risk

---

## What We Found

### 🔴 Critical Issues
| Issue | Detail |
|-------|--------|
| First Class is SLOWER than Standard Class | Systemic carrier misassignment |
| Sugar Shack → Pacific: 1,517 day avg lead time | Worst route in the network |
| The Other Factory: 42.7% profit margin | Far below 66.5% company average |

### 🏆 Top Opportunity
| Product | Action | Lead Time Saved | Risk |
|---------|--------|----------------|------|
| Everlasting Gobstopper | Move from Secret Factory to Lot's O' Nuts | **115.7 days** | 🟢 LOW |

### 📋 Full Recommendation Summary
| Priority | Product | Move To | Days Saved | Risk |
|----------|---------|---------|-----------|------|
| 1 | Everlasting Gobstopper | Lot's O' Nuts | +115.7d | 🟢 Low |
| 2 | SweeTARTS | Secret Factory | +72.9d | 🟡 Medium |
| 3 | Laffy Taffy | Wicked Choccy's | +37.2d | 🟡 Medium |
| 4 | Fizzy Lifting Drinks | Lot's O' Nuts | +24.7d | 🟡 Medium |
| 5 | Lickable Wallpaper | Wicked Choccy's | +16.6d | 🟡 Medium |
| — | Hair Toffee, Nerds, Wonka Gum, Kazookles, Fun Dip | Stay put | — | 🔴 Do Not Move |

---

## Financial Impact
| Metric | Value |
|--------|-------|
| Total potential days saved (all actionable) | 292.9 days |
| Avg saving per product | 29.3 days |
| Products with positive ROI on reallocation | 10 of 15 |
| Overall avg profit margin maintained | 66.5% |
| Highest margin product (Everlasting Gobstopper) | 80.0% |

---

## Recommended Actions — In Order

**Week 1–2 (Immediate):**
Move Everlasting Gobstopper to Lot's O' Nuts.
Low risk, high confidence, 115.7 day saving.

**Month 1–2 (Evaluate):**
Commission detailed logistics review for SweeTARTS and Laffy Taffy
reallocation. Margin sensitivity analysis recommended before execution.

**Month 2–3 (Systemic):**
Audit First Class carrier contracts — this shipping mode is
underperforming Standard Class, which is a direct cost inefficiency.
Review The Other Factory's profitability with operations leadership.

**Ongoing:**
Use the delivered Streamlit dashboard for quarterly reallocation reviews
as product portfolio and market conditions change.

---

## Deliverables Submitted
- Research paper with full methodology and findings
- Streamlit live dashboard (4 modules: Simulator, What-If, Recommendations, Risk)
- Cleaned dataset and all simulation outputs (CSV files)
- This executive summary

---

*This analysis was produced using Gradient Boosting machine learning,
K-Means route clustering, and Haversine-based geospatial simulation
across 60 factory-product scenarios.*
