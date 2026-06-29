import streamlit as st
import pandas as pd
import joblib
from datetime import datetime

# =====================================================
# Load Model & Scaler
# =====================================================
@st.cache_resource
def load_resources():
    model = joblib.load("stress_prediction_model.pkl")
    scaler = joblib.load("scaler.pkl")
    return model, scaler

try:
    model, scaler = load_resources()
except Exception as e:
    st.error(f"Gagal memuat model/scaler. Pastikan file tersedia. Error: {e}")

# =====================================================
# Konfigurasi Halaman
# =====================================================
st.set_page_config(
    page_title="Stress Level Analyzer PRO",
    page_icon="🧠",
    layout="wide"
)

# =====================================================
# Mapping Data
# =====================================================
gender_map = {0: "Perempuan", 1: "Laki-laki"}
occupation_map = {0: "Doctor", 1: "Employee", 2: "Student", 3: "Teacher"}

# =====================================================
# Sidebar Informasi & Anggota Kelompok
# =====================================================
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 70px; margin-bottom: 0;'>🧠</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; margin-top: 0;'>Stress Analyzer v2.0</h2>", unsafe_allow_html=True)
    st.write(
        """
        Aplikasi ini menggunakan algoritma *Machine Learning* untuk mendeteksi tingkat stres berdasarkan aktivitas digital dan pola tidur Anda.
        """
    )
    
    st.markdown("---")
    
    # Menampilkan Nama Anggota Kelompok
    st.markdown("### 👥 Anggota Kelompok:")
    st.markdown("""
    * **Mochammad Hidayatulloh A.** <span style='color: gray; font-size: 13px;'>NBI: 1462400044</span>
    * **Delphi Raida Althafiyani** <span style='color: gray; font-size: 13px;'>NBI: 1462400072</span>
    * **Iqbal Babussalam** <span style='color: gray; font-size: 13px;'>NBI: 1462400104</span>
    * **Muchamad Zidan Amirulloh** <span style='color: gray; font-size: 13px;'>NBI: 1462400178</span>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption(f"© {datetime.now().year} | Ditenagai oleh Streamlit")

# =====================================================
# Main Header & Tabs
# =====================================================
st.title("🧠 Stress Level Analyzer & Health Tracker")
st.write("Kenali kondisi kesehatan mental dan kebiasaan digital Anda secara mendalam.")

tab1, tab2, tab3 = st.tabs(["📊 Prediksi Stres", "🔍 Cek Rasio Digital", "💡 Tips Manajemen Stres"])

# =====================================================
# TAB 1: PREDIKSI STRES & DOWNLOAD REPORT
# =====================================================
with tab1:
    st.subheader("📝 Pengisian Data Harian")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 👤 Profil Dasar")
        age = st.number_input("Usia (Tahun)", min_value=18, max_value=80, value=25)
        gender = st.selectbox("Jenis Kelamin", options=list(gender_map.keys()), format_func=lambda x: gender_map[x])
        occupation = st.selectbox("Pekerjaan", options=list(occupation_map.keys()), format_func=lambda x: occupation_map[x])
        coffee = st.slider("Konsumsi Kafein (Gelas/Hari)", 0, 10, 3)

    with col2:
        st.markdown("### 📱 Kebiasaan Digital")
        screen = st.slider("Durasi Screen Time (Jam/Hari)", 0.0, 15.0, 8.0, step=0.5)
        phone = st.slider("Main HP Sebelum Tidur (Menit)", 0, 180, 60, step=5)
        notif = st.slider("Jumlah Notifikasi/Hari", 0, 300, 120, step=10)

    with col3:
        st.markdown("### 🛌 Kualitas Hidup & Fisik")
        sleep = st.slider("Durasi Tidur (Jam)", 3.0, 12.0, 6.0, step=0.5)
        quality = st.slider("Skor Kualitas Tidur (0-100)", 0, 100, 55)
        physical = st.slider("Aktivitas Fisik (Menit/Hari)", 0, 180, 30, step=5)
        fatigue = st.slider("Skor Kelelahan Mental (0-100)", 0, 100, 80)

    st.markdown("---")

    if st.button("🔍 Mulai Analisis Tingkat Stress", use_container_width=True, type="primary"):
        ratio = screen / sleep if sleep > 0 else screen / 0.1
        
        data = pd.DataFrame({
            "age": [age], "gender": [gender], "occupation": [occupation],
            "daily_screen_time_hours": [screen], "phone_usage_before_sleep_minutes": [phone],
            "sleep_duration_hours": [sleep], "sleep_quality_score": [quality],
            "caffeine_intake_cups": [coffee], "physical_activity_minutes": [physical],
            "notifications_received_per_day": [notif], "mental_fatigue_score": [fatigue],
            "screen_sleep_ratio": [ratio]
        })

        data_scaled = scaler.transform(data)
        pred = model.predict(data_scaled)[0]

        with st.container(border=True):
            st.subheader("📊 Hasil Analisis Kesehatan Mental")
            
            if pred < 4.0:
                kategori = "Rendah 😊"
                warna_box = st.success
                delta_info = "Kondisi Anda aman!"
            elif pred < 7.0:
                kategori = "Sedang 😐"
                warna_box = st.warning
                delta_info = "Perlu waspada & relaksasi."
            else:
                kategori = "Tinggi 😟"
                warna_box = st.error
                delta_info = "Butuh istirahat segera!"

            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.metric(label="Skor Prediksi Stres (Skala 0-10)", value=f"{pred:.2f}")
            with res_col2:
                st.metric(label="Kategori Stres Anda", value=kategori, delta=delta_info, delta_color="off")

            warna_box(f"Berdasarkan analisis model, tingkat stres Anda berada di kategori **{kategori.split()[0]}**.")

            st.markdown("### 🛠️ Rekomendasi Khusus Untuk Anda:")
            rekomendasi_ada = False
            if coffee > 4:
                st.warning("⚠️ **Konsumsi Kafein Tinggi**: Kurangi minum kopi di atas jam 2 siang agar tidak mengganggu fase tidur dalam (*deep sleep*).")
                rekomendasi_ada = True
            if phone > 60:
                st.warning("⚠️ **Paparan Blue Light Berlebih**: Batasi main HP maksimal 30 menit sebelum tidur untuk meningkatkan hormon melatonin.")
                rekomendasi_ada = True
            if physical < 20:
                st.info("💡 **Kurang Gerak**: Coba luangkan waktu berjalan kaki 15 menit hari ini untuk membantu mereduksi hormon kortisol (stres).")
                rekomendasi_ada = True
            if not rekomendasi_ada:
                st.success("✅ Kebiasaan harian Anda secara umum sudah cukup seimbang!")

            report_text = f"""=== LAPORAN ANALISIS TINGKAT STRES ===
Tanggal Analisis : {datetime.now().strftime('%Y-%m-%d %H:%M')}
Skor Prediksi    : {pred:.2f}
Kategori Stres   : {kategori.split()[0]}
-------------------------------------
DATA INPUT:
- Usia           : {age} Tahun
- Screen Time    : {screen} Jam/Hari
- Durasi Tidur   : {sleep} Jam
- Kualitas Tidur : {quality}/100
====================================="""
            
            st.markdown("---")
            st.download_button(
                label="📥 Unduh Laporan Hasil (.txt)",
                data=report_text,
                file_name=f"Stress_Report_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True
            )

# =====================================================
# TAB 2: CEK RASIO DIGITAL (KALKULATOR)
# =====================================================
with tab2:
    st.subheader("🔍 Kalkulator Rasio Screen Time vs Waktu Tidur")
    st.write("Fitur ini menganalisis apakah durasi menatap layar Anda lebih mendominasi daripada waktu tubuh Anda beristirahat.")
    
    current_ratio = screen / sleep if sleep > 0 else 0
    st.write(f"Rasio Anda saat ini: **{current_ratio:.2f}**")
    
    if current_ratio <= 1.0:
        st.success("✅ **Rasio Sehat**: Waktu tidur Anda lebih banyak atau seimbang dengan waktu melihat layar. Pertahankan!")
    elif current_ratio <= 1.5:
        st.warning("⚠️ **Rasio Lampu Kuning**: Waktu menatap layar sudah mulai melampaui waktu tidur Anda. Kurangi aktivitas digital non-esensial.")
    else:
        st.error("🚨 **Rasio Tidak Sehat**: Waktu *screen time* Anda jauh lebih tinggi daripada durasi istirahat. Ini adalah pemicu utama kelelahan mental.")

# =====================================================
# TAB 3: TIPS MANAJEMEN STRES
# =====================================================
with tab3:
    st.subheader("💡 Tips Praktis Mengurangi Stres")
    t_col1, t_col2 = st.columns(2)
    with t_col1:
        st.markdown("""
        #### 📱 Detoks Digital
        * **Batasi Screen Time**: Kurangi penggunaan HP minimal 30 menit sebelum tidur.
        * **Filter Notifikasi**: Matikan notifikasi aplikasi yang tidak mendesak.
        """)
    with t_col2:
        st.markdown("""
        #### 🛌 Optimalkan Tidur
        * Pertahankan durasi tidur ideal **7-8 jam** per hari.
        * Buat suasana kamar sejuk, gelap, dan tenang.
        """)
