CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=DM+Serif+Display:ital@0;1&display=swap');

:root {
    --purple-deep:  #3B0764;
    --purple-mid:   #6D28D9;
    --purple-light: #A78BFA;
    --purple-soft:  #EDE9FE;
    --purple-pale:  #F5F3FF;
    --lavender:     #C4B5FD;
    --text-dark:    #1E1B4B;
    --text-mid:     #4C1D95;
}

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif !important;
    background-color: #FAFAFA !important;
    color: var(--text-dark) !important;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2.5rem !important; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--purple-deep) 0%, #4C1D95 60%, #5B21B6 100%) !important;
}
[data-testid="stSidebar"] * { color: white !important; }
[data-testid="stSidebar"] label {
    color: var(--lavender) !important;
    font-weight: 500 !important;
    font-size: 0.82rem !important;
}

/* Tombol */
.stButton > button {
    background: linear-gradient(135deg, var(--purple-mid), #9333EA) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 1.8rem !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    box-shadow: 0 4px 16px rgba(109,40,217,0.3) !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(109,40,217,0.4) !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    overflow: hidden !important;
    box-shadow: 0 4px 20px rgba(109,40,217,0.1) !important;
}

/* Tab */
.stTabs [data-baseweb="tab-list"] {
    background: var(--purple-pale) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 9px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    color: var(--text-mid) !important;
    padding: 0.5rem 1.2rem !important;
}
.stTabs [aria-selected="true"] {
    background: var(--purple-mid) !important;
    color: white !important;
}

/* Komponen reusable */
.hero-banner {
    background: linear-gradient(135deg, var(--purple-deep) 0%, var(--purple-mid) 45%, #9333EA 75%, #C084FC 100%);
    border-radius: 20px;
    padding: 2.5rem 3rem;
    margin-bottom: 1.8rem;
    box-shadow: 0 20px 60px rgba(109,40,217,0.35);
}
.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.15);
    color: white;
    padding: 0.25rem 0.85rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
    border: 1px solid rgba(255,255,255,0.2);
}
.hero-title {
    font-family: 'DM Serif Display', serif !important;
    font-size: 2.8rem;
    color: white;
    margin: 0;
    line-height: 1.1;
}
.hero-subtitle {
    font-size: 1rem;
    color: var(--lavender);
    margin-top: 0.5rem;
}

.section-header {
    font-family: 'DM Serif Display', serif !important;
    font-size: 1.5rem;
    color: var(--purple-deep);
    margin: 1.5rem 0 0.75rem 0;
}
.section-divider {
    height: 2px;
    background: linear-gradient(90deg, var(--purple-mid), var(--lavender), transparent);
    border: none;
    border-radius: 2px;
    margin-bottom: 1rem;
}

.metric-row  { display: flex; gap: 1rem; margin-bottom: 1.5rem; flex-wrap: wrap; }
.metric-card {
    background: white;
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    flex: 1; min-width: 160px;
    box-shadow: 0 2px 16px rgba(109,40,217,0.08);
    border-left: 4px solid var(--purple-mid);
}
.metric-card.rose { border-left-color: #D946EF; }
.metric-card.mint { border-left-color: #10B981; }
.metric-card.sky  { border-left-color: #3B82F6; }
.metric-value { font-size: 1.9rem; font-weight: 700; color: var(--purple-deep); line-height: 1; }
.metric-label { font-size: 0.78rem; color: #6B7280; font-weight: 500; margin-top: 0.25rem; }

.info-box {
    background: linear-gradient(135deg, #EDE9FE, #F5F3FF);
    border-left: 4px solid var(--purple-mid);
    border-radius: 10px;
    padding: 1rem 1.25rem;
    margin: 0.75rem 0;
    font-size: 0.88rem;
    color: var(--text-dark);
}

.step-badge {
    display: inline-flex;
    align-items: center; justify-content: center;
    width: 28px; height: 28px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--purple-mid), #9333EA);
    color: white; font-weight: 700; font-size: 0.8rem;
    margin-right: 0.5rem; flex-shrink: 0;
}
.step-row {
    display: flex; align-items: flex-start; gap: 0.5rem;
    padding: 0.6rem 0;
    border-bottom: 1px solid var(--purple-soft);
}

.weight-chips { display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 0.75rem 0; }
.chip {
    background: var(--purple-pale);
    border: 1px solid var(--lavender);
    border-radius: 999px;
    padding: 0.25rem 0.75rem;
    font-size: 0.78rem; font-weight: 600;
    color: var(--purple-mid);
}

.top3-container { display: flex; gap: 1rem; margin: 1rem 0; flex-wrap: wrap; }
.top3-card {
    flex: 1; min-width: 180px;
    border-radius: 16px; padding: 1.4rem;
    text-align: center;
}
.top3-card.gold   { background: linear-gradient(135deg, #FEF3C7, #FDE68A); border: 2px solid #F59E0B; }
.top3-card.silver { background: linear-gradient(135deg, #F1F5F9, #E2E8F0); border: 2px solid #94A3B8; }
.top3-card.bronze { background: linear-gradient(135deg, #FEF0E6, #FDDCBE); border: 2px solid #D97706; }
.top3-rank  { font-size: 2rem; }
.top3-name  { font-weight: 700; font-size: 0.9rem; color: var(--text-dark); margin: 0.35rem 0 0.2rem; }
.top3-score { font-size: 1.1rem; font-weight: 800; color: var(--purple-deep); }

.sidebar-logo {
    text-align: center;
    padding: 1.5rem 0 1rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    margin-bottom: 1.5rem;
}

.profile-card {
    background: white; border-radius: 16px; padding: 1.5rem;
    box-shadow: 0 4px 20px rgba(109,40,217,0.1);
    border-top: 4px solid var(--purple-mid);
    text-align: center;
}
.profile-avatar {
    width: 72px; height: 72px; border-radius: 50%;
    background: linear-gradient(135deg, var(--purple-mid), #9333EA);
    display: flex; align-items: center; justify-content: center;
    font-size: 2rem; margin: 0 auto 1rem;
}
.profile-name { font-weight: 700; font-size: 1rem; color: var(--purple-deep); }
.profile-nim  { font-size: 0.82rem; color: #6B7280; margin-top: 0.2rem; }
</style>
"""
