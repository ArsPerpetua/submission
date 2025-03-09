import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi halaman
st.set_page_config(page_title="Dashboard Bike Sharing", page_icon="🚴", layout="wide")

# Judul utama
st.title("📊 Dashboard Analisis Data Bike Sharing")

# Memuat data
@st.cache_data
def load_data():
    url = "https://github.com/ArsPerpetua/submission/blob/main/dashboard/all_data.csv"
    df = pd.read_csv(url)
    # Ubah format data
    month_map = {1: 'Januari', 2: 'Februari', 3: 'Maret', 4: 'April', 5: 'Mei', 6: 'Juni',
                 7: 'Juli', 8: 'Agustus', 9: 'September', 10: 'Oktober', 11: 'November', 12: 'Desember'}
    season_map = {1: 'Musim Semi', 2: 'Musim Panas', 3: 'Musim Gugur', 4: 'Musim Dingin'}
    weather_map = {1: 'Cerah', 2: 'Berkabut', 3: 'Hujan Ringan', 4: 'Hujan Lebat'}
    
    df['mnth'] = df['mnth'].map(month_map)
    df['season'] = df['season'].map(season_map)
    df['weathersit'] = df['weathersit'].map(weather_map)
    df['yr'] = df['yr'].map({0: 2011, 1: 2012})
    df['dteday'] = pd.to_datetime(df['dteday'])
    
    return df

df = load_data()

# Sidebar - Filter Data
st.sidebar.header("🔍 Filter Data")
selected_year = st.sidebar.selectbox("📅 Pilih Tahun", df['yr'].unique())
selected_month = st.sidebar.selectbox("📆 Pilih Bulan", df['mnth'].unique())
selected_weather = st.sidebar.selectbox("⛅ Pilih Kondisi Cuaca", df['weathersit'].unique())

# Filter data
filtered_df = df[(df['yr'] == selected_year) & (df['mnth'] == selected_month) & (df['weathersit'] == selected_weather)]

# Menampilkan data
st.subheader("📌 Data yang Difilter")
st.dataframe(filtered_df.head())

# Visualisasi 1: Tren Penyewaan Sepeda Bulanan
st.subheader("📈 Tren Penyewaan Sepeda Bulanan")
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='mnth', y='cnt', data=df, estimator=sum, ax=ax)
plt.xticks(rotation=45)
plt.xlabel('Bulan')
plt.ylabel('Total Penyewaan')
plt.title('Total Penyewaan Sepeda per Bulan')
st.pyplot(fig)

# Visualisasi 2: Pengaruh Cuaca terhadap Penyewaan
st.subheader("⛅ Pengaruh Cuaca terhadap Penyewaan")
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(x='weathersit', y='cnt', data=df, ax=ax)
plt.xlabel('Kondisi Cuaca')
plt.ylabel('Jumlah Penyewaan')
st.pyplot(fig)

# Visualisasi 3: Penyewaan Berdasarkan Hari dalam Seminggu
st.subheader("📅 Penyewaan Sepeda Berdasarkan Hari dalam Seminggu")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='weekday', y='cnt', data=df, estimator=np.mean, ax=ax)
plt.xlabel('Hari dalam Seminggu')
plt.ylabel('Rata-rata Penyewaan')
st.pyplot(fig)

# Visualisasi 4: Penyewaan Berdasarkan Jam (Data Hourly)
if 'hr' in df.columns:
    st.subheader("⏰ Distribusi Penyewaan Sepeda per Jam")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x='hr', y='cnt', data=df, estimator=np.mean, ax=ax)
    plt.xlabel('Jam')
    plt.ylabel('Rata-rata Penyewaan')
    plt.title('Penyewaan Sepeda Berdasarkan Waktu')
    st.pyplot(fig)

# Visualisasi 5: Heatmap Korelasi Variabel
st.subheader("🔥 Korelasi Variabel")
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm', fmt='.2f', ax=ax)
st.pyplot(fig)

# Visualisasi 6: Scatter Plot Temperatur vs Penyewaan
st.subheader("🌡️ Hubungan Temperatur dan Penyewaan Sepeda")
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(x='temp', y='cnt', data=df, alpha=0.6)
plt.xlabel('Temperatur')
plt.ylabel('Jumlah Penyewaan')
st.pyplot(fig)

# Visualisasi 7: Penyewaan Berdasarkan Musim
st.subheader("🍂 Penyewaan Sepeda Berdasarkan Musim")
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(x='season', y='cnt', data=df, ax=ax)
plt.xlabel('Musim')
plt.ylabel('Jumlah Penyewaan')
st.pyplot(fig)

# Visualisasi 8: Penyewaan pada Hari Kerja vs Akhir Pekan
st.subheader("🏢 Penyewaan pada Hari Kerja vs Akhir Pekan")
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(x='workingday', y='cnt', data=df, ax=ax)
plt.xlabel('Hari Kerja (1=Ya, 0=Tidak)')
plt.ylabel('Jumlah Penyewaan')
st.pyplot(fig)

# Footer - Informasi Proyek
st.markdown("""
### 📌 Proyek Analisis Data: Bike Sharing Dataset
- **Nama:** Dicksa Ananda Christian Tue  
- **Email:** diksaanandaa@gmail.com  
- **ID Dicoding:** diksa_0707  

© 2025 Dicksa Ananda Christian Tue. All Rights Reserved.
""")
