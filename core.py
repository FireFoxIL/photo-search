import cv2
import numpy as np
import matplotlib.pyplot as plt
from keras_facenet import FaceNet

from mtcnn.mtcnn import MTCNN

from utils import use_tqdm

model = MTCNN()
embedder = FaceNet()

plt.rcParams["figure.figsize"] = (15, 14) # (w, h)


def encode_face(img):
    location = locate_faces(img)[:1]
    face_img = extract_faces(img, location)
    return embedder.embeddings(face_img)[0]


def encode_faces(img, locations):
    return embedder.embeddings(extract_faces(img, locations))


def extract_faces(img, locations):
    res_imgs = []
    for (y1, x1, y2, x2) in locations:
        res_imgs.append(img[y1:y2, x2:x1])
    return res_imgs


def draw_faces(img, locations, verbose=True):
    res_img = img.copy()
    for (y1, x1, y2, x2) in locations:
        cv2.rectangle(res_img, (x1, y2), (x2, y1), (0, 255, 0), 8)
    if verbose:
        plt.imshow(res_img)
        plt.show()
    return res_img


def locate_faces(img):
    faces = model.detect_faces(img)
    faces = [x['box'] for x in faces]
    faces = [(max(y, 0),
              min(x+w, img.shape[1]),
              min(y+h, img.shape[0]),
              max(x, 0)) for x, y, w, h in faces]
    return np.array(faces)


def face_distance(face1, face2):
    return np.linalg.norm(face1 - face2, axis=1)


def compare_faces(face1, face2, tolerance=0.9):
    return list(face_distance(face1, face2) <= tolerance)


def process_images(images, scale=0.5):
    """Get face locations and encodings from given images."""
    face_information = {}

    for i, (img_name, img) in use_tqdm(enumerate(images.items()), desc="Processing faces in images", total=len(images)):
        # Scale down for faster processing
        small_img = cv2.resize(img, (0, 0), fx=scale, fy=scale)

        # Face detection
        face_locations = locate_faces(small_img)
        if len(face_locations) == 0:
            # Ignoring empty
            face_encodings = []
        else:
            # Face extraction
            face_encodings = encode_faces(small_img, face_locations)

        face_information[img_name] = {
            'locations': face_locations,
            'encodings': face_encodings
        }

    return face_information


def find_images_with_person(face_encoding, face_information):
    images_with_person = []
    for i, (img_name, face_info) in use_tqdm(enumerate(face_information.items()),
                                       desc=f'Finding images',
                                       total=len(face_information)):
        face_info_locations = face_info['locations']
        face_info_encodings = face_info['encodings']

        if len(face_info_locations) == 0 or len(face_info_encodings) == 0:
            continue

        matches = compare_faces(face_encoding, face_info_encodings)

        if any(matches):
            images_with_person.append(img_name)

    return images_with_person
