import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="EDA Dashboard", layout="wide")
sns.set(style="whitegrid")

avgFreightbyCity_df = pd.read_csv("dashboard/avg_freight_by_city.csv")
creditCards_df = pd.read_csv("dashboard/credit_cards.csv")
reviews_df = pd.read_csv("dashboard/reviews.csv")
rfm_df = pd.read_csv("dashboard/rfm.csv")

st.sidebar.title("📊 Dashboard Navigation")
page = st.sidebar.radio("Select Page:", [
    "📦 Shipping Cost by City in Sao Paulo", 
    "💳 Installments vs Total Payment", 
    "🚚 On-time Delivery and Customer Satisfaction", 
    "🔍 Customer Segmentation: RFM Analysis"
])

if page == "📦 Shipping Cost by City in Sao Paulo":
    st.title("📦 What is the average shipping cost per seller city in the state of Sao Paulo?")

    avgFreightbyCity_df = avgFreightbyCity_df.head(5)
    colors = ['#1f77b4'] + ['#a6cee3'] * (len(avgFreightbyCity_df) - 1)

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x='seller_city', y='freight_value', data=avgFreightbyCity_df, palette=colors, ax=ax)
    ax.set_title('Top 5 Cities with Highest Average Shipping Costs', fontsize=16)
    ax.set_xlabel('Seller City', fontsize=12)
    ax.set_ylabel('Average Shipping Cost', fontsize=12)

    st.pyplot(fig)

    st.markdown("By identifying average shipping costs, companies can consider more efficient logistics strategies or price adjustments to improve competitiveness and reduce operational costs in the region.")

elif page == "💳 Installments vs Total Payment":
    st.title("💳 What is the relationship between payment installments and total transaction value using credit cards?")

    colors = ['#1f77b4' if x > 8 else '#a6cee3' for x in creditCards_df['payment_installments']]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.scatter(creditCards_df['payment_installments'], creditCards_df['payment_value'], c=colors)
    ax.set_title("Installments vs Payment Value", fontsize=16)
    ax.set_xlabel("Installments", fontsize=12)
    ax.set_ylabel("Payment", fontsize=12)

    st.pyplot(fig)

    st.markdown("The positive correlation between the number of installments and total payment reveals a business opportunity—offering more installment options could increase transaction values and attract consumers sensitive to upfront payments.")

elif page == "🚚 On-time Delivery and Customer Satisfaction":
    st.title("🚚 What percentage of orders are delivered later than the estimated date, and how are they reviewed by customers?")

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x='late_delivery', y='review_score', data=reviews_df,
                palette={"False": "#1f77b4", "True": "#a6cee3"}, ax=ax)
    ax.set_title("On-time vs Late Deliveries")
    ax.set_xlabel("Late Delivery")
    ax.set_ylabel("Review")
    ax.set_xticklabels(["No", "Yes"])

    st.pyplot(fig)

    st.markdown("Percentage of late orders: 8.11%")
    st.markdown("Improving delivery punctuality can directly contribute to higher customer satisfaction, as reflected in better review scores. Optimizing logistics and ensuring timely delivery significantly impacts customer loyalty, leading to business growth through positive word-of-mouth and repeat transactions.")

elif page == "🔍 Customer Segmentation: RFM Analysis":
    st.title("🔍 How are customers segmented based on Recency, Frequency, and Monetary value of their transactions over the past year, and which segment is most promising for promotion?")

    col1, col2, col3 = st.columns(3)
    with col1:
        selected_r = st.multiselect("Filter Recency Score (R):", sorted(rfm_df['R_score'].unique()), default=sorted(rfm_df['R_score'].unique()))
    with col2:
        selected_f = st.multiselect("Filter Frequency Score (F):", sorted(rfm_df['F_score'].unique()), default=sorted(rfm_df['F_score'].unique()))
    with col3:
        selected_m = st.multiselect("Filter Monetary Score (M):", sorted(rfm_df['M_score'].unique()), default=sorted(rfm_df['M_score'].unique()))

    filtered_rfm = rfm_df[
        (rfm_df['R_score'].isin(selected_r)) &
        (rfm_df['F_score'].isin(selected_f)) &
        (rfm_df['M_score'].isin(selected_m))
    ]
    filtered_rfm['RFM_Segment'] = filtered_rfm['RFM_Segment'].astype(str)

    unique_segments = filtered_rfm['RFM_Segment'].unique()
    colors = {segment: '#a6cee3' for segment in unique_segments}
    if '333' in colors:
        colors['333'] = '#1f77b4'

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.countplot(data=filtered_rfm, x='RFM_Segment', palette=colors, ax=ax)
    ax.set_title('Customer Distribution by RFM Score (Filtered)', fontsize=16)
    ax.set_xlabel('RFM Segment', fontsize=12)
    ax.set_ylabel('Number of Customers', fontsize=12)
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

    top_customers = filtered_rfm[filtered_rfm['RFM_Segment'] == '333']
    if filtered_rfm.shape[0] > 0:
        percentage_top_customers = (top_customers.shape[0] / filtered_rfm.shape[0]) * 100
        st.markdown(f"Segment *333* in the current filter represents **{percentage_top_customers:.2f}%** of the displayed segments.")
    else:
        st.warning("No customer data matches the selected filters.")

    st.markdown("Focusing on RFM segment *333*—which accounts for *3.89%* of total customers—can be highly impactful, as these customers are the most loyal, active, and have the highest transaction values. Targeting them with special promotions or loyalty programs can boost retention and drive sustainable revenue growth.")
