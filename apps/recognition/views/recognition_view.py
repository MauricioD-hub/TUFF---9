from django.shortcuts import render
from apps.recognition.services.face_recognition_service import FaceRecognitionService
from apps.recognition.models.person import FaceImage

face_service = FaceRecognitionService()

def upload_and_recognize(request):
    context = {}

    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']

        embedding = face_service.get_embedding(image)
        
        if embedding is not None:
            person = face_service.find_best_match(embedding)

            if person:
                face_image = FaceImage.objects.filter(person=person).first()

                context['recognized'] = {
                    'nombre': person.nombre,
                    'apellidos': person.apellidos,
                    'dni': person.dni,
                    'foto': face_image.imagen.url if face_image else None,
                }
            else:
                context['error'] = "No se encontró coincidencia."
        else:
            context['error'] = "No se detectó ninguna cara en la imagen subida."

    return render(request, 'recognition/upload.html', context)
