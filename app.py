import streamlit as st
import pandas as pd
import joblib

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
    page_title="Stress Level Analyzer",
    page_icon="🧠",
    layout="wide"  # Mengubah ke wide agar layout kolom lebih leluasa
)

# =====================================================
# Mapping Data
# =====================================================
gender_map = {0: "Perempuan", 1: "Laki-laki"}
occupation_map = {0: "Doctor", 1: "Employee", 2: "Student", 3: "Teacher"}

# =====================================================
# Sidebar Informasi
# =====================================================
with st.sidebar:
    st.image("https://img.icons8.com/illustrations/external-pack-avocado-thb-photos/512/external-Mental-Health-medical-pack-avocado-thb-photos.png", use_container_width=True)
    st.title("🧠 Tentang Aplikasi")
    st.write(
        """
        Aplikasi **Stress Level Analyzer** ini memanfaatkan *Machine Learning* untuk memprediksi tingkat stres Anda berdasarkan pola hidup digital, 
        kualitas tidur, dan aktivitas harian.
        """
    )
    st.markdown("---")
    st.caption("Dibuat dengan ❤️ menggunakan Streamlit.")

# =====================================================
# Main Header & Tabs
# =====================================================
st.title("🧠 Stress Level Analyzer & Predictor")
st.write("Kenali kondisi kesehatan mental Anda melalui analisis kebiasaan harian.")

tab1, tab2 = st.tabs(["📊 Prediksi Stres", "💡 Tips Manajemen Stres"])

# =====================================================
# TAB 1: PREDIKSI STRES
# =====================================================
with tab1:
    st.subheader("📝 Pengisian Data Harian")
    st.info("Silakan isi data di bawah ini dengan kondisi yang paling mendekati rutinitas Anda sehari-hari.")
    
    # Membuat 3 kolom untuk form input agar lebih ringkas dan rapi
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

    # Tombol Prediksi besar di tengah
    if st.button("🔍 Mulai Analisis Tingkat Stress", use_container_width=True, type="primary"):
        
        # Validasi pembagian dengan nol
        ratio = screen / sleep if sleep > 0 else screen / 0.1
        
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

        # Proses Prediksi
        data_scaled = scaler.transform(data)
        pred = model.predict(data_scaled)[0]

        # Tampilan Hasil Masuk ke dalam container khusus
        with st.container(border=True):
            st.subheader("📊 Hasil Analisis Kesehatan Mental")
            
            # Menentukan kategori dan warna visual
            if pred < 4.0:
                kategori = "Rendah 😊"
                warna_box = st.success
                delta_info = "Kondisi Anda sangat baik!"
            elif pred < 7.0:
                kategori = "Sedang 😐"
                warna_box = st.warning
                delta_info = "Perlu sedikit relaksasi."
            else:
                kategori = "Tinggi 😟"
                warna_box = st.error
                delta_info = "Sangat disarankan untuk beristirahat."

            # Tampilan Ringkasan dengan Metric Layout
            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.metric(label="Skor Prediksi Stres (Skala 0-10)", value=f"{pred:.2f}")
            with res_col2:
                st.metric(label="Kategori Stres Anda", value=kategori, delta=delta_info, delta_color="off")

            # Pesan Kotak Berwarna sesuai Kategori
            warna_box(f"Berdasarkan analisis, tingkat stres Anda masuk dalam kategori **{kategori.split()[0]}**.")

            # Menampilkan Ringkasan Data Input Pembaca
            with st.expander("🔎 Lihat Detail Data yang Anda Masukkan"):
                tampil = data.copy()
                tampil["gender"] = gender_map[gender]
                tampil["occupation"] = occupation_map[occupation]
                st.dataframe(tampil, use_container_width=True)

# =====================================================
# TAB 2: TIPS MANAJEMEN STRES
# =====================================================
with tab2:
    st.subheader("💡 Tips Praktis Mengurangi Stres")
    st.write("Berikut beberapa langkah kecil yang bisa Anda lakukan berdasarkan riset kesehatan:")
    
    t_col1, t_col2 = st.columns(2)
    with t_col1:
        st.markdown("""
        #### 📱 Detoks Digital
        * **Batasi Screen Time**: Kurangi penggunaan HP minimal 30 menit sebelum tidur.
        * **Filter Notifikasi**: Matikan notifikasi aplikasi yang tidak mendesak agar fokus terjaga.
        
        #### 🛌 Optimalkan Tidur
        * Pertahankan durasi tidur ideal **7-8 jam** per hari.
        * Buat suasana kamar sejuk, gelap, dan tenang untuk menaikkan *Sleep Quality Score*.
        """)
        
    with t_col2:
        st.markdown("""
        #### 🧘 Kesehatan Fisik & Mental
        * Lakukan aktivitas fisik ringan (seperti jalan kaki atau peregangan) selama **15-30 menit** sehari.
        * Batasi asupan kafein, terutama di sore dan malam hari.
        
        #### ☕ Mindful Break
        * Jika *Mental Fatigue Score* Anda tinggi, terapkan teknik **Pomodoro** (25 menit kerja, 5 menit istirahat) saat beraktivitas atau bekerja.
        """)
