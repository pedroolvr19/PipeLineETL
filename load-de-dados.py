import pandas as pd
import os
from sqlalchemy import create_engine
import time


db_user = 'postgres'
db_pass = '123456'
db_name = 'ecommerce_db'
db_host = 'ecommerce-etl-project:us-central1:ecommerce-etl-project'


connection_string = f'postgresql://{db_user}:{db_pass}@{db_host}/{db_name}'


engine = create_engine(connection_string)


def load_data_to_sql(file_path, table_name, chunksize=10000):
    print(f"Carregando {table_name}...")
    

    for chunk in pd.read_csv(file_path, chunksize=chunksize):
 
        chunk = chunk.fillna({col: '' for col in chunk.select_dtypes(include=['object']).columns})
 
        date_columns = [col for col in chunk.columns if 'date' in col or 'timestamp' in col]
        for date_col in date_columns:
            chunk[date_col] = pd.to_datetime(chunk[date_col], errors='coerce')
        
  
        chunk.to_sql(table_name, engine, if_exists='append', index=False)
        print(f"  Carregados {len(chunk)} registros")
        time.sleep(1)  
    
    print(f"Concluído carregamento de {table_name}")


files_to_tables = {
    'olist_customers_dataset.csv': 'customers',
    'olist_products_dataset.csv': 'products',
    'olist_orders_dataset.csv': 'orders',
    'olist_order_items_dataset.csv': 'order_items',
    'olist_sellers_dataset.csv': 'sellers'
}

for file, table in files_to_tables.items():
    file_path = os.path.join('data', file)
    load_data_to_sql(file_path, table)

print("Todos os dados foram carregados com sucesso!")