from django.db import models
from django.contrib.auth.models import User


class TimeStampedModel(models.Model):
    """Abstracto: agrega created_at / updated_at."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Person(TimeStampedModel):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=25, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="person_user")
    is_client = models.BooleanField(default=False)
    client_type = models.CharField(max_length=50, choices=[
        ("regular", "Regular"),
        ("premium", "Premium"),
        ("vip", "VIP"),
    ], blank=True, null=True)

    def __str__(self):
        return self.name


class ConsoleType(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class LocalSetting(TimeStampedModel):  # Configuración por tipo de dispositivo
    company_name = models.CharField(max_length=255)
    currency = models.CharField(max_length=10, default="USD")
    minimum_time = models.PositiveIntegerField(help_text="Tiempo mínimo (minutos) para alquilar / jugar")

    def __str__(self):
        return f"{self.company_name} - {self.device_type.name}"


class Game(TimeStampedModel):
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=50, choices=[
        ("action", "Acción"),
        ("adventure", "Aventura"),
        ("rpg", "RPG"),
        ("shooter", "Shooter"),
        ("sports", "Deportes"),
    ])
    release_year = models.PositiveIntegerField()  # Solo año
    description = models.TextField(blank=True)
    game_material_type = models.CharField(max_length=50, choices=[
        ("digital", "Digital"),
        ("fisico", "Físico"),
    ])
    is_active = models.BooleanField(default=True, db_index=True)

    def __str__(self):
        return self.name

class ConsoleTypeGame(TimeStampedModel):
    console_type = models.ForeignKey(ConsoleType, on_delete=models.CASCADE, related_name="console_games")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="console_types")

    class Meta:
        unique_together = ("console_type", "game")

    def __str__(self):
        return f"{self.console_type.name} - {self.game.name}"


class Category(TimeStampedModel):
    group = models.CharField(max_length=100) 
    name = models.CharField(max_length=255)

    class Meta:
        unique_together = ("group", "name")

    def __str__(self):
        return f"{self.group}:{self.name}"


class Product(TimeStampedModel):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="product_category")
    image = models.URLField(null=True, blank=True)
    console_type = models.ForeignKey(ConsoleType, on_delete=models.PROTECT, related_name="product_console_type")
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        unique_together = ("name", "category")

    def __str__(self):
        return self.name

class Price(TimeStampedModel):
    unit_measurement = models.CharField(max_length=100, choices=[
        ("unidad", "Unidad"),
        ("min", "Minutos"),
    ])
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - {self.unit_measurement}"
    

class Lots(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="lots_product")
    lot_number = models.CharField(max_length=100, null=True, blank=True)
    manufacturing_date = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    initial_stock = models.PositiveIntegerField(null=True, blank=True)
    current_stock = models.PositiveIntegerField(default=0, null=True, blank=True)
    price = models.ForeignKey(Price, on_delete=models.CASCADE, related_name="lots_price", null=True, blank=True)
    state = models.CharField(max_length=50, choices=[
        ("available", "Disponible"),
        ("unavailable", "No disponible"),
    ])
    entry_date = models.DateField(null=True, blank=True)
    observations = models.TextField(blank=True)

    class Meta:
        unique_together = ("product", "lot_number")

    def __str__(self):
        return f"Lot {self.lot_number} - {self.product.name}"

class ConsoleReservations(TimeStampedModel):
    client = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="reservations_client")
    lots = models.OneToOneField(Lots, on_delete=models.CASCADE, related_name="reservations_lots")
    reservation_date = models.DateField(auto_now_add=True)
    hour_count = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    start_hour = models.DateTimeField(null=True, blank=True)
    end_hour = models.DateTimeField(null=True, blank=True)
    state = models.CharField(max_length=50, choices=[
        ("reservado", "Reservado"),
        ("cancelado", "Cancelado"),
    ], default="reservado")
    advance_payment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

class ConsoleMaintenance(TimeStampedModel):
    console = models.ForeignKey(ConsoleType, on_delete=models.CASCADE, related_name="maintenance_console")
    maintenance_date = models.DateField(auto_now_add=True)
    maintenance_reason = models.CharField(max_length=255, choices=[
        ("reparación", "Reparación"),
        ("limpieza", "Limpieza"),
    ])
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    responsible = models.CharField(max_length=255, null=True, blank=True)
    observations = models.TextField(null=True, blank=True)

class Session(TimeStampedModel):
    lots = models.OneToOneField(Lots, on_delete=models.CASCADE, related_name="sessions_lots")
    hour_count = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    session_date = models.DateField(auto_now_add=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    state = models.CharField(max_length=50, choices=[
        ("en curso", "En curso"),
        ("finalizado", "Finalizado"),
    ], default="en curso")

    def __str__(self):
        return f"Sesión {self.id} - {self.client}"

    
class SalesBox(TimeStampedModel):
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    initial_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True, db_index=True)

    def __str__(self):
        return f"Caja {self.id} ({self.name})"


class OpeningSalesBox(TimeStampedModel):
    sales_box = models.ForeignKey(SalesBox, on_delete=models.CASCADE, related_name="opening_sales_box")
    user = models.ForeignKey(Person, on_delete=models.PROTECT, related_name="opening_sales_box")
    opening_date = models.DateField(auto_now_add=True)
    opening_amount = models.DecimalField(max_digits=10, decimal_places=2)
    closing_date = models.DateField(null=True, blank=True)
    closing_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Apertura de Caja {self.sales_box.id} - {self.user.username}"


class Sale(TimeStampedModel):
    client = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="sales_client")
    user = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="sales_user")
    opening_sales_box = models.ForeignKey(OpeningSalesBox, on_delete=models.CASCADE, related_name="sales")
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="sales_session", null=True, blank=True)
    date_sale = models.DateField(auto_now_add=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    igv = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_method = models.CharField(max_length=50, choices=[
        ("efectivo", "Efectivo"),
        ("tarjeta", "Tarjeta"),
        ("transferencia", "Transferencia"),
    ], null=True, blank=True)
    state = models.CharField(max_length=50, choices=[
        ("pendiente", "Pendiente"),
        ("completado", "Completado"),
        ("cancelado", "Cancelado"),
    ], default="pendiente")

    def __str__(self):
        return f"Venta {self.id} - {self.client}"



