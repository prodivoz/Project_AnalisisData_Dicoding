import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Membaca dataset
@st.cache_data
def load_data():
    df = pd.read_csv('hour.csv')
    df['dteday'] = pd.to_datetime(df['dteday'])
    df['is_weekday'] = df['weekday'].apply(lambda x: 1 if x in range(1, 6) else 0)
    return df

df = load_data()

# Judul Dashboard
st.title('Dashboard Tren Penyewaan Sepeda')

# Sidebar: Filter
st.sidebar.header('Filter Data')
season_filter = st.sidebar.multiselect('Pilih Musim', df['season'].unique(), format_func=lambda x: ['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin'][x - 1])
weather_filter = st.sidebar.multiselect('Pilih Kondisi Cuaca', df['weathersit'].unique(), format_func=lambda x: ['Cerah/Berawan', 'Kabut/Awan', 'Hujan Ringan', 'Hujan Lebat'][x - 1])

# Filter Data
df_filtered = df.copy()
if season_filter:
    df_filtered = df_filtered[df_filtered['season'].isin(season_filter)]
if weather_filter:
    df_filtered = df_filtered[df_filtered['weathersit'].isin(weather_filter)]

# Pilihan Rentang Waktu
time_range = st.selectbox('Pilih Rentang Waktu', ['Jam', 'Hari', 'Bulan', 'Tahun', 'Hari Kerja vs. Akhir Pekan', 'Distribusi Suhu'])

# Visualisasi Tren Berdasarkan Waktu
if time_range == 'Jam':
    hourly_rentals = df_filtered.groupby('hr')['cnt'].mean()
    fig, ax = plt.subplots()
    hourly_rentals.plot(kind='line', ax=ax)
    ax.set_title('Tren Penyewaan Sepeda per Jam')
    ax.set_xlabel('Jam')
    ax.set_ylabel('Rata-rata Jumlah Penyewaan')
    ax.set_xticks(range(24))
    st.pyplot(fig)

elif time_range == 'Hari':
    daily_rentals = df_filtered.groupby(df_filtered['dteday'].dt.dayofweek)['cnt'].mean()
    fig, ax = plt.subplots()
    daily_rentals.plot(kind='line', ax=ax)
    ax.set_title('Tren Penyewaan Sepeda per Hari')
    ax.set_xlabel('Hari')
    ax.set_ylabel('Rata-rata Jumlah Penyewaan')
    ax.set_xticks(range(7))
    ax.set_xticklabels(['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu'])
    st.pyplot(fig)

elif time_range == 'Bulan':
    monthly_rentals = df_filtered.groupby(df_filtered['dteday'].dt.month)['cnt'].mean()
    fig, ax = plt.subplots()
    monthly_rentals.plot(kind='line', ax=ax)
    ax.set_title('Tren Penyewaan Sepeda per Bulan')
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Rata-rata Jumlah Penyewaan')
    ax.set_xticks(range(1, 13))
    st.pyplot(fig)

elif time_range == 'Tahun':
    yearly_rentals = df_filtered.groupby(df_filtered['dteday'].dt.year)['cnt'].mean()
    fig, ax = plt.subplots()
    yearly_rentals.plot(kind='line', ax=ax)
    ax.set_title('Tren Penyewaan Sepeda per Tahun')
    ax.set_xlabel('Tahun')
    ax.set_ylabel('Rata-rata Jumlah Penyewaan')
    ax.set_xticks(df_filtered['dteday'].dt.year.unique())
    st.pyplot(fig)

elif time_range == 'Hari Kerja vs. Akhir Pekan':
    weekday_weekend_rentals = df_filtered.groupby('is_weekday')['cnt'].mean()
    fig, ax = plt.subplots()
    weekday_weekend_rentals.plot(kind='bar', ax=ax)
    ax.set_title('Tren Penyewaan Sepeda per Hari Kerja vs. Akhir Pekan')
    ax.set_xlabel('Hari')
    ax.set_ylabel('Rata-rata Jumlah Penyewaan')
    ax.set_xticks([0, 1])
    ax.set_xticklabels(['Akhir Pekan', 'Hari Kerja'])
    st.pyplot(fig)

elif time_range == 'Distribusi Suhu':
    fig, ax = plt.subplots()
    sns.histplot(df_filtered['temp'], kde=True, ax=ax)
    ax.set_title('Distribusi Penyewaan Sepeda Berdasarkan Suhu')
    ax.set_xlabel('Suhu')
    ax.set_ylabel('Frekuensi')
    st.pyplot(fig)
