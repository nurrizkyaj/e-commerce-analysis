import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Dashboard EDA", layout="wide")
sns.set(style="whitegrid")

avgFreightbyCity_df = pd.read_csv("dashboard/avg_freight_by_city.csv")
creditCards_df = pd.read_csv("dashboard//credit_cards.csv")
reviews_df = pd.read_csv("dashboard//reviews.csv")
rfm_df = pd.read_csv("dashboard//rfm.csv")

st.sidebar.title("📊 Navigasi Dashboard")
page = st.sidebar.radio("Pilih Halaman:", [
    "📦 Ongkos Kirim Berdasarkan Kota di Sao Paulo", 
    "💳 Hubungan Cicilan Pembayaran dan Total Pembayaran", 
    "🚚 Pengiriman Tepat Waktu dan Kepuasan Pelanggan", 
    "🔍 Segmentasi Pelanggan: RFM Analysis"
])

if page == "📦 Ongkos Kirim Berdasarkan Kota di Sao Paulo":
    st.title("📦 Bagaimana rata-rata ongkos kirim untuk setiap kota asal penjual di negara bagian Sao Paulo?")

    avgFreightbyCity_df = avgFreightbyCity_df.head(5)
    colors = ['#1f77b4'] + ['#a6cee3'] * (len(avgFreightbyCity_df) - 1)

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x='seller_city', y='freight_value', data=avgFreightbyCity_df, palette=colors, ax=ax)
    ax.set_title('5 Kota dengan Rata-rata Ongkos Kirim Tertinggi', fontsize=16)
    ax.set_xlabel('Kota Penjual', fontsize=12)
    ax.set_ylabel('Rata-rata Ongkos Kirim', fontsize=12)

    st.pyplot(fig)
    
    st.markdown("Dengan mengidentifikasi rata-rata ongkos kirim perusahaan dapat mempertimbangkan strategi logistik yang lebih efisien atau penyesuaian harga untuk meningkatkan daya saing dan mengurangi biaya operasional di wilayah tersebut.")

elif page == "💳 Hubungan Cicilan Pembayaran dan Total Pembayaran":
    st.title("💳 Bagaimana hubungan antara cicilan pembayaran dengan total pembayaran dalam transaksi yang dilakukan menggunakan kartu kredit?")

    colors = ['#1f77b4' if x > 8 else '#a6cee3' for x in creditCards_df['payment_installments']]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.scatter(creditCards_df['payment_installments'], creditCards_df['payment_value'], c=colors)
    ax.set_title("Hubungan Cicilan vs Nilai Pembayaran", fontsize=16)
    ax.set_xlabel("Cicilan", fontsize=12)
    ax.set_ylabel("Pembayaran", fontsize=12)

    st.pyplot(fig)
    
    st.markdown("Korelasi positif antara jumlah cicilan dan total pembayaran membuka peluang strategi bisnis, menyediakan lebih banyak opsi cicilan dapat mendorong peningkatan nilai transaksi dan memperluas jangkauan konsumen, khususnya segmen yang sensitif terhadap pembayaran langsung.")

elif page == "🚚 Pengiriman Tepat Waktu dan Kepuasan Pelanggan":
    st.title("🚚 Berapa persen pesanan yang dikirimkan lebih lambat dari tanggal estimasi pengiriman, dan bagaimana skor review yang diberikan pelanggan pada pesanan tersebut?")

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x='late_delivery', y='review_score', data=reviews_df,
                palette={"False": "#1f77b4", "True": "#a6cee3"}, ax=ax)
    ax.set_title("Tepat Waktu vs Terlambat")
    ax.set_xlabel("Pengiriman Terlambat")
    ax.set_ylabel("Review")
    ax.set_xticklabels(["Tidak", "Ya"])

    st.pyplot(fig)
    
    st.markdown("Persentase pesanan yang terlambat: 8.11%")
    st.markdown("Meningkatkan ketepatan waktu pengiriman dapat berkontribusi langsung pada peningkatan kepuasan pelanggan, yang tercermin dalam skor review yang lebih tinggi. Mengoptimalkan logistik dan pengiriman tepat waktu akan berpengaruh besar pada loyalitas pelanggan, yang pada gilirannya dapat mendukung pertumbuhan bisnis melalui rekomendasi positif dan pengulangan transaksi.")

elif page == "🔍 Segmentasi Pelanggan: RFM Analysis":
    st.title("🔍 Bagaimana segmentasi pelanggan berdasarkan Recency, Frequency, dan Monetary value dari transaksi mereka selama satu tahun terakhir, dan segmen mana yang paling potensial untuk ditargetkan promosi?")

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
    ax.set_title('Distribusi Pelanggan Berdasarkan Skor RFM (Filtered)', fontsize=16)
    ax.set_xlabel('RFM Segment', fontsize=12)
    ax.set_ylabel('Jumlah Pelanggan', fontsize=12)
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

    top_customers = filtered_rfm[filtered_rfm['RFM_Segment'] == '333']
    if filtered_rfm.shape[0] > 0:
        percentage_top_customers = (top_customers.shape[0] / filtered_rfm.shape[0]) * 100
        st.markdown(f"Segmen *333* dalam hasil filter saat ini berjumlah **{percentage_top_customers:.2f}%** dari total segmen yang tampil.")
    else:
        st.warning("Tidak ada data pelanggan yang sesuai dengan filter yang dipilih.")
        
    st.markdown("Fokus pada pelanggan dengan segmen RFM *333* yang mencakup *3.89%* dari total pelanggan dapat memberikan dampak signifikan, karena mereka adalah pelanggan yang paling loyal, aktif, dan mengeluarkan nilai transaksi tertinggi. Menargetkan mereka dengan promosi khusus atau program loyalitas dapat meningkatkan retensi dan mendorong peningkatan pendapatan secara berkelanjutan.")
