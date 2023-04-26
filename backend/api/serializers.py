from rest_framework import serializers

from .models import Csvfile,Pdfprogress

class CsvfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Csvfile
        fields = ['title', 'file']
        
class PdfprogressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pdfprogress
        fields = ['title', 'csvfile']