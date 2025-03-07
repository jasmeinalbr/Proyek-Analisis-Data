import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

sns.set(style='darkgrid')

# Tentukan path absolut relatif ke lokasi script
script_dir = os.path.dirname(__file__)  # Direktori tempat dashboard.py berada
day_path = os.path.join(script_dir, "day_clean.csv")
hour_path = os.path.join(script_dir, "hour_clean.csv")

# Load data dengan path yang sudah dikonfigurasi
day_df = pd.read_csv(day_path)
hour_df = pd.read_csv(hour_path)

# Convert date column to datetime format
day_df['date'] = pd.to_datetime(day_df['date'])
hour_df['date'] = pd.to_datetime(hour_df['date'])

# Menu sidebar
menu = st.sidebar.radio("**Navigation**", [
    "📊 Dashboard",
    "🏢 Working vs Holiday",
    "🌤️ Weather Impact",
    "📈 Other Insights"
])

# Tampilkan judul sesuai menu yang dipilih
st.title(menu)

# Dashboard
if menu == "📊 Dashboard":
    st.title("🚴 Bike Rental (2011-2012)")
    st.subheader("📌 General Information")
    
    # Menghitung total dan rata-rata rental
    total_rentals = day_df['count'].sum()
    avg_rentals = round(day_df['count'].mean())

    # Menampilkan informasi
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Rentals", value=f"{total_rentals:,}")  
    with col2:
        st.metric("Average Daily Rentals", value=f"{avg_rentals:,}")  
    
    # Visualisasi Time Series Bike Rentals (2011-2012)
    st.subheader("📈 Bike Rentals Over Time (2011-2012)")
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(day_df["date"], day_df["count"], marker='o', linestyle='-', color="#001f3f", alpha=0.8)
    ax.set_xlabel("Date")
    ax.set_ylabel("Total Rentals")
    ax.grid(True, linestyle='--', alpha=0.7)

    st.pyplot(fig)

    # Visualisasi Rata-rata Penyewaan Sepeda Per Hari dalam Seminggu
    st.subheader("📅 Average Bike Rentals Per Day of the Week")
    
    # Menghitung rata-rata jumlah penyewaan berdasarkan hari dalam seminggu
    day_of_week_rentals = day_df.groupby('day_of_week')['count'].mean().reindex([
        'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
    ])

    base_color = "#001f3f"  
    highlight_color = "#0074D9"  # Warna lebih terang untuk nilai tertinggi
    colors = [highlight_color if v == day_of_week_rentals.max() else base_color for v in day_of_week_rentals.values]

    # Membuat bar chart
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(day_of_week_rentals.index, day_of_week_rentals.values, color=colors, alpha=0.8)

    # Menampilkan angka di atas batang
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 50, f"{int(height)}", ha='center', fontsize=11, fontweight='bold')

    # Label sumbu dan judul
    ax.set_xlabel("Day of the Week")
    ax.set_ylabel("Average Rentals")
    ax.set_ylim(0, day_of_week_rentals.max() * 1.2)  
    ax.grid(True, linestyle='--', alpha=0.6)

    st.pyplot(fig)

