import mysql.connector
import pandas as pd
from config import DB_CONFIG, ALTERNATIVE_COL


def get_connection():
    """Buat koneksi ke database MySQL."""
    return mysql.connector.connect(**DB_CONFIG)


# ── READ ─────────────────────────────────────────────────────────────────────

def fetch_all():
    """
    Ambil semua data dari DB, agregasi per Brand+Model+Size,
    kembalikan DataFrame siap pakai (format sama dengan load_data lama).
    """
    conn   = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tyre_data")
    rows   = cursor.fetchall()
    cursor.close()
    conn.close()

    df = pd.DataFrame(rows)
    if df.empty:
        return df

    # Rename agar sesuai config
    df = df.rename(columns={
        'tyre_brand':     'Tyre Brand',
        'model':          'Model',
        'size':           'Size',
        'selling_price':  'SellingPrice',
        'original_price': 'OriginalPrice',
        'load_index':     'LoadIndex',
        'rating':         'Rating',
        'velg_size':      'VelgSize',
    })

    # Agregasi per Brand + Model + Size
    df_agg = df.groupby(['Tyre Brand', 'Model', 'Size']).agg(
        SellingPrice=('SellingPrice',   'mean'),
        OriginalPrice=('OriginalPrice', 'mean'),
        LoadIndex=('LoadIndex',         'max'),
        Rating=('Rating',               'mean'),
        VelgSize=('VelgSize',           'max'),
    ).reset_index()

    df_agg[ALTERNATIVE_COL] = (
        df_agg['Tyre Brand'] + ' ' +
        df_agg['Model']      + ' (' +
        df_agg['Size']       + ')'
    )
    df_agg['TyreBrand'] = df_agg['Tyre Brand']

    return df_agg


# ── CREATE ────────────────────────────────────────────────────────────────────

def insert_data(tyre_brand, model, size,
                selling_price, original_price,
                load_index, rating, velg_size):
    """Tambah satu baris data ban baru ke database."""
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tyre_data
        (tyre_brand, model, size, selling_price, original_price, load_index, rating, velg_size)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (tyre_brand, model, size,
          selling_price, original_price,
          load_index, rating, velg_size))
    conn.commit()
    cursor.close()
    conn.close()


# ── UPDATE ────────────────────────────────────────────────────────────────────

def update_data(record_id, tyre_brand, model, size,
                selling_price, original_price,
                load_index, rating, velg_size):
    """Update data ban berdasarkan ID."""
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tyre_data SET
            tyre_brand     = %s,
            model          = %s,
            size           = %s,
            selling_price  = %s,
            original_price = %s,
            load_index     = %s,
            rating         = %s,
            velg_size      = %s
        WHERE id = %s
    """, (tyre_brand, model, size,
          selling_price, original_price,
          load_index, rating, velg_size,
          record_id))
    conn.commit()
    cursor.close()
    conn.close()


# ── DELETE ────────────────────────────────────────────────────────────────────

def delete_data(record_id):
    """Hapus data ban berdasarkan ID."""
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tyre_data WHERE id = %s", (record_id,))
    conn.commit()
    cursor.close()
    conn.close()


def fetch_raw():
    """Ambil semua data mentah (dengan ID) untuk keperluan Edit dan Delete."""
    conn   = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tyre_data ORDER BY id")
    rows   = cursor.fetchall()
    cursor.close()
    conn.close()
    return pd.DataFrame(rows)