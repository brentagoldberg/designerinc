
import pandas as pd
import numpy as np
import pickle
from pymongo import MongoClient
from src.create_model import model

def predict(item):
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)

    item['prediction'] = model.predict(item)

    item = item.rename(index=str, columns={"product_id": "_id"}).to_dict('records')[0]

    return new_data['prediction'], new_data['_id']

    client = MongoClient()
    db = client.results
    collection = db.test_collection
    collection.insert(new_data)
    print(collection.find_one(_id))

if __name__ == '__main__':
    predict(item)