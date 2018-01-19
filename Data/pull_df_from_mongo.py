import pymongo
import pandas as pd
import numpy as np
 
# get connected to the database

def make_df():
    cl = pymongo.MongoClient()

    coll = cl.desinc_collection.products_db
    coll2 = cl.desinc_db.products_coll

    cursor = coll2.find()
    df = pd.DataFrame(list(cursor))
    return df

def main():
    return make_df()

if __name__ == '__main__':
    main()