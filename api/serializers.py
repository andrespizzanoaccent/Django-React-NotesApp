from rest_framework.serializers import ModelSerializer
from .models import Note, Category


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class NoteSerializer(ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'
