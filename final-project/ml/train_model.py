import h5py
import numpy as np
import os, os.path
import pathlib
import shutil
import sys
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

sys.path.append('.')
from mmodel import MModel


def main():
    moth_model = MModel(
        '5_species_model',
        'CLASSIFIER',
        '5 species + miscellaneous',
        6,
        model='5_species_model.h5',
        # f_url='https://www.mothclassifier.org/api/v1/images/download/?is_training=true',
        # f_name='moth_images',
    )

    # moth_model.train(200)
    # moth_model.test_dir()
    moth_model.test(url='http://167.172.31.118:8000/images/Phigalia%20denticulata/hSyjWWcV7BbeDKtHj7KnZqKSohF2_1617757299638..jpg', name = 'Test', is_local = False)
    moth_model.test(url='hypoprepiafucosa.jpeg', is_local = True)
    moth_model.test(url='Melanolophia-signataria.jpeg', is_local = True)
    moth_model.test(url='microcrambus.jpeg', is_local = True)
    moth_model.test(url='phigaliastrigataria.jpeg', is_local = True)
    
    
    moth_model.clear()
main()

