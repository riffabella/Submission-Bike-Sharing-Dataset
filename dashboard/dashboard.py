import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load Data & Helper Functions
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/all_data.csv", parse_dates=["dteday"])
    return df

df = load_data()

# Sidebar with Filters & Logo
st.sidebar.image("data/bike.png", width=200)
st.sidebar.title("Dashboard Peminjaman Sepeda")
st.sidebar.markdown("---")

# Sidebar Filters
date_range = st.sidebar.date_input("Pilih Rentang Tanggal", [df["dteday"].min(), df["dteday"].max()])
df_filtered = df[(df["dteday"] >= pd.to_datetime(date_range[0])) & (df["dteday"] <= pd.to_datetime(date_range[1]))]

option = st.sidebar.selectbox("Pilih Analisis", ["Analisis Bulanan", "Analisis Faktor Cuaca & Waktu", "Pola Peminjaman Harian", "Analisis RFM"])

# Dashboard Sections
if option == "Analisis Bulanan":
    st.title("Analisis Bulanan Peminjaman Sepeda 🚴‍♂️")
    
    monthly_rentals = df_filtered.groupby("mnth_daily")["cnt_daily"].sum().reset_index()
    highest_month = monthly_rentals.loc[monthly_rentals["cnt_daily"].idxmax()]
    lowest_month = monthly_rentals.loc[monthly_rentals["cnt_daily"].idxmin()]
    
    st.write(f"Bulan dengan peminjaman tertinggi: {highest_month['mnth_daily']} - {highest_month['cnt_daily']}")
    st.write(f"Bulan dengan peminjaman terendah: {lowest_month['mnth_daily']} - {lowest_month['cnt_daily']}")
    
    fig, ax = plt.subplots()
    sns.barplot(x="mnth_daily", y="cnt_daily", data=monthly_rentals, color="#ADD8E6", ax=ax)
    ax.set_title("Total Peminjaman Sepeda per Bulan")
    st.pyplot(fig)

elif option == "Analisis Faktor Cuaca & Waktu":
    st.title("Analisis Pengaruh Faktor Cuaca dan Waktu terhadap Peminjaman Sepeda🚴‍♂️")
    correlation = df_filtered[['temp_daily', 'hum_daily', 'windspeed_daily', 'cnt_daily']].corr()
    st.write("Korelasi antara faktor cuaca dan jumlah peminjaman:")
    st.write(correlation)
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    sns.scatterplot(x="temp_daily", y="cnt_daily", data=df_filtered, ax=axes[0], color="red")
    axes[0].set_title("Pengaruh Temperatur")
    sns.scatterplot(x="hum_daily", y="cnt_daily", data=df_filtered, ax=axes[1], color="blue")
    axes[1].set_title("Pengaruh Kelembaban")
    sns.scatterplot(x="windspeed_daily", y="cnt_daily", data=df_filtered, ax=axes[2], color="green")
    axes[2].set_title("Pengaruh Kecepatan Angin")
    st.pyplot(fig)

elif option == "Pola Peminjaman Harian":
    st.title("Pola Peminjaman Sepeda dalam Sehari 🚴‍♂️")
    hourly_rentals = df_filtered.groupby("hr")["cnt_hourly"].sum().reset_index()
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x="hr", y="cnt_hourly", data=hourly_rentals, color="#ADD8E6", ax=ax)
    ax.set_title("Jumlah Peminjaman Sepeda per Jam")
    st.pyplot(fig)

elif option == "Analisis RFM":
    st.title("Analisis RFM (Recency, Frequency, Monetary)")
    df_filtered["recency"] = (df_filtered["dteday"].max() - df_filtered["dteday"]).dt.days
    freq_per_month = df_filtered.groupby("mnth_daily")["cnt_daily"].count().reset_index()
    freq_per_month.columns = ["mnth_daily", "frequency"]
    monetary_per_month = df_filtered.groupby("mnth_daily")["cnt_daily"].sum().reset_index()
    monetary_per_month.columns = ["mnth_daily", "monetary"]
    rfm_df = freq_per_month.merge(monetary_per_month, on="mnth_daily")
    rfm_df["recency"] = df_filtered.groupby("mnth_daily")["recency"].min().values
    
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(rfm_df["recency"], bins=10, kde=True, color="blue", ax=ax)
    ax.set_title("Distribusi Recency")
    st.pyplot(fig)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x="mnth_daily", y="frequency", data=rfm_df, color="#ADD8E6", ax=ax)
    ax.set_title("Total Peminjaman Sepeda per Bulan (Frequency)")
    st.pyplot(fig)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x="mnth_daily", y="monetary", data=rfm_df, marker="o", color="green", ax=ax)
    ax.set_title("Total Peminjaman Sepeda per Bulan (Monetary)")
    st.pyplot(fig)