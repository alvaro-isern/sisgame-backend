from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from gamecenter.models import Product
from gamecenter.serializers.ProductSerializer import ProductSerializer
from gamecenter.actions.product.get_product_details import get_product_details

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=['get'])
    def product_details(self, request):
        """
        Endpoint que muestra el detalle de productos incluyendo nombre, categoría,
        precio actual, stock actual y estado.
        
        Parámetros existentes:
            search (str): Término de búsqueda para filtrar productos por nombre
            category (int): ID de la categoría para filtrar productos
        """
        search_query = request.query_params.get('search', None)
        category_id = request.query_params.get('category', None)
        
        result = get_product_details(
            search_query=search_query,
            category_id=category_id
        )
        return Response(result)