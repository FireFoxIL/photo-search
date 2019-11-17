import os
import glob
import cv2
import json
import pickle
import re

from tqdm import tqdm


def load_images(path, image_type='.jpg'):
    images = {}
    for file_path in glob.glob(os.path.join(path, f'*{image_type}')):
        images[file_path] = load_image(file_path)
    return images


def load_image(path):
    image = cv2.imread(path)
    cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image


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


class ImageLoader:
    """Lazy image loader."""
    def __init__(self, path, image_type='.jpg',
                 return_full_path=True, sort_numerically=True):
        self.image_paths = glob.glob(os.path.join(path, f'*{image_type}'))
        if sort_numerically:
            self.image_paths = sorted(self.image_paths, key=self.__num_keys)
        self.return_full_path = return_full_path
    
    
    def __num_keys(self, s):
        """Key values for proper numerical sort of strings."""
        key = []
        for c in re.split('(\d+)', s):
            key.append(int(c) if c.isdigit() else c)
        return key
            

    def __len__(self):
        return len(self.image_paths)


    def __iter__(self):
        for img_path in self.image_paths:
            yield self.__return_path_and_img(img_path)


    def __return_path_and_img(self, img_path):
        # handle slices
        if isinstance(img_path, list):
            return [self.__return_path_and_img(path) for path in img_path]
#             for path in img_path:
#                 yield self.__return_path_and_img(path)
        else:
            img = load_image(img_path)
            if not self.return_full_path:
                img_path = os.path.split(img_path)[1]
            return img_path, img


    def __getitem__(self, ind):
        img_path = self.image_paths[ind]
        return self.__return_path_and_img(img_path)
