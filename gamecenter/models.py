from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser, Group, Permission

class TimeStampedModel(models.Model):
    """Abstracto: agrega created_at / updated_at."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Person(TimeStampedModel):
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    dni = models.CharField(max_length=20, null=True, blank=True)
    phone = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class MembershipType(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class PersonMembership(TimeStampedModel):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="personmembership_person")
    membership_type = models.ForeignKey(MembershipType, on_delete=models.CASCADE, related_name="personmembership_membershiptype")

    def __str__(self):
        return f"{self.person.name} - {self.membership_type.name}"

class ConsoleType(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class LocalSettings(TimeStampedModel):  # Configuración por tipo de dispositivo
    currency = models.CharField(max_length=10, default="PEN", choices=[
        ("PEN", "PEN"),
        ("USD", "USD"),
        ("EUR", "EUR"),
        ("BRL", "BRL")
    ])  # Moneda local
    minimum_time_sessions = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):  # Tiempo mínimo de sesión en minutos
        return f"{self.minimum_time_sessions} minutos - {self.currency}"

class Subsidiary(TimeStampedModel):
    name = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    contact_number = models.CharField(max_length=25, blank=True, null=True)
    date_opened = models.DateField(null=True, blank=True)
    local_setting = models.ForeignKey(LocalSettings, on_delete=models.CASCADE, related_name="subsidiary_localsetting")
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class User(AbstractUser):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="user_person", null=True, blank=True)
    subsidiary = models.ForeignKey(Subsidiary, on_delete=models.CASCADE, related_name="user_subsidiary", null=True, blank=True)
    groups = models.ManyToManyField(
        Group,
        related_name="user_groups",  # <-- Cambia el related_name
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="user_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )


class Game(TimeStampedModel):
    name = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=50, choices=[
        ("action", "Acción"),
        ("adventure", "Aventura"),
        ("rpg", "RPG"),
        ("shooter", "Shooter"),
        ("sports", "Deportes"),
        ("strategy", "Estrategia"),
        ("simulation", "Simulación"),
        ("puzzle", "Puzzle"),
        ("horror", "Horror"),
        ("other", "Otro"),
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
    name = models.CharField(max_length=255)
    group = models.CharField(max_length=50, choices=[
        ("comestibles", "Comestibles"),
        ("dispositivos", "Dispositivos"),
        ("accesorios", "Accesorios"),
    ], null=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.type}: {self.name}"


class Product(TimeStampedModel):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="product_category")
    image = models.URLField(null=True, blank=True)
    is_active = models.BooleanField(default=True, db_index=True)
    console_type = models.ForeignKey(ConsoleType, on_delete=models.PROTECT, 
                                   related_name="product_console_type", 
                                   null=True, blank=True)  # Solo para accesorios

    class Meta:
        unique_together = ("name", "category")

    def __str__(self):
        return self.name

class Price(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="prices")
    unit_measurement = models.CharField(max_length=100, choices=[
        ("unidad", "Unidad"),
        ("min", "Minutos"),
        ("hora", "Hora"),
    ])
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product.name} - {self.sale_price} por {self.unit_measurement}"
    

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
    client = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="consolereservations_client")
    lots = models.ForeignKey(Lots, on_delete=models.CASCADE, related_name="consolereservations_lots")
    reservation_date = models.DateField(auto_now_add=True)
    hour_count = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    start_hour = models.DateTimeField(null=True, blank=True)
    end_hour = models.DateTimeField(null=True, blank=True)
    accessory_count = models.PositiveIntegerField(default=2)  # Número de accesorios solicitados
    state = models.CharField(max_length=50, choices=[
        ("reservado", "Reservado"),
        ("cancelado", "Cancelado"),
        ("completado", "Completado"),
    ], default="reservado")
    advance_payment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Reserva {self.id} - {self.client.name} - {self.lots.product.name}"

class ConsoleMaintenance(TimeStampedModel):
    console = models.ForeignKey(ConsoleType, on_delete=models.CASCADE, related_name="maintenance_console")
    maintenance_date = models.DateField(auto_now_add=True)
    maintenance_reason = models.CharField(max_length=255, choices=[
        ("reparación", "Reparación"),
        ("limpieza", "Limpieza"),
        ("actualización", "Actualización"),
        ("sobrecalentamiento", "Sobrecalentamiento"),
        ("problemas de hardware", "Problemas de hardware"),
        ("problemas de software", "Problemas de software"),
        ("otro", "Otro"),
    ])
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    responsible = models.CharField(max_length=255, null=True, blank=True)
    observations = models.TextField(null=True, blank=True)


class Session(TimeStampedModel):
    client = models.ForeignKey(Person, on_delete=models.PROTECT, related_name="client_sessions")
    hour_count = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    session_date = models.DateField(auto_now_add=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    accessory_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    state = models.CharField(max_length=50, choices=[
        ("en curso", "En curso"),
        ("finalizado", "Finalizado"),
    ], default="en curso")

    # def assign_accessories(self, requested_accessories):
    #     """
    #     Asigna accesorios gratuitos y extras según el tipo de consola.
    #     requested_accessories: dict con {product_id: cantidad}
    #     """
    #     console_type = self.lots.product.console_type
    #     console_name = console_type.name.lower()

    #     # Obtén la configuración local
    #     local_setting = LocalSetting.objects.first()
    #     if not local_setting:
    #         raise ValidationError("No hay configuración local definida")

    #     # Reglas para PlayStation
    #     if "playstation" in console_name:
    #         mandos = Product.objects.filter(
    #             console_type=console_type,
    #             is_accessory=True,
    #             name__icontains="mando"
    #         )
            
    #         for mando in mandos:
    #             cantidad_pedida = requested_accessories.get(str(mando.id), 0)
    #             if cantidad_pedida > 0:
    #                 # Asignar mandos gratuitos
    #                 free_qty = min(cantidad_pedida, local_setting.free_accessories)
    #                 if free_qty > 0:
    #                     SessionAccessory.objects.create(
    #                         session=self,
    #                         product=mando,
    #                         quantity=free_qty,
    #                         is_charged=False,
    #                         price=0
    #                     )
                    
    #                 # Asignar mandos extras (cobrados)
    #                 extra_qty = cantidad_pedida - free_qty
    #                 if extra_qty > 0:
    #                     precio = mando.prices.filter(
    #                         unit_measurement="unidad",
    #                         is_active=True
    #                     ).first()
    #                     if not precio:
    #                         raise ValidationError(f"No hay precio definido para {mando.name}")
                        
    #                     SessionAccessory.objects.create(
    #                         session=self,
    #                         product=mando,
    #                         quantity=extra_qty,
    #                         is_charged=True,
    #                         price=precio.sale_price
    #                     )

    #     # Reglas para PC
    #     elif "pc" in console_name:
    #         # Asignar teclado y mouse gratuitos
    #         for acc_type in ["teclado", "mouse"]:
    #             acc = Product.objects.filter(
    #                 console_type=console_type,
    #                 is_accessory=True,
    #                 name__icontains=acc_type
    #             ).first()
                
    #             if acc:
    #                 SessionAccessory.objects.create(
    #                     session=self,
    #                     product=acc,
    #                     quantity=1,
    #                     is_charged=False,
    #                     price=0
    #                 )
            
    #         # Procesar accesorios extras solicitados
    #         for pid, qty in requested_accessories.items():
    #             if qty > 0:
    #                 product = Product.objects.get(id=pid)
    #                 # Si no es el teclado o mouse base
    #                 if not (product.name.lower().startswith(("teclado", "mouse"))):
    #                     precio = product.prices.filter(
    #                         unit_measurement="unidad",
    #                         is_active=True
    #                     ).first()
    #                     if not precio:
    #                         raise ValidationError(f"No hay precio definido para {product.name}")
                        
    #                     SessionAccessory.objects.create(
    #                         session=self,
    #                         product=product,
    #                         quantity=qty,
    #                         is_charged=True,
    #                         price=precio.sale_price
    #                     )    
    # def clean(self):
    #     console = self.lots.product.console_type
    #     maintance = ConsoleMaintenance.objects.filter(
    #         console=console,
    #         end_date__isnull=True
    #     ).exists()
    #     if maintance:
    #         raise ValidationError(f"La consola {console.name} está en mantenimiento y no puede ser usada.")

    # def __str__(self):
    #     return f"Sesión {self.id} - {self.client.name}"

    # def calculate_total(self):
    #     """Calcula el total incluyendo tiempo y accesorios extras"""
    #     if not self.hour_count:
    #         raise ValidationError("Debe especificar la cantidad de horas")

    #     # Obtener precio activo para el lote
    #     price = self.lots.price
    #     if not price or not price.is_active:
    #         raise ValidationError("No hay un precio activo para esta consola")

    #     # Calcular monto por tiempo
    #     time_amount = float(self.hour_count) * float(price.sale_price)

    #     # Calcular monto por accesorios extras
    #     self.accessory_amount = sum(
    #         float(acc.price) * acc.quantity
    #         for acc in self.accessories.filter(is_charged=True)
    #         if acc.price is not None
    #     )

    #     # Calcular total
    #     self.total_amount = time_amount + self.accessory_amount
    #     self.save()


class SessionLots(TimeStampedModel):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='lots', null=True, blank=True)
    lots = models.ForeignKey(Lots, on_delete=models.CASCADE, related_name='sessions_lots', null=True, blank=True)

    def __str__(self):
        return f"{self.session.id} - {self.lots.product.name} x{self.lots.quantity}"

class OpeningSalesBox(TimeStampedModel):
    user = models.ForeignKey(Person, on_delete=models.PROTECT, related_name="opening_sales_box")
    opening_date = models.DateField(auto_now_add=True)
    opening_amount = models.DecimalField(max_digits=10, decimal_places=2)
    closing_date = models.DateField(null=True, blank=True)
    closing_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Apertura de Caja {self.id} - {self.user.username}"


class Sale(TimeStampedModel):
    client = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="sales_client")
    user = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="sales_user")
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
    ], default="pendiente")

    def __str__(self):
        return f"Venta {self.id} - {self.client}"
    
class SaleDetail(TimeStampedModel):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="sale_details")
    lot = models.ForeignKey(Lots, on_delete=models.CASCADE, related_name="sale_details_lot")
    amount = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle de Venta {self.id} - {self.sale.client.name}"
    

class SaleBoxMovement(TimeStampedModel):
    opening_sales_box = models.ForeignKey(OpeningSalesBox, on_delete=models.CASCADE, related_name="movements_opening_sales_box")
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="movements_sale")
    movement_type = models.CharField(max_length=50, choices=[
        ("entrada", "Entrada"),
        ("salida", "Salida"),
    ])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    movement_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Movimiento de Caja {self.id} - {self.opening_sales_box.sales_box.name}"
