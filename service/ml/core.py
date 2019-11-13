import cv2
import numpy as np

from keras_facenet import FaceNet
from mtcnn.mtcnn import MTCNN


class FaceRegModel(object):
    def __init__(self):
        self.model = MTCNN()
        self.embedder = FaceNet()

    @staticmethod
    def load_from_file(f):
        img_str = f.read()
        nparr = np.fromstring(img_str, np.uint8)
        img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
        return img_np

    def encode_face(self, img):
        location = self.locate_faces(img)[:1]
        face_img = self.extract_faces(img, location)
        return self.embedder.embeddings(face_img)[0]

    def encode_faces(self, img, locations):
        return self.embedder.embeddings(self.extract_faces(img, locations))

    def extract_faces(self, img, locations):
        res_imgs = []
        for (y1, x1, y2, x2) in locations:
            res_imgs.append(img[y1:y2, x2:x1])
        return res_imgs

    def locate_faces(self, img):
        faces = self.model.detect_faces(img)
        faces = [x['box'] for x in faces]
        faces = [(max(y, 0),
                  min(x + w, img.shape[1]),
                  min(y + h, img.shape[0]),
                  max(x, 0)) for x, y, w, h in faces]
        return np.array(faces)

    @staticmethod
    def face_distance(face1, face2):
        return np.linalg.norm(face1 - face2, axis=1)

    @staticmethod
    def compare_faces(face1, face2, tolerance=0.9):
        return list(FaceRegModel.face_distance(face1, face2) <= tolerance)

    def process_images(self, images, scale=0.5):
        """Get face locations and encodings from given images."""
        face_information = {}

        for (img_name, img) in images.items():
            # Scale down for faster processing
            small_img = cv2.resize(img, (0, 0), fx=scale, fy=scale)

            # Face detection
            face_locations = self.locate_faces(small_img)
            if len(face_locations) == 0:
                # Ignoring empty
                face_encodings = []
            else:
                # Face extraction
                face_encodings = self.encode_faces(small_img, face_locations)

            face_information[img_name] = {
                'locations': face_locations,
                'encodings': face_encodings
            }

        return face_information

    def find_images_with_person(self, face_encoding, face_information):
        images_with_person = []
        for img_name, face_info in face_information.items():
            face_info_encodings = face_info

            if len(face_info_encodings) == 0:
                continue

            matches = self.compare_faces(face_encoding, face_info_encodings)

            if any(matches):
                images_with_person.append(img_name)

        return images_with_person
