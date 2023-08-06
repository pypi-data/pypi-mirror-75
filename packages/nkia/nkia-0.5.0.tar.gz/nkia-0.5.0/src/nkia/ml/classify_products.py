import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))

import tensorflow_datasets as tfds
import pickle
import numpy as np
import tarfile
import gdown

import utils.utils as utils
from nkia.ml.cnn_nlp_model import CNN

class classifyProducts(object):

    def __init__(self):
        self.utils = utils

    def load_model_to_memory(self, model_name):
        if 'category_model' not in os.listdir():
            self.download_model(
                'https://drive.google.com/u/1/uc?export=download&confirm=pr2B&id=1ZYDT0sWE0XMK-reUnkYDPoJFi1NZt-za', 'category_model.tar.gz')

        if 'food_model' not in os.listdir():
            self.download_model(
                'https://drive.google.com/u/1/uc?export=download&confirm=8g0K&id=1cC5i6hplYq3j13plJc3x6BcvmEskC_bp', 'food_model.tar.gz')

        self.tokenizer = tfds.features.text.SubwordTextEncoder.load_from_file(
            './' + model_name +'/v1/token')

        nb_classes = 29 if model_name == 'category_model' else 2

        cnn = CNN(vocab_size=self.tokenizer.vocab_size, emb_dim=300, nb_filters=100,
            ffn_units=256, nb_classes=nb_classes, dropout_rate=0.2)

        cnn.load_weights('./' + model_name +'/v1/model_checkpoint/cp.ckpt').expect_partial()
        return cnn

    def inference_from_category_model(
        self, model, ingredients=[''], allergics=[''], description=[''], product_name=['']): 
        """
        This method is responsible to infer the product category based on your caracteristics. Pass just one product
        by time.

        Args:
            ingredients (list): ['água açúcar baunilha']
            allergics (list): ['contém glúten, pode conter nozes']
            description (list):  ['Esse produto é simplesmente fantástico']
            product_name (list):  ['energético sabor baunilha']

        Returns:
            str: Category name. e.g: 'Bebidas não alcoolicas'

        """     
        X = self.utils.get_cleaned_predictor([ingredients], [allergics], [description], [product_name])
        X = self.preprocessing_fn(X, './category_model/v1/token')

        label_encoder = self.get_label_encoder('./category_model/v1/label_encoder.pkl')

        product_category = label_encoder.inverse_transform(
            [model(np.array(X), training=False).numpy().argmax()])[0]

        return product_category

    def inference_from_food_model(self, model, product_name):
        """
        This method is responsible to infer if a product is a food or not. Pass just one product
        by time.

        Args:
            product_name (list):  ['energético sabor baunilha']

        Returns:
            str: food or not food.

        """     
        X = self.utils.get_description_and_name(product_name)
        X = self.preprocessing_fn([X], './food_model/v1/token')

        label_encoder = self.get_label_encoder('./food_model/v1/label_encoder.pkl')

        product_type = model(np.array(X), training=False).numpy()
        product_type = 1 if product_type > 0.5 else 0

        return label_encoder.inverse_transform([product_type])[0] 

    def download_model(self, url, output):
        gdown.download(url, output, quiet=False) 

        tar = tarfile.open(output)
        tar.extractall()
        tar.close()

    def preprocessing_fn(self, X, token_path):
        self.tokenizer = tfds.features.text.SubwordTextEncoder.load_from_file(token_path)
        tokenized_predictor = [self.tokenizer.encode(sentence) for sentence in  X] 

        return tokenized_predictor

    def get_label_encoder(self, encoder_path):
        pkl_encoder_file = open(encoder_path, 'rb')
        encoder = pickle.load(pkl_encoder_file) 
        pkl_encoder_file.close()
        return encoder

classifyProducts()