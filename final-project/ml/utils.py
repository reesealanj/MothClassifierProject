import os
from zipfile import ZipFile
import shutil
import tensorflow as tf


def extract_dataset(url, dataset_name, save_dir=None):
    """
    Downloads the dataset located at url and extracts it to the specified directory
    Specific to the Moth Classifier API

    Parameters
    ----------
    url: str
        The url for the dataset
    dataset_name: str
        The name of the dataset. Creates a folder with that name in the save_dir that holds the dataset contents
    save_dir: str
        The base directory where the dataset should be saved (default is None). If it is None, then the default directory will be '~/.keras'

    Returns
    -------
    tuple
        A tuple of the dataset directory and its underlying images directory
    """

    if save_dir is None:
        save_dir = os.path.expanduser(os.path.join('~', '.keras'))
    save_dir = os.path.join(save_dir, dataset_name)
    dataset = tf.keras.utils.get_file(
        'training.zip', url, extract=True, cache_subdir=save_dir
    )
    print(dataset)
    # Extract all the files to save_dir
    with ZipFile(dataset, 'r') as zip_file:
        for file in zip_file.namelist():
            zip_file.extract(file, save_dir)

    # Clean up
    os.remove(os.path.join(save_dir, 'training.zip'))

    image_dir = os.path.join(save_dir, 'images')
    return save_dir, image_dir

def filter_dataset(path, num_classes):
    """
    Sorts a specified dataset by folder size. The sorted dataset is limited to a specified
    number of folders.

    Parameters
    ----------
    path: str
        The file path of the base directory
    num_classes: int
        The desired number of folders to use in the dataset

    Returns
    -------
    String
        A string of the original dataset directory that contains (num_classes) folders that are
        sorted by size.
    """
    im_dir = os.listdir(path)
    folders = {}
    file_names = []

    for file in im_dir:
        if file != '.DS_Store':
            folders[file] = len(os.listdir(os.path.join(path, file)))
    # Sorted dictionary of folder names and size in descending order
    folders = sorted(folders.items(), key=lambda x: x[1], reverse=True)
    print(str(len(folders)) + " species in dataset")
    # Create new directory with filtered list of folders
    filter_dir = 'filter_dir'

    # Delete directory if it already exists
    if os.path.isdir(path + '/' + filter_dir):
        shutil.rmtree(path + '/' + filter_dir)

    new_path = os.path.join(path, filter_dir)
    # Create miscellaneous folder 
    miscellaneous = 'Miscellaneous'
    misc_path = os.path.join(new_path, miscellaneous)
    if os.path.isdir(misc_path):
        shutril.rmtree(misc_path)
    os.makedirs(misc_path)
    # Keep track of most populated classes and merge the least populated into a miscellaneous class
    spc_count = 0
    for count, x in enumerate(folders):
        if count < num_classes:
            file_names.append(x[0])
        else:
            temp_path = os.path.join(path, x[0])
            img_list = os.listdir(temp_path)
            for img in img_list:
                shutil.copyfile(os.path.join(temp_path, img), os.path.join(misc_path, img))


    # Copy folders into new filter_dir directory
    for x in file_names:
        shutil.copytree(os.path.join(path, x), os.path.join(new_path, x))
    return new_path

def limit_dataset(path, limit):
    img_count = 0
    limit_dir = 'limit_dir'
    new_path = os.path.join(path, limit_dir)

    if os.path.isdir(new_path):
        shutil.rmtree(new_path)

    os.mkdir(new_path)
    # print(val_path) #/validation_dir
    # List of image folders
    im_dir = os.listdir(path)
    for folder in im_dir:
        # Directory of training images
        new_folder_path = os.path.join(new_path, str(folder))
        os.mkdir(new_folder_path)

        # Number of pictures to be deleted
        temp = limit
        img_count += len(os.listdir(path + '/' + folder))

        for picture in os.listdir(path + '/' + folder):
            
            # Run loop until limit
            # Copy picture to new directory
            if temp == 0:
                break
            if ('.jpg' in picture or '.png' in picture) and temp > 0:
                pic_path = path + '/' + folder + '/' + picture
                shutil.copyfile(pic_path, os.path.join(new_folder_path, picture))
            temp -= 1
    return new_path, img_count
                
def print_metadata(path):
    print('------------------\nDirectory Metadata\n------------------')          
    print_dir = os.listdir(path)
    count = 0
    for folder in print_dir:
        print(str(folder) + ': ' + str(len(os.listdir(os.path.join(path, folder)))) + ' pictures')
        count += len(os.listdir(os.path.join(path, folder)))
    print('Total dataset size: ' + str(count) + ' pictures')

    

