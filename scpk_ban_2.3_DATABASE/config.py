CRITERIA = [
    'SellingPrice',
    'OriginalPrice',
    'LoadIndex',
    'Rating',
    'VelgSize',
]

CRITERIA_LABEL = {
    'SellingPrice':  '💰 Harga Jual',
    'OriginalPrice': '🏪 Harga Asli',
    'LoadIndex':     '🏋️ Load Index',
    'Rating':        '⭐ Rating',
    'VelgSize':      '🔧 Ukuran Velg (R)',
}
                
ATTRIBUTE_TYPES = {
    'SellingPrice':  'cost',
    'OriginalPrice': 'cost',
    'LoadIndex':     'benefit',
    'Rating':        'benefit',
    'VelgSize':      'benefit',
}

DEFAULT_WEIGHTS = {
    'SellingPrice':  0.25,
    'OriginalPrice': 0.15,
    'LoadIndex':     0.20,
    'Rating':        0.20,
    'VelgSize':      0.20,
}

# Kolom identifikasi alternatif
ALTERNATIVE_COL = 'NamaBan'


# Konfigurasi Database MySQL 
DB_CONFIG = {
    "host":     "localhost",
    "user":     "root",
    "password": "", 
    "database": "spk_ban",
}
