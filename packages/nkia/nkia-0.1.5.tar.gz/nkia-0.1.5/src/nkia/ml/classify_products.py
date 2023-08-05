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

    def inference_from_model(self, ingredients=[''], allergics=[''], description=[''], product_name=['']): 
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
        if 'model_checkpoint' not in os.listdir():
            self.download_model(
                'https://drive.google.com/u/1/uc?export=download&confirm=pgRf&id=1jDL1j1cdEAPr4avB19bsx-90nnuCv1-s', 'nlp_model.tar.gz')

        X = self.utils.get_cleaned_predictor([ingredients], [allergics], [description], [product_name])
        X = self.preprocessing_fn(X)

        label_encoder = self.get_label_encoder()

        cnn = CNN(vocab_size=self.tokenizer.vocab_size, emb_dim=300, nb_filters=100,
            ffn_units=256, nb_classes=29, dropout_rate=0.2)

        cnn.load_weights('./model_checkpoint/cp.ckpt')

        product_category = label_encoder.inverse_transform(
            [cnn(np.array(X), training=False).numpy().argmax()])[0]

        return product_category

    def download_model(self, url, output):
        gdown.download(url, output, quiet=False) 

        tar = tarfile.open(output)
        tar.extractall()
        tar.close()

    def preprocessing_fn(self, X):
        self.tokenizer = tfds.features.text.SubwordTextEncoder.load_from_file('token')
        tokenized_predictor = [self.tokenizer.encode(sentence) for sentence in  X] 

        return tokenized_predictor

    def get_label_encoder(self):
        pkl_encoder_file = open('label_encoder.pkl', 'rb')
        encoder = pickle.load(pkl_encoder_file) 
        pkl_encoder_file.close()
        return encoder

classifyProducts()