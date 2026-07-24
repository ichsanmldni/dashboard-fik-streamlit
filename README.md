# Dashboard BI Akademik FIK — Prototipe Streamlit

Prototipe dashboard Business Intelligence untuk data mahasiswa FIK:
status akademik, IPK, tunggakan UKT, dan tingkat kehadiran.
**Semua data di dalamnya masih simulasi**, bukan data mahasiswa asli.

---

## 1. Apa itu Streamlit (versi singkat)

Streamlit adalah library Python untuk membuat aplikasi web tanpa perlu menulis
HTML, CSS, atau JavaScript. Kita menulis skrip Python biasa, lalu setiap
`st.…` berubah jadi elemen di halaman web:

```python
import streamlit as st
st.title("Halo FIK")            # judul
st.metric("Rata-rata IPK", 3.21)  # kartu KPI
st.plotly_chart(fig)              # grafik interaktif
st.dataframe(df)                  # tabel
```

Cara kerjanya: setiap kali pengguna menggerakkan filter, Streamlit menjalankan
ulang seluruh skrip dari atas ke bawah, lalu menggambar ulang halamannya.
Itu sebabnya kodenya tetap sederhana — tidak ada state management seperti di
React.

Perbandingan cepat: kalau Power BI / Tableau itu tools klik-dan-tarik,
Streamlit itu "dashboard-as-code" — gratis, open source, dan bebas
dikustomisasi karena semuanya Python.

---

## 2. Isi folder

| Berkas | Fungsi |
|---|---|
| `app.py` | Aplikasi dashboard-nya (file utama) |
| `generate_data.py` | Pembuat data simulasi 900 mahasiswa |
| `data_mahasiswa.csv` | Data simulasi yang dipakai dashboard |
| `requirements.txt` | Daftar library yang perlu di-install |
| `.streamlit/config.toml` | Tema warna (folder ini diawali titik, jadi mungkin tersembunyi) |

---

## 3. Cara menjalankan di laptop

Butuh Python 3.9+ terpasang.

```bash
cd dashboard-fik

# (disarankan) bikin virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
streamlit run app.py
```

Browser otomatis terbuka di `http://localhost:8501`. Setiap kali `app.py`
disimpan, cukup klik **Rerun** di pojok kanan atas — tidak perlu restart.

Mau data simulasi yang berbeda? Jalankan `python generate_data.py`.

---

## 4. Mengganti data simulasi dengan data asli

Cukup ubah fungsi `muat_data()` di `app.py`. Selama nama kolomnya sama,
seluruh grafik ikut menyesuaikan sendiri.

Kolom yang dipakai: `nim, nama, jenis_kelamin, program_studi, angkatan,
semester, status_akademik, ipk, sks_lulus, kehadiran_persen, golongan_ukt,
nominal_ukt, tunggakan_ukt, status_pembayaran, dosen_pa`.

**Dari Excel kiriman Dikjar:**

```python
df = pd.read_excel("data_dikjar.xlsx", sheet_name="Mahasiswa")
```

**Langsung dari database SIAKAD (paling ideal untuk jangka panjang):**

```python
conn = st.connection("siakad", type="sql")   # kredensial di .streamlit/secrets.toml
df = conn.query("SELECT * FROM v_dashboard_mahasiswa", ttl="30m")
```

Catatan: `@st.cache_data` di atas fungsi itu yang bikin query tidak diulang
setiap kali filter digeser. Untuk data harian, cukup pakai `ttl`.

---

## 5. Deploy ke streamlit.app (Streamlit Community Cloud)

1. Push folder ini ke repository GitHub (boleh private).
2. Buka <https://share.streamlit.io>, login pakai akun GitHub.
3. Klik **New app** → pilih repo, branch, dan isi main file: `app.py`.
4. Tunggu ±2 menit, aplikasi dapat URL publik `nama-app.streamlit.app`.

Yang perlu diperhatikan:

- Gratis, tapi resource-nya terbatas (± 1 GB RAM per app) dan app "tidur"
  kalau lama tidak dibuka — cukup untuk demo, bukan untuk produksi fakultas.
- **Jangan pernah meng-upload data mahasiswa asli ke sini.** UKT, IPK, dan
  identitas mahasiswa itu data pribadi (UU PDP). Untuk data asli, pasang
  Streamlit di server kampus sendiri (`streamlit run` di balik Nginx, atau
  Docker) supaya tetap di dalam jaringan internal dan bisa dikasih login SSO.

---

## 6. Bahan diskusi sore

**Kelebihan Streamlit untuk kasus kita**
- Prototipe jadi dalam hitungan jam, bukan minggu — bagus untuk cari bentuk
  dashboard yang benar-benar dipakai pimpinan sebelum dibangun serius.
- Gratis dan open source, tidak ada biaya lisensi per user seperti Power BI.
- Karena Python, nanti gampang disambung ke analitik lanjutan (prediksi
  mahasiswa berpotensi DO, segmentasi penunggak UKT).

**Keterbatasan yang perlu dijawab sebelum dipakai luas**
- Tidak ada sistem login/hak akses bawaan. Perlu tambahan (SSO kampus,
  `streamlit-authenticator`, atau reverse proxy) supaya Kaprodi hanya melihat
  data prodinya sendiri.
- Bukan alat self-service. Kalau pimpinan ingin bikin grafik sendiri, itu
  wilayah Power BI/Metabase; di Streamlit setiap perubahan lewat kode.
- Performa turun kalau data ratusan ribu baris ditarik mentah-mentah — solusinya
  agregasi di sisi database atau data warehouse kecil.

**Usulan langkah berikutnya**
1. Sepakati dulu daftar KPI dan siapa penggunanya (Dekan / Kaprodi / dosen PA).
2. Minta 1 tarikan data nyata (boleh dianonimkan) dari Dikjar untuk validasi
   struktur kolom.
3. Sepakati sumber data resmi: ekspor berkala dari SIAKAD, atau akses
   read-only ke view database.
4. Tentukan hosting: server kampus untuk data asli, streamlit.app hanya
   untuk demo dengan data dummy.
