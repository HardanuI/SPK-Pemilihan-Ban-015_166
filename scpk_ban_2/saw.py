# modules/saw.py — Logika SAW dengan perhitungan manual (NumPy)
# Alternatif: Tyre Brand + Model + Size (488 kombinasi unik)

import pandas as pd
import numpy as np
from config import CRITERIA, ATTRIBUTE_TYPES, ALTERNATIVE_COL


def load_data(filepath='Car_Tyres_Dataset_Clean.csv'):
    """
    Baca CSV, preprocessing, lalu agregasi per Tyre Brand + Model + Size.
    Menghasilkan 488 alternatif unik (>250 sesuai ketentuan).
    """
    df = pd.read_csv(filepath)
    df.columns = df.columns.str.strip()

    # 1. Bersihkan harga
    df['Selling Price']  = pd.to_numeric(
        df['Selling Price'].astype(str).str.replace(',', '').str.extract(r'(\d+)')[0],
        errors='coerce'
    )
    df['Original Price'] = pd.to_numeric(
        df['Original Price'].astype(str).str.replace(',', '').str.extract(r'(\d+)')[0],
        errors='coerce'
    )

    # 2. Ekstrak ukuran velg dari kolom Size (contoh: "165/80 R 14" → 14)
    df['VelgSize'] = df['Size'].astype(str).str.extract(r'R\s*(\d+)').astype(float)

    # 3. Konversi kolom numerik
    df['Load Index'] = pd.to_numeric(df['Load Index'], errors='coerce')
    df['Rating']     = pd.to_numeric(df['Rating'],     errors='coerce')

    # 4. Isi missing value
    df['Selling Price']  = df['Selling Price'].fillna(df['Selling Price'].median())
    df['Original Price'] = df['Original Price'].fillna(df['Original Price'].median())
    df['VelgSize']       = df['VelgSize'].fillna(df['VelgSize'].median())
    df['Load Index']     = df['Load Index'].fillna(df['Load Index'].median())
    df['Rating']         = df['Rating'].fillna(df['Rating'].mean())

    # 5. Bersihkan string
    df['Size']       = df['Size'].astype(str).str.strip()
    df['Tyre Brand'] = df['Tyre Brand'].astype(str).str.strip()
    df['Model']      = df['Model'].astype(str).str.strip()

    # 6. Agregasi per Tyre Brand + Model + Size → 488 alternatif unik
    df_agg = df.groupby(['Tyre Brand', 'Model', 'Size']).agg(
        SellingPrice=('Selling Price',  'mean'),
        OriginalPrice=('Original Price', 'mean'),
        LoadIndex=('Load Index',        'max'),
        Rating=('Rating',               'mean'),
        VelgSize=('VelgSize',           'max'),
    ).reset_index()

    # 7. Buat kolom NamaBan sebagai identitas alternatif
    df_agg[ALTERNATIVE_COL] = (
        df_agg['Tyre Brand'] + ' ' + df_agg['Model'] + ' (' + df_agg['Size'] + ')'
    )

    # Simpan kolom filter untuk sidebar
    df_agg['TyreBrand'] = df_agg['Tyre Brand']

    return df_agg


def run_saw(df, weights):
    # Matriks keputusan
    alternative = df[ALTERNATIVE_COL].values
    matriks = df[CRITERIA].astype(float).to_numpy()

    # Tampilkan matriks keputusan
    df_grouped = pd.DataFrame(matriks, columns=CRITERIA)
    df_grouped.insert(0, ALTERNATIVE_COL, alternative)

    # Normalisasi SAW
    R = np.zeros_like(matriks)

    for j, col in enumerate(CRITERIA):
        data = matriks[:, j]

        if ATTRIBUTE_TYPES.get(col, 'benefit') == 'benefit':
            R[:, j] = data / np.max(data)
        else:
            R[:, j] = np.min(data) / data

    # Bobot
    weight_array = np.array([weights[c] for c in CRITERIA])

    # Nilai preferensi SAW
    V = np.dot(R, weight_array)

    # Tabel normalisasi
    df_norm = pd.DataFrame(R, columns=CRITERIA)
    df_norm.insert(0, ALTERNATIVE_COL, alternative)
    df_norm["Score"] = V

    # Ranking
    df_ranked = (
        df_norm.sort_values("Score", ascending=False)
        .reset_index(drop=True)
    )
    df_ranked.insert(0, "Peringkat", range(1, len(df_ranked) + 1))

    return df_grouped, df_norm, df_ranked