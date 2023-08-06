import sys
import os
from sys import argv
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))

import tensorflow as tf
from sklearn.model_selection import train_test_split

from utils import utils
from database.db_mongo import MongoDatabase

class trainProductsClassifier(object):

    def __init__(self, environment, show_confusion_matrix=True):
        self.environment = environment
        self.confusion_matrix = show_confusion_matrix
        self.train_model()

    def train_model(self):
        utils.create_saved_model_folder('category_model')
        dataframe, y = self.get_data()
        X = self.get_previsors_attrib(dataframe)
        
        X_train, X_test, y_train, y_test = train_test_split(X,
                                                            y,
                                                            test_size=0.3,
                                                            stratify=y) 

        cnn = utils.create_model_instance(y, self.tokenizer)
        cnn.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath='./src/nkia/ml/saved_model/category_model/v1/model_checkpoint/cp.ckpt',
                                                        save_weights_only=True,
                                                        verbose=1)

        cnn.fit(X_train, y_train,
                batch_size = 64,
                epochs = 5,
                verbose = 1,
                validation_split = 0.10,
                callbacks=[cp_callback])

        utils.evaluate_model(cnn, X_test, y_test)

        if self.confusion_matrix:
            y_pred_test = cnn.predict(X_test)
            predicted = [result.argmax() for result in y_pred_test]
            utils.show_confusion_matrix(y_test, predicted)

    def get_data(self):
        self.open_mongo_connections()
        dataframe = utils.get_dataframe_from_mongo(self.mongo_conn)
        self.close_mongo_connection()

        dataframe['description'].fillna('', inplace=True)

        y = utils.encode_class_value(
            dataframe['Category'].values, './src/nkia/ml/saved_model/category_model/v1/label_encoder.pkl')

        print('Restored data from Mongo')
        sys.stdout.flush()
        return dataframe, y

    def open_mongo_connections(self):
        self.mongo = MongoDatabase(self.environment)
        self.mongo.connect()
        self.mongo_conn = self.mongo

    def close_mongo_connection(self):
        self.mongo.close_connection()

    def get_previsors_attrib(self, dataframe):
        ingredients = [x for x in dataframe['ingredients']] 
        # allergics = [x for x in dataframe['allergics']]
        description = [[x] for x in dataframe['description']]
        product_name = [[x] for x in dataframe['name']]

        X = utils.get_cleaned_predictor(ingredients, [], description, product_name)
        
        X, self.tokenizer = utils.preprocessing_fn(
            X, './src/nkia/ml/saved_model/category_model/v1/token')

        return X


trainProductsClassifier(argv[1] if len(argv) > 1 else 'dev')
