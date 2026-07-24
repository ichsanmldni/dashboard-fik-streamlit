"""
Generator data simulasi mahasiswa FIK.

Dipakai untuk mengisi dashboard sebelum data asli dari Dikjar tersedia.
Jalankan: python generate_data.py
Hasil: data_mahasiswa.csv
"""

from pathlib import Path

import numpy as np
import pandas as pd

SEED = 7

PRODI = {
    "S1 Informatika": {"kode": "01", "porsi": 0.36, "geser_ipk": 0.00},
    "S1 Sistem Informasi": {"kode": "02", "porsi": 0.32, "geser_ipk": 0.06},
    "S1 Sains Data": {"kode": "03", "porsi": 0.18, "geser_ipk": 0.10},
    "D3 Sistem Informasi": {"kode": "04", "porsi": 0.14, "geser_ipk": -0.02},
}

# angkatan -> semester berjalan (asumsi TA 2026/2027 ganjil)
ANGKATAN = {2022: 9, 2023: 7, 2024: 5, 2025: 3}

# golongan UKT -> nominal per semester (rupiah)
GOLONGAN_UKT = {
    1: 500_000,
    2: 1_000_000,
    3: 2_400_000,
    4: 3_500_000,
    5: 4_600_000,
    6: 5_800_000,
    7: 7_000_000,
    8: 8_500_000,
}
PELUANG_GOLONGAN = [0.05, 0.08, 0.16, 0.20, 0.19, 0.15, 0.11, 0.06]

DEPAN_L = [
    "Ahmad", "Aditya", "Bagas", "Bayu", "Dimas", "Fajar", "Gilang", "Ilham",
    "Joko", "Lutfi", "Naufal", "Rizky", "Satrio", "Taufik", "Umar", "Wahyu",
    "Yusuf", "Bimo", "Dandi", "Fikri", "Reza", "Andre", "Hafiz", "Galih",
]
DEPAN_P = [
    "Citra", "Dewi", "Farah", "Hana", "Indah", "Kartika", "Maya", "Nadia",
    "Oktavia", "Putri", "Rani", "Sinta", "Tiara", "Vina", "Zahra", "Andini",
    "Cahaya", "Elsa", "Gita", "Salsabila", "Ayu", "Melati", "Anisa", "Laras",
]
BELAKANG = [
    "Pratama", "Wijaya", "Nugroho", "Santoso", "Maulana", "Ramadhan", "Kusuma",
    "Hidayat", "Setiawan", "Anggraini", "Permata", "Saputra", "Rahmawati",
    "Lestari", "Firmansyah", "Halim", "Syahputra", "Wibowo", "Utami", "Hakim",
]
DOSEN_PA = [
    "Dr. Arief Rahman", "Dr. Sri Wahyuni", "Ir. Bambang Setyo, M.Kom",
    "Dwi Handayani, M.Kom", "Rizal Fadhillah, M.T", "Nur Aisyah, M.Sc",
    "Hendra Gunawan, M.Kom", "Yuni Kartika, M.T",
]


def buat_data_simulasi(jumlah: int = 900, seed: int = SEED) -> pd.DataFrame:
    """Bikin DataFrame mahasiswa simulasi yang polanya masuk akal.

    Sengaja dibuat berkorelasi: kehadiran rendah -> IPK rendah -> risiko
    menunggak UKT lebih besar, supaya grafiknya punya cerita saat didemokan.
    """
    rng = np.random.default_rng(seed)

    nama_prodi = list(PRODI)
    porsi = [PRODI[p]["porsi"] for p in nama_prodi]
    prodi = rng.choice(nama_prodi, size=jumlah, p=porsi)
    angkatan = rng.choice(list(ANGKATAN), size=jumlah, p=[0.22, 0.25, 0.26, 0.27])

    geser = np.array([PRODI[p]["geser_ipk"] for p in prodi])
    ipk = np.clip(rng.normal(3.18, 0.44, jumlah) + geser, 1.40, 4.00).round(2)

    kehadiran = np.clip(
        82 + 13 * (ipk - 3.2) + rng.normal(0, 6, jumlah), 38, 100
    ).round(1)

    semester = np.array([ANGKATAN[a] for a in angkatan])
    sks_lulus = np.clip(
        ((semester - 1) * 20 * (0.75 + 0.25 * (ipk / 4)) + rng.normal(0, 6, jumlah)),
        0, 148,
    ).round().astype(int)

    # --- status akademik -------------------------------------------------
    status = np.full(jumlah, "Aktif", dtype=object)
    undian = rng.random(jumlah)
    status[(undian < 0.035)] = "Cuti"
    status[(undian >= 0.035) & (undian < 0.075)] = "Non-Aktif"
    # angkatan 2022 dengan IPK bagus + SKS cukup: sebagian sudah lulus
    calon_lulus = (angkatan == 2022) & (ipk >= 2.9) & (sks_lulus >= 120)
    status[calon_lulus & (rng.random(jumlah) < 0.55)] = "Lulus"
    # yang IPK-nya sangat rendah dan jarang hadir cenderung mangkir
    status[(ipk < 2.0) & (kehadiran < 60) & (rng.random(jumlah) < 0.5)] = "Non-Aktif"

    # --- UKT --------------------------------------------------------------
    golongan = rng.choice(list(GOLONGAN_UKT), size=jumlah, p=PELUANG_GOLONGAN)
    nominal = np.array([GOLONGAN_UKT[g] for g in golongan])

    peluang_nunggak = np.clip(
        0.04 + 0.022 * golongan + 0.25 * (kehadiran < 70) + 0.10 * (ipk < 2.5),
        0, 0.85,
    )
    nunggak = rng.random(jumlah) < peluang_nunggak
    nunggak[status == "Lulus"] = False
    nunggak[status == "Non-Aktif"] = True  # non-aktif hampir selalu ada tunggakan

    kelipatan = rng.choice([0.5, 1.0, 1.5, 2.0], size=jumlah, p=[0.34, 0.4, 0.16, 0.10])
    tunggakan = np.where(nunggak, (nominal * kelipatan).round(-3), 0).astype(int)

    status_bayar = np.where(
        tunggakan == 0, "Lunas",
        np.where(tunggakan < nominal, "Cicilan", "Menunggak"),
    )

    # --- identitas --------------------------------------------------------
    jenis_kelamin = rng.choice(["L", "P"], size=jumlah, p=[0.58, 0.42])
    nama = [
        f"{rng.choice(DEPAN_L if jk == 'L' else DEPAN_P)} {rng.choice(BELAKANG)}"
        for jk in jenis_kelamin
    ]
    urut = {}
    nim = []
    for a, p in zip(angkatan, prodi):
        kunci = (a, p)
        urut[kunci] = urut.get(kunci, 0) + 1
        nim.append(f"{str(a)[2:]}{PRODI[p]['kode']}{urut[kunci]:04d}")

    df = pd.DataFrame(
        {
            "nim": nim,
            "nama": nama,
            "jenis_kelamin": jenis_kelamin,
            "program_studi": prodi,
            "angkatan": angkatan,
            "semester": semester,
            "status_akademik": status,
            "ipk": ipk,
            "sks_lulus": sks_lulus,
            "kehadiran_persen": kehadiran,
            "golongan_ukt": golongan,
            "nominal_ukt": nominal,
            "tunggakan_ukt": tunggakan,
            "status_pembayaran": status_bayar,
            "dosen_pa": rng.choice(DOSEN_PA, size=jumlah),
        }
    )
    return df.sort_values(["angkatan", "program_studi", "nim"]).reset_index(drop=True)


if __name__ == "__main__":
    berkas = Path(__file__).with_name("data_mahasiswa.csv")
    data = buat_data_simulasi()
    data.to_csv(berkas, index=False)
    print(f"{len(data)} baris data simulasi tersimpan di {berkas}")
