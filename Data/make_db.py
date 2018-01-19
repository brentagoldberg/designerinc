import pymongo
import pandas as pd
import numpy as np

def designerinc_mongodb():
    cl = pymongo.MongoClient()

    coll = cl.desinc_collection.products_db
    coll2 = cl.desinc_db.products_coll

    cursor = coll.find()

    cl.drop_database(cl.desinc_db)

    for doc in cursor:
        for key, val in doc.iteritems():
            if key == "_id":
                continue
            else:
                for i in val:
                    coll2.insert_one(i)

def main():
    designerinc_mongodb()
                    
if __name__ == '__main__':
    main()