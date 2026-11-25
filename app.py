import streamlit as st
import datetime
import pandas as pd

st.set_page_config(page_title="Booking Lab Komputer 4 IBM", page_icon="💻", layout="wide")

st.markdown("""
<style>
  .header { background:linear-gradient(135deg,#667eea,#764ba2); color:white; padding:25px; border-radius:15px; text-align:center; }
  .libur { background:#ffe0e0; color:red; font-weight:bold; text-align:center; padding:10px; border-radius:10px; }
</style>
<div class="header"><h1>💻 JADWAL BOOKING LAB KOMPUTER 4 IBM</h1><p>SMA PUTRA • DESEMBER 2026 • JUMAT LIBUR • MINGGU MASUK</p></div>
""", unsafe_allow_html=True)

JAM_LIST = [
    ("Jam ke-1", "07.00 - 07.40"), ("Jam ke-2", "07.40 - 08.20"),
    ("Jam ke-3", "08.20 - 09.00"), ("Jam ke-4", "09.00 - 09.40"),
    ("Jam ke-5", "10.10 - 10.50"), ("Jam ke-6", "10.50 - 11.30"),
    ("Jam ke-7", "11.30 - 12.10"), ("Jam ke-8", "13.40 - 14.20"),
    ("Jam ke-9", "14.20 - 15.00"),
]
HARI_ID = ["Senin","Selasa","Rabu","Kamis","Jumat","Sabtu","Minggu"]

if "booking" not in st.session_state:
    st.session_state.booking = [
        {"Tanggal": 1, "Hari": "Selasa", "Jam": "Jam ke-1", "Waktu": "07.00 - 07.40", "Kelas": "X-1", "Pelajaran": "Informatika", "Guru": "Bpk. Ahmad", "Materi": "Pengenalan Lab"},
    ]

st.markdown("### 📝 FORM BOOKING - GURU ISI DI SINI")
with st.form("form_booking"):
    c1, c2, c3 = st.columns(3)
    with c1:
        tanggal = st.selectbox("📅 Tanggal", list(range(1, 32)), format_func=lambda x: f"{x} Desember 2026 - {HARI_ID[datetime.date(2026,12,x).weekday()]}")
        hari = HARI_ID[datetime.date(2026,12,tanggal).weekday()]
        kelas = st.text_input("🏫 Kelas", placeholder="Contoh: X-1")
    with c2:
        jam_pilih = st.selectbox("🕐 Jam Ke", [j[0] for j in JAM_LIST])
        waktu = dict(JAM_LIST)[jam_pilih]
        pelajaran = st.text_input("📚 Pelajaran", placeholder="Contoh: Informatika")
    with c3:
        guru = st.text_input("👨‍🏫 Nama Guru", placeholder="Contoh: Bpk. Ahmad")
        materi = st.text_input("📝 Materi", placeholder="Contoh: Microsoft Word")
    if hari == "Jumat":
        st.markdown('<div class="libur">🕌 HARI JUMAT LIBUR - TIDAK BISA BOOKING</div>', unsafe_allow_html=True)
    tombol = st.form_submit_button("✅ SIMPAN BOOKING", use_container_width=True)
    if tombol:
        if hari == "Jumat":
            st.error("Maaf, Hari Jumat Libur!")
        elif not kelas or not guru:
            st.warning("Kelas dan Guru wajib diisi!")
        else:
            bentrok = [b for b in st.session_state.booking if b["Tanggal"]==tanggal and b["Jam"]==jam_pilih]
            if bentrok:
                st.error(f"❌ SUDAH DIBOOKING! Tanggal {tanggal} {jam_pilih} sudah dipakai kelas {bentrok[0]['Kelas']} oleh {bentrok[0]['Guru']}.")
            else:
                st.session_state.booking.append({"Tanggal": tanggal, "Hari": hari, "Jam": jam_pilih, "Waktu": waktu, "Kelas": kelas, "Pelajaran": pelajaran, "Guru": guru, "Materi": materi})
                st.success(f"✅ Berhasil! {kelas} tanggal {tanggal} Desember {jam_pilih} sudah dibooking.")

st.markdown("---")
st.markdown("### 📋 JADWAL YANG SUDAH DIBOOKING")
cari = st.text_input("🔍 Cari Kelas / Guru / Pelajaran...", "")
df = pd.DataFrame(st.session_state.booking).sort_values(["Tanggal", "Jam"]) if st.session_state.booking else pd.DataFrame(columns=["Tanggal","Hari","Jam","Waktu","Kelas","Pelajaran","Guru","Materi"])
if cari:
    df = df[df.apply(lambda r: cari.lower() in str(r.values).lower(), axis=1)]
if len(df) > 0:
    df_tampil = df.copy()
    df_tampil["Tanggal"] = df_tampil["Tanggal"].apply(lambda x: f"{x} Desember 2026")
    st.dataframe(df_tampil, use_container_width=True, hide_index=True)
else:
    st.info("Belum ada booking.")
