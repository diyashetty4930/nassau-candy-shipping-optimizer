# ============================================================
#  Nassau Candy Distributor — Streamlit Dashboard
#  Factory Reallocation & Shipping Optimization System
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from math import radians, cos, sin, asin, sqrt

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nassau Candy — Shipping Optimizer",
    page_icon="🍫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Color palette ─────────────────────────────────────────────────────────────
FACTORY_COLORS = {
    "Lot's O' Nuts"    : "#6C63FF",
    "Wicked Choccy's"  : "#FF6584",
    "Sugar Shack"      : "#43B89C",
    "Secret Factory"   : "#F9A825",
    "The Other Factory": "#EF5350",
}
RISK_COLORS = {
    "🟢 LOW RISK"    : "#43B89C",
    "🟡 MEDIUM RISK" : "#F9A825",
    "🔴 DO NOT MOVE" : "#EF5350",
}

# ── Constants ─────────────────────────────────────────────────────────────────
FACTORY_COORDS = {
    "Lot's O' Nuts"    : (32.881893, -111.768036),
    "Wicked Choccy's"  : (32.076176,  -81.088371),
    "Sugar Shack"      : (48.119140,  -96.181150),
    "Secret Factory"   : (41.446333,  -90.565487),
    "The Other Factory": (35.117500,  -89.971107),
}
REGION_COORDS = {
    "Atlantic" : (35.5,  -78.0),
    "Gulf"     : (30.0,  -90.5),
    "Interior" : (41.5,  -93.0),
    "Pacific"  : (37.5, -122.0),
}

# ── Helper ────────────────────────────────────────────────────────────────────
def haversine(lat1, lon1, lat2, lon2):
    R = 3958.8
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    a = sin((lat2-lat1)/2)**2 + cos(lat1)*cos(lat2)*sin((lon2-lon1)/2)**2
    return R * 2 * asin(sqrt(a))

# ── Data loader ───────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df    = pd.read_csv("nassau_candy_clean.csv",
                        parse_dates=["Order Date","Ship Date"])
    recs  = pd.read_csv("nassau_final_recommendations.csv")
    sim   = pd.read_csv("nassau_simulation_all.csv")
    return df, recs, sim

df, recs, sim = load_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Wonka_candy.svg/200px-Wonka_candy.svg.png",
             width=80)
    st.title("🍫 Nassau Candy")
    st.markdown("**Shipping Optimization System**")
    st.markdown("---")
    st.markdown("### Filters")
    selected_region   = st.multiselect("Region",
                                        df["Region"].unique().tolist(),
                                        default=df["Region"].unique().tolist())
    selected_shipmode = st.multiselect("Ship Mode",
                                        df["Ship Mode"].unique().tolist(),
                                        default=df["Ship Mode"].unique().tolist())
    selected_division = st.multiselect("Division",
                                        df["Division"].unique().tolist(),
                                        default=df["Division"].unique().tolist())
    st.markdown("---")
    opt_weight = st.slider("Optimization Priority",
                           min_value=0, max_value=100, value=60,
                           help="0 = Prioritize Profit  |  100 = Prioritize Speed")
    st.caption(f"Speed weight: {opt_weight}%  |  Profit weight: {100-opt_weight}%")
    st.markdown("---")
    st.markdown("**Model:** Gradient Boosting")
    st.markdown("**R² Score:** 0.5807")
    st.markdown("**Best RMSE:** 170.17 days")

# ── Apply filters ─────────────────────────────────────────────────────────────
df_f = df[
    df["Region"].isin(selected_region) &
    df["Ship Mode"].isin(selected_shipmode) &
    df["Division"].isin(selected_division)
]

# ── Page title ────────────────────────────────────────────────────────────────
st.title("🍫 Nassau Candy Distributor")
st.markdown("### Factory Reallocation & Shipping Optimization Dashboard")
st.markdown("---")

