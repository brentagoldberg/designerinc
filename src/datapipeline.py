import pandas as pd
import numpy as np
import re

furniture_finish = ['cherry','white','espresso', 'black','chrome','mahogony', 'walnut', 'oak','birch', 'gold', 'brass', 'beech', 'bronze', 'pine', 'silver']
upholstery_material = ["leather", "linen", "polyurethane", "polyester", "cotton", "vinyl", "velvet", "chenille", "microfiber", "wool", "faux leather"]
other_materials = ["wood", "plastic", "fabric", "metal", "rattan"]
materials = set()
materials.update(furniture_finish)
materials.update(upholstery_material)
materials.update(other_materials)

def pipeline(df):
    df = materials_dummy(df)
    df = transform(df)
    df = dummies(df)
    df = pick_dims(df)
    return df
    
def materials_dummy(df):
    for i in materials:
        df[i]=0
    ##### check to see appropriate idx vs prod_id coding ######
    for idx,prod_id in enumerate(df['product_id']):
        desc = []
        titl = []
        if df[df["product_id"] == prod_id]['description']:
            desc = df[idx]['description'].lower().split()
        if df[idx]['titl']:
            titl = df[idx]['title'].lower().split()
        texts = set()
        texts.update(desc)
        texts.update(titl)
        for i in materials:
            if i in texts:
                df[idx][i] = 1
    return df

def pick_dims(df):
    
    
    
    
    
    
    
if __name__ == '__main__':
    pipeline(df)
    
    
    
    