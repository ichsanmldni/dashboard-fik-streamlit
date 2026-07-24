"""
Dashboard BI Akademik — Fakultas Ilmu Komputer
Prototipe dengan data SIMULASI. Jalankan: streamlit run app.py
"""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# ---------------------------------------------------------------- Konfigurasi Page
st.set_page_config(
    page_title="Dashboard BI Akademik FIK",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------- Palet Warna Modern & Clean
NAVY = "#0F172A"        # Slate 900
BLUE = "#1E40AF"        # Blue 800
TEAL = "#0D9488"        # Teal 600
HIJAU = "#059669"       # Emerald 600
AMBER = "#D97706"       # Amber 600
MERAH = "#E11D48"       # Rose 600
UNGU = "#6366F1"        # Indigo 500
SKY = "#0284C7"         # Sky 600

PALET = [BLUE, TEAL, UNGU, AMBER, SKY, HIJAU]

WARNA_STATUS = {
    "Aktif": HIJAU,
    "Lulus": BLUE,
    "Cuti": AMBER,
    "Non-Aktif": MERAH,
}
WARNA_BAYAR = {
    "Lunas": HIJAU,
    "Cicilan": AMBER,
    "Menunggak": MERAH,
}

BATAS_IPK_RAWAN = 2.50
BATAS_HADIR_RAWAN = 75.0

# ---------------------------------------------------------------- Custom CSS (Minimal & Professional)
st.markdown(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
      
      html, body, [class*="css"], div[data-testid="stAppViewContainer"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #1E293B;
      }
      
      /* Fix Streamlit top navbar overlap */
      header[data-testid="stHeader"] {
        background-color: transparent !important;
        z-index: 100 !important;
      }
      
      /* Main Container Padding & Spacing */
      .block-container {
        padding-top: 4.5rem !important;
        padding-bottom: 3rem !important;
        max-width: 1400px !important;
      }
      
      /* Header Banner Styling */
      .main-header {
        background: #0F172A;
        padding: 24px 28px;
        border-radius: 12px;
        color: #FFFFFF;
        margin-bottom: 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 16px;
      }
      .main-header-text h1 {
        font-weight: 700;
        font-size: 1.65rem;
        letter-spacing: -0.01em;
        margin: 0 0 4px 0;
        color: #FFFFFF !important;
      }
      .main-header-text p {
        color: #94A3B8;
        font-size: 0.88rem;
        margin: 0;
      }
      .header-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.1);
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        color: #38BDF8;
        margin-bottom: 8px;
      }
      .header-status-pill {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.12);
        padding: 6px 14px;
        border-radius: 8px;
        font-size: 0.8rem;
        color: #CBD5E1;
        display: flex;
        align-items: center;
        gap: 8px;
      }
      .status-dot {
        width: 8px;
        height: 8px;
        background-color: #10B981;
        border-radius: 50%;
        display: inline-block;
      }
      
      /* Metric Cards Styling */
      div[data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 14px 18px;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
      }
      div[data-testid="stMetricLabel"] p {
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        color: #64748B !important;
      }
      div[data-testid="stMetricValue"] div {
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        color: #0F172A !important;
      }
      
      /* Tabs Custom Styling */
      div[data-testid="stTabs"] {
        margin-top: 8px;
      }
      button[data-baseweb="tab"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        padding: 8px 16px !important;
        border-radius: 8px !important;
        color: #64748B !important;
        margin-right: 4px !important;
        border: 1px solid transparent !important;
      }
      button[aria-selected="true"] {
        color: #0F172A !important;
        background-color: #F1F5F9 !important;
        border-color: #E2E8F0 !important;
      }
      
      /* Sidebar Clean Styling */
      section[data-testid="stSidebar"] {
        background-color: #F8FAFC;
        border-right: 1px solid #E2E8F0;
      }
      section[data-testid="stSidebar"] h1, 
      section[data-testid="stSidebar"] h2, 
      section[data-testid="stSidebar"] h3 {
        color: #0F172A;
        font-weight: 600;
        font-size: 1.1rem;
      }

      /* Alert Callout Box Customization */
      div.stAlert {
        border-radius: 10px;
        border: 1px solid #E2E8F0;
      }
      
      /* Table Customization */
      div[data-testid="stDataFrame"] {
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        overflow: hidden;
      }

      /* Headings */
      h2, h3 {
        color: #0F172A;
        font-weight: 600;
        letter-spacing: -0.01em;
      }
    </style>
    """,
    unsafe_allow_html=True,
)


# ------------------------------------------------------------------ Data Load
@st.cache_data
def muat_data() -> pd.DataFrame:
    """Baca data mahasiswa. Ganti isi fungsi ini saat data asli sudah ada."""
    berkas = Path(__file__).with_name("data_mahasiswa.csv")
    if berkas.exists():
        df = pd.read_csv(berkas)
    else:
        from generate_data import buat_data_simulasi

        df = buat_data_simulasi()

    df["perlu_perhatian"] = (
        (df["ipk"] < BATAS_IPK_RAWAN)
        | (df["kehadiran_persen"] < BATAS_HADIR_RAWAN)
        | (df["tunggakan_ukt"] > 0)
    ) & (df["status_akademik"] != "Lulus")
    return df


def rupiah(nilai: float, singkat: bool = False) -> str:
    if singkat and nilai >= 1_000_000_000:
        return f"Rp {nilai / 1_000_000_000:.2f} M"
    if singkat and nilai >= 1_000_000:
        return f"Rp {nilai / 1_000_000:.1f} jt"
    return "Rp " + f"{nilai:,.0f}".replace(",", ".")


def rapikan(
    fig,
    tinggi: int = 390,
    judul: str = "",
    xlabel: str = "",
    ylabel: str = "",
    legend_top: bool = True,
):
    """Format grafik Plotly agar lega, bersih, dan tidak dempet."""
    layout_update = dict(
        height=tinggi,
        margin=dict(
            l=30,
            r=30,
            t=60 if (judul or legend_top) else 35,
            b=60 if not legend_top else 45,
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#334155", size=12),
        hoverlabel=dict(
            bgcolor="#0F172A",
            font_size=12,
            font_family="Plus Jakarta Sans, sans-serif",
            font_color="#FFFFFF",
        ),
    )

    if legend_top:
        layout_update["legend"] = dict(
            orientation="h",
            yanchor="bottom",
            y=1.04,
            x=1 if judul else 0,
            xanchor="right" if judul else "left",
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=11, color="#475569"),
            title=dict(text=""),
        )
    else:
        layout_update["legend"] = dict(
            orientation="h",
            yanchor="top",
            y=-0.22,
            x=0.5,
            xanchor="center",
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=11, color="#475569"),
            title=dict(text=""),
        )

    if judul:
        layout_update["title"] = dict(
            text=f"<b>{judul}</b>",
            font=dict(size=14, color="#0F172A", family="Plus Jakarta Sans, sans-serif"),
            x=0,
            xanchor="left",
            y=0.98,
        )

    fig.update_layout(**layout_update)
    fig.update_xaxes(
        gridcolor="#F1F5F9",
        zeroline=False,
        showline=True,
        linecolor="#E2E8F0",
        tickfont=dict(size=11, color="#64748B"),
        title_font=dict(size=12, color="#475569", family="Plus Jakarta Sans"),
        title_text=xlabel if xlabel else None,
    )
    fig.update_yaxes(
        gridcolor="#F1F5F9",
        zeroline=False,
        showline=True,
        linecolor="#E2E8F0",
        tickfont=dict(size=11, color="#64748B"),
        title_font=dict(size=12, color="#475569", family="Plus Jakarta Sans"),
        title_text=ylabel if ylabel else None,
    )
    return fig


data = muat_data()

# --------------------------------------------------------------------- Sidebar Filter
st.sidebar.markdown("### Filter data")
st.sidebar.caption("Sesuaikan parameter untuk memfilter dasbor:")

LABEL_PRODI = "Semua program studi"
LABEL_ANGKATAN = "Semua angkatan"
LABEL_STATUS = "Semua status akademik"

def tangani_filter_semua(key_name, semua_opsi_str, semua_label):
    pilihan = st.session_state.get(key_name, [])
    if not pilihan:
        st.session_state[key_name] = [semua_label]
        return

    if semua_label in pilihan:
        if pilihan[-1] == semua_label or len(pilihan) == len(semua_opsi_str) + 1:
            st.session_state[key_name] = [semua_label]
        else:
            n_pilihan = [p for p in pilihan if p != semua_label]
            if set(n_pilihan) == set(semua_opsi_str):
                st.session_state[key_name] = [semua_label]
            else:
                st.session_state[key_name] = n_pilihan
    else:
        if set(pilihan) == set(semua_opsi_str):
            st.session_state[key_name] = [semua_label]


if "filter_prodi" not in st.session_state:
    st.session_state["filter_prodi"] = [LABEL_PRODI]
if "filter_angkatan" not in st.session_state:
    st.session_state["filter_angkatan"] = [LABEL_ANGKATAN]
if "filter_status" not in st.session_state:
    st.session_state["filter_status"] = [LABEL_STATUS]

semua_prodi = sorted(list(data["program_studi"].unique()))
st.sidebar.multiselect(
    "Program studi",
    options=[LABEL_PRODI] + semua_prodi,
    key="filter_prodi",
    on_change=tangani_filter_semua,
    args=("filter_prodi", semua_prodi, LABEL_PRODI),
)
prodi_pilih = st.session_state["filter_prodi"]
prodi_aktif = semua_prodi if (LABEL_PRODI in prodi_pilih or not prodi_pilih) else prodi_pilih

semua_angkatan_str = [str(a) for a in sorted(list(data["angkatan"].unique()))]
st.sidebar.multiselect(
    "Angkatan",
    options=[LABEL_ANGKATAN] + semua_angkatan_str,
    key="filter_angkatan",
    on_change=tangani_filter_semua,
    args=("filter_angkatan", semua_angkatan_str, LABEL_ANGKATAN),
)
angkatan_pilih = st.session_state["filter_angkatan"]
angkatan_aktif = [int(a) for a in sorted(list(data["angkatan"].unique()))] if (LABEL_ANGKATAN in angkatan_pilih or not angkatan_pilih) else [int(a) for a in angkatan_pilih if a != LABEL_ANGKATAN]

semua_status = ["Aktif", "Cuti", "Non-Aktif", "Lulus"]
st.sidebar.multiselect(
    "Status akademik",
    options=[LABEL_STATUS] + semua_status,
    key="filter_status",
    on_change=tangani_filter_semua,
    args=("filter_status", semua_status, LABEL_STATUS),
)
status_pilih = st.session_state["filter_status"]
status_aktif = semua_status if (LABEL_STATUS in status_pilih or not status_pilih) else status_pilih

ipk_min, ipk_maks = st.sidebar.slider("Rentang IPK", 0.0, 4.0, (0.0, 4.0), 0.05)
hanya_rawan = st.sidebar.checkbox("Hanya mahasiswa perlu perhatian")

df = data[
    data["program_studi"].isin(prodi_aktif)
    & data["angkatan"].isin(angkatan_aktif)
    & data["status_akademik"].isin(status_aktif)
    & data["ipk"].between(ipk_min, ipk_maks)
]
if hanya_rawan:
    df = df[df["perlu_perhatian"]]

st.sidebar.markdown("---")
st.sidebar.markdown(
    f"""
    <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px; font-size: 0.82rem; color: #475569;">
        Menampilkan <b>{len(df):,}</b> dari <b>{len(data):,}</b> mahasiswa.<br>
        <hr style="margin: 8px 0; border-color: #F1F5F9;">
        <span style="font-size: 0.76rem; color: #64748B;">
            Kriteria <i>perlu perhatian</i>: IPK &lt; 2,50 <b>atau</b> kehadiran &lt; 75% <b>atau</b> memiliki tunggakan UKT.
        </span>
    </div>
    """.replace(",", "."),
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------- Header Banner
st.markdown(
    """
    <div class="main-header">
        <div class="main-header-text">
            <div class="header-badge">Dashboard BI Akademik</div>
            <h1>Dashboard Akademik — Fakultas Ilmu Komputer</h1>
            <p>Sistem informasi & analitik data kinerja mahasiswa (Simulasi SIAKAD)</p>
        </div>
        <div class="header-status-pill">
            <span class="status-dot"></span> Status: Data aktif
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if df.empty:
    st.warning("Tidak ada data yang cocok dengan kombinasi filter di sidebar.")
    st.stop()