# Working Days vs Holidays
elif menu == "🏢 Working vs Holiday":
    # Menghitung informasi utama
    total_rentals_working = int(day_df[day_df['workingday'] == "Yes"]['count'].sum())
    total_rentals_weekend = int(day_df[day_df['workingday'] == "No"]['count'].sum())
    total_rentals_holiday = int(day_df[day_df['holiday'] == "Yes"]['count'].sum())
    total_rentals_regular = int(day_df[day_df['holiday'] == "No"]['count'].sum())
    
    st.subheader("📌 Key Highlights Totals")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Working Days", value=f"{total_rentals_working:,}")  
    with col2:
        st.metric("Weekends", value=f"{total_rentals_weekend:,}")  
    with col3:
        st.metric("Holidays", value=f"{total_rentals_holiday:,}")  
    with col4:
        st.metric("Regular Days", value=f"{total_rentals_regular:,}")

    st.subheader("Average Bike Rentals Working Days vs Weekend")

    # Menghitung rata-rata jumlah penyewaan pada hari kerja dan akhir pekan
    working_vs_weekend = day_df.groupby('workingday')['count'].mean()

    # Buat DataFrame baru untuk mempermudah visualisasi
    data = pd.DataFrame({
        'Kategori': ['Working Days' if k == "Yes" else 'Weekends' for k in working_vs_weekend.index],
        'Jumlah Penyewaan': working_vs_weekend.values
    })

    # Menentukan warna
    base_color = "#001f3f"  
    highlight_color = "#0074D9"  
    colors = [highlight_color if v == max(data['Jumlah Penyewaan']) else base_color for v in data['Jumlah Penyewaan']]

    # Membuat bar chart
    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(data['Kategori'], data['Jumlah Penyewaan'], color=colors, alpha=0.8)

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 50, f"{int(height)}", ha='center', fontsize=12, fontweight='bold')

    ax.set_ylabel("Average Rentals")
    ax.set_ylim(0, max(data['Jumlah Penyewaan']) * 1.2)  
    ax.grid(True, linestyle='--', alpha=0.6)

    st.pyplot(fig)

    st.subheader("Average Bike Rentals Regular Days vs Holidays")

    # Menghitung rata-rata jumlah penyewaan pada hari biasa dan hari libur
    holiday_rentals = day_df.groupby('holiday')['count'].mean()

    # Buat DataFrame baru untuk visualisasi
    data = pd.DataFrame({
        'Kategori': ['Regular Days' if k == "No" else 'Holidays' for k in holiday_rentals.index],
        'Jumlah Penyewaan': holiday_rentals.values
    })

    # Menentukan warna
    colors = [highlight_color if v == max(data['Jumlah Penyewaan']) else base_color for v in data['Jumlah Penyewaan']]

    # Membuat bar chart
    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(data['Kategori'], data['Jumlah Penyewaan'], color=colors, alpha=0.8)

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 50, f"{int(height)}", ha='center', fontsize=12, fontweight='bold')

    ax.set_ylabel("Average Rentals")
    ax.set_ylim(0, max(data['Jumlah Penyewaan']) * 1.2)  
    ax.grid(True, linestyle='--', alpha=0.6)

    st.pyplot(fig)

    st.subheader("⏰ Bike Rental Trends by Hour")

    # Menghitung rata-rata penyewaan berdasarkan jam untuk hari kerja, akhir pekan, dan hari libur
    hourly_pattern = hour_df.groupby(['workingday', 'hours'])['count'].mean().reset_index()
    holiday_pattern = hour_df.groupby(['holiday', 'hours'])['count'].mean().reset_index()

    # Membuat line chart
    fig, ax = plt.subplots(figsize=(8, 5))

    # Plot hari kerja
    sns.lineplot(data=hourly_pattern[hourly_pattern['workingday'] == "Yes"], x='hours', y='count', label="Working Days", color=highlight_color)
    # Plot akhir pekan
    sns.lineplot(data=hourly_pattern[hourly_pattern['workingday'] == "No"], x='hours', y='count', label="Weekends", color="orange")
    # Plot hari libur
    sns.lineplot(data=holiday_pattern[holiday_pattern['holiday'] == "Yes"], x='hours', y='count', label="Holidays", color="red")

    ax.set_xlabel("Hours")
    ax.set_ylabel("Average Rentals")
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.6)

    st.pyplot(fig)

# Weather Impact
elif menu == "🌤️ Weather Impact":
    st.title("Weather Influence on Bike Rentals")
    
    # Menghitung rata-rata suhu, kelembaban, dan kecepatan angin saat penyewaan tinggi
    avg_temp = day_df['temp'].mean()
    avg_humidity = day_df['humidity'].mean()
    avg_wind_speed = day_df['wind_speed'].mean()

    # Menentukan faktor cuaca yang paling berpengaruh berdasarkan korelasi
    correlation = day_df[['temp', 'humidity', 'wind_speed', 'count']].corr()['count'].drop('count')
    most_influential_factor = correlation.idxmax()
    highest_correlation = correlation.max()

    # Menampilkan highlight informasi
    st.subheader("📌 Key Highlights")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Avg Temperature (°C)", value=f"{avg_temp:.1f}°C")
    with col2:
        st.metric("Avg Humidity (%)", value=f"{avg_humidity:.1f}%")
    with col3:
        st.metric("Avg Wind Speed (km/h)", value=f"{avg_wind_speed:.1f} km/h")

    st.write(
        f"📊 Faktor cuaca yang paling mempengaruhi penyewaan sepeda adalah **{most_influential_factor.capitalize()}**, "
        f"dengan korelasi **{highest_correlation:.2f}** terhadap jumlah penyewaan. "
        f"Rata-rata suhu selama periode ini adalah **{avg_temp:.1f}°C**, "
        f"yang menunjukkan bahwa suhu memiliki peran penting dalam keputusan pengguna untuk menyewa sepeda."
    )

    # Scatter Plot Faktor Cuaca vs Penyewaan
    st.subheader("🌡️ Weather Factors vs Bike Rentals")
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    sns.scatterplot(x=day_df['temp'], y=day_df['count'], ax=axes[0], color="#FF4136")  # Merah
    axes[0].set_title("Temperature vs Rentals")
    sns.scatterplot(x=day_df['humidity'], y=day_df['count'], ax=axes[1], color="#0074D9")  # Biru
    axes[1].set_title("Humidity vs Rentals")
    sns.scatterplot(x=day_df['wind_speed'], y=day_df['count'], ax=axes[2], color="#2ECC40")  # Hijau
    axes[2].set_title("Wind Speed vs Rentals")

    st.pyplot(fig)

    # Korelasi Faktor Cuaca dengan Jumlah Penyewaan
    st.subheader("📊 Correlation: Weather Factors vs Bike Rentals")

    # Membuat bar chart
    fig, ax = plt.subplots(figsize=(6, 4))

    colors = ["#FF4136", "#0074D9", "#2ECC40"]
    bars = ax.bar(correlation.index, correlation.values, color=colors, alpha=0.8)

    for bar, value in zip(bars, correlation.values):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.02, f"{value:.2f}", ha='center', fontsize=12, fontweight='bold')

    ax.set_ylabel("Correlation")
    ax.set_ylim(-1, 1)  # Korelasi berkisar dari -1 hingga 1
    ax.grid(True, linestyle='--', alpha=0.6)

    st.pyplot(fig)

# Other Insights
elif menu == "📈 Other Insights":
    st.title("🚲 Bike Rentals per Season")

    # Menghitung rata-rata penyewaan sepeda per musim
    season_rentals = day_df.groupby('season')['count'].mean().reset_index()

    # Menentukan musim dengan jumlah penyewaan tertinggi & terendah
    max_season = season_rentals.loc[season_rentals['count'].idxmax()]
    min_season = season_rentals.loc[season_rentals['count'].idxmin()]

    # Menampilkan highlight informasi
    st.subheader("📌 Key Highlights")

    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            label=f"🌟 Most Rentals in {max_season['season']}",
            value=f"{int(max_season['count'])} rentals"
        )
    with col2:
        st.metric(
            label=f"📉 Least Rentals in {min_season['season']}",
            value=f"{int(min_season['count'])} rentals"
        )

    st.write(
        f"🔍 Jumlah penyewaan sepeda tertinggi terjadi pada **{max_season['season']}** dengan rata-rata **{int(max_season['count'])}** penyewaan per hari. "
        f"Sebaliknya, jumlah penyewaan terendah terjadi pada **{min_season['season']}** dengan rata-rata **{int(min_season['count'])}** per hari. "
        f"Hal ini menunjukkan bahwa perubahan musim memiliki pengaruh signifikan terhadap permintaan penyewaan sepeda."
    )

    # Membuat bar chart
    st.subheader("📊 Average Bike Rentals per Season")

    fig, ax = plt.subplots(figsize=(8, 5))
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']  # Warna sesuai dashboard

    sns.barplot(x='season', y='count', data=season_rentals, palette=colors, ax=ax)

    # Menambahkan angka di atas setiap bar
    for i, v in enumerate(season_rentals['count']):
        ax.text(i, v + 100, f"{int(v)}", ha='center', fontsize=12, fontweight='bold')

    ax.set_xlabel("Season")
    ax.set_ylabel("Average Rentals")
    ax.set_title("🚲 Seasonal Impact on Bike Rentals")
    ax.grid(True, linestyle='--', alpha=0.6)

    st.pyplot(fig)

st.caption('© 2025 Bike Rental Service. All rights reserved.')
