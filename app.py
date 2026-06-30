import streamlit as st
import pandas as pd
import joblib
from datetime import datetime
import io
import plotly.graph_objects as go
from fpdf import FPDF  # Mengganti weasyprint dengan fpdf2

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
# INSIALISASI SESSION STATE (FITUR RIWAYAT)
# =====================================================
if "riwayat_prediksi" not in st.session_state:
    st.session_state.riwayat_prediksi = []

# =====================================================
# Konfigurasi Halaman & Custom CSS
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
    .stressio-card {
        background-color: #1e1e2f;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #2d2d44;
        margin-bottom: 15px;
    }
    .stressio-header {
        color: #4b6cb7;
        font-weight: bold;
        margin-bottom: 10px;
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

    output_container = st.container()

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

        with output_container:
            st.container(border=True)
            st.markdown("### 📊 Hasil Analisis Tingkat Stres")
            
            if pred < 4.0:
                kategori = "Rendah 😊"
                warna_box = st.success
                delta_info = "Kondisi Anda aman!"
                kat_murni = "Rendah"
            elif pred < 7.0:
                kategori = "Sedang 😐"
                warna_box = st.warning
                delta_info = "Perlu waspada & relaksasi."
                kat_murni = "Sedang"
            else:
                kategori = "Tinggi 😟"
                warna_box = st.error
                delta_info = "Butuh istirahat segera!"
                kat_murni = "Tinggi"

            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.metric(label="Skor Prediksi Stres (Skala 0-10)", value=f"{pred:.2f}")
                st.progress(min(max(pred / 10.0, 0.0), 1.0))
            with res_col2:
                st.metric(label="Kategori Stres Anda", value=kategori, delta=delta_info, delta_color="off")

            warna_box(f"Berdasarkan analisis model AI, tingkat stres Anda berada di kategori **{kategori.split()[0]}**.")

            st.markdown("#### 🛠️ Rekomendasi Personalisasi:")
            saran_list = []
            
            if coffee > 4:
                msg = "Batasi Kafein: Konsumsi kafein berlebih dapat menaikkan detak jantung mendadak."
                st.warning(f"⚠️ {msg}")
                saran_list.append(msg)
            if phone > 60:
                msg = "Kurangi Screen-Time Malam: Pancaran sinar biru HP mengacaukan ritme sirkadian tubuh."
                st.warning(f"⚠️ {msg}")
                saran_list.append(msg)
            if physical < 20:
                msg = "Kurang Aktivitas Fisik: Sempatkan berolahraga ringan atau sekadar peregangan."
                st.info(f"💡 {msg}")
                saran_list.append(msg)
                
            if not saran_list:
                msg = "Pola hidup Anda saat ini sudah sangat seimbang! Pertahankan rutinitas baik ini."
                st.success(f"✅ {msg}")
                saran_list.append(msg)

            # 1. Simpan ke Riwayat State
            waktu_sekarang = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data_riwayat = {
                "Waktu": waktu_sekarang,
                "Age": age,
                "Screen Time": f"{screen} Jam",
                "Sleep Duration": f"{sleep} Jam",
                "Sleep Quality": quality,
                "Mental Fatigue": fatigue,
                "Prediksi Stress": round(pred, 2),
                "Kategori": kat_murni
            }
            st.session_state.riwayat_prediksi.append(data_riwayat)

            # 2. GENERATE PDF MENGGUNAKAN FPDF2 (Aman dari OSError)
            class DI_PDF(FPDF):
                def header(self):
                    self.set_fill_color(30, 30, 47) # Dark theme background
                    self.rect(0, 0, 210, 297, "F")
                    self.set_text_color(75, 108, 183)
                    self.set_font("Arial", "B", 18)
                    self.cell(0, 10, "OFFICIAL MEDICAL REPORT", ln=1, align="L")
                    self.set_font("Arial", "", 10)
                    self.set_text_color(160, 160, 176)
                    self.cell(0, 5, "Stress Level Analyzer & Health Dashboard", ln=1, align="L")
                    self.set_draw_color(75, 108, 183)
                    self.line(10, 28, 200, 28)
                    self.ln(8)

            pdf = DI_PDF()
            pdf.add_page()
            
            # Metadata Box
            pdf.set_fill_color(45, 45, 68)
            pdf.rect(10, 32, 190, 25, "F")
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("Arial", "", 9)
            pdf.set_xy(12, 34)
            pdf.cell(95, 6, f"Waktu Pemeriksaan: {waktu_sekarang}")
            pdf.cell(95, 6, f"Skor Prediksi Stres: {pred:.2f} / 10.00", ln=1)
            pdf.set_x(12)
            pdf.cell(95, 6, "Status Prediksi: SELESAI")
            pdf.cell(95, 6, f"Kategori Stres: {kat_murni.upper()}", ln=1)

            # Table Header
            pdf.ln(10)
            pdf.set_font("Arial", "B", 11)
            pdf.set_text_color(75, 108, 183)
            pdf.cell(0, 8, "Ringkasan Metrik Aktivitas", ln=1)
            
            pdf.set_fill_color(75, 108, 183)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("Arial", "B", 10)
            pdf.cell(110, 8, " Komponen Komparasi Kesehatan", fill=True)
            pdf.cell(80, 8, " Nilai Input Pengguna", fill=True, ln=1)
            
            # Table Content
            pdf.set_font("Arial", "", 9)
            metrics_data = [
                ("Usia / Jenis Kelamin", f"{age} Tahun / {gender_map[gender]}"),
                ("Bidang Pekerjaan", f"{occupation_map[occupation]}"),
                ("Durasi Layar harian (Screen Time)", f"{screen} Jam / Hari"),
                ("Interaksi Gawai Pra-Tidur", f"{phone} Menit"),
                ("Durasi & Kualitas Tidur", f"{sleep} Jam (Skor Kualitas: {quality}/100)"),
                ("Intake Kafein Harian", f"{coffee} Gelas / Hari"),
                ("Alokasi Aktivitas Fisik", f"{physical} Menit / Hari"),
                ("Skor Kelelahan Saraf Kognitif", f"{fatigue} / 100")
            ]
            
            toggle_bg = False
            for item, val in metrics_data:
                if toggle_bg: pdf.set_fill_color(37, 37, 56)
                else: pdf.set_fill_color(30, 30, 47)
                pdf.set_text_color(230, 230, 230)
                pdf.cell(110, 7, f" {item}", fill=True)
                pdf.cell(80, 7, f" {val}", fill=True, ln=1)
                toggle_bg = not toggle_bg

            # Recommendations
            pdf.ln(8)
            pdf.set_font("Arial", "B", 11)
            pdf.set_text_color(75, 108, 183)
            pdf.cell(0, 8, "Saran Tambahan Tim Medis AI", ln=1)
            pdf.set_font("Arial", "", 9)
            pdf.set_fill_color(37, 37, 56)
            
            for s in saran_list:
                pdf.set_text_color(220, 220, 220)
                pdf.multi_cell(0, 6, f" {s}", fill=True)
                pdf.ln(1)

            pdf_output = pdf.output()
            
            st.markdown("---")
            st.download_button(
                label="📥 Unduh Laporan Resmi Hasil Pemeriksaan (.pdf)",
                data=bytes(pdf_output),
                file_name=f"Laporan_Resmi_Stres_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

            # =====================================================
            # VISUALISASI INTERAKTIF PLOTLY
            # =====================================================
            st.markdown("### 📊 Visualisasi Profil Kesehatan Anda")
            vis_col1, vis_col2 = st.columns(2)

            features = [
                'Screen Time', 'Phone Before Sleep', 'Sleep Duration', 
                'Sleep Quality', 'Caffeine Intake', 'Physical Activity', 
                'Notifications/Day', 'Mental Fatigue'
            ]
            values_radar = [
                (screen/15)*100, (phone/180)*100, (sleep/12)*100, 
                quality, (coffee/10)*100, (physical/180)*100, 
                (notif/300)*100, fatigue
            ]
            values_original = [screen, phone, sleep, quality, coffee, physical, notif, fatigue]

            with vis_col1:
                st.markdown("<div style='text-align: center; font-weight: bold;'>Radar Chart (Skala Relatif %)</div>", unsafe_allow_html=True)
                fig_radar = go.Figure()
                fig_radar.add_trace(go.Scatterpolar(
                    r=values_radar, theta=features, fill='toself',
                    fillcolor='rgba(75, 108, 183, 0.3)', line=dict(color='#4b6cb7', width=2)
                ))
                fig_radar.update_layout(
                    polar=dict(
                        radialaxis=dict(visible=True, range=[0, 100], gridcolor="#2d2d44"),
                        angularaxis=dict(gridcolor="#2d2d44")
                    ),
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#182848'), margin=dict(l=50, r=50, t=30, b=30)
                )
                st.plotly_chart(fig_radar, use_container_width=True)

            with vis_col2:
                st.markdown("<div style='text-align: center; font-weight: bold;'>Bar Chart (Nilai Aktual Komponen)</div>", unsafe_allow_html=True)
                fig_bar = go.Figure(go.Bar(
                    x=values_original, y=features, orientation='h',
                    marker=dict(color='#4b6cb7', line=dict(color='#182848', width=1))
                ))
                fig_bar.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(gridcolor="#e0e0e0"), margin=dict(l=50, r=50, t=30, b=30)
                )
                st.plotly_chart(fig_bar, use_container_width=True)

            # =====================================================
            # WORKPLACE INSIGHT AUTOMATION
            # =====================================================
            st.markdown("### 🔍 Workplace Insight with Stressio")
            
            # Menggunakan st.container dengan border=True agar serasi dengan tema dark mode tanpa bug HTML
            with st.container(border=True):
                st.markdown("<h4 style='color: #4b6cb7; font-weight: bold; margin-bottom: 15px;'>💡 Insight Hasil Prediksi</h4>", unsafe_allow_html=True)
                
                insight_found = False
                if screen > 8:
                    st.info("📱 **Screen time** yang tinggi dapat meningkatkan risiko kelelahan mental.")
                    insight_found = True
                if sleep < 7:
                    st.warning("🛌 **Durasi tidur** masih kurang dari rekomendasi umum.")
                    insight_found = True
                if quality < 60:
                    st.error("📉 **Kualitas tidur** tergolong rendah.")
                    insight_found = True
                if fatigue > 70:
                    st.error("🧠 Tingkat **kelelahan mental** cukup tinggi.")
                    insight_found = True
                if physical < 45:
                    st.info("🏃 **Aktivitas fisik** masih rendah.")
                    insight_found = True
                if notif > 100:
                    st.warning("🔔 Jumlah **notifikasi** yang tinggi dapat mengganggu fokus.")
                    insight_found = True
                if phone > 45:
                    st.warning("🌙 Penggunaan **HP sebelum tidur** cukup tinggi.")
                    insight_found = True
                    
                if not insight_found:
                    st.success("✨ Semua komponen kebiasaan harian Anda berada di parameter ideal dan sehat!")

            # =====================================================
            # REKOMENDASI BERDASARKAN KATEGORI
            # =====================================================
            with st.container(border=True):
                st.markdown(f"<h4 style='color: #4b6cb7; font-weight: bold; margin-bottom: 15px;'>🎯 Rekomendasi Khusus (Kategori: {kat_murni})</h4>", unsafe_allow_html=True)
                
                if kat_murni == "Rendah":
                    st.markdown("""
                    * 🟢 **Pertahankan pola tidur** yang konsisten.
                    * 🟢 **Tetap rutin berolahraga** untuk menjaga kebugaran sel saraf.
                    * 🟢 **Batasi screen time** agar terhindar dari akumulasi stres mendadak.
                    """)
                elif kat_murni == "Sedang":
                    st.markdown("""
                    * 🟡 **Kurangi screen time** di sela-sela waktu istirahat kerja.
                    * 🟡 **Tidur minimal 7 jam** untuk pemulihan sistem metabolisme.
                    * 🟡 **Luangkan waktu untuk relaksasi** (mindfulness/meditasi ringan).
                    * 🟡 **Kurangi penggunaan HP sebelum tidur** demi kualitas sirkadian optimal.
                    """)
                elif kat_murni == "Tinggi":
                    st.markdown("""
                    * 🔴 **Tingkatkan kualitas tidur** dengan mematikan paparan cahaya lampu kamar.
                    * 🔴 **Kurangi screen time secara bertahap** melalui penjadwalan ketat.
                    * 🔴 **Batasi notifikasi** yang tidak penting atau gunakan profil senyap kerja.
                    * 🔴 **Lakukan aktivitas fisik minimal 30 menit** guna melepaskan endorfin.
                    * 🔴 **Luangkan waktu untuk istirahat dari pekerjaan** atau tugas akademis.
                    * ⚠️ *Jika kondisi berlangsung lama, pertimbangkan berkonsultasi dengan tenaga profesional.*
                    """)

    # =====================================================
    # TABEL RIWAYAT PENYIMPANAN DATA (SESSION STATE)
    # =====================================================
    st.markdown("---")
    st.markdown("### 📜 Riwayat Analisis Pengguna")
    
    if st.session_state.riwayat_prediksi:
        df_riwayat = pd.DataFrame(st.session_state.riwayat_prediksi)
        st.dataframe(df_riwayat, use_container_width=True)
        
        if st.button("🗑️ Hapus Riwayat", type="secondary"):
            st.session_state.riwayat_prediksi = []
            st.rerun()
    else:
        st.info("Belum ada data pemeriksaan terekam pada sesi ini.")

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
