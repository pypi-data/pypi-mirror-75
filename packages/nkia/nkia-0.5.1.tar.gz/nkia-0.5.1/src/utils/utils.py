import pandas as pd
import pymongo
import unidecode
import re 
import string
import nltk
import sys
import tensorflow_datasets as tfds
import tensorflow as tf
import pickle
import os
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from nkia.ml.cnn_nlp_model import CNN

def get_dataframe_from_mongo(mongo_conn):
    products_df = mongo_conn.db.df_products.find({}).sort('created', pymongo.DESCENDING)
    
    if products_df:
        return pd.DataFrame(products_df[0]['df'])

    return ''

def get_cleaned_predictor(ingredients, allergics, description, product_name):
    ingredients_and_allergics = list(map(get_ingredients_and_allergics, ingredients))
    description = list(map(get_description_and_name, description))
    product_name = list(map(get_description_and_name, product_name))

    X = join_all_predictors(ingredients_and_allergics, description, product_name)

    return X

def get_ingredients_and_allergics(ingredients):
    # ingredients += allergics if allergics != '[]' else ''   
    ingredient = list(map(lambda x: unidecode.unidecode(x).lower(), ingredients))
    
    return ' '.join(ingredient)

def get_description_and_name(data):    
    stop_words = nltk.corpus.stopwords.words('portuguese')

    data = unidecode.unidecode(data[0]).lower()
    data = re.sub(r'['+string.punctuation+']', '', data)
    data = [word for word in data.split() if word not in stop_words]
    
    return ' '.join(data)   

def join_all_predictors(ingredients_and_allergics, description, product_name):
    count = 0
    X = []

    for name in product_name:
        X.append(name + ' ' + description[count] + ' ' + ingredients_and_allergics[count])
        count += 1

    return X

def preprocessing_fn(X, token_path):
    X, tokenizer = tokenize_data(X, token_path)
    X = padding_matrix(X)

    print('Preprocessing_fn finished')
    sys.stdout.flush()
    return X, tokenizer

def tokenize_data(data, token_path):
    tokenizer = tfds.features.text.SubwordTextEncoder.build_from_corpus(
        data, target_vocab_size=2**14)

    tokenizer.save_to_file(token_path)
    data = [tokenizer.encode(sentence) for sentence in data]

    return data, tokenizer

def padding_matrix(data):
    max_sentence_len = max([len(sentence) for sentence in data])
    data = tf.keras.preprocessing.sequence.pad_sequences(data,
                                                            value=0,
                                                            padding='post',
                                                            maxlen=max_sentence_len)

    return data

def encode_class_value(class_value, encoder_path):
    encoder = LabelEncoder()
    y = encoder.fit_transform(class_value)

    output_encoder = open(encoder_path, 'wb')
    pickle.dump(encoder, output_encoder)
    output_encoder.close()
    
    return y

def evaluate_model(cnn, X_test, y_test):
    results = cnn.evaluate(X_test, y_test, batch_size=64)
    print('Loss and Accuracy: ', results)

def show_confusion_matrix(y_test, predicted):
    fig, ax = plt.subplots(figsize=(10,10))
    cm = confusion_matrix(y_test, predicted)
    sns.heatmap(cm, annot=True)
    plt.show()

def create_model_instance(y, tokenizer):
    vocab_size = tokenizer.vocab_size
    nb_classes = len(set(y))

    cnn = CNN(vocab_size=vocab_size, emb_dim=300, nb_filters=100,
        ffn_units=256, nb_classes=nb_classes, dropout_rate=0.2)

    print('Created model instance')
    sys.stdout.flush()
    return cnn

def create_saved_model_folder(model_name):
    if 'saved_model' not in os.listdir('./src/nkia/ml/'):
        os.makedirs('./src/nkia/ml/saved_model/' + model_name + '/v1')
    elif model_name not in os.listdir('./src/nkia/ml/saved_model'):
        os.makedirs('./src/nkia/ml/saved_model/' + model_name + '/v1')
    