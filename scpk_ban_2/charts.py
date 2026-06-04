# modules/charts.py — Fungsi grafik untuk SPK Ban

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from config import CRITERIA, CRITERIA_LABEL, ALTERNATIVE_COL

BG     = '#F5F3FF'
P_DEEP = '#3B0764'
P_MID  = '#4C1D95'
P_GRID = '#EDE9FE'
P_SPNE = '#DDD6FE'

CRITERIA_LABEL_CHART = {
    'SellingPrice':  'Harga Jual',
    'OriginalPrice': 'Harga Asli',
    'LoadIndex':     'Load Index',
    'Rating':        'Rating',
    'VelgSize':      'Ukuran Velg',
}


def _base_ax(ax, bg=BG):
    ax.set_facecolor(bg)
    ax.tick_params(colors=P_MID, labelsize=8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(P_SPNE)
    ax.spines['bottom'].set_color(P_SPNE)


def chart_ranking(ranking, top_n):
    """Grafik 1: Horizontal bar chart Top-N ban berdasarkan skor SAW."""
    top = ranking.head(top_n)
    fig, ax = plt.subplots(figsize=(10, max(4, top_n * 0.40)))
    fig.patch.set_facecolor(BG)
    _base_ax(ax)

    colors = [plt.cm.RdPu(0.3 + 0.6 * i / max(top_n, 1)) for i in range(top_n)]
    bars = ax.barh(
        top[ALTERNATIVE_COL][::-1],
        top['Score'][::-1],
        color=colors,
        edgecolor='white', linewidth=0.7, height=0.65,
    )
    for bar, score in zip(bars, top['Score'][::-1]):
        ax.text(
            bar.get_width() + 0.002,
            bar.get_y() + bar.get_height() / 2,
            f'{score:.4f}', va='center', ha='left',
            fontsize=8, fontweight='600', color=P_MID,
        )

    ax.set_xlabel('Skor SAW', fontsize=9, color=P_MID)
    ax.set_title(f'Top {top_n} Ban — Skor SAW',
                 fontsize=12, fontweight='700', color=P_DEEP, pad=12)
    ax.grid(axis='x', color=P_GRID, linewidth=0.5)
    plt.tight_layout()
    return fig


def chart_boxplot(df_raw):
    """Grafik 2: Boxplot distribusi nilai per kriteria."""
    crit_available = [c for c in CRITERIA if c in df_raw.columns]

    fig, ax = plt.subplots(figsize=(11, 5))
    fig.patch.set_facecolor(BG)
    _base_ax(ax)

    data_box   = [df_raw[col].dropna().values for col in crit_available]
    colors_box = [plt.cm.RdPu(0.3 + 0.6 * i / len(crit_available)) for i in range(len(crit_available))]

    bp = ax.boxplot(
        data_box, patch_artist=True,
        medianprops=dict(color='white', linewidth=2),
        whiskerprops=dict(color='#7C3AED', linewidth=1.2),
        capprops=dict(color='#7C3AED', linewidth=1.5),
        flierprops=dict(marker='o', color='#C084FC', markersize=3, alpha=0.5),
    )
    for patch, color in zip(bp['boxes'], colors_box):
        patch.set_facecolor(color)
        patch.set_alpha(0.85)

    ax.set_xticklabels(
        [CRITERIA_LABEL_CHART[c] for c in crit_available],
        rotation=25, ha='right', fontsize=8, color=P_DEEP,
    )
    ax.set_ylabel('Nilai', fontsize=9, color=P_MID)
    ax.set_title('Distribusi Nilai per Kriteria',
                 fontsize=12, fontweight='700', color=P_DEEP, pad=12)
    ax.grid(axis='y', color=P_GRID, linewidth=0.5)
    plt.tight_layout()
    return fig


def chart_radar(ranking, df_grouped):
    """Grafik 3: Radar chart profil Top-5 produk ban."""
    top5_names = ranking.head(5)[ALTERNATIVE_COL].tolist()
    df_g5 = (
        df_grouped[df_grouped[ALTERNATIVE_COL].isin(top5_names)]
        .set_index(ALTERNATIVE_COL)
    )
    df_g5 = df_g5.reindex([n for n in top5_names if n in df_g5.index])

    categories = [CRITERIA_LABEL_CHART[c] for c in CRITERIA]
    N      = len(categories)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    radar_colors  = ['#6D28D9', '#EC4899', '#10B981', '#F59E0B', '#3B82F6']
    line_styles   = ['-', '--', '-.', ':', '-']
    marker_styles = ['o', 's', '^', 'D', 'P']

    for i, ban in enumerate(df_g5.index):
        vals = df_g5.loc[ban, CRITERIA].tolist()
        vals += vals[:1]
        color = radar_colors[i % len(radar_colors)]
        ax.plot(
            angles, vals,
            linestyle=line_styles[i % len(line_styles)],
            marker=marker_styles[i % len(marker_styles)],
            linewidth=2.5, markersize=6,
            color=color, label=ban, zorder=5 - i,
        )
        ax.fill(angles, vals, alpha=0.10, color=color)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=8.5, color=P_DEEP, fontweight='600')
    ax.set_ylim(0, None)
    ax.set_yticks([])
    ax.spines['polar'].set_color(P_SPNE)
    ax.grid(color=P_SPNE, linewidth=0.8)
    ax.set_title('Profil Top 5 Ban per Kriteria',
                 fontsize=13, fontweight='700', color=P_DEEP, pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.55, 1.18),
              fontsize=7.5, framealpha=0.9, edgecolor=P_SPNE)
    plt.tight_layout()
    return fig


