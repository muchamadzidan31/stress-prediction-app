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
# Konfigurasi Halaman & Suntikan Custom CSS
# =====================================================
st.set_page_config(
    page_title="Stress Level Analyzer",
    page_icon="🧠",
    layout="wide"
)

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        background: linear-gradient(45deg, #4b6cb7, #182848);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(75,108,183,0.4);
    }
    div[data-testid="stMetricValue"] {
        font-size: 36px;
        font-weight: 800;
    }
    </style>
""", unsafe_allow_html=True)

# =====================================================
# Mapping Data
# =====================================================
gender_map = {0: "Perempuan", 1: "Laki-laki"}
occupation_map = {0: "Doctor", 1: "Employee", 2: "Student", 3: "Teacher"}

# =====================================================
# Sidebar Informasi & Anggota Kelompok
# =====================================================
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 60px; margin-bottom: 0;'>🧠</h1>", unsafe_allow_html=True)
    # Judul diperbarui sesuai permintaan
    st.markdown("<h3 style='text-align: center; margin-top: 0; color: #4b6cb7;'>Stress Level Analyzer</h3>", unsafe_allow_html=True)
    # Deskripsi disesuaikan agar lebih padat dan elegan
    st.write("Sistem analisis kesehatan mental berbasis kecerdasan buatan untuk mengevaluasi tingkat stres harian Anda.")
    
    st.markdown("---")
    
    with st.sidebar.expander("👥 Anggota Kelompok (NBI)", expanded=True):
        st.markdown("""
        * **Mochammad Hidayatulloh A.** <br><code style='color:#4b6cb7;'>1462400044</code>
        * **Delphi Raida Althafiyani** <br><code style='color:#4b6cb7;'>1462400072</code>
        * **Iqbal Babussalam** <br><code style='color:#4b6cb7;'>14624000104</code>
        * **Muchamad Zidan Amirulloh** <br><code style='color:#4b6cb7;'>1462400178</code>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption(f"© {datetime.now().year} | Ditenagai oleh Streamlit")

# =====================================================
# Main Header & Tabs
# =====================================================
st.title("🧠 Stress Level Analyzer & Health Dashboard")
st.write("Optimalkan produktivitas Anda dengan menjaga keseimbangan antara ekosistem digital dan waktu istirahat tubuh.")

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Prediksi Stres & Analisis", 
    "🔍 Kalkulator Rasio Digital", 
    "💡 Tips Manajemen Stres",
    "🎯 Tantangan Hidup Sehat"
])

# =====================================================
# TAB 1: PREDIKSI STRES & DOWNLOAD REPORT
# =====================================================
with tab1:
    st.subheader("📝 Pengisian Data Aktivitas Harian")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 👤 Profil Dasar")
        age = st.number_input("Usia (Tahun)", min_value=18, max_value=80, value=25)
        gender = st.selectbox("Jenis Kelamin", options=list(gender_map.keys()), format_func=lambda x: gender_map[x])
        occupation = st.selectbox("Pekerjaan", options=list(occupation_map.keys()), format_func=lambda x: occupation_map[x])
        coffee = st.slider("Konsumsi Kafein (Gelas/Hari)", 0, 10, 3)

    with col2:
        st.markdown("#### 📱 Kebiasaan Digital")
        screen = st.slider("Durasi Screen Time (Jam/Hari)", 0.0, 15.0, 8.0, step=0.5)
        phone = st.slider("Main HP Sebelum Tidur (Menit)", 0, 180, 60, step=5)
        notif = st.slider("Jumlah Notifikasi/Hari", 0, 300, 120, step=10)

    with col3:
        st.markdown("#### 🛌 Kualitas Hidup & Fisik")
        sleep = st.slider("Durasi Tidur (Jam)", 3.0, 12.0, 6.0, step=0.5)
        quality = st.slider("Skor Kualitas Tidur (0-100)", 0, 100, 55)
        physical = st.slider("Aktivitas Fisik (Menit/Hari)", 0, 180, 30, step=5)
        fatigue = st.slider("Skor Kelelahan Mental (0-100)", 0, 100, 80)

    st.markdown("---")

    if st.button("🔍 Mulai Analisis Tingkat Stress", use_container_width=True):
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
            st.markdown("### 📊 Hasil Analisis Tingkat Stres")
            
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
                st.progress(min(max(pred / 10.0, 0.0), 1.0))
            with res_col2:
                st.metric(label="Kategori Stres Anda", value=kategori, delta=delta_info, delta_color="off")

            warna_box(f"Berdasarkan analisis model AI, tingkat stres Anda berada di kategori **{kategori.split()[0]}**.")

            # Rekomendasi Dinamis & Pembuatan Teks untuk Laporan
            st.markdown("#### 🛠️ Rekomendasi Personalisasi:")
            saran_list = []
            
            if coffee > 4:
                msg = "- Batasi Kafein: Konsumsi kafein berlebih dapat menaikkan detak jantung mendadak dan memicu kecemasan."
                st.warning(f"⚠️ {msg[2:]}")
                saran_list.append(msg)
            if phone > 60:
                msg = "- Kurangi Screen-Time Malam: Pancaran sinar biru HP mengacaukan ritme sirkadian tubuh."
                st.warning(f"⚠️ {msg[2:]}")
                saran_list.append(msg)
            if physical < 20:
                msg = "- Kurang Aktivitas Fisik: Sempatkan berolahraga ringan atau sekadar peregangan agar hormon endorfin keluar."
                st.info(f"💡 {msg[2:]}")
                saran_list.append(msg)
                
            if not saran_list:
                msg = "- Pola hidup Anda saat ini sudah sangat seimbang! Pertahankan rutinitas baik ini."
                st.success(f"✅ {msg[2:]}")
                saran_list.append(msg)

            saran_text = "\n".join(saran_list)

            # FITUR BARU: LAPORAN HASIL .TXT YANG JAUH LEBIH RAPI & PROFESIONAL
            report_text = f"""=======================================================
               OFFICIAL MEDICAL REPORT                  
                STRESS LEVEL ANALYZER                  
=======================================================
Waktu Pemeriksaan : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Status Prediksi   : SELESAI

[ HASIL ANALISIS UTAMA ]
-------------------------------------------------------
* Skor Prediksi Stres : {pred:.2f} / 10.00
* Kategori Stres      : {kategori.split()[0].upper()}

[ RINGKASAN METRIK AKTIVITAS ]
-------------------------------------------------------
- Usia / Gender       : {age} Tahun / {gender_map[gender]}
- Pekerjaan           : {occupation_map[occupation]}
- Durasi Layar (HP)   : {screen} Jam/Hari
- Penggunaan Pra-Tidur: {phone} Menit
- Durasi & Kual. Tidur: {sleep} Jam (Skor Kualitas: {quality}/100)
- Rasio Layar/Tidur   : {ratio:.2f}
- Konsumsi Kafein     : {coffee} Gelas/Hari
- Aktivitas Fisik     : {physical} Menit/Hari
- Skor Kelelahan Saraf: {fatigue}/100

[ REKOMENDASI TIM AHLI ]
-------------------------------------------------------
{saran_text}

=======================================================
               TIM PENGUJI (KELOMPOK)                  
-------------------------------------------------------
1. Mochammad Hidayatulloh Ardiansyah (1462400044)
2. Delphi Raida Althafiyani         (1462400072)
3. Iqbal Babussalam                 (1462400104)
4. Muchamad Zidan Amirulloh         (1462400178)
=======================================================
"""
            st.markdown("---")
            st.download_button(
                label="📥 Unduh Laporan Resmi Hasil Pemeriksaan (.txt)",
                data=report_text,
                file_name=f"Laporan_Resmi_Stres_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain",
                use_container_width=True
            )

