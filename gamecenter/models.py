from django.db import models


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

    # Rol simple para evitar tablas extra (interno / cliente). Si se necesitan más
    # permisos, migrar a django.contrib.auth.User o un CustomUser.
    ROLE_INTERNAL = "internal"
    ROLE_CLIENT = "client"
    ROLE_CHOICES = [
        (ROLE_INTERNAL, "Interno"),
        (ROLE_CLIENT, "Cliente"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_CLIENT)

    def __str__(self):
        return self.name


class User(TimeStampedModel):  # Usuario interno que opera el sistema/caja
    person = models.OneToOneField(Person, on_delete=models.CASCADE, related_name="user")
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)  # TODO: migrar a Auth User y hashes.
    is_active = models.BooleanField(default=True, db_index=True)

    def __str__(self):
        return self.username


class Client(TimeStampedModel):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, related_name="client")
    type = models.CharField(max_length=50)  # Tipo de cliente (regular, vip, etc.)
    is_active = models.BooleanField(default=True, db_index=True)

    def __str__(self):
        return f"Cliente {self.person.name} ({self.type})"


class DeviceType(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class LocalSetting(TimeStampedModel):  # Configuración por tipo de dispositivo
    device_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE, related_name="local_settings")
    company_name = models.CharField(max_length=255)
    currency = models.CharField(max_length=10, default="USD")
    minimum_time = models.PositiveIntegerField(help_text="Tiempo mínimo (minutos) para alquilar / jugar")

    class Meta:
        unique_together = ("device_type", "company_name")

    def __str__(self):
        return f"{self.company_name} - {self.device_type.name}"


class Device(TimeStampedModel):
    name = models.CharField(max_length=255)
    device_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE, related_name="devices")
    is_active = models.BooleanField(default=True, db_index=True)
    device_state = models.CharField(max_length=50, default="available", db_index=True)

    class Meta:
        unique_together = ("name", "device_type")

    def __str__(self):
        return self.name


class Game(TimeStampedModel):
    device_type = models.ForeignKey(DeviceType, on_delete=models.SET_NULL, null=True, blank=True, related_name="games")
    name = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)  # Normaliza nombre del campo
    release_year = models.PositiveIntegerField()  # Solo año
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        unique_together = ("name", "device_type")

    def __str__(self):
        return self.name


class Category(TimeStampedModel):
    group = models.CharField(max_length=100)  # Renombrado de 'type' para evitar colisión futura
    name = models.CharField(max_length=255)

    class Meta:
        unique_together = ("group", "name")

    def __str__(self):
        return f"{self.group}:{self.name}"


class Product(TimeStampedModel):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    initial_stock = models.PositiveIntegerField()
    available_stock = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        unique_together = ("name", "category")

    def __str__(self):
        return self.name


class Inventory(TimeStampedModel):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="inventories")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="inventories")
    # Eliminado game: se asume stock físico por dispositivo/producto. Si era necesario, crear DeviceGame intermedio.

    class Meta:
        unique_together = ("device", "product")

    def __str__(self):
        return f"Inv {self.device} / {self.product}"


class Payment(TimeStampedModel):
    method = models.CharField(max_length=50)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.method} {self.payment_amount}"


class Sale(TimeStampedModel):
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="sales")
    sale_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Venta {self.id} - {self.client}"


class SalePayment(TimeStampedModel):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="payments")
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name="sales")

    class Meta:
        unique_together = ("sale", "payment")

    def __str__(self):
        return f"Pago venta {self.sale_id}"


class SaleProduct(TimeStampedModel):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="products")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="sale_items")

    class Meta:
        unique_together = ("sale", "product")

    def __str__(self):
        return f"Prod {self.product_id} venta {self.sale_id}"


class Session(TimeStampedModel):
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="sessions")
    device = models.ForeignKey(Device, on_delete=models.PROTECT, related_name="sessions")
    game = models.ForeignKey(Game, on_delete=models.PROTECT, related_name="sessions")
    session_type = models.CharField(max_length=50)
    hour_cost = models.DecimalField(max_digits=10, decimal_places=2)
    hour_count = models.DecimalField(max_digits=5, decimal_places=2, help_text="Horas consumidas")
    session_date = models.DateField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["client", "session_date"]),
        ]

    def __str__(self):
        return f"Sesión {self.id} - {self.client}"


class SessionPayment(TimeStampedModel):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="payments")
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name="sessions")

    class Meta:
        unique_together = ("session", "payment")

    def __str__(self):
        return f"Pago sesión {self.session_id}"


class SessionProduct(TimeStampedModel):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="products")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="session_items")

    class Meta:
        unique_together = ("session", "product")

    def __str__(self):
        return f"Prod {self.product_id} sesión {self.session_id}"


class Box(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="boxes")
    initial_amount = models.DecimalField(max_digits=10, decimal_places=2)
    opened_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Caja {self.id} ({self.user.username})"


