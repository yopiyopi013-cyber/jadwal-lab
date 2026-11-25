import streamlit as st
import datetime
import pandas as pd
import requests
import time

st.set_page_config(page_title="Booking Lab Komputer 4 IBM", page_icon="💻", layout="wide")
PASSWORD_ADMIN = "admin123"
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz5Fvgn134jxIHddk8AfMKjgj_-SouPQfyHmKT709_RWOiLUgca3mxepqXYv3iLqwZwqA/exec"

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

def load_data():
    try:
        r = requests.get(SCRIPT_URL, timeout=10)
        data = r.json()
        out = []
        for b in data:
            out.append({"Tanggal": int(b.get("Tanggal", 0)), "Hari": b.get("Hari",""), "Jam": b.get("Jam",""), "Waktu": b.get("Waktu",""), "Kelas": b.get("Kelas",""), "Pelajaran": b.get("Pelajaran",""), "Guru": b.get("Guru",""), "Materi": b.get("Materi",""), "_row": b.get("_row", 0)})
        return out
    except:
        return []

booking = load_data()

st.markdown("### 📝 FORM BOOKING - GURU ISI DI SINI")
with st.form("form_booking", clear_on_submit=True):
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
        elif not kelas or not guru or not pelajaran:
            st.warning("Kelas, Pelajaran, dan Guru wajib diisi!")
        else:
            bentrok = [b for b in booking if b["Tanggal"]==tanggal and b["Jam"]==jam_pilih]
            if bentrok:
                st.error(f"❌ SUDAH DIBOOKING! Tanggal {tanggal} {jam_pilih} sudah dipakai kelas {bentrok[0]['Kelas']} oleh {bentrok[0]['Guru']}.")
            else:
                try:
                    requests.post(SCRIPT_URL, json={"action":"add","Tanggal":tanggal,"Hari":hari,"Jam":jam_pilih,"Waktu":waktu,"Kelas":kelas,"Pelajaran":pelajaran,"Guru":guru,"Materi":materi}, timeout=10)
                    st.success(f"✅ Berhasil! {kelas} tanggal {tanggal} Desember {jam_pilih} sudah dibooking dan tersimpan permanen.")
                    time.sleep(1)
                    st.rerun()
                except:
                    st.error("Gagal simpan, coba lagi.")

st.markdown("---")
st.markdown("### 📋 JADWAL YANG SUDAH DIBOOKING")
cari = st.text_input("🔍 Cari Kelas / Guru / Pelajaran...", "")
if len(booking) == 0:
    st.info("📭 Jadwal masih KOSONG. Belum ada yang booking.")
else:
    df = pd.DataFrame(booking).sort_values(["Tanggal", "Jam"])
    if cari:
        df = df[df.apply(lambda r: cari.lower() in str(r.values).lower(), axis=1)]
    df_tampil = df.copy()
    df_tampil["Tanggal"] = df_tampil["Tanggal"].apply(lambda x: f"{x} Desember 2026")
    df_tampil["Status"] = "✅ TERISI"
    st.dataframe(df_tampil[["Tanggal","Hari","Jam","Waktu","Kelas","Pelajaran","Guru","Materi","Status"]], use_container_width=True, hide_index=True)

st.markdown("---")
st.markdown("### 🔐 HAPUS BOOKING - KHUSUS ADMIN (PEMBATALAN)")
if len(booking) == 0:
    st.write("Tidak ada jadwal untuk dihapus.")
else:
    pilihan_list = [f"{b['Tanggal']} Des - {b['Jam']} - {b['Kelas']} - {b['Pelajaran']} - {b['Guru']}" for b in booking]
    c_hapus1, c_hapus2, c_hapus3 = st.columns([3, 2, 1])
    with c_hapus1:
        pilih_hapus = st.selectbox("Pilih jadwal yang mau dibatalkan:", pilihan_list)
    with c_hapus2:
        pw = st.text_input("Password Admin", type="password", placeholder="Masukkan password admin")
    with c_hapus3:
        st.write("")
        st.write("")
        tombol_hapus = st.button("🗑️ HAPUS", type="primary")
    if tombol_hapus:
        if pw != PASSWORD_ADMIN:
            st.error("❌ Password salah! Hanya admin yang bisa menghapus.")
        else:
            idx = pilihan_list.index(pilih_hapus)
            hapus_data = booking[idx]
            requests.post(SCRIPT_URL, json={"action":"delete","row":hapus_data["_row"]}, timeout=10)
            st.success(f"✅ Berhasil dibatalkan: {hapus_data['Kelas']} tanggal {hapus_data['Tanggal']} {hapus_data['Jam']}")
            time.sleep(1)
            st.rerun()
