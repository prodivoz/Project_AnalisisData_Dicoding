import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi Tema
st.set_page_config(page_title="Dashboard Penyewaan Sepeda", layout="wide")

# Membaca dataset
@st.cache_data
def load_data():
    df = pd.read_csv('hour.csv')
    df['dteday'] = pd.to_datetime(df['dteday'])
    df['hour'] = df['dteday'].dt.hour
    df['dayofweek'] = df['dteday'].dt.dayofweek
    df['month'] = df['dteday'].dt.month
    df['year'] = df['dteday'].dt.year
    return df

df = load_data()

# Fungsi untuk mengubah kode cuaca menjadi deskripsi teks
def weather_description(code):
    if code == 1:
        return "Cerah/Berawan"
    elif code == 2:
        return "Kabut/Berawan"
    elif code == 3:
        return "Hujan Ringan/Salju Ringan"
    elif code == 4:
        return "Hujan Lebat/Salju Lebat"
    else:
        return "Tidak Diketahui"

# Menerapkan fungsi deskripsi cuaca ke kolom 'weathersit'
df['weather_desc'] = df['weathersit'].apply(weather_description)

# Sidebar
st.sidebar.header("Filter Data")
time_range = st.sidebar.selectbox("Rentang Waktu", ['Jam', 'Rentang Jam', 'Hari dalam Seminggu', 'Bulan', 'Tahun'])
weather_filter = st.sidebar.multiselect("Kondisi Cuaca", df['weather_desc'].unique())

# Filter Data
if weather_filter:
    df_filtered = df[df['weather_desc'].isin(weather_filter)]
else:
    df_filtered = df

# Filter Tambahan untuk Hari dan Jam
if time_range == 'Hari dalam Seminggu':
    day_filter = st.sidebar.multiselect("Pilih Hari", df_filtered['dayofweek'].unique(), format_func=lambda x: ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu'][x])
    if day_filter:
        df_filtered = df_filtered[df_filtered['dayofweek'].isin(day_filter)]

if time_range == 'Jam':
    hour_filter = st.sidebar.multiselect("Pilih Jam", df_filtered['hour'].unique())
    if hour_filter:
        df_filtered = df_filtered[df_filtered['hour'].isin(hour_filter)]

# Filter Tambahan untuk Rentang Jam
if time_range == 'Rentang Jam':
    start_hour, end_hour = st.sidebar.slider("Pilih Rentang Jam", 0, 23, (0, 23))
    df_filtered = df_filtered[(df_filtered['hour'] >= start_hour) & (df_filtered['hour'] <= end_hour)]

# Layout Utama
st.title("Dashboard Analisis Penyewaan Sepeda")

# Kolom 1: Pengaruh Cuaca
st.header("Pengaruh Kondisi Cuaca")
col1, col2 = st.columns(2)

with col1:
    fig_weather = px.box(df_filtered, x='weather_desc', y='cnt',
                     labels={'weather_desc': 'Kondisi Cuaca', 'cnt': 'Jumlah Penyewaan'},
                     title='Distribusi Penyewaan Berdasarkan Cuaca')
    st.plotly_chart(fig_weather, use_container_width=True)

with col2:
    weather_summary = df_filtered.groupby('weather_desc')['cnt'].mean().reset_index()
    st.write("Rata-rata Penyewaan Berdasarkan Cuaca:")
    st.dataframe(weather_summary)

# Kolom 2: Tren Waktu
st.header("Tren Penyewaan Berdasarkan Waktu")

if time_range == 'Jam':
    hourly_rentals = df_filtered.groupby('hour')['cnt'].mean().reset_index()
    fig_time = px.line(hourly_rentals, x='hour', y='cnt',
                     labels={'hour': 'Jam', 'cnt': 'Rata-rata Penyewaan'},
                     title='Tren Penyewaan per Jam')
    st.plotly_chart(fig_time, use_container_width=True)

elif time_range == 'Rentang Jam':
    hourly_rentals = df_filtered.groupby('hour')['cnt'].mean().reset_index()
    fig_time = px.line(hourly_rentals, x='hour', y='cnt',
                     labels={'hour': 'Jam', 'cnt': 'Rata-rata Penyewaan'},
                     title=f'Tren Penyewaan Jam {start_hour} - {end_hour}')
    st.plotly_chart(fig_time, use_container_width=True)

elif time_range == 'Hari dalam Seminggu':
    daily_rentals = df_filtered.groupby('dayofweek')['cnt'].mean().reset_index()
    fig_time = px.line(daily_rentals, x='dayofweek', y='cnt',
                     labels={'dayofweek': 'Hari', 'cnt': 'Rata-rata Penyewaan'},
                     title='Tren Penyewaan per Hari dalam Seminggu')
    fig_time.update_xaxes(tickvals=list(range(7)), ticktext=['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu'])
    st.plotly_chart(fig_time, use_container_width=True)

elif time_range == 'Bulan':
    monthly_rentals = df_filtered.groupby('month')['cnt'].mean().reset_index()
    fig_time = px.line(monthly_rentals, x='month', y='cnt',
                     labels={'month': 'Bulan', 'cnt': 'Rata-rata Penyewaan'},
                     title='Tren Penyewaan per Bulan')
    st.plotly_chart(fig_time, use_container_width=True)

else:  # Tahun
    yearly_rentals = df_filtered.groupby('year')['cnt'].mean().reset_index()
    fig_time = px.line(yearly_rentals, x='year', y='cnt',
                     labels={'year': 'Tahun', 'cnt': 'Rata-rata Penyewaan'},
                     title='Tren Penyewaan per Tahun')
    st.plotly_chart(fig_time, use_container_width=True)

# Informasi Tambahan
st.header("Informasi Tambahan")
col3, col4 = st.columns(2)

with col3:
    st.metric("Total Penyewaan", int(df['cnt'].sum()))
    st.metric("Rata-rata Penyewaan", round(df['cnt'].mean(), 2))

with col4:
    st.metric("Penyewaan Tertinggi", int(df['cnt'].max()))
    st.metric("Penyewaan Terendah", int(df['cnt'].min()))