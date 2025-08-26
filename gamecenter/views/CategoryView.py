from rest_framework import viewsets
from gamecenter.models import Category
from gamecenter.serializers import CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer