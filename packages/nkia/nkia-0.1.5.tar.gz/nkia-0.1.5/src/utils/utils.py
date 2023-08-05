import pandas as pd
import pymongo
import unidecode
import re 
import string
import nltk

def get_dataframe_from_mongo(mongo_conn):
    products_df = mongo_conn.db.df_products.find({}).sort('created', pymongo.DESCENDING)
    
    if products_df:
        return pd.DataFrame(products_df[0]['df'])

    return ''

def get_cleaned_predictor(ingredients, allergics, description, product_name):
    ingredients_and_allergics = list(map(get_ingredients_and_allergics, ingredients, allergics))
    description = list(map(get_description_and_name, description))
    product_name = list(map(get_description_and_name, product_name))

    X = join_all_predictors(ingredients_and_allergics, description, product_name)

    return X

def get_ingredients_and_allergics(ingredients, allergics):
    ingredients += allergics if allergics != '[]' else ''   
    ingredient = list(map(lambda x: unidecode.unidecode(x).lower(), ingredients))
    
    return ' '.join(ingredient)

def get_description_and_name(data):    
    stop_words = nltk.corpus.stopwords.words('portuguese')

    data = unidecode.unidecode(data[0]).lower()
    data = re.sub(r'['+string.punctuation+']', '', data)
    data = [plv for plv in data.split() if plv not in stop_words]
    
    return ' '.join(data)   

def join_all_predictors(ingredients_and_allergics, description, product_name):
    count = 0
    X = []

    for name in product_name:
        X.append(name + ' ' + description[count] + ' ' + ingredients_and_allergics[count])
        count += 1

    return X