# ---------------------------------------------------------------- KPI Cards Row
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total mahasiswa", f"{len(df):,}".replace(",", "."))
k2.metric(
    "Mahasiswa aktif",
    f"{(df['status_akademik'] == 'Aktif').sum():,}".replace(",", "."),
)
k3.metric("Rata-rata IPK", f"{df['ipk'].mean():.2f}")
k4.metric("Rata-rata kehadiran", f"{df['kehadiran_persen'].mean():.1f}%")
k5.metric(
    "Total tunggakan UKT",
    rupiah(df["tunggakan_ukt"].sum(), singkat=True),
    delta=f"{(df['tunggakan_ukt'] > 0).sum()} mahasiswa",
    delta_color="inverse",
)

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

# ---------------------------------------------------------------- Navigation Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "Ringkasan",
        "Akademik",
        "Keuangan (UKT)",
        "Kehadiran",
        "Data & Ekspor",
    ]
)

# ---------------------------------------------------------------- TAB 1: Ringkasan
with tab1:
    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1.25], gap="large")

    with c1:
        komposisi = df["status_akademik"].value_counts().reset_index()
        komposisi.columns = ["status", "jumlah"]
        fig = px.pie(
            komposisi,
            names="status",
            values="jumlah",
            hole=0.62,
            color="status",
            color_discrete_map=WARNA_STATUS,
        )
        fig.update_traces(
            textinfo="percent",
            textposition="inside",
            hoverinfo="label+value+percent",
            marker=dict(line=dict(color="#FFFFFF", width=2)),
        )
        fig.add_annotation(
            text=f"<b>{len(df):,}</b><br><span style='font-size:11px;color:#64748B;'>Total</span>".replace(",", "."),
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="#0F172A", family="Plus Jakarta Sans"),
        )
        st.plotly_chart(
            rapikan(fig, tinggi=380, judul="Komposisi status akademik"),
            use_container_width=True,
        )

    with c2:
        per_prodi = (
            df.groupby(["program_studi", "angkatan"]).size().reset_index(name="jumlah")
        )
        fig = px.bar(
            per_prodi,
            x="program_studi",
            y="jumlah",
            color="angkatan",
            barmode="stack",
            color_discrete_sequence=PALET,
            text_auto=True,
        )
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(
            rapikan(
                fig,
                tinggi=380,
                judul="Jumlah mahasiswa per prodi & angkatan",
                ylabel="Mahasiswa",
            ),
            use_container_width=True,
        )

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    st.markdown("### Ringkasan kinerja per program studi")
    ringkas = (
        df.groupby("program_studi")
        .agg(
            mahasiswa=("nim", "count"),
            rata_ipk=("ipk", "mean"),
            rata_kehadiran=("kehadiran_persen", "mean"),
            penunggak=("tunggakan_ukt", lambda s: (s > 0).sum()),
            total_tunggakan=("tunggakan_ukt", "sum"),
            perlu_perhatian=("perlu_perhatian", "sum"),
        )
        .reset_index()
    )
    st.dataframe(
        ringkas,
        use_container_width=True,
        hide_index=True,
        column_config={
            "program_studi": "Program studi",
            "mahasiswa": st.column_config.NumberColumn("Mahasiswa"),
            "rata_ipk": st.column_config.NumberColumn("Rata IPK", format="%.2f"),
            "rata_kehadiran": st.column_config.NumberColumn(
                "Rata kehadiran", format="%.1f%%"
            ),
            "penunggak": st.column_config.NumberColumn("Penunggak UKT"),
            "total_tunggakan": st.column_config.NumberColumn(
                "Total tunggakan", format="Rp %d"
            ),
            "perlu_perhatian": st.column_config.NumberColumn("Perlu perhatian"),
        },
    )

# ---------------------------------------------------------------- TAB 2: Akademik
with tab2:
    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1], gap="large")

    with c1:
        fig = px.histogram(
            df,
            x="ipk",
            nbins=28,
            color_discrete_sequence=[BLUE],
        )
        fig.update_traces(marker_line_width=0)
        fig.add_vline(
            x=BATAS_IPK_RAWAN,
            line_dash="dash",
            line_color=MERAH,
            line_width=2,
            annotation_text="Batas rawan 2,50",
            annotation_position="top left",
            annotation_font=dict(color=MERAH, size=11),
        )
        st.plotly_chart(
            rapikan(
                fig,
                tinggi=380,
                judul="Sebaran IPK mahasiswa",
                xlabel="Nilai IPK",
                ylabel="Jumlah mahasiswa",
            ),
            use_container_width=True,
        )

    with c2:
        fig = px.box(
            df,
            x="program_studi",
            y="ipk",
            color="program_studi",
            color_discrete_sequence=PALET,
            points=False,
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(
            rapikan(
                fig,
                tinggi=380,
                judul="Sebaran IPK per program studi",
                ylabel="IPK",
            ),
            use_container_width=True,
        )

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    tren = df.groupby(["angkatan", "program_studi"])["ipk"].mean().reset_index()
    fig = px.line(
        tren,
        x="angkatan",
        y="ipk",
        color="program_studi",
        markers=True,
        color_discrete_sequence=PALET,
    )
    fig.update_traces(line=dict(width=2.5), marker=dict(size=8))
    fig.update_xaxes(tickmode="array", tickvals=sorted(df["angkatan"].unique()))
    st.plotly_chart(
        rapikan(
            fig,
            tinggi=380,
            judul="Tren rata-rata IPK per angkatan",
            xlabel="Tahun angkatan",
            ylabel="Rata-rata IPK",
        ),
        use_container_width=True,
    )

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    st.markdown(f"### Mahasiswa dengan IPK di bawah {BATAS_IPK_RAWAN:.2f}")
    rawan = df[df["ipk"] < BATAS_IPK_RAWAN].sort_values("ipk")
    st.caption(
        f"Daftar {len(rawan)} mahasiswa berisiko akademik — memerlukan pembimbingan dosen PA."
    )
    st.dataframe(
        rawan[
            [
                "nim",
                "nama",
                "program_studi",
                "angkatan",
                "ipk",
                "sks_lulus",
                "kehadiran_persen",
                "status_akademik",
                "dosen_pa",
            ]
        ],
        use_container_width=True,
        hide_index=True,
        height=290,
    )

# ---------------------------------------------------------------- TAB 3: Keuangan
with tab3:
    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    penunggak = df[df["tunggakan_ukt"] > 0]

    m1, m2, m3 = st.columns(3)
    m1.metric("Jumlah penunggak", f"{len(penunggak):,}".replace(",", "."))
    m2.metric(
        "Rasio penunggak",
        f"{len(penunggak) / len(df) * 100:.1f}%" if len(df) else "0%",
    )
    m3.metric(
        "Rata-rata tunggakan",
        rupiah(penunggak["tunggakan_ukt"].mean()) if len(penunggak) else "Rp 0",
    )

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns([1.3, 1], gap="large")

    with c1:
        per_prodi = (
            df.groupby("program_studi")["tunggakan_ukt"]
            .sum()
            .reset_index()
            .sort_values("tunggakan_ukt", ascending=True)
        )
        fig = px.bar(
            per_prodi,
            x="tunggakan_ukt",
            y="program_studi",
            orientation="h",
            color_discrete_sequence=[BLUE],
            text_auto=".2s",
        )
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(
            rapikan(
                fig,
                tinggi=380,
                judul="Total tunggakan UKT per program studi",
                xlabel="Nominal tunggakan (Rupiah)",
                legend_top=False,
            ),
            use_container_width=True,
        )

    with c2:
        komposisi = df["status_pembayaran"].value_counts().reset_index()
        komposisi.columns = ["status", "jumlah"]
        fig = px.pie(
            komposisi,
            names="status",
            values="jumlah",
            hole=0.62,
            color="status",
            color_discrete_map=WARNA_BAYAR,
        )
        fig.update_traces(
            textinfo="percent",
            textposition="inside",
            hoverinfo="label+value+percent",
            marker=dict(line=dict(color="#FFFFFF", width=2)),
        )
        st.plotly_chart(
            rapikan(fig, tinggi=380, judul="Status pembayaran UKT"),
            use_container_width=True,
        )

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    per_gol = (
        df.groupby("golongan_ukt")
        .agg(mahasiswa=("nim", "count"), tunggakan=("tunggakan_ukt", "sum"))
        .reset_index()
    )
    fig = px.bar(
        per_gol,
        x="golongan_ukt",
        y="tunggakan",
        color_discrete_sequence=[TEAL],
        text_auto=".2s",
        hover_data={"mahasiswa": True},
    )
    fig.update_traces(marker_line_width=0)
    fig.update_xaxes(tickmode="linear", dtick=1)
    st.plotly_chart(
        rapikan(
            fig,
            tinggi=360,
            judul="Distribusi tunggakan per golongan UKT",
            xlabel="Golongan UKT",
            ylabel="Total tunggakan (Rupiah)",
        ),
        use_container_width=True,
    )

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    st.markdown("### 15 tunggakan UKT terbesar")
    tabel = (
        penunggak.sort_values("tunggakan_ukt", ascending=False)
        .head(15)[
            [
                "nim",
                "nama",
                "program_studi",
                "angkatan",
                "golongan_ukt",
                "nominal_ukt",
                "tunggakan_ukt",
                "status_akademik",
                "ipk",
            ]
        ]
    )
    st.dataframe(
        tabel,
        use_container_width=True,
        hide_index=True,
        column_config={
            "nominal_ukt": st.column_config.NumberColumn(
                "UKT / semester", format="Rp %d"
            ),
            "tunggakan_ukt": st.column_config.NumberColumn(
                "Tunggakan", format="Rp %d"
            ),
        },
    )

# ---------------------------------------------------------------- TAB 4: Kehadiran
with tab4:
    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1], gap="large")

    with c1:
        fig = px.histogram(
            df,
            x="kehadiran_persen",
            nbins=25,
            color_discrete_sequence=[TEAL],
        )
        fig.update_traces(marker_line_width=0)
        fig.add_vline(
            x=BATAS_HADIR_RAWAN,
            line_dash="dash",
            line_color=MERAH,
            line_width=2,
            annotation_text="Batas 75%",
            annotation_position="top left",
            annotation_font=dict(color=MERAH, size=11),
        )
        st.plotly_chart(
            rapikan(
                fig,
                tinggi=380,
                judul="Sebaran tingkat kehadiran presensi",
                xlabel="Persentase kehadiran (%)",
                ylabel="Mahasiswa",
            ),
            use_container_width=True,
        )

    with c2:
        fig = px.scatter(
            df,
            x="kehadiran_persen",
            y="ipk",
            color="program_studi",
            opacity=0.7,
            color_discrete_sequence=PALET,
            hover_data=["nim", "nama", "angkatan"],
        )
        fig.update_traces(marker=dict(size=7))
        st.plotly_chart(
            rapikan(
                fig,
                tinggi=380,
                judul="Korelasi kehadiran kuliah vs IPK",
                xlabel="Kehadiran (%)",
                ylabel="IPK",
            ),
            use_container_width=True,
        )

    korelasi = df["kehadiran_persen"].corr(df["ipk"])
    st.info(
        f"**Insight presensi**: Korelasi kehadiran terhadap IPK pada data terfilter adalah **{korelasi:.2f}** "
        "(Korelasi positif kuat: semakin tinggi kehadiran, cenderung semakin baik raihan IPK)."
    )

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    per_prodi = (
        df.groupby(["program_studi", "angkatan"])["kehadiran_persen"]
        .mean()
        .reset_index()
    )
    fig = px.bar(
        per_prodi,
        x="program_studi",
        y="kehadiran_persen",
        color="angkatan",
        barmode="group",
        color_discrete_sequence=PALET,
    )
    fig.update_traces(marker_line_width=0)
    fig.update_yaxes(range=[0, 100])
    st.plotly_chart(
        rapikan(
            fig,
            tinggi=380,
            judul="Rata-rata kehadiran per prodi & angkatan",
            ylabel="Rata kehadiran (%)",
        ),
        use_container_width=True,
    )

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    st.markdown(f"### Mahasiswa dengan kehadiran di bawah {BATAS_HADIR_RAWAN:.0f}%")
    kurang = df[df["kehadiran_persen"] < BATAS_HADIR_RAWAN].sort_values(
        "kehadiran_persen"
    )
    st.caption(
        f"Daftar {len(kurang)} mahasiswa berisiko tidak memenuhi batas minimal presensi ujian."
    )
    st.dataframe(
        kurang[
            [
                "nim",
                "nama",
                "program_studi",
                "angkatan",
                "kehadiran_persen",
                "ipk",
                "status_akademik",
                "dosen_pa",
            ]
        ],
        use_container_width=True,
        hide_index=True,
        height=290,
    )

# ---------------------------------------------------------------- TAB 5: Data & Ekspor
with tab5:
    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    cari = st.text_input(
        "Cari mahasiswa",
        placeholder="Ketik nama atau NIM (contoh: 2301 atau Dewi)...",
    )
    tampil = df
    if cari:
        kunci = cari.lower()
        tampil = df[
            df["nama"].str.lower().str.contains(kunci)
            | df["nim"].astype(str).str.contains(kunci)
        ]

    st.dataframe(
        tampil,
        use_container_width=True,
        hide_index=True,
        height=450,
        column_config={
            "nominal_ukt": st.column_config.NumberColumn(
                "Nominal UKT", format="Rp %d"
            ),
            "tunggakan_ukt": st.column_config.NumberColumn(
                "Tunggakan UKT", format="Rp %d"
            ),
            "perlu_perhatian": st.column_config.CheckboxColumn("Perlu perhatian"),
        },
    )

    st.download_button(
        "Unduh data terfilter (CSV)",
        tampil.to_csv(index=False).encode("utf-8"),
        file_name="data_mahasiswa_terfilter.csv",
        mime="text/csv",
    )

st.markdown("---")
st.caption(
    "Dashboard BI FIK — Prototipe Business Intelligence Fakultas Ilmu Komputer. Powered by Streamlit & Plotly."
)
