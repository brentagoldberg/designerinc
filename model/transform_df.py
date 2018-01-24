import sys
sys.path.append("..")
import Data.pull_df_from_mongo as pull_df
import pandas as pd
import numpy as np



def main():
    df = pull_df.main()
    transform_df = df_pipeline(df)
    return transform_df

def df_pipeline(df):
    ## drop cols
    drop_cols = ["_highlightResult",'_id','cleanSpecs','colors','diffbotUri','dimensions',
                 "hidden","in_page_variations","isbn","mpn","offerPriceDetails","overriddenStyles",
                 "pageUrl","prefixCode","priceRange","primaryImage","private", "processedCategory",
                 "processedImages","productId","productOrigin","projects","otherImages",
                 "regularPrice","regularPriceDetails","resolvedPageUrl","saveAmount","saveAmountDetails",
                 "shippingAmount","sku","specs","tradePrice","type","upc","url","variations",
                 "visibleVerified"]
    df.drop(drop_cols,axis=1,inplace=True)
    
    ## extract cols 
    col_name, grab_cols = 'normalizedDimensions', unique_dict_keys(df,'normalizedDimensions',{})['normalizedDimensions']
    df = df_extract_cols(df,col_name,grab_cols)
    df.drop(col_name,axis=1,inplace=True)
    
    col_name, grab_cols = 'hierarchicalCategories', unique_dict_keys(df,'hierarchicalCategories',{})['hierarchicalCategories']
    df = df_extract_cols(df,col_name,grab_cols)
    df.drop(col_name,axis=1,inplace=True)
    
    col_name, grab_cols = 'predominantColorsResult', unique_dict_keys(df,'predominantColorsResult',{})['predominantColorsResult']
    df = df_extract_cols(df,col_name,grab_cols)
    df.drop(col_name,axis=1,inplace=True)    
    
    df = extract_showroom_ids(df)
    
    df = category_fix(df)
    
    
    ## dummies for styles
    df = df_extract_styles(df)
    
    ## extract url from dictionary
    df = df_extract_url(df)
    
    ## clean text
    df = clean_text(df)
    
    
    ## clean column duplicates
    df = clean_cols(df)
    
    ## remove column name spaces
    df = df_remove_col_name_spaces(df)

    return df
    
        
def df_extract_cols(df,col_name,grab_cols):
    col_prefix = {"_highlightResult":"HR","normalizedDimensions":"dim","hierarchicalCategories":"Categories",
                 "predominantColorsResult":"color"}
    lst = list(df[col_name])
    for col in grab_cols:
        
        load_col = []
        for item in lst:
            try:
                if col in item.iterkeys():
                    if type(item[col]) == list:
                        item[col] = "".join(item[col])
                    load_col.append(item[col])
                else:
                    load_col.append(0)
            except:
                load_col.append(0)
        df["{}_{}".format(col_prefix[col_name],col)] = load_col
    return df

def df_extract_styles(df):

    check = df['_styles']

    categories = set()

    for category_group in set(check):
    
        try:
            lst = str(category_group).split(",")
            categories.update(lst)
        except:
            continue
    
    
    for category in list(categories):
        col = []
    
        for row in check:
            if str(category) in str(row):
                col.append(1)
            else:
                col.append(0)

        df['{}_style'.format(str(category))] = col
    
    return df

def extract_showroom_ids(df):
    check = df["showrooms"]
    col = []
    for idx,i in enumerate(check):
        if i in [[],np.nan]:
            col.append(0)
        else:
            lst = []
            for group in i:
                lst.append("id_{}".format(group["id"]))
            col.append(lst)
    df['showroom_ids'] = col


    showrm_ids = set()

    check = df['showroom_ids']
    c=0
    for showroom_ids in check:
        if showroom_ids == 0:
            c+=1
            continue
        else:
            for i in showroom_ids:
                showrm_ids.add(i)

    for i in list(showrm_ids):
        col = []
        for idx in check:
            if idx == 0:
                col.append(0)
            elif i in idx:
                col.append(1)
            else:
                col.append(0)
        df[i] = col
    return df



def clean_cols(df):
    df['Mid-Century_style'] = df['Mid Century_style'] + df['Mid-Century_style']
    df['c_style'] = df['Coastal _style'] + df['Coastal_style']
    df['Country_style'] = df['Country _style'] + df['Country_style']
    df['t_style'] = df['Transitional _style'] + df['Transitional_style']
    df.drop(['Transitional_style','Coastal_style'],axis=1,inplace=True)
    df['Transitional_style'] = [min(i,1) for i in df['t_style']]
    df['Coastal_style'] = [min(i,1) for i in df['c_style']]
    df['styles'] = df['_styles']
    comb = ['Mid Century_style','Coastal _style',"Country_style","_styles","Transitional _style","Coastal _style","c_style","t_style","nan_style"]
    df.drop(comb,axis=1,inplace=True)

    return df

def category_fix(df):
    check = list(df['Categories_lvl0'])
    df["Categories_lvl1"] = [i if i!=0 else check[idx] for idx,i in enumerate(df['Categories_lvl1'])]
    check = list(df['Categories_lvl1'])
    df["Categories_lvl2"] = [i if i!=0 else check[idx] for idx,i in enumerate(df['Categories_lvl2'])]
    
    check = list(df['Categories_lvl2'])
    df["Categories_lvl3"] = [i if i!=0 else check[idx] for idx,i in enumerate(df['Categories_lvl3'])]
    return df

def unique_dict_keys(df,col,uniques):
    check = df[col]
    uniques[col] = set()
    for i in check:
        if i in [check[0],{},np.nan]:
            continue
        else:
            for dim,val in i.iteritems():
                uniques[col].add(dim)
    return uniques

def df_extract_url(df):
    col = []
    for row in df['images']:
        try:
            col.append(row[0]['url'])
        except:
            col.append(0)
    df['images'] = col
    return df

def clean_text(df):
    df["new_text"] = df['text'].fillna('')
    return df

def df_remove_col_name_spaces(df):
    cols = list(df.columns)
    for idx,col in enumerate(cols):
        if " " in str(col):
            cols[idx] = str(col).replace(" ","")
        else:
            cols[idx] = str(col)
    df.columns = cols
    return df


if __name__ == "__main__":
    main()