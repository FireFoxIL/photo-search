import numpy as np
from index.models import ImageIndex, FaceIndex

from index.apps import MachineLearningModel
from index.models import FaceIndex

__all__ = ['upload_files', 'search_for_face']


def upload_files(request):
    for field in request.FILES.keys():
        for f in request.FILES.getlist(field):
            handle_image(f)


def handle_image(f):
    img = ImageIndex(image=f)
    img.save()

    img.image.open()
    for face_embedding in list_faces(img.image):
        face_embedding_l = face_embedding.tolist()
        face = FaceIndex(image_id=img, face_vector=face_embedding_l)
        face.save()

    img.image.close()


def list_faces(image):
    img = MachineLearningModel.face_reg.load_from_file(image)
    face_locations = MachineLearningModel.face_reg.locate_faces(img)

    if len(face_locations) == 0:
        # Ignoring empty
        face_encodings = []
    else:
        # Face extraction
        face_encodings = MachineLearningModel.face_reg.encode_faces(img, face_locations)

    return face_encodings


def search_for_face(request):
    fields = list(request.FILES.keys())
    if len(fields) == 0:
        return []
    f = request.FILES.getlist(fields[0])[:1]
    if f is None or len(f) == 0:
        return []
    f = f[0]

    f.open()
    img = MachineLearningModel.face_reg.load_from_file(f)
    f.close()

    face_vector = MachineLearningModel.face_reg.encode_face(img)

    face_information = {}
    for face in FaceIndex.objects.all():
        url = face.image_id.image.url
        face_vector = np.array(face.face_vector)
        face_information.setdefault(url, []).append(face_vector)

    urls = MachineLearningModel.face_reg.find_images_with_person(
        face_vector, face_information
    )

    return urls
