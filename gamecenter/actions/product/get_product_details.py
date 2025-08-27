from gamecenter.models import Product, Price, Lots
from django.db.models import Sum

def get_product_details(search_query=None, category_id=None):
    """
    Obtiene detalles de productos con filtros opcionales
    
    Args:
        search_query (str): Término de búsqueda para filtrar productos por nombre
        category_id (int): ID de la categoría para filtrar productos
    """
    products = Product.objects.all()

    # Aplicar filtro de búsqueda si existe
    if search_query:
        products = products.filter(name__icontains=search_query)

    # Aplicar filtro de categoría si existe
    if category_id:
        products = products.filter(category_id=category_id)

    result = []
    
    for product in products:
        latest_price = Price.objects.filter(
            product=product
        ).order_by('-created_at').first()
        
        current_stock = Lots.objects.filter(
            product=product
        ).aggregate(total=Sum('current_stock'))['total'] or 0
        
        product_data = {
            'id': product.id,
            'name': product.name,
            'category': product.category.name,
            'category_id': product.category.id,
            'price': {
                'sale_price': str(latest_price.sale_price) if latest_price else None,
                'unit_measurement': latest_price.unit_measurement if latest_price else None
            },
            'current_stock': current_stock,
            'status': "Activo" if product.is_active else "Inactivo"
        }
        result.append(product_data)
    
    return result