# ── TOP KPI METRICS ROW ───────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("📦 Total Orders",       f"{len(df_f):,}")
k2.metric("⏱️ Avg Lead Time",       f"{df_f['Lead Time'].mean():.0f}d")
k3.metric("📏 Avg Distance",        f"{df_f['Shipping Distance (miles)'].mean():.0f} mi")
k4.metric("💰 Avg Profit Margin",   f"{df_f['Profit Margin (%)'].mean():.1f}%")
k5.metric("🏭 Active Factories",    f"{df_f['Factory'].nunique()}")
st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# TAB LAYOUT
# ══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4 = st.tabs([
    "🏭 Factory Simulator",
    "🔄 What-If Analysis",
    "🏆 Recommendations",
    "⚠️ Risk & Impact"
])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — FACTORY OPTIMIZATION SIMULATOR
# ─────────────────────────────────────────────────────────────────────────────
with tab1:
    st.subheader("🏭 Factory Optimization Simulator")
    st.markdown("Select a product to see its predicted performance across all factories.")

    col1, col2 = st.columns([1, 2])

    with col1:
        selected_product = st.selectbox("Select Product", sorted(df["Product Name"].unique()))
        selected_sm      = st.selectbox("Ship Mode", df["Ship Mode"].unique())
        selected_reg     = st.selectbox("Target Region", df["Region"].unique())

        # Current assignment info
        current_factory = df[df["Product Name"]==selected_product]["Factory"].iloc[0]
        current_lt      = df[df["Product Name"]==selected_product]["Lead Time"].mean()
        current_pm      = df[df["Product Name"]==selected_product]["Profit Margin (%)"].mean()
        current_dist    = df[df["Product Name"]==selected_product]["Shipping Distance (miles)"].mean()

        st.markdown("**Current Assignment**")
        st.info(f"**Factory:** {current_factory}\n\n"
                f"**Avg Lead Time:** {current_lt:.0f} days\n\n"
                f"**Avg Distance:** {current_dist:.0f} miles\n\n"
                f"**Profit Margin:** {current_pm:.1f}%")

    with col2:
        # Performance across all factories
        factory_perf = []
        for fname, (flat, flon) in FACTORY_COORDS.items():
            r_lat, r_lon = REGION_COORDS[selected_reg]
            dist = haversine(flat, flon, r_lat, r_lon)
            prod_data = df[df["Product Name"] == selected_product]
            avg_lt  = prod_data["Lead Time"].mean()
            avg_pm  = prod_data["Profit Margin (%)"].mean()
            # Simulate distance effect (proxy)
            dist_ratio   = dist / current_dist if current_dist > 0 else 1
            sim_lt = avg_lt * (0.85 + 0.15 * dist_ratio)
            factory_perf.append({
                "Factory"         : fname,
                "Distance (mi)"   : round(dist, 1),
                "Est. Lead Time"  : round(sim_lt, 1),
                "Profit Margin %"  : round(avg_pm, 1),
                "Current"         : "⭐ Current" if fname == current_factory else ""
            })

        perf_df = pd.DataFrame(factory_perf).sort_values("Est. Lead Time")

        fig = make_subplots(rows=1, cols=2,
                            subplot_titles=("Estimated Lead Time by Factory",
                                            "Distance to Region"))
        colors = [FACTORY_COLORS[f] for f in perf_df["Factory"]]

        fig.add_trace(go.Bar(
            x=perf_df["Factory"], y=perf_df["Est. Lead Time"],
            marker_color=colors, name="Est. Lead Time",
            text=perf_df["Est. Lead Time"].apply(lambda x: f"{x:.0f}d"),
            textposition="outside"
        ), row=1, col=1)

        fig.add_trace(go.Bar(
            x=perf_df["Factory"], y=perf_df["Distance (mi)"],
            marker_color=colors, name="Distance (mi)",
            text=perf_df["Distance (mi)"].apply(lambda x: f"{x:.0f}mi"),
            textposition="outside"
        ), row=1, col=2)

        fig.update_layout(height=420, showlegend=False,
                          plot_bgcolor="#FAFAFA", paper_bgcolor="white")
        fig.update_xaxes(tickangle=20)
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(perf_df.set_index("Factory"), use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — WHAT-IF SCENARIO ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
with tab2:
    st.subheader("🔄 What-If Scenario Analysis")
    st.markdown("Compare the current factory assignment vs any alternative for each product.")

    col1, col2 = st.columns([1, 3])
    with col1:
        wi_product = st.selectbox("Product", sorted(df["Product Name"].unique()), key="wi_prod")
        wi_alt     = st.selectbox("Alternative Factory", list(FACTORY_COORDS.keys()), key="wi_alt")

    # Pull simulation data for this product
    prod_sim = sim[sim["Product"] == wi_product].copy()
    current_row = {
        "Recommended Factory" : df[df["Product Name"]==wi_product]["Factory"].iloc[0],
        "Current LT (days)"   : df[df["Product Name"]==wi_product]["Lead Time"].mean(),
        "Predicted LT (days)" : df[df["Product Name"]==wi_product]["Lead Time"].mean(),
        "LT Improvement (days)": 0,
        "Profit Margin %"      : df[df["Product Name"]==wi_product]["Profit Margin (%)"].mean(),
        "Improvement %"        : 0,
    }

    alt_row = prod_sim[prod_sim["Recommended Factory"] == wi_alt]

    with col2:
        if len(alt_row) > 0:
            alt = alt_row.iloc[0]
            imp = alt["LT Improvement (days)"]
            imp_pct = alt["Improvement %"]

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Current LT",    f"{current_row['Current LT (days)']:.0f}d")
            m2.metric("Predicted LT",  f"{alt['Predicted LT (days)']:.0f}d",
                      delta=f"{-imp:.0f}d" if imp > 0 else f"+{abs(imp):.0f}d",
                      delta_color="inverse")
            m3.metric("Improvement",   f"{imp:.1f} days",
                      delta=f"{imp_pct:.1f}%")
            m4.metric("Profit Margin", f"{alt['Profit Margin %']:.1f}%")

            # Waterfall chart
            fig_wf = go.Figure(go.Waterfall(
                orientation="v",
                measure=["absolute", "relative", "total"],
                x=["Current Lead Time", "Improvement", "Predicted Lead Time"],
                y=[current_row["Current LT (days)"], -imp,
                   alt["Predicted LT (days)"]],
                connector={"line":{"color":"#ccc"}},
                decreasing={"marker":{"color":"#43B89C"}},
                increasing={"marker":{"color":"#EF5350"}},
                totals={"marker":{"color":"#6C63FF"}},
                text=[f"{current_row['Current LT (days)']:.0f}d",
                      f"{-imp:.0f}d",
                      f"{alt['Predicted LT (days)']:.0f}d"],
                textposition="outside"
            ))
            fig_wf.update_layout(
                title=f"Lead Time Change: {wi_product}",
                height=380,
                plot_bgcolor="#FAFAFA",
                paper_bgcolor="white"
            )
            st.plotly_chart(fig_wf, use_container_width=True)

            if imp > 0:
                st.success(f"✅ Moving to **{wi_alt}** saves **{imp:.1f} days** ({imp_pct:.1f}% improvement)")
            else:
                st.error(f"❌ Moving to **{wi_alt}** would INCREASE lead time by **{abs(imp):.1f} days**. Keep current factory.")
        else:
            st.info("This is the current factory assignment — select a different alternative factory.")

    # Full scenario table for this product
    st.markdown("#### All scenarios for this product")
    prod_sim_display = prod_sim[["Recommended Factory","Current LT (days)",
                                  "Predicted LT (days)","LT Improvement (days)",
                                  "Improvement %","Profit Margin %"]].sort_values(
                                  "LT Improvement (days)", ascending=False)
    st.dataframe(prod_sim_display.set_index("Recommended Factory"),
                 use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — RECOMMENDATION DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────
with tab3:
    st.subheader("🏆 Factory Reallocation Recommendations")
    st.markdown("Ranked by Priority Score — combining lead time gain, profit margin, and confidence.")

    # Apply optimization slider to re-rank
    speed_w  = opt_weight / 100
    profit_w = 1 - speed_w
    recs_copy = recs.copy()
    recs_copy["Adjusted Score"] = (
        recs_copy["LT Improvement (days)"].clip(lower=0) * speed_w * 0.8 +
        recs_copy["Profit Margin %"]                     * profit_w * 0.4
    ).round(2)
    recs_copy = recs_copy.sort_values("Adjusted Score", ascending=False).reset_index(drop=True)
    recs_copy.index += 1

    # Color code risk
    def color_risk(val):
        if "LOW"      in str(val): return "background-color: #d4edda; color: #155724"
        if "MEDIUM"   in str(val): return "background-color: #fff3cd; color: #856404"
        if "DO NOT"   in str(val): return "background-color: #f8d7da; color: #721c24"
        return ""

    col1, col2 = st.columns([3, 1])
    with col1:
        display_cols = ["Product","Current Factory","Recommended Factory",
                        "LT Improvement (days)","Improvement %",
                        "Profit Margin %","Risk Level","Confidence","Adjusted Score"]
        styled = recs_copy[display_cols].style.map(
            color_risk, subset=["Risk Level"]
        ).format({
            "LT Improvement (days)": "{:+.1f}",
            "Improvement %"         : "{:+.2f}%",
            "Profit Margin %"       : "{:.1f}%",
            "Adjusted Score"        : "{:.2f}",
        })
        st.dataframe(styled, use_container_width=True, height=460)

    with col2:
        # Summary counts
        st.markdown("#### Summary")
        low  = (recs_copy["Risk Level"].str.contains("LOW")).sum()
        med  = (recs_copy["Risk Level"].str.contains("MEDIUM")).sum()
        high = (recs_copy["Risk Level"].str.contains("DO NOT")).sum()
        st.metric("🟢 Low Risk",    f"{low} products")
        st.metric("🟡 Medium Risk", f"{med} products")
        st.metric("🔴 Do Not Move", f"{high} products")
        st.markdown("---")
        act = recs_copy[recs_copy["LT Improvement (days)"] > 0]
        st.metric("Total Days Saved", f"{act['LT Improvement (days)'].sum():.0f}d")
        st.metric("Avg Improvement",  f"{act['LT Improvement (days)'].mean():.1f}d")

    # Visual: Priority bar chart
    st.markdown("#### Priority Score Chart")
    plot_recs = recs_copy.sort_values("Adjusted Score")
    bar_colors = [RISK_COLORS.get(r, "#B0BEC5") for r in plot_recs["Risk Level"]]
    fig_rank = go.Figure(go.Bar(
        x=plot_recs["Adjusted Score"],
        y=plot_recs["Product"],
        orientation="h",
        marker_color=bar_colors,
        text=plot_recs["Adjusted Score"].apply(lambda x: f"{x:.1f}"),
        textposition="outside"
    ))
    fig_rank.update_layout(
        height=480, xaxis_title="Adjusted Priority Score",
        plot_bgcolor="#FAFAFA", paper_bgcolor="white",
        showlegend=False
    )
    st.plotly_chart(fig_rank, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 — RISK & IMPACT PANEL
# ─────────────────────────────────────────────────────────────────────────────
with tab4:
    st.subheader("⚠️ Risk & Impact Panel")
    st.markdown("Profit impact alerts and high-risk reassignment warnings.")

    # ── Alert cards ───────────────────────────────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🔴 High Risk Warnings")
        danger = recs[recs["LT Improvement (days)"] < 0].sort_values("LT Improvement (days)")
        for _, row in danger.iterrows():
            imp = row["LT Improvement (days)"]
            st.error(f"**{row['Product']}**\n\n"
                     f"Moving to {row['Recommended Factory']} would ADD "
                     f"**{abs(imp):.1f} days** to lead time.\n\n"
                     f"Margin: {row['Profit Margin %']:.1f}%  |  Keep in: {row['Current Factory']}")

    with col2:
        st.markdown("#### 🟢 Low Risk Opportunities")
        safe = recs[recs["Risk Level"].str.contains("LOW")].sort_values(
            "LT Improvement (days)", ascending=False)
        for _, row in safe.iterrows():
            imp = row["LT Improvement (days)"]
            st.success(f"**{row['Product']}**\n\n"
                       f"Move to **{row['Recommended Factory']}**\n\n"
                       f"Save **{imp:.1f} days** | "
                       f"Margin: {row['Profit Margin %']:.1f}% | "
                       f"Confidence: {row['Confidence']}")

    st.markdown("---")

    # ── Profit Sensitivity Chart ───────────────────────────────────────────────
    st.markdown("#### 💰 Profit Margin Sensitivity — All Products")
    fig_pm = px.scatter(
        recs,
        x="LT Improvement (days)",
        y="Profit Margin %",
        color="Risk Level",
        color_discrete_map=RISK_COLORS,
        size=recs["LT Improvement (days)"].abs() + 5,
        hover_name="Product",
        hover_data=["Current Factory","Recommended Factory","Confidence"],
        text="Product",
        height=480,
        title="Lead Time Improvement vs Profit Margin — Each bubble is a product"
    )
    fig_pm.update_traces(textposition="top center", textfont_size=9)
    fig_pm.add_vline(x=0, line_dash="dash", line_color="#555",
                     annotation_text="No improvement threshold")
    fig_pm.update_layout(plot_bgcolor="#FAFAFA", paper_bgcolor="white")
    st.plotly_chart(fig_pm, use_container_width=True)

    # ── Factory load impact table ──────────────────────────────────────────────
    st.markdown("#### 🏭 Factory Order Load — Before vs After Low Risk Moves")
    before = df["Factory"].value_counts().reset_index()
    before.columns = ["Factory", "Before (Orders)"]
    after_df = df.copy()
    low_moves = recs[recs["Risk Level"].str.contains("LOW")][["Product","Recommended Factory"]]
    for _, move in low_moves.iterrows():
        after_df.loc[after_df["Product Name"]==move["Product"], "Factory"] = move["Recommended Factory"]
    after = after_df["Factory"].value_counts().reset_index()
    after.columns = ["Factory", "After (Orders)"]
    load_df = before.merge(after, on="Factory")
    load_df["Change"] = load_df["After (Orders)"] - load_df["Before (Orders)"]
    load_df["Change"] = load_df["Change"].apply(lambda x: f"+{x}" if x > 0 else str(x))
    st.dataframe(load_df.set_index("Factory"), use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#888; font-size:13px'>"
    "Nassau Candy Distributor · Factory Reallocation & Shipping Optimization System · "
    "Powered by Gradient Boosting + KMeans Clustering"
    "</div>",
    unsafe_allow_html=True
)
