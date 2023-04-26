from rest_framework import viewsets
from django.http import HttpResponse



from .serializers import CsvfileSerializer,PdfprogressSerializer
from .models import Csvfile,Pdfprogress


class CsvfileViewSet(viewsets.ModelViewSet):
    queryset = Csvfile.objects.all()
    serializer_class = CsvfileSerializer
    def post(self, request, *args, **kwargs):
        file = request.data['file']
        title = request.data['title']
        Csvfile.objects.create(title=title, file=file)
        return HttpResponse({'message': 'Csvfile uploaded'}, status=200)
    
class PdfprogressViewSet(viewsets.ModelViewSet):
    queryset = Pdfprogress.objects.all()
    serializer_class = PdfprogressSerializer
    def post(self, request, *args, **kwargs):
        csvfile = request.data['csvfile']
        title = request.data['title']
        Pdfprogress.objects.create(title=title, csvfile=csvfile)
        return HttpResponse({'message':title+csvfile}, status=200)


