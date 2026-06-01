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

    # Bersihkan harga
    df['Selling Price']  = pd.to_numeric(
        df['Selling Price'].astype(str).str.replace(',', '').str.extract(r'(\d+)')[0],
        errors='coerce'
    )
    df['Original Price'] = pd.to_numeric(
        df['Original Price'].astype(str).str.replace(',', '').str.extract(r'(\d+)')[0],
        errors='coerce'
    )

    # Ekstrak ukuran velg dari kolom Size (contoh: "165/80 R 14" → 14)
    df['VelgSize'] = df['Size'].astype(str).str.extract(r'R\s*(\d+)').astype(float)

    # Konversi kolom numerik
    df['Load Index'] = pd.to_numeric(df['Load Index'], errors='coerce')
    df['Rating']     = pd.to_numeric(df['Rating'],     errors='coerce')

    # Isi missing value
    df['Selling Price']  = df['Selling Price'].fillna(df['Selling Price'].median())
    df['Original Price'] = df['Original Price'].fillna(df['Original Price'].median())
    df['VelgSize']       = df['VelgSize'].fillna(df['VelgSize'].median())
    df['Load Index']     = df['Load Index'].fillna(df['Load Index'].median())
    df['Rating']         = df['Rating'].fillna(df['Rating'].mean())

    # Bersihkan string
    df['Size']       = df['Size'].astype(str).str.strip()
    df['Tyre Brand'] = df['Tyre Brand'].astype(str).str.strip()
    df['Model']      = df['Model'].astype(str).str.strip()

    # Agregasi per Tyre Brand + Model + Size → 488 alternatif unik
    df_agg = df.groupby(['Tyre Brand', 'Model', 'Size']).agg(
        SellingPrice=('Selling Price',  'mean'),
        OriginalPrice=('Original Price', 'mean'),
        LoadIndex=('Load Index',        'max'),
        Rating=('Rating',               'mean'),
        VelgSize=('VelgSize',           'max'),
    ).reset_index()

    # Buat kolom NamaBan sebagai identitas alternatif
    df_agg[ALTERNATIVE_COL] = (
        df_agg['Tyre Brand'] + ' ' + df_agg['Model'] + ' (' + df_agg['Size'] + ')'
    )

    # Simpan kolom filter untuk sidebar
    df_agg['TyreBrand'] = df_agg['Tyre Brand']

    return df_agg


def run_saw(df, weights):
    """
    Langkah:
      1. Bentuk matriks keputusan dari data teragregasi
      2. Normalisasi: benefit r_ij = x_ij/max | cost r_ij = min/x_ij
      3. Nilai preferensi: V_i = sum(w_j * r_ij)
      4. Ranking dari V_i tertinggi

    Return:
      df_grouped — matriks keputusan
      df_norm    — matriks ternormalisasi + Score
      df_ranked  — hasil akhir terurut dengan kolom Peringkat
    """

    # Susun matriks dari data teragregasi 
    alternative = df[ALTERNATIVE_COL].values
    n_alt  = len(alternative)
    n_crit = len(CRITERIA)

    matriks = np.zeros((n_alt, n_crit))
    for j, col in enumerate(CRITERIA):
        matriks[:, j] = df[col].values.astype(float)

    df_grouped = pd.DataFrame(matriks, columns=CRITERIA)
    df_grouped.insert(0, ALTERNATIVE_COL, alternative)

    # Normalisasi
    R = np.zeros((n_alt, n_crit))
    for j in range(n_crit):
        attr_type = ATTRIBUTE_TYPES.get(CRITERIA[j], 'benefit')

        if attr_type == 'benefit':
            max_val = 0.0
            for i in range(n_alt):
                if matriks[i][j] > max_val:
                    max_val = matriks[i][j]
            for i in range(n_alt):
                R[i][j] = matriks[i][j] / max_val if max_val != 0 else 0.0

        else:  # cost
            min_val = matriks[0][j]
            for i in range(1, n_alt):
                if matriks[i][j] < min_val:
                    min_val = matriks[i][j]
            for i in range(n_alt):
                R[i][j] = min_val / matriks[i][j] if matriks[i][j] != 0 else 0.0

    df_norm = pd.DataFrame(R, columns=CRITERIA)
    df_norm.insert(0, ALTERNATIVE_COL, alternative)

    # Nilai preferensi
    weight_array = np.array([weights[c] for c in CRITERIA])

    V = np.zeros(n_alt)
    for i in range(n_alt):
        skor = 0.0
        for j in range(n_crit):
            skor += weight_array[j] * R[i][j]
        V[i] = skor

    df_norm['Score'] = V

    # Ranking 
    urutan    = np.argsort(V)[::-1]
    df_ranked = df_norm.iloc[urutan].reset_index(drop=True)
    df_ranked.insert(0, 'Peringkat', range(1, n_alt + 1))

    return df_grouped, df_norm, df_ranked
