import sys
import os
from sys import argv
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))

import tensorflow_datasets as tfds
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import pickle

import utils.utils as utils
from database.db_mongo import MongoDatabase
from nkia.ml.cnn_nlp_model import CNN

class trainProductsClassifier(object):

    def __init__(self, environment):
        self.utils = utils
        self.environment = environment
        self.train_model()

    def train_model(self):
        dataframe, y = self.get_data()
        X = self.get_previsors_attrib(dataframe)
        
        X_train, X_test, y_train, y_test = train_test_split(X,
                                                            y,
                                                            test_size=0.3) 

        cnn = self.create_model_instance(y)
        cnn.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath='./src/nkia/ml/saved_model/nlp_model/model_checkpoint/cp.ckpt',
                                                        save_weights_only=True,
                                                        verbose=1)

        cnn.fit(X_train, y_train,
                batch_size = 64,
                epochs = 1,
                verbose = 1,
                validation_split = 0.10,
                callbacks=[cp_callback])

        self.evaluate_model(cnn, X_test, y_test)

    def get_data(self):
        self.open_mongo_connections()
        dataframe = self.utils.get_dataframe_from_mongo(self.mongo_conn)
        self.close_mongo_connection()

        dataframe['allergics'].fillna('[]', inplace=True)
        dataframe['description'].fillna('', inplace=True)

        y = self.encode_class_value(dataframe['Category'].values)

        print('Restored data from Mongo')
        sys.stdout.flush()
        return dataframe, y

    def open_mongo_connections(self):
        self.mongo = MongoDatabase(self.environment)
        self.mongo.connect()
        self.mongo_conn = self.mongo

    def close_mongo_connection(self):
        self.mongo.close_connection()

    def encode_class_value(self, class_value):
        encoder = LabelEncoder()
        y = encoder.fit_transform(class_value)

        output_encoder = open('./src/nkia/ml/saved_model/nlp_model/label_encoder.pkl', 'wb')
        pickle.dump(encoder, output_encoder)
        output_encoder.close()
        
        return y

    def get_previsors_attrib(self, dataframe):
        ingredients = [x for x in dataframe['ingredients']] 
        allergics = [x for x in dataframe['allergics']]
        description = [[x] for x in dataframe['description']]
        product_name = [[x] for x in dataframe['name']]

        X = self.utils.get_cleaned_predictor(ingredients, allergics, description, product_name)
        
        X = self.preprocessing_fn(X)

        return X

    def preprocessing_fn(self, X):
        X = self.tokenize_data(X)
        X = self.padding_matrix(X)

        print('Preprocessing_fn finished')
        sys.stdout.flush()
        return X

    def tokenize_data(self, data):
        self.tokenizer = tfds.features.text.SubwordTextEncoder.build_from_corpus(
            data, target_vocab_size=2**14)

        self.tokenizer.save_to_file('./src/nkia/ml/saved_model/nlp_model/token')
        data = [self.tokenizer.encode(sentence) for sentence in data]

        return data

    def padding_matrix(self, data):
        max_sentence_len = max([len(sentence) for sentence in data])
        data = tf.keras.preprocessing.sequence.pad_sequences(data,
                                                             value=0,
                                                             padding='post',
                                                             maxlen=max_sentence_len)

        return data

    def create_model_instance(self, y):
        vocab_size = self.tokenizer.vocab_size
        nb_classes = len(set(y))

        cnn = CNN(vocab_size=vocab_size, emb_dim=300, nb_filters=100,
            ffn_units=256, nb_classes=nb_classes, dropout_rate=0.2)

        print('Created model instance')
        sys.stdout.flush()
        return cnn
    
    def evaluate_model(self, cnn, X_test, y_test, vz_results=False):
        results = cnn.evaluate(X_test, y_test, batch_size=64)
        print('Loss and Accuracy: ', results)

        if vz_results:
            y_pred_test = cnn.predict(X_test)
            predicted = [result.argmax() for result in y_pred_test]
            fig, ax = plt.subplots(figsize=(10,10))
            cm = confusion_matrix(y_test, predicted)
            sns.heatmap(cm, annot=True, vmin=0, vmax=1)
            plt.show()


trainProductsClassifier(argv[1] if len(argv) > 1 else 'dev')
