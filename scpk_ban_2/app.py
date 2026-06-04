import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
import pandas as pd
import numpy as np

from config import CRITERIA, CRITERIA_LABEL, DEFAULT_WEIGHTS, ALTERNATIVE_COL
from saw import load_data, run_saw
from charts import chart_ranking, chart_harga_pie_top5, chart_scatter_top5
from styles import CSS

# ─── Konfigurasi halaman ────────
st.set_page_config(
    page_title="SPK Ban — SAW",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(CSS, unsafe_allow_html=True)

# ─── Load data ────────
@st.cache_data
def get_data():
    return load_data('Car_Tyres_Dataset_Clean.csv')

df_all = get_data()

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div style="font-size:2.5rem">🚗</div>
        <div style="font-family:'DM Serif Display',serif;font-size:1.3rem;font-weight:700;margin-top:0.3rem">TyreRank</div>
        <div style="font-size:0.72rem;color:#C4B5FD;margin-top:0.2rem;letter-spacing:1px;text-transform:uppercase">Pemilihan Ban Terbaik</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Bobot Kriteria ───────────────────────────────────────────────────────
    st.markdown("### ⚖️ Bobot Kriteria")
    st.caption("Total bobot harus = 1.00")

    weights = {}
    for col in CRITERIA:
        weights[col] = st.slider(
            CRITERIA_LABEL[col],
            min_value=0.0, max_value=1.0,
            value=DEFAULT_WEIGHTS[col], step=0.05,
            key=f"w_{col}"
        )

    total_w = sum(weights.values())
    if abs(total_w - 1.0) < 1e-9:
        st.success(f"✅ Total bobot: {total_w:.2f}")
    else:
        st.warning(f"⚠️ Total bobot: {total_w:.2f} (harus 1.00)")

    st.markdown("---")

    # ── Pencarian Ban ────────────────────────────────────────────────────────
    st.markdown("### 🔍 Pencarian Ban")

    # Filter 1: Ukuran Ban (dari kolom Size asli)
    all_sizes  = sorted(df_all['Size'].dropna().unique().tolist())
    pilih_size = st.selectbox(
        "📐 Ukuran Ban",
        options=["Semua Ukuran"] + all_sizes,
        index=0,
        key="filter_size"
    )

    # Filter 2: Merk Ban
    all_brands  = sorted(df_all['TyreBrand'].dropna().unique().tolist())
    pilih_brand = st.selectbox(
        "🏷️ Merk Ban",
        options=["Semua Merk"] + all_brands,
        index=0,
        key="filter_brand"
    )

    # Terapkan filter
    df_filtered = df_all.copy()
    if pilih_size != "Semua Ukuran":
        df_filtered = df_filtered[df_filtered['Size'] == pilih_size]
    if pilih_brand != "Semua Merk":
        df_filtered = df_filtered[df_filtered['TyreBrand'] == pilih_brand]

    n_hasil = len(df_filtered)
    if pilih_size != "Semua Ukuran" or pilih_brand != "Semua Merk":
        st.info(f"🎯 {n_hasil} produk ban ditemukan")

    st.markdown("---")

    # ── Filter Tampilan ──────────────────────────────────────────────────────
    st.markdown("### 🔢 Filter Tampilan")
    top_n = st.selectbox("Tampilkan Top-N Ban", [5, 10, 15, 20, 30, 50], index=1)

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.75rem;color:#A78BFA;text-align:center;padding:0.5rem">
    Metode: <strong style="color:white">SAW</strong><br>
    Simple Additive Weighting<br><br>
    SCPK 2025/2026
    </div>
    """, unsafe_allow_html=True)

# ─── Hero banner ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-badge">🚗 Sistem Pendukung Keputusan</div>
    <h1 class="hero-title">Pemilihan Ban Mobil<br>Terbaik</h1>
    <p class="hero-subtitle">Menggunakan Metode Simple Additive Weighting (SAW) &nbsp;·&nbsp; SCPK 2025/2026</p>
</div>
""", unsafe_allow_html=True)

# ─── Metric cards ─────────────────────────────────────────────────────────────
n_alternatif = len(df_filtered)
n_total      = len(df_all)
n_kriteria   = len(CRITERIA)

st.markdown(f"""
<div class="metric-row">
    <div class="metric-card">
        <div class="metric-value">{n_alternatif}</div>
        <div class="metric-label">Jumlah Alternatif</div>
    </div>
    <div class="metric-card rose">
        <div class="metric-value">{n_total:,}</div>
        <div class="metric-label">Total Data</div>
    </div>
    <div class="metric-card mint">
        <div class="metric-value">{n_kriteria}</div>
        <div class="metric-label">Jumlah Kriteria</div>
    </div>
    <div class="metric-card sky">
        <div class="metric-value">{total_w:.2f}</div>
        <div class="metric-label">Total Bobot</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 Dataset",
    "⚙️ Proses SAW",
    "🏆 Hasil Perangkingan",
    "📊 Visualisasi",
    "👥 Profil Kelompok",
])

# ════════════════════════════════════════════════════════
# TAB 1 — DATASET
# ════════════════════════════════════════════════════════
with tab1:
    st.markdown('<h2 class="section-header">📋 Dataset Ban Mobil</h2>', unsafe_allow_html=True)
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        Dataset berisi <strong>488 kombinasi unik</strong> ban mobil berdasarkan Merk + Model + Ukuran.
        Setiap baris adalah satu alternatif dengan 5 kriteria penilaian.
        Gunakan filter <strong>Pencarian Ban</strong> di sidebar untuk menyaring data.
    </div>
    """, unsafe_allow_html=True)

    if pilih_size != "Semua Ukuran" or pilih_brand != "Semua Merk":
        filter_aktif = []
        if pilih_size  != "Semua Ukuran": filter_aktif.append(f"Ukuran: **{pilih_size}**")
        if pilih_brand != "Semua Merk":   filter_aktif.append(f"Merk: **{pilih_brand}**")
        st.markdown(f"🎯 Filter aktif: {' · '.join(filter_aktif)}")

    # Tampilkan kolom yang relevan
    cols_display = [ALTERNATIVE_COL, 'Tyre Brand', 'Model', 'Size'] + CRITERIA
    st.dataframe(
        df_filtered[cols_display].rename(columns=CRITERIA_LABEL),
        use_container_width=True,
        height=420,
    )

    st.markdown("---")
    st.markdown('<h3 style="color:#4C1D95;font-size:1.1rem">📈 Statistik Deskriptif</h3>', unsafe_allow_html=True)
    st.dataframe(
        df_filtered[CRITERIA].describe().rename(columns=CRITERIA_LABEL).round(3),
        use_container_width=True,
    )

# ════════════════════════════════════════════════════════
# TAB 2 — PROSES SAW
# ════════════════════════════════════════════════════════
with tab2:
    st.markdown('<h2 class="section-header">⚙️ Proses Perhitungan SAW</h2>', unsafe_allow_html=True)
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    if abs(total_w - 1.0) > 1e-9:
        st.error("⚠️ Total bobot belum = 1.00. Sesuaikan di sidebar sebelum menjalankan perhitungan!")

    elif n_alternatif < 2:
        st.warning(
            f"⚠️ Filter terlalu ketat — hanya ditemukan **{n_alternatif} alternatif**. "
            "Minimal dibutuhkan 2 alternatif untuk perhitungan SAW. "
            "Coba pilih ukuran ban lain atau pilih **Semua Ukuran**."
        )
        st.session_state['saw_done'] = False

    else:
        # Tampilkan bobot aktif
        st.markdown("**Bobot Kriteria Aktif:**")
        chips_html = '<div class="weight-chips">'
        for col in CRITERIA:
            tipe = 'Cost' if col in ['SellingPrice', 'OriginalPrice'] else 'Benefit'
            chips_html += f'<span class="chip">{CRITERIA_LABEL[col]} ({tipe}): {weights[col]:.0%}</span>'
        chips_html += '</div>'
        st.markdown(chips_html, unsafe_allow_html=True)

        st.markdown("---")

        col_btn, _ = st.columns([1, 3])
        with col_btn:
            run_button = st.button("🚀 Jalankan Perhitungan SAW", use_container_width=True)

        # Reset saw_done jika filter berubah
        filter_key = f"{pilih_size}|{pilih_brand}"
        if st.session_state.get('last_filter') != filter_key:
            st.session_state['saw_done']    = False
            st.session_state['last_filter'] = filter_key

        if run_button or st.session_state.get('saw_done'):
            st.session_state['saw_done'] = True
            df_grouped, df_norm, df_ranked = run_saw(df_filtered, weights)
            st.session_state['df_ranked']  = df_ranked
            st.session_state['df_grouped'] = df_grouped
            st.session_state['df_norm']    = df_norm

            # Step 1 — Matriks Keputusan
            st.markdown("""
            <div class="step-row">
                <span class="step-badge">1</span>
                <div><strong>Matriks Keputusan</strong><br>
                <span style="font-size:0.83rem;color:#6B7280">
                    Data teragregasi per kombinasi Merk + Model + Ukuran Ban.
                </span></div>
            </div>
            """, unsafe_allow_html=True)
            st.dataframe(
                df_grouped.set_index(ALTERNATIVE_COL).rename(columns=CRITERIA_LABEL).round(3),
                use_container_width=True, height=280
            )

            # Step 2 — Normalisasi
            st.markdown("""
            <div class="step-row">
                <span class="step-badge">2</span>
                <div><strong>Normalisasi Matriks</strong><br>
                <span style="font-size:0.83rem;color:#6B7280">
                    Benefit: r<sub>ij</sub> = x<sub>ij</sub> / max(x<sub>j</sub>) &nbsp;|&nbsp;
                    Cost: r<sub>ij</sub> = min(x<sub>j</sub>) / x<sub>ij</sub>
                </span></div>
            </div>
            """, unsafe_allow_html=True)
            norm_show = df_norm[[ALTERNATIVE_COL] + CRITERIA].rename(columns=CRITERIA_LABEL)
            st.dataframe(norm_show.round(4), use_container_width=True, height=280)

            # Step 3 — Nilai Preferensi
            st.markdown("""
            <div class="step-row">
                <span class="step-badge">3</span>
                <div><strong>Nilai Preferensi (Skor SAW)</strong><br>
                <span style="font-size:0.83rem;color:#6B7280">
                    V<sub>i</sub> = Σ (w<sub>j</sub> × r<sub>ij</sub>)
                </span></div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<small style='color:#6B7280'>Bobot tiap kriteria (w<sub>j</sub>):</small>", unsafe_allow_html=True)
            weight_df = pd.DataFrame([
                {
                    'Kriteria': CRITERIA_LABEL[c],
                    'Tipe': 'Cost' if c in ['SellingPrice', 'OriginalPrice'] else 'Benefit',
                    'Bobot (w)': f"{weights[c]:.0%}"
                }
                for c in CRITERIA
            ])
            st.dataframe(weight_df, use_container_width=True, hide_index=True)

            st.markdown("<small style='color:#6B7280;margin-top:0.5rem;display:block'>Hasil perkalian bobot × normalisasi (w<sub>j</sub> × r<sub>ij</sub>):</small>", unsafe_allow_html=True)
            df_pref = df_norm[[ALTERNATIVE_COL] + CRITERIA].copy()
            for col in CRITERIA:
                df_pref[col] = df_norm[col] * weights[col]
            df_pref['V_i (Skor SAW)'] = df_pref[CRITERIA].sum(axis=1).round(4)
            df_pref[CRITERIA] = df_pref[CRITERIA].round(4)
            st.dataframe(
                df_pref.set_index(ALTERNATIVE_COL).rename(columns=CRITERIA_LABEL),
                use_container_width=True, height=280
            )

            st.success("✅ Perhitungan SAW selesai! Lihat hasil di tab **Hasil Perangkingan**.")

        else:
            st.info("👈 Sesuaikan bobot di sidebar, lalu klik **Jalankan Perhitungan SAW**.")

# ════════════════════════════════════════════════════════
# TAB 3 — HASIL PERANGKINGAN
# ════════════════════════════════════════════════════════
with tab3:
    st.markdown('<h2 class="section-header">🏆 Hasil Perangkingan Ban</h2>', unsafe_allow_html=True)
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    if 'df_ranked' not in st.session_state or not st.session_state.get('saw_done'):
        st.info("⚙️ Jalankan perhitungan SAW terlebih dahulu di tab **Proses SAW**.")
    else:
        df_ranked = st.session_state['df_ranked']

        # Podium Top 3
        top3   = df_ranked.head(3)
        medals = [('🥇', 'gold'), ('🥈', 'silver'), ('🥉', 'bronze')]
        podium_html = '<div class="top3-container">'
        for i, (_, row) in enumerate(top3.iterrows()):
            emoji, cls = medals[i]
            podium_html += f"""
            <div class="top3-card {cls}">
                <div class="top3-rank">{emoji}</div>
                <div class="top3-name">{row[ALTERNATIVE_COL]}</div>
                <div class="top3-score">{row['Score']:.4f}</div>
            </div>"""
        podium_html += '</div>'
        st.markdown(podium_html, unsafe_allow_html=True)

        st.markdown(f"**Menampilkan Top {top_n} ban dari {len(df_ranked)} total alternatif:**")

        display = df_ranked.head(top_n)[['Peringkat', ALTERNATIVE_COL, 'Score'] + CRITERIA].copy()
        display = display.rename(columns={**{ALTERNATIVE_COL: 'Produk Ban', 'Score': 'Skor SAW'}, **CRITERIA_LABEL})
        display['Skor SAW'] = display['Skor SAW'].round(4)
        for lbl in CRITERIA_LABEL.values():
            if lbl in display.columns:
                display[lbl] = display[lbl].round(4)

        st.dataframe(
            display.set_index('Peringkat'),
            use_container_width=True,
            height=460,
        )

# ════════════════════════════════════════════════════════
# TAB 4 — VISUALISASI
# ════════════════════════════════════════════════════════
with tab4:
    st.markdown('<h2 class="section-header">📊 Visualisasi Analitik</h2>', unsafe_allow_html=True)
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    if 'df_ranked' not in st.session_state or not st.session_state.get('saw_done'):
        st.info("⚙️ Jalankan perhitungan SAW terlebih dahulu di tab **Proses SAW**.")
    else:
        df_ranked  = st.session_state['df_ranked']
        df_grouped = st.session_state['df_grouped']

        st.markdown("#### 📈 Grafik 1: Top Ban berdasarkan Skor SAW")
        st.pyplot(chart_ranking(df_ranked, top_n), use_container_width=True)

        st.pyplot(chart_harga_pie_top5(df_ranked, df_grouped))
        st.pyplot(chart_scatter_top5(df_ranked, df_grouped))

# ════════════════════════════════════════════════════════
# TAB 5 — PROFIL KELOMPOK
# ════════════════════════════════════════════════════════
with tab5:
    st.markdown('<h2 class="section-header">👥 Profil Kelompok</h2>', unsafe_allow_html=True)
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown("""
        <div class="profile-card">
            <div class="profile-avatar">👤</div>
            <div class="profile-name">Krocasadigandra Arzaq Kubro Muhammad</div>
            <div class="profile-nim">NIM: 123240015</div>
        </div>
        """, unsafe_allow_html=True)
    with col_p2:
        st.markdown("""
        <div class="profile-card">
            <div class="profile-avatar">👤</div>
            <div class="profile-name">Hardanu Ilham Purnama</div>
            <div class="profile-nim">NIM: 123240166</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**📐 Metode SAW — Rumus Dasar:**")
    st.latex(r"V_i = \sum_{j=1}^{n} w_j \cdot r_{ij}")
    st.markdown("""
    - $V_i$ = Nilai preferensi alternatif ke-$i$
    - $w_j$ = Bobot kriteria ke-$j$
    - $r_{ij}$ = Nilai ternormalisasi alternatif ke-$i$ pada kriteria ke-$j$
    - Normalisasi benefit: $r_{ij} = x_{ij}$ / max($x_j$)
    - Normalisasi cost: $r_{ij}$ = min($x_j$) / $x_{ij}$
    """)
