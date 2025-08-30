from django.core.management.base import BaseCommand
from django.db import transaction
from decimal import Decimal
from datetime import date, datetime, timedelta

from gamecenter.models import (
    Person, LocalSettings, Subsidiary, Category, Product, Price, Lots, Game, ProductGame, ProductDevices
)


class Command(BaseCommand):
    help = 'Crear datos mínimos para pruebas rápidas'

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write(self.style.SUCCESS('Creando datos básicos para pruebas...'))
            
            # Configuración local
            local_settings = LocalSettings.objects.create(
                currency="PEN",
                minimum_time_sessions=30
            )
            
            # Sucursal principal
            subsidiary = Subsidiary.objects.create(
                name='GameCenter Principal',
                address='Av. Principal 123, Lima',
                contact_number='+51 999 123 456',
                date_opened=date.today(),
                local_setting=local_settings,
                is_main=True
            )
            
            # Personas básicas
            persons_data = [
                {
                    'first_name': 'Juan',
                    'last_name': 'Pérez',
                    'email': 'juan.perez@test.com',
                    'dni': '12345678',
                    'phone': '+51 999 111 111'
                },
                {
                    'first_name': 'María',
                    'last_name': 'García',
                    'email': 'maria.garcia@test.com',
                    'dni': '87654321',
                    'phone': '+51 999 222 222'
                },
                {
                    'first_name': 'Cliente',
                    'last_name': 'Anónimo',
                    'email': 'anonimo@test.com',
                    'dni': '00000000',
                    'phone': '+51 999 000 000'
                }
            ]
            
            persons = []
            for data in persons_data:
                person, created = Person.objects.get_or_create(
                    email=data['email'],
                    defaults=data
                )
                persons.append(person)
            
            # Categorías básicas
            categories_data = [
                {'name': 'PlayStation', 'group': 'dispositivos'},
                {'name': 'Xbox', 'group': 'dispositivos'},
                {'name': 'Controles', 'group': 'accesorios'},
                {'name': 'Bebidas', 'group': 'comestibles'},
                {'name': 'Snacks', 'group': 'comestibles'}
            ]
            
            categories = []
            for data in categories_data:
                category, created = Category.objects.get_or_create(
                    name=data['name'],
                    group=data['group']
                )
                categories.append(category)
            
            # Productos básicos
            products_data = [
                {'name': 'PlayStation 5', 'category_idx': 0, 'price': 12.00},
                {'name': 'Xbox Series X', 'category_idx': 1, 'price': 10.00},
                {'name': 'Control PS5', 'category_idx': 2, 'price': 25.00},
                {'name': 'Coca Cola', 'category_idx': 3, 'price': 3.50},
                {'name': 'Doritos', 'category_idx': 4, 'price': 4.00}
            ]
            
            products = []
            for data in products_data:
                product, created = Product.objects.get_or_create(
                    name=data['name'],
                    category=categories[data['category_idx']]
                )
                
                if created:
                    # Crear precio
                    unit_measurement = 'hora' if product.category.group == 'dispositivos' else 'unidad'
                    price = Price.objects.create(
                        unit_measurement=unit_measurement,
                        sale_price=Decimal(str(data['price'])),
                        purchase_price=Decimal(str(data['price'] * 0.6))
                    )
                    
                    # Crear lote
                    lot = Lots.objects.create(
                        product=product,
                        lot_number=f"TEST-{product.id:03d}",
                        initial_stock=20,
                        current_stock=15,
                        price=price,
                        state='available',
                        entry_date=date.today()
                    )
                    
                    # Crear ProductDevices para dispositivos gaming
                    if product.category.group == 'dispositivos':
                        ProductDevices.objects.create(
                            device=product,
                            code=f"DEV-{product.id:03d}"
                        )
                
                products.append(product)
            
            # Juegos básicos
            games_data = [
                {
                    'name': 'FIFA 24',
                    'gender': 'sports',
                    'release_year': 2023,
                    'description': 'Simulador de fútbol',
                    'game_material_type': 'digital'
                },
                {
                    'name': 'Call of Duty MW3',
                    'gender': 'shooter',
                    'release_year': 2023,
                    'description': 'Shooter multijugador',
                    'game_material_type': 'digital'
                },
                {
                    'name': 'Super Mario Odyssey',
                    'gender': 'adventure',
                    'release_year': 2017,
                    'description': 'Aventura de plataformas',
                    'game_material_type': 'fisico'
                }
            ]
            
            games = []
            for data in games_data:
                game, created = Game.objects.get_or_create(
                    name=data['name'],
                    release_year=data['release_year'],
                    defaults=data
                )
                games.append(game)
                if created:
                    self.stdout.write(f'✓ Juego creado: {game.name}')
            
            # Crear relaciones entre productos gaming y juegos
            gaming_products = [p for p in products if p.category.group == 'dispositivos']
            for product in gaming_products:
                # Asociar algunos juegos a cada producto gaming
                for game in games[:2]:  # Primeros 2 juegos para cada producto
                    ProductGame.objects.get_or_create(
                        product=product,
                        game=game
                    )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Datos básicos creados:\n'
                    f'  - 1 configuración local\n'
                    f'  - 1 sucursal\n'
                    f'  - {len(persons)} personas\n'
                    f'  - {len(categories)} categorías\n'
                    f'  - {len(products)} productos con precios y lotes\n'
                    f'  - {len(games_data)} juegos\n'
                    f'  - {ProductGame.objects.count()} relaciones producto-juego'
                )
            )
