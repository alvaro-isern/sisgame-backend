from rest_framework import serializers
from gamecenter.models import ProductMaintenance, Product


class ProductMaintenanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductMaintenance
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar productos solo de categorías con grupos 'dispositivos' y 'accesorios'
        self.fields['product'].queryset = Product.objects.filter(
            category__group__in=['dispositivos', 'accesorios'],
            is_active=True
        ).select_related('category')

    def validate_product(self, value):
        """
        Validar que el producto seleccionado pertenezca solo a categorías 
        con grupos 'dispositivos' o 'accesorios', excluyendo 'comestibles'
        """
        if not value.category or value.category.group not in ['dispositivos', 'accesorios']:
            raise serializers.ValidationError(
                'Solo se pueden realizar mantenimientos a productos de categorías '
                'del grupo "dispositivos" y "accesorios". No se permiten productos '
                'del grupo "comestibles".'
            )
        return value
