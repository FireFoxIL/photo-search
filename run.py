import argparse
import os
import numpy as np

from utils import load_images, load_face_information, load_image, cache_face_information
from core import process_images, encode_face, find_images_with_person

cache_file = '/cache.pickle'


def main(path_to_person, path_to_storage, to_show):
    if os.path.exists(path_to_storage + cache_file):
        face_information = load_face_information(path_to_storage + cache_file)
    else:
        images = load_images(path_to_storage)
        face_information = process_images(images)
        cache_face_information(face_information, path_to_storage + cache_file)

    person_image = load_image(path_to_person)
    person_encoding = encode_face(person_image).reshape(1, -1)

    image_names_founded = find_images_with_person(person_encoding, face_information)

    print(image_names_founded)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Processes images and searches for given person', allow_abbrev=False)

    parser.add_argument('--person', action='store', help='Path to image of person to be searched', required=True)
    parser.add_argument('--storage', action='store', help='Directory with images', required=True)
    parser.add_argument('--show', action='store_true', help='Show founded pictures')

    args = parser.parse_args()

    main(args.person, args.storage, args.show)
