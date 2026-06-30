import streamlit as st
import pandas as pd
import joblib
from datetime import datetime
import plotly.graph_objects as object_plotly
import plotly.express as px

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
# Inisialisasi Session State (FITUR BARU 1)
# =====================================================
# Digunakan untuk menyimpan riwayat prediksi tanpa database
if "riwayat_prediksi" not in st.session_state:
    st.session_state.riwayat_prediksi = []

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

    # Penentuan Kategori
    if pred < 4:
        kategori = "Rendah"
        st.success(f"Kategori Stress : **{kategori}** 😊")
    elif pred < 7:
        kategori = "Sedang"
        st.warning(f"Kategori Stress : **{kategori}** 😐")
    else:
        kategori = "Tinggi"
        st.error(f"Kategori Stress : **{kategori}** 😟")

    # FITUR BARU 1: Menyimpan ke Riwayat Prediksi
    waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_riwayat = {
        "Waktu": waktu_sekarang,
        "Age": age,
        "Screen Time": screen,
        "Sleep Duration": sleep,
        "Sleep Quality": quality,
        "Mental Fatigue": fatigue,
        "Prediksi Stress": round(pred, 2),
        "Kategori": kategori
    }
    st.session_state.riwayat_prediksi.append(data_riwayat)

    st.write("### Data yang Dimasukkan")

    tampil = data.copy()
    tampil["gender"] = gender_map[gender]
    tampil["occupation"] = occupation_map[occupation]

    st.dataframe(
        tampil,
        use_container_width=True
    )

    # =====================================================
    # FITUR BARU 2: Visualisasi Input User (Plotly)
    # =====================================================
    st.divider()
    st.subheader("📈 Visualisasi Faktor Input")

    # Menyiapkan data untuk grafik
    fitur_visual = [
        "Screen Time (Jam)", "Phone Before Sleep (Min)", "Sleep Duration (Jam)",
        "Sleep Quality", "Caffeine (Cups)", "Physical Act. (Min)", 
        "Notifications", "Mental Fatigue"
    ]
    nilai_visual = [screen, phone, sleep, quality, coffee, physical, notif, fatigue]

    # Grafik 1: Radar Chart
    fig_radar = object_plotly.Figure()
    fig_radar.add_trace(object_plotly.Scatterpolar(
        r=nilai_visual,
        theta=fitur_visual,
        fill='toself',
        name='Nilai Input',
        marker=dict(color='#8884d8')
    ))
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, showticklabels=False),
            gridshape='circular'
        ),
        template="plotly_dark",
        title="Radar Chart Distribusi Faktor Risiko",
        height=400
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    # Grafik 2: Bar Chart Sederhana
    df_bar = pd.DataFrame({"Fitur": fitur_visual, "Nilai": nilai_visual})
    fig_bar = px.bar(
        df_bar, 
        x="Fitur", 
        y="Nilai", 
        color="Nilai",
        color_continuous_scale="Purples",
        template="plotly_dark",
        title="Perbandingan Nilai Faktor Secara Linear"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # =====================================================
    # FITUR BARU 3: Insight Hasil Prediksi
    # =====================================================
    st.divider()
    st.subheader("💡 Insight Hasil Prediksi")
    
    insights = []
    
    if screen > 8:
        insights.append("• **Screen time yang tinggi** dapat meningkatkan risiko kelelahan mental.")
    if sleep < 7:
        insights.append("• **Durasi tidur** masih kurang dari rekomendasi medis (minimal 7 jam).")
    if quality < 60:
        insights.append("• **Kualitas tidur** Anda tergolong rendah, cobalah kurangi distraksi malam.")
    if fatigue > 70:
        insights.append("• **Tingkat kelelahan mental** Anda tergolong cukup tinggi saat ini.")
    if physical < 45:
        insights.append("• **Aktivitas fisik** Anda masih rendah. Tubuh yang aktif membantu mereduksi stres.")
    if notif > 100:
        insights.append("• **Jumlah notifikasi yang tinggi** yang masuk berisiko mengganggu fokus dan ketenangan.")
    if phone > 45:
        insights.append("• **Penggunaan HP sebelum tidur** cukup tinggi, mengganggu sekresi melatonin.")

    if insights:
        # Menampilkan kumpulan insight dalam satu box info bermotif gelap/biru
        st.info("\n".join(insights))
    else:
        st.success("✨ Faktor kebiasaan harian Anda secara umum terpantau berada di batas aman.")

    # =====================================================
    # FITUR BARU 4: Rekomendasi Berdasarkan Hasil Kategori
    # =====================================================
    st.subheader("🌱 Rekomendasi Tindakan")
    
    if kategori == "Rendah":
        st.markdown("""
        <div style="background-color: #1e293b; padding: 20px; border-radius: 10px; border-left: 5px solid #22c55e;">
            <h4 style="margin-top:0; color:#22c55e;">🟢 Pola Hidup Sehat Terjaga</h4>
            <ul>
                <li>Pertahankan pola tidur yang teratur.</li>
                <li>Tetap rutin berolahraga setiap pekan.</li>
                <li>Batasi screen time agar tetap proporsional.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    elif kategori == "Sedang":
        st.markdown("""
        <div style="background-color: #1e293b; padding: 20px; border-radius: 10px; border-left: 5px solid #eab308;">
            <h4 style="margin-top:0; color:#eab308;">🟡 Perlu Penyesuaian Ringan</h4>
            <ul>
                <li>Kurangi penggunaan screen time harian Anda secara bertahap.</li>
                <li>Usahakan untuk tidur minimal 7 jam per malam.</li>
                <li>Luangkan waktu sejenak di sela kesibukan untuk relaksasi.</li>
                <li>Kurangi penggunaan HP minimal 30-45 menit sebelum tidur.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    else: # Kategori Tinggi
        st.markdown("""
        <div style="background-color: #1e293b; padding: 20px; border-radius: 10px; border-left: 5px solid #ef4444;">
            <h4 style="margin-top:0; color:#ef4444;">🔴 Perhatian Khusus Diperlukan</h4>
            <ul>
                <li>Prioritaskan tindakan untuk meningkatkan kualitas tidur Anda.</li>
                <li>Kurangi screen time harian Anda secara signifikan.</li>
                <li>Batasi atau matikan notifikasi aplikasi yang tidak penting (Do Not Disturb).</li>
                <li>Lakukan aktivitas fisik ringan minimal 30 menit demi melepas ketegangan saraf.</li>
                <li>Luangkan waktu penuh untuk istirahat total dari pekerjaan/studi.</li>
                <li><i>Jika kondisi ini terus berlangsung lama dan mengganggu fungsi harian, pertimbangkan berkonsultasi dengan tenaga profesional atau psikolog.</i></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# =====================================================
# Tampilan Tabel Riwayat Prediksi (Berada di Luar Blok Tombol Prediksi agar Permanen)
# =====================================================
st.divider()
st.subheader("📜 Tabel Riwayat Prediksi")

if st.session_state.riwayat_prediksi:
    # Mengubah list dictionary riwayat menjadi DataFrame
    df_riwayat = pd.DataFrame(st.session_state.riwayat_prediksi)
    
    # Menampilkan tabel dengan urutan terbaru di atas
    st.dataframe(df_riwayat.iloc[::-1], use_container_width=True, hide_index=True)
    
    # Tombol Aksi Hapus Riwayat
    if st.button("🗑️ Hapus Riwayat", type="secondary"):
        st.session_state.riwayat_prediksi = []
        st.rerun()
else:
    st.caption("Belum ada riwayat prediksi dalam sesi ini.")
