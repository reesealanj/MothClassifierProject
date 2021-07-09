import io
import matplotlib.pyplot as plt
import numpy as np
import os
import requests
import shutil
import tensorflow as tf
from pathlib import Path
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from utils import extract_dataset, filter_dataset, limit_dataset, print_metadata
import zipfile

"""
Name
Model Type: DETECTOR/CLASSIFIER
Rating: 0-100
Comments
"""


class MModel:

    # Initializes machine learning model with an 80-20 image validation split
    # If a trained model also exists, it can be directly loaded into the MModel class
    def __init__(
        self, m_name, m_type, comment, num_classes, f_url=None, f_name=None, batch_size=32, model=None
    ):
        self.name = m_name
        self.model_type = m_type
        self.comments = comment
        self.num_classes = num_classes
        self.txtfile = self.name + '_class_names.txt'
        if model is None:
            # Retrieve dataset directory
            _, image_dir = extract_dataset(f_url, f_name)

            # Filter dataset
            image_dir = filter_dataset(image_dir, num_classes-1)
            print_metadata(image_dir)
            # Set picture capacity on dataset folders
            image_dir, img_count = limit_dataset(image_dir, 1500)

            # Initialize training and validation datasets
            self.temp_ds = tf.keras.preprocessing.image_dataset_from_directory(
                image_dir,
                validation_split=0.2,
                subset='training',
                seed=123,
                image_size=(180, 180),
                batch_size=batch_size,
            )

            train_percent = int(round(img_count * 0.8, 0))
            validate_percent = int(round(img_count * 0.2, 0))
            self.train_ds = self.temp_ds.take(train_percent)
            self.validate_ds = self.temp_ds.take(validate_percent)

            self.test_ds = tf.keras.preprocessing.image_dataset_from_directory(
                image_dir,
                validation_split=0.2,
                subset='validation',
                seed=123,
                image_size=(180, 180),
                batch_size=batch_size,
            )

            self.class_names = self.temp_ds.class_names

            with open(self.txtfile, 'w') as f:
                for name in self.class_names:
                    f.write("%s\n" % name)

            AUTOTUNE = tf.data.experimental.AUTOTUNE
            self.train_ds = (
                self.train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
            )
            self.validate_ds = self.validate_ds.cache().prefetch(buffer_size=AUTOTUNE)
        else:
            with open(self.txtfile) as f:
                self.class_names = f.read().splitlines()
            self.load(model)

    # Prints out build summary and information to be sent to API
    def __str__(self):
        self.model.summary()
        return f'\nName: {self.name} \nModel Type: {self.model_type} \nRating: {self.rating:.3f} \nComments: {self.comments}'

    # Builds image classification model with a default 80-20 split. The model uses data augmentation before processing images.
    def train(self, epochs):

        normalization_layer = layers.experimental.preprocessing.Rescaling(1.0 / 255)

        # Image augmentation of picture and orientation
        data_augmentation = keras.Sequential(
            [
                layers.experimental.preprocessing.RandomFlip(
                    'horizontal', input_shape=(180, 180, 3)
                ),
                layers.experimental.preprocessing.RandomRotation(0.1),
                layers.experimental.preprocessing.RandomZoom(0.1),
            ]
        )

        # Groups a stack of layers for the model
        self.model = Sequential(
            [
                data_augmentation,
                layers.experimental.preprocessing.Rescaling(1.0 / 255),
                layers.Conv2D(16, 3, padding='same', activation='relu'),
                layers.MaxPooling2D(pool_size=(2, 2)),
                layers.Conv2D(16, 3, padding='same', activation='relu'),
                layers.MaxPooling2D(pool_size=(2, 2)),
                layers.Conv2D(32, 3, padding='same', activation='relu'),
                layers.MaxPooling2D(pool_size=(2, 2)),
                layers.Conv2D(32, 3, padding='same', activation='relu'),
                layers.MaxPooling2D(pool_size=(2, 2)),
                layers.Conv2D(64, 3, padding='same', activation='relu'),
                layers.MaxPooling2D(pool_size=(2, 2)),
                layers.Conv2D(64, 3, padding='same', activation='relu'),
                layers.MaxPooling2D(pool_size=(2, 2)),
                layers.Dropout(0.2),
                layers.Flatten(),
                layers.Dense(128, activation='relu'),
                layers.Dense(self.num_classes),
            ]
        )

        self.model.compile(
            optimizer='adam',
            loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
            metrics=['accuracy'],
        )

        train_history = self.model.fit(
            self.train_ds, validation_data=self.validate_ds, epochs=epochs
        )

        result = self.model.evaluate(self.test_ds)
        print('Test Loss, Test Accuracy: ', result)
        self.rating = train_history.history['val_accuracy'][0] * 100

        # Saves model with given name
        self.model.save(self.name + '.h5')

        loss = train_history.history['loss']
        val_loss = train_history.history['val_loss']
        plt.plot(loss)
        plt.plot(val_loss)
        plt.legend(['loss', 'val_loss'])
        plt.show()

    def load(self, file):
        self.model = tf.keras.models.load_model(file)

    # Function that tests a single input image on the trained AI
    def test(self, url = None, name = None, is_local = False):
        image_path = None;
        if not is_local:
            image_path = tf.keras.utils.get_file(name, origin=url)
        else: 
            image_path = url
        img = keras.preprocessing.image.load_img(image_path, target_size=(180, 180))
        img_array = keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)

        predictions = self.model.predict(img_array)
        score = tf.nn.softmax(predictions[0])

        print(
            f'Class: {self.class_names[np.argmax(score)]}, Image: {url}, {100 * np.max(score) : .2f} percent confidence.'
        )
        if not is_local:
            os.remove(image_path)
        return self.class_names[np.argmax(score)], round(100 * np.max(score), 3)


    # Extract and test a zip file of images
    def test_zip(self, url):
        # Extract and save zip file
        print('Extracting zipfile...')
        keras_path = os.path.expanduser(os.path.join('~', '.keras'))
        path = os.path.join(keras_path, 'test_folder')
        r = requests.get(url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(path)
        path = os.path.join(path, 'images/Test Moth')
        test_dir = os.listdir(path)
        # Test each image in zip file
        data_dictionary = {}
        for file in test_dir:
            image_path = os.path.join(path, file)
            img = keras.preprocessing.image.load_img(image_path, target_size=(180, 180))
            img_array = keras.preprocessing.image.img_to_array(img)
            img_array = tf.expand_dims(img_array, 0)

            predictions = self.model.predict(img_array)
            score = tf.nn.softmax(predictions[0])

            print(
                f'Class: {self.class_names[np.argmax(score)]}, {100 * np.max(score) : .2f} percent confidence.'
            )
            # Add test image to dictionary
            data_dictionary['Prediction: ' + self.class_names[np.argmax(score)]] = image_path
            
            # Add example image to directory
            example_path = os.path.join(keras_path, 'moth_images/images/filter_dir', self.class_names[np.argmax(score)])
            data_dictionary[self.class_names[np.argmax(score)]] = os.path.join(keras_path, 'moth_images/images/filter_dir', self.class_names[np.argmax(score)], os.listdir(example_path)[0])
        
        # Plot prediction images next to actual images
        plt.figure(figsize=(8, 8))
        for i in range(len(data_dictionary)):
            plt.subplot((len(data_dictionary)/2), 2, i + 1)
            plt.imshow(plt.imread(list(data_dictionary.values())[i]))
            plt.title(list(data_dictionary)[i])
            plt.axis("off")
        plt.show()
    
    # Remove local data created from mmodel.py functions
    def clear(self):
        dir_path = str(Path.home()) + '/.keras'
        try:
            shutil.rmtree(dir_path)
        except OSError as e:
            print("Error: %s : %s" % (dir_path, e.strerror))
                