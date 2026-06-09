import pandas as pd
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="spk_ban"
)
cursor = conn.cursor()

df = pd.read_csv('Car_Tyres_Dataset_Clean.csv')
df.columns = df.columns.str.strip()
df['Selling Price']  = pd.to_numeric(df['Selling Price'].astype(str).str.replace(',',''), errors='coerce').fillna(0)
df['Original Price'] = pd.to_numeric(df['Original Price'].astype(str).str.replace(',',''), errors='coerce').fillna(0)
df['Load Index']     = pd.to_numeric(df['Load Index'], errors='coerce').fillna(0).astype(int)
df['Rating']         = pd.to_numeric(df['Rating'], errors='coerce').fillna(0)
df['VelgSize']       = df['Size'].astype(str).str.extract(r'R\s*(\d+)').astype(float).fillna(0).astype(int)
df['Tyre Brand']     = df['Tyre Brand'].str.strip()
df['Model']          = df['Model'].str.strip()
df['Size']           = df['Size'].str.strip()

for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO tyre_data 
        (tyre_brand, model, size, selling_price, original_price, load_index, rating, velg_size)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        row['Tyre Brand'], row['Model'], row['Size'],
        row['Selling Price'], row['Original Price'],
        int(row['Load Index']), row['Rating'], int(row['VelgSize'])
    ))

conn.commit()
cursor.close()
conn.close()
print(f"Selesai: {len(df)} baris diimport.")