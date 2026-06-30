import streamlit as st
import pandas as pd
import joblib
from datetime import datetime
import plotly.graph_objects as go  # Tambahan untuk visualisasi Plotly

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
    /* Style tambahan untuk card dark mode mirip Stressio */
    .stressio-card {
        background-color: #1e1e2f;
        padding: 20px;
        border-radius: 12px;
        color: #ffffff;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# =====================================================
# INITIALIZATION: Inisialisasi Riwayat (Session State)
# =====================================================
if "prediction_history" not in st.session_state:
    st.session_state.prediction_history = []

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
    st.markdown("<h3 style='text-align: center; margin-top: 0; color: #4b6cb7;'>Stress Level Analyzer</h3>", unsafe_allow_html=True)
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
    st.caption(f"© {datetime.now().year} | Powered by Streamlit")

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

    # Memicu proses prediksi
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

        # Simpan state hasil prediksi agar visualisasi & riwayat persisten saat berinteraksi
        st.session_state["last_pred"] = {
            "pred": pred, "age": age, "gender": gender, "occupation": occupation, "coffee": coffee,
            "screen": screen, "phone": phone, "notif": notif, "sleep": sleep, "quality": quality,
            "physical": physical, "fatigue": fatigue, "ratio": ratio
        }

        # Kategori Penentuan
        if pred < 4.0:
            kategori_murni = "Rendah"
            kategori = "Rendah 😊"
        elif pred < 7.0:
            kategori_murni = "Sedang"
            kategori = "Sedang 😐"
        else:
            kategori_murni = "Tinggi"
            kategori = "Tinggi 😟"

        # FITUR BARU 1: Menyimpan riwayat ke st.session_state
        history_entry = {
            "Waktu": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "Age": age,
            "Screen Time": screen,
            "Sleep Duration": sleep,
            "Sleep Quality": quality,
            "Mental Fatigue": fatigue,
            "Prediksi Stress": round(pred, 2),
            "Kategori": kategori_murni
        }
        st.session_state.prediction_history.append(history_entry)

    # Mengecek apakah sudah ada riwayat prediksi sebelumnya untuk ditampilkan
    if "last_pred" in st.session_state:
        lp = st.session_state["last_pred"]
        pred = lp["pred"]
        
        if pred < 4.0:
            kategori = "Rendah 😊"
            warna_box = st.success
            delta_info = "Kondisi Anda aman!"
            kategori_murni = "Rendah"
        elif pred < 7.0:
            kategori = "Sedang 😐"
            warna_box = st.warning
            delta_info = "Perlu waspada & relaksasi."
            kategori_murni = "Sedang"
        else:
            kategori = "Tinggi 😟"
            warna_box = st.error
            delta_info = "Butuh istirahat segera!"
            kategori_murni = "Tinggi"

        with st.container(border=True):
            st.markdown("### 📊 Hasil Analisis Tingkat Stres")
            
            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.metric(label="Skor Prediksi Stres (Skala 0-10)", value=f"{pred:.2f}")
                st.progress(min(max(pred / 10.0, 0.0), 1.0))
            with res_col2:
                st.metric(label="Kategori Stres Anda", value=kategori, delta=delta_info, delta_color="off")

            warna_box(f"Berdasarkan analisis model AI, tingkat stres Anda berada di kategori **{kategori.split()[0]}**.")

            st.markdown("#### 🛠️ Rekomendasi Personalisasi:")
            saran_list = []
            
            if lp["coffee"] > 4:
                msg = "- Batasi Kafein: Konsumsi kafein berlebih dapat menaikkan detak jantung mendadak dan memicu kecemasan."
                st.warning(f"⚠️ {msg[2:]}")
                saran_list.append(msg)
            if lp["phone"] > 60:
                msg = "- Kurangi Screen-Time Malam: Pancaran sinar biru HP mengacaukan ritme sirkadian tubuh."
                st.warning(f"⚠️ {msg[2:]}")
                saran_list.append(msg)
            if lp["physical"] < 20:
                msg = "- Kurang Aktivitas Fisik: Sempatkan berolahraga ringan atau sekadar peregangan agar hormon endorfin keluar."
                st.info(f"💡 {msg[2:]}")
                saran_list.append(msg)
                
            if not saran_list:
                msg = "- Pola hidup Anda saat ini sudah sangat seimbang! Pertahankan rutinitas baik ini."
                st.success(f"✅ {msg[2:]}")
                saran_list.append(msg)

            saran_text = "\n".join(saran_list)

            # Pembuatan Dokumen Laporan .txt
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
- Usia / Gender       : {lp['age']} Tahun / {gender_map[lp['gender']]}
- Pekerjaan           : {occupation_map[lp['occupation']]}
- Durasi Layar (HP)   : {lp['screen']} Jam/Hari
- Penggunaan Pra-Tidur: {lp['phone']} Menit
- Durasi & Kual. Tidur: {lp['sleep']} Jam (Skor Kualitas: {lp['quality']}/100)
- Rasio Layar/Tidur   : {lp['ratio']:.2f}
- Konsumsi Kafein     : {lp['coffee']} Gelas/Hari
- Aktivitas Fisik     : {lp['physical']} Menit/Hari
- Skor Kelelahan Saraf: {lp['fatigue']}/100

[ REKOMENDASI TIM AHLI ]
-------------------------------------------------------
{saran_text}
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
        # FITUR BARU 2: VISUALISASI INPUT USER (PLOTLY RADAR & BAR)
        # =====================================================
        st.markdown("---")
        st.markdown("### 📈 Visualisasi Fitur Aktivitas")
        
        # Penyiapan Data Fitur
        labels = [
            'Screen Time (Hr)', 'Phone Before Sleep (Min)', 'Sleep Duration (Hr)', 
            'Sleep Quality (Score)', 'Caffeine Intake (Cup)', 'Physical Activity (Min)', 
            'Notification/Day', 'Mental Fatigue (Score)'
        ]
        values = [
            lp["screen"], lp["phone"], lp["sleep"], 
            lp["quality"], lp["coffee"], lp["physical"], 
            lp["notif"], lp["fatigue"]
        ]
        
        v_col1, v_col2 = st.columns(2)
        
        with v_col1:
            # 1. Radar Chart Plotly (Tema Dark)
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=values + [values[0]],
                theta=labels + [labels[0]],
                fill='toself',
                fillcolor='rgba(75, 108, 183, 0.3)',
                line=dict(color='#4b6cb7', width=2),
                name='Metrik Aktivitas'
            ))
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, gridcolor='#44445c'),
                    angularaxis=dict(gridcolor='#44445c')
                ),
                paper_bgcolor='#1e1e2f',
                plot_bgcolor='#1e1e2f',
                font=dict(color='#ffffff'),
                margin=dict(t=40, b=40, l=40, r=40),
                title=dict(text="Radar Chart Karakteristik Gaya Hidup", x=0.5, font=dict(size=16))
            )
            st.plotly_chart(fig_radar, use_container_width=True)
            
        with v_col2:
            # 2. Bar Chart Plotly (Tema Dark)
            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(
                x=labels,
                y=values,
                marker=dict(
                    color=values,
                    colorscale='Cividis',
                    line=dict(color='#182848', width=1)
                )
            ))
            fig_bar.update_layout(
                paper_bgcolor='#1e1e2f',
                plot_bgcolor='#1e1e2f',
                font=dict(color='#ffffff'),
                xaxis=dict(gridcolor='#44445c', tickangle=-25),
                yaxis=dict(gridcolor='#44445c'),
                margin=dict(t=40, b=40, l=40, r=40),
                title=dict(text="Bar Chart Distribusi Nilai Fitur", x=0.5, font=dict(size=16))
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        # =====================================================
        # FITUR BARU 3: INSIGHT HASIL PREDIKSI (OTOMATIS BERDASARKAN ATURAN)
        # =====================================================
        st.markdown("---")
        st.markdown("### 💡 Insight Hasil Prediksi")
        
        insights = []
        if lp["screen"] > 8:
            insights.append("📱 **Screen time yang tinggi** dapat meningkatkan risiko kelelahan mental.")
        if lp["sleep"] < 7:
            insights.append("🛌 **Durasi tidur** masih kurang dari rekomendasi ideal (7-8 jam).")
        if lp["quality"] < 60:
            insights.append("📉 **Kualitas tidur** Anda tergolong rendah, tubuh kurang beristirahat sempurna.")
        if lp["fatigue"] > 70:
            insights.append("🧠 **Tingkat kelelahan mental** Anda saat ini cukup tinggi.")
        if lp["physical"] < 45:
            insights.append("🏃‍♂️ **Aktivitas fisik** masih rendah. Tubuh membutuhkan stimulasi endorfin.")
        if lp["notif"] > 100:
            insights.append("🔔 **Jumlah notifikasi yang tinggi** berpotensi besar mengganggu fokus dan ketenangan.")
        if lp["phone"] > 45:
            insights.append("🌙 **Penggunaan HP sebelum tidur** cukup tinggi, mengganggu sekresi melatonin.")
            
        if insights:
            # Tampilan dalam komponen bergaya card dark-mode
            insight_html = "".join([f"<li style='margin-bottom:10px;'>{ins}</li>" for ins in insights])
            st.markdown(f"""
                <div class="stressio-card">
                    <h4 style="color:#4b6cb7; margin-top:0;">🔍 Temuan Kunci Analisis:</h4>
                    <ul style="padding-left:20px; margin-bottom:0;">
                        {insight_html}
                    </ul>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.info("✅ Gaya hidup Anda ideal secara metrik harian. Tidak ditemukan parameter kritis!")

        # =====================================================
        # FITUR BARU 4: REKOMENDASI BERDASARKAN KATEGORI
        # =====================================================
        st.markdown("---")
        st.markdown("### 🎯 Rekomendasi Pemulihan")
        
        if kategori_murni == "Rendah":
            st.markdown("""
                <div class="stressio-card" style="border-left: 6px solid #28a745;">
                    <h4 style="color:#28a745; margin-top:0;">😊 Kategori Stres: RENDAH</h4>
                    <p>Pertahankan ritme harian Anda dengan langkah berikut:</p>
                    <ul>
                        <li>✨ Pertahankan pola tidur sehat yang sudah berjalan.</li>
                        <li>🏋️ Tetap rutin berolahraga untuk menjaga kebugaran sel tubuh.</li>
                        <li>🛑 Batasi screen time agar terhindar dari kelelahan mata mendadak.</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
            
        elif kategori_murni == "Sedang":
            st.markdown("""
                <div class="stressio-card" style="border-left: 6px solid #ffc107;">
                    <h4 style="color:#ffc107; margin-top:0;">😐 Kategori Stres: SEDANG</h4>
                    <p>Segera lakukan penyesuaian kecil sebelum kelelahan menumpuk:</p>
                    <ul>
                        <li>📉 Kurangi screen time secara sadar di sela aktivitas pekerjaan.</li>
                        <li>🛌 Upayakan tidur minimal 7 jam pada malam hari ini.</li>
                        <li>🧘 Luangkan waktu 10-15 menit khusus untuk relaksasi atau pernapasan dalam.</li>
                        <li>📴 Kurangi penggunaan HP minimal 30 menit sebelum tidur.</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
            
        else:  # Tinggi
            st.markdown("""
                <div class="stressio-card" style="border-left: 6px solid #dc3545;">
                    <h4 style="color:#dc3545; margin-top:0;">😟 Kategori Stres: TINGGI</h4>
                    <p>Tubuh Anda memberikan sinyal darurat. Lakukan tindakan segera:</p>
                    <ul>
                        <li>🛑 <b>Tingkatkan kualitas tidur:</b> Pastikan kamar gelap dan tenang.</li>
                        <li>📉 Kurangi screen time secara bertahap dan buat batasan ketat.</li>
                        <li>🔕 Batasi atau senapkan (mute) notifikasi aplikasi yang tidak mendesak.</li>
                        <li>🏃‍♂️ Lakukan aktivitas fisik ringan/peregangan minimal 30 menit demi sirkulasi darah.</li>
                        <li>💼 Luangkan waktu penuh untuk beristirahat dan putuskan koneksi dari pekerjaan sejenak.</li>
                        <li>🩺 <i>Jika kondisi ini berlangsung lama atau memburuk, sangat dianjurkan berkonsultasi dengan tenaga profesional kesehatan mental.</i></li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)

        # =====================================================
        # FITUR BARU 1 (LANJUTAN): TABEL RIWAYAT PREDIKSI
        # =====================================================
        st.markdown("---")
        st.markdown("### 📜 Riwayat Prediksi Pengguna")
        
        if st.session_state.prediction_history:
            df_history = pd.DataFrame(st.session_state.prediction_history)
            st.dataframe(df_history, use_container_width=True, hide_index=True)
            
            # Tombol untuk mengosongkan riwayat prediksi
            if st.button("🗑️ Hapus Riwayat", type="secondary"):
                st.session_state.prediction_history = []
                st.rerun()
        else:
            st.info("Belum ada riwayat pemeriksaan. Silakan tekan tombol analisis di atas.")

# =====================================================
# TAB 2: CEK RASIO DIGITAL (KALKULATOR)
# =====================================================
with tab2:
    st.subheader("🔍 Kalkulator Rasio Gawai vs Tidur")
    # Menggunakan session state jika sudah ada input agar nilainya sinkron
    s_time = st.session_state["last_pred"]["screen"] if "last_pred" in st.session_state else screen
    sl_time = st.session_state["last_pred"]["sleep"] if "last_pred" in st.session_state else sleep
    
    current_ratio = s_time / sl_time if sl_time > 0 else 0
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