def chart_heatmap(df_raw):
    """Grafik 4: Heatmap korelasi antar kriteria."""
    crit_available = [c for c in CRITERIA if c in df_raw.columns]

    fig, ax = plt.subplots(figsize=(9, 6))
    fig.patch.set_facecolor(BG)

    corr = df_raw[crit_available].corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    cmap = sns.diverging_palette(280, 150, s=80, l=55, as_cmap=True)

    sns.heatmap(
        corr, mask=mask, annot=True, fmt='.2f', cmap=cmap,
        xticklabels=[CRITERIA_LABEL_CHART[c] for c in crit_available],
        yticklabels=[CRITERIA_LABEL_CHART[c] for c in crit_available],
        ax=ax, linewidths=0.5, linecolor=P_GRID,
        annot_kws={'size': 8, 'weight': '600'},
        vmin=-1, vmax=1,
    )
    ax.set_title('Korelasi Antar Kriteria',
                 fontsize=12, fontweight='700', color=P_DEEP, pad=12)
    ax.tick_params(colors=P_DEEP, labelsize=8)
    plt.xticks(rotation=30, ha='right')
    plt.tight_layout()
    return fig


def chart_harga_pie_top5(ranking, df_grouped):
    """Grafik: Donut/Pie chart proporsi Harga Asli Top 5."""
    top5 = ranking.head(5)
    names = top5[ALTERNATIVE_COL].tolist()
    df_g5 = df_grouped[df_grouped[ALTERNATIVE_COL].isin(names)].set_index(ALTERNATIVE_COL)
    df_g5 = df_g5.reindex([n for n in names if n in df_g5.index])

    prices = df_g5['OriginalPrice'].values
    short_names = [n.split(' (')[0] for n in names]
    colors = ['#534AB7', '#1D9E75', '#D85A30', '#BA7517', '#7F77DD']

    fig, ax = plt.subplots(figsize=(7, 5))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    wedges, texts, autotexts = ax.pie(
        prices,
        labels=None,
        autopct='%1.1f%%',
        colors=colors,
        startangle=90,
        wedgeprops=dict(width=0.55, edgecolor='white', linewidth=2),
        pctdistance=0.75,
    )
    for at in autotexts:
        at.set_fontsize(8)
        at.set_color('white')
        at.set_fontweight('600')

    ax.legend(
        wedges,
        [f'{n}  Rp {p:,.0f}' for n, p in zip(short_names, prices)],
        loc='lower center',
        bbox_to_anchor=(0.5, -0.18),
        ncol=2, fontsize=7.5,
        framealpha=0.9, edgecolor=P_SPNE,
    )
    ax.set_title('Proporsi Harga Asli — Top 5 Alternatif',
                 fontsize=12, fontweight='700', color=P_DEEP, pad=12)
    plt.tight_layout()
    return fig


def chart_scatter_top5(ranking, df_grouped):
    """Grafik: Scatter plot Rating vs Skor SAW Top 5."""
    top5 = ranking.head(5)
    names = top5[ALTERNATIVE_COL].tolist()
    scores = top5['Score'].tolist()

    df_g5 = df_grouped[df_grouped[ALTERNATIVE_COL].isin(names)].set_index(ALTERNATIVE_COL)
    ratings = [df_g5.loc[n, 'Rating'] for n in names if n in df_g5.index]

    colors  = ['#534AB7', '#1D9E75', '#D85A30', '#BA7517', '#7F77DD']
    markers = ['o', '^', 's', 'D', 'P']
    short   = [n.split(' (')[0] for n in names]

    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor(BG)
    _base_ax(ax)

    for i, (r, s, c, m, lbl) in enumerate(zip(ratings, scores, colors, markers, short)):
        ax.scatter(r, s, color=c, marker=m, s=110, zorder=5, label=f'#{i+1} {lbl}')
        ax.annotate(f'#{i+1}', (r, s),
                    textcoords='offset points', xytext=(7, 4),
                    fontsize=7.5, color=c, fontweight='600')

    ax.set_xlabel('Rating', fontsize=9, color=P_MID)
    ax.set_ylabel('Skor SAW', fontsize=9, color=P_MID)
    ax.set_title('Rating vs Skor SAW — Top 5 Alternatif',
                 fontsize=12, fontweight='700', color=P_DEEP, pad=12)
    ax.legend(loc='lower right', fontsize=7.5, framealpha=0.9, edgecolor=P_SPNE)
    ax.grid(color=P_GRID, linewidth=0.5)
    plt.tight_layout()
    return fig