# =====================================================
# TAB 2: CEK RASIO DIGITAL (KALKULATOR)
# =====================================================
with tab2:
    st.subheader("🔍 Kalkulator Rasio Gawai vs Tidur")
    current_ratio = screen / sleep if sleep > 0 else 0
    st.write(f"Rasio penggunaan gadget berbanding durasi istirahat Anda saat ini: **{current_ratio:.2f}**")
    
    if current_ratio <= 1.0:
        st.success("✅ **Rasio Ideal**: Waktu tidur Anda tercukupi dengan baik dibandingkan waktu di depan layar.")
    elif current_ratio <= 1.5:
        st.warning("⚠️ **Rasio Rawan**: Aktivitas digital Anda mulai mengorbankan waktu pemulihan energi sel tubuh.")
    else:
        st.error("🚨 **Rasio Kritis**: Durasi screen time terlalu dominan. Sangat berisiko memicu *burnout*.")

# =====================================================
# TAB 3: TIPS MANAJEMEN STRES
# =====================================================
with tab3:
    st.subheader("💡 Tips Praktis Berdasarkan Sains")
    t_col1, t_col2 = st.columns(2)
    with t_col1:
        st.markdown("""
        #### 📱 Regulasi Digital
        * Gunakan fitur *Do Not Disturb* saat jam istirahat.
        * Batasi durasi berselancar di media sosial maksimal 2 jam sehari.
        """)
    with t_col2:
        st.markdown("""
        #### 🧘 Regulasi Biologis
        * Terapkan aturan 20-20-20 (setiap 20 menit melihat layar, tatap objek sejauh 20 kaki selama 20 detik).
        * Konsumsi air putih yang cukup untuk meredakan ketegangan saraf kepala.
        """)

# =====================================================
# TAB 4: TANTANGAN HIDUP SEHAT
# =====================================================
with tab4:
    st.subheader("🎯 Self-Care Challenge Hari Ini")
    st.write("Centang tantangan di bawah ini jika Anda berhasil melakukannya hari ini!")
    
    c1 = st.checkbox("Saya tidak membuka HP 30 menit sebelum tidur semalam.")
    c2 = st.checkbox("Saya berolahraga atau berjalan kaki minimal 15 menit hari ini.")
    c3 = st.checkbox("Saya membatasi konsumsi kopi/kafein hari ini.")
    c4 = st.checkbox("Saya meluangkan waktu minum air putih minimal 2 liter.")

    if c1 and c2 and c3 and c4:
        st.balloons()
        st.success("🎉 **Luar Biasa!** Anda telah menyelesaikan seluruh komitmen sehat hari ini. Pertahankan demi kesehatan mental Anda!")
