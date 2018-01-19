import pandas as pd
import numpy as np
import psycopg2 as pg
 
# get connected to the database

def designerinc_dbs():
    connection = pg.connect(dbname='brent', user='brent', host='localhost', password='brent')

    cur = connection.cursor()

    table_names = ['addresses','categories',
                'categories_products','category_features','clients',
                   'companies','featured_items','invitations','order_items',
                   'orders','popular_items','products','projects','projects_collaborators',
                   'projects_products','proposal_product','proposals','saved_searches',
                   'schema_version','showrooms','showrooms_vendors','spring_session',
                   'spring_session_attributes','styles','user_addresses',
                   'users','vendors','vendors_styles']

    d = {}
    for i in table_names:
        cur.execute('SELECT * FROM {}'.format(i))
        the_data = cur.fetchall()
        colnames = [desc[0] for desc in cur.description]

        d[i] = pd.DataFrame(the_data)
        if len(d[i].columns) == len(colnames):
            d[i].columns = colnames
        
        df_transactions = pd.read_csv('/home/brent/Downloads/transactions_export.csv')
        
    return d

def designerinc_transactions_and_orders(d):
    d["transactions"] =  pd.read_csv('/home/brent/Downloads/transactions_export.csv')
    d["orders_exp"] = pd.read_csv('/home/brent/Downloads/orders_export.csv') 
    return d

def main():
    d = designerinc_dbs()
    d = designerinc_transactions_and_orders(d)
    return d

if __name__ == '__main__':
    return main()

