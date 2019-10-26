import os
import glob
import cv2
import json
import pickle

from tqdm import tqdm


def load_images(path, image_type='.jpg'):
    images = {}
    for file_path in glob.glob(os.path.join(path, f'*{image_type}')):
        images[file_path] = cv2.imread(file_path)
        # Convert BGR to RGB
        images[file_path] = images[file_path][:, :, ::-1]
    return images


def load_image(path):
    image = cv2.imread(path)
    cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image


def new_load_images(glob_path):
    images = []
    for file_path in glob.glob(glob_path):
        images.append(cv2.imread(file_path))
        # Convert BGR to RGB
        images[-1] = cv2.cvtColor(images[-1], cv2.COLOR_BGR2RGB)
    return images


def use_tqdm(iterable, desc=None, total=None):
    total = total or len(iterable)
    return tqdm(iterable, total=total, desc=desc, ncols=100, position=0, leave=True)


def cache_face_information(face_information, path):
    with open(path, 'wb') as f:
        pickle.dump(face_information, f)


def load_face_information(path):
    with open(path, 'rb') as f:
        res = pickle.load(f)
        return res
