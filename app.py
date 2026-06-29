import streamlit as st
import pandas as pd
import joblib

# =====================================================
# Load Model
# =====================================================

model = joblib.load("stress_prediction_model.pkl")
scaler = joblib.load("scaler.pkl")

# =====================================================
# Konfigurasi Halaman
# =====================================================

st.set_page_config(
    page_title="Prediksi Tingkat Stress",
    page_icon="📱",
    layout="centered"
)

# =====================================================
# Judul
# =====================================================

st.title("📱 Prediksi Tingkat Stress")

st.write(
    """
    Aplikasi ini digunakan untuk memprediksi **tingkat stres**
    berdasarkan durasi penggunaan smartphone, kualitas tidur,
    dan beberapa faktor pendukung lainnya.
    """
)

st.divider()

# =====================================================
# Mapping Gender & Occupation
# =====================================================

gender_map = {
    0: "Perempuan",
    1: "Laki-laki"
}

occupation_map = {
    0: "Doctor",
    1: "Employee",
    2: "Student",
    3: "Teacher"
}

# =====================================================
# Input User
# =====================================================

st.subheader("📝 Input Data")

age = st.number_input(
    "Usia",
    min_value=18,
    max_value=80,
    value=25
)

gender = st.selectbox(
    "Jenis Kelamin",
    options=list(gender_map.keys()),
    format_func=lambda x: gender_map[x]
)

occupation = st.selectbox(
    "Pekerjaan",
    options=list(occupation_map.keys()),
    format_func=lambda x: occupation_map[x]
)

screen = st.slider(
    "Durasi Screen Time (Jam/Hari)",
    0.0,
    15.0,
    8.0
)

phone = st.slider(
    "Penggunaan HP Sebelum Tidur (Menit)",
    0,
    180,
    60
)

sleep = st.slider(
    "Durasi Tidur (Jam)",
    3.0,
    12.0,
    6.0
)

quality = st.slider(
    "Skor Kualitas Tidur",
    0,
    100,
    55
)

coffee = st.slider(
    "Konsumsi Kafein (Gelas/Hari)",
    0,
    10,
    3
)

physical = st.slider(
    "Aktivitas Fisik (Menit/Hari)",
    0,
    180,
    30
)

notif = st.slider(
    "Jumlah Notifikasi/Hari",
    0,
    300,
    120
)

fatigue = st.slider(
    "Mental Fatigue Score",
    0,
    100,
    80
)

# =====================================================
# Prediksi
# =====================================================

if st.button("🔍 Prediksi Tingkat Stress", use_container_width=True):

    ratio = screen / sleep

    data = pd.DataFrame({

        "age": [age],
        "gender": [gender],
        "occupation": [occupation],
        "daily_screen_time_hours": [screen],
        "phone_usage_before_sleep_minutes": [phone],
        "sleep_duration_hours": [sleep],
        "sleep_quality_score": [quality],
        "caffeine_intake_cups": [coffee],
        "physical_activity_minutes": [physical],
        "notifications_received_per_day": [notif],
        "mental_fatigue_score": [fatigue],
        "screen_sleep_ratio": [ratio]

    })

    data_scaled = scaler.transform(data)

    pred = model.predict(data_scaled)[0]

    st.divider()

    st.subheader("📊 Hasil Prediksi")

    st.success(f"Prediksi Tingkat Stress : **{pred:.2f}**")

    if pred < 4:
        st.success("Kategori Stress : **Rendah** 😊")

    elif pred < 7:
        st.warning("Kategori Stress : **Sedang** 😐")

    else:
        st.error("Kategori Stress : **Tinggi** 😟")

    st.write("### Data yang Dimasukkan")

    tampil = data.copy()

    tampil["gender"] = gender_map[gender]
    tampil["occupation"] = occupation_map[occupation]

    st.dataframe(
        tampil,
        use_container_width=True
    )