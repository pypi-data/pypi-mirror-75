import os
from pathlib import Path
from setuptools import setup


def read(file_name):
    with open(os.path.join(Path(os.path.dirname(__file__)), file_name)) as _file:
        return _file.read()


long_description = read('README.md')

setup(
    name='nkia',
    version='0.5.0',
    description='This is a module to predict the products category using artificial inteligence.',
    url='https://bitbucket.org/nksistemasdeinformacao/servicos-biodigital/src/master/',
    download_url='https://bitbucket.org/nksistemasdeinformacao/servicos-biodigital/src/master/',
    license='Apache License 2.0',
    author='NK Sistemas de Informacao em Saude',
    author_email='ti@nkodontologia.com.br',

    py_modules=['nkia/ml/classify_products', 'nkia/ml/cnn_nlp_model', 'utils/utils'],
    
    package_dir={'': 'src'},

    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['tensorflow', 'nlp', 'nk',
              'python3', 'cnn', 'food-products'],
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Communications :: Email',
    ],
    python_requires='>=3.6',
    install_requires=[
        'tensorflow==2.2.0',
        'numpy==1.19.0',
        'tensorflow-datasets==3.2.1',
        'Unidecode==1.1.1',
        'nltk==3.5',
        'gdown==3.12.0'
    ],
    extras_require={
        'dev': [
            'pytest>=3.7'
        ]
    }
)