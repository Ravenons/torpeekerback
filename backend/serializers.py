from backend.models import Visit
from rest_framework import serializers

class VisitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Visit
        fields = ('url', 'is_ready', 'screenshot', 'ref')
