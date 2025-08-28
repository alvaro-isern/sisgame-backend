from django.db.models import Q, Count, Case, When, IntegerField
from gamecenter.models import Product, Category, Lots, Session, ConsoleMaintenance
from decimal import Decimal
from datetime import datetime


def get_devices_status():
    """
    Función que devuelve el estado de todos los dispositivos de gaming
    agrupados por tipo de consola con sus estadísticas y detalles.
    
    Returns:
        dict: Estructura JSON con el estado de los dispositivos
    """
    
    # Obtener la categoría de dispositivos
    try:
        devices_category = Category.objects.get(group="dispositivos")
    except Category.DoesNotExist:
        return {}
    
    # Obtener todos los productos activos de la categoría dispositivos
    devices = Product.objects.filter(
        category=devices_category,
        is_active=True
    ).prefetch_related('lots_product__price')
    
    result = {}
    
    for device in devices:
        device_name = device.name
        
        # Obtener todos los lotes del dispositivo
        lots = Lots.objects.filter(
            product=device,
            state="available"
        ).select_related('price')
        
        # Inicializar contadores
        available_count = 0
        in_use_count = 0
        maintenance_count = 0
        devices_list = []
        
        for lot in lots:
            # Determinar el estado del dispositivo
            device_status = get_device_status(lot)
            
            # Contar por estado
            if device_status == "available":
                available_count += 1
            elif device_status == "in_use":
                in_use_count += 1
            elif device_status == "maintenance":
                maintenance_count += 1
            
            # Obtener precio por hora
            hourly_rate = "0.00"
            if lot.price and lot.price.unit_measurement == "hora":
                hourly_rate = str(lot.price.sale_price)
            
            # Crear el objeto del dispositivo
            device_info = {
                "id": lot.id,
                "name": f"{device_name} #{lot.lot_number or lot.id}",
                "status": device_status,
                "hourly_rate": hourly_rate,
                "image": device.image or ""
            }
            
            devices_list.append(device_info)
        
        # Solo agregar al resultado si hay dispositivos
        if devices_list:
            result[device_name] = {
                "available": available_count,
                "in_use": in_use_count,
                "maintenance": maintenance_count,
                "devices": devices_list
            }
    
    return result


def get_device_status(lot):
    """
    Determina el estado actual de un dispositivo específico.
    
    Args:
        lot (Lots): El lote del dispositivo
        
    Returns:
        str: Estado del dispositivo ('available', 'in_use', 'maintenance')
    """
    
    # Verificar si está en mantenimiento
    active_maintenance = ConsoleMaintenance.objects.filter(
        console=lot.product,
        start_date__lte=datetime.now().date(),
        end_date__isnull=True
    ).exists()
    
    if active_maintenance:
        return "maintenance"
    
    # Verificar si está en uso (sesión activa)
    active_session = Session.objects.filter(
        lots__lots=lot,
        state="en curso"
    ).exists()
    
    if active_session:
        return "in_use"
    
    # Si no está en mantenimiento ni en uso, está disponible
    return "available"


def get_devices_status_json():
    """
    Función helper que devuelve el estado de los dispositivos en formato JSON.
    
    Returns:
        dict: Estructura JSON con el estado de los dispositivos
    """
    return get_devices_status()
