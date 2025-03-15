import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_data():
    df = pd.read_csv('day.csv')
    df = pd.read_csv('hour.csv')
    df['dteday'] = pd.to_datetime(df['dteday'])
    df['hour'] = df['dteday'].dt.hour
    df['month'] = df['dteday'].dt.month
    df['year'] = df['dteday'].dt.year
    df['day_of_week'] = df['dteday'].dt.dayofweek
    return df

df = load_data()

# Judul Dashboard
st.title('Dashboard Analisis Penyewaan Sepeda')

# Filter berdasarkan jam dan hari
st.sidebar.header('Filter Data')
selected_hour = st.sidebar.slider('Pilih Jam', 0, 23, (0, 23))
selected_day = st.sidebar.multiselect('Pilih Hari', df['day_of_week'].unique(), df['day_of_week'].unique())

# Filter data berdasarkan jam dan hari yang dipilih
filtered_df = df[(df['hour'] >= selected_hour[0]) & (df['hour'] <= selected_hour[1]) & (df['day_of_week'].isin(selected_day))]


# 1. Pengaruh Kondisi Cuaca terhadap Jumlah Penyewaan Sepeda
st.header('Pengaruh Kondisi Cuaca terhadap Jumlah Penyewaan Sepeda')

weather_rentals = df.groupby('weathersit')['cnt'].mean().reset_index()

fig1, ax1 = plt.subplots(figsize=(8, 6))
sns.barplot(x='weathersit', y='cnt', data=weather_rentals, ax=ax1)
ax1.set_title('Rata-rata Penyewaan Sepeda per Kondisi Cuaca')
ax1.set_xlabel('Kondisi Cuaca')
import matplotlib.pyplot as plt

# Misalkan ax1 adalah objek Axes Anda
ax1.set_xticks([0, 1, 2, 3])  # Menetapkan posisi tick
ax1.set_xticklabels(['Cerah', 'Kabut', 'Hujan Ringan', 'Hujan Lebat']) # Menetapkan label
st.pyplot(fig1)

# 2. Tren Penyewaan Sepeda Berdasarkan Waktu
st.header('Tren Penyewaan Sepeda Berdasarkan Waktu')

# Tren Penyewaan per Jam
st.subheader('Tren Penyewaan Sepeda per Jam')
hourly_rentals = df.groupby('hr')['cnt'].mean()
fig2, ax2 = plt.subplots(figsize=(12, 6))
hourly_rentals.plot(kind='line', ax=ax2)
ax2.set_title('Tren Penyewaan Sepeda per Jam')
ax2.set_xlabel('Jam')
ax2.set_ylabel('Rata-rata Jumlah Penyewaan')
ax2.set_xticks(range(24))
ax2.grid(True)
st.pyplot(fig2)

# Tren Penyewaan per Hari dalam Seminggu
st.subheader('Tren Penyewaan Sepeda per Hari dalam Seminggu')
daily_rentals = df.groupby('day_of_week')['cnt'].mean()
fig3, ax3 = plt.subplots(figsize=(10, 6))
daily_rentals.plot(kind='line', ax=ax3)
ax3.set_title('Tren Penyewaan Sepeda per Hari dalam Seminggu')
ax3.set_xlabel('Hari dalam Seminggu (0=Senin, 6=Minggu)')
ax3.set_ylabel('Rata-rata Jumlah Penyewaan')
ax3.set_xticks(range(7))
ax3.grid(True)
st.pyplot(fig3)

# Tren Penyewaan per Bulan
st.subheader('Tren Penyewaan Sepeda per Bulan')
monthly_rentals = df.groupby('month')['cnt'].mean()
fig4, ax4 = plt.subplots(figsize=(10, 6))
monthly_rentals.plot(kind='line', ax=ax4)
ax4.set_title('Tren Penyewaan Sepeda per Bulan')
ax4.set_xlabel('Bulan')
ax4.set_ylabel('Rata-rata Jumlah Penyewaan')
ax4.set_xticks(range(1, 13))
ax4.grid(True)
st.pyplot(fig4)

# Tren Penyewaan per Tahun
st.subheader('Tren Penyewaan Sepeda per Tahun')
yearly_rentals = df.groupby('year')['cnt'].mean()
fig5, ax5 = plt.subplots(figsize=(8, 6))
yearly_rentals.plot(kind='line', ax=ax5)
ax5.set_title('Tren Penyewaan Sepeda per Tahun')
ax5.set_xlabel('Tahun')
ax5.set_ylabel('Rata-rata Jumlah Penyewaan')
ax5.set_xticks(range(df['year'].min(), df['year'].max() + 1))
ax5.grid(True)
st.pyplot(fig5)
