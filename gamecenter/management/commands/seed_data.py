from django.core.management.base import BaseCommand
from django.db import transaction
from decimal import Decimal
from datetime import date, datetime, timedelta
import random

from gamecenter.models import (
    Person, MembershipType, PersonMembership, LocalSettings, Subsidiary, User,
    Game, Category, Product, Price, Lots, ConsoleReservations, ConsoleMaintenance,
    Session, SessionLots, OpeningSalesBox, Sale, SaleDetail, SaleBoxMovement
)


class Command(BaseCommand):
    help = 'Crear datos de prueba en español para el sistema de gamecenter'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Eliminar todos los datos existentes antes de crear nuevos',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Eliminando datos existentes...'))
            self.clear_data()

        with transaction.atomic():
            self.stdout.write(self.style.SUCCESS('Creando datos de prueba...'))
            
            # Crear datos base
            local_settings = self.create_local_settings()
            subsidiaries = self.create_subsidiaries(local_settings)
            membership_types = self.create_membership_types()
            persons = self.create_persons()
            self.create_person_memberships(persons, membership_types)
            users = self.create_users(persons, subsidiaries)
            
            # Crear datos de productos y gaming
            categories = self.create_categories()
            products = self.create_products(categories)
            prices = self.create_prices(products)
            lots = self.create_lots(products, prices)
            games = self.create_games()
            
            # Crear datos de operaciones
            console_maintenances = self.create_console_maintenances(products)
            opening_boxes = self.create_opening_sales_boxes(persons)
            sessions = self.create_sessions(persons, lots)
            reservations = self.create_console_reservations(persons, lots)
            sales = self.create_sales(persons, sessions)
            sale_details = self.create_sale_details(sales, lots)
            
            self.stdout.write(self.style.SUCCESS('¡Datos de prueba creados exitosamente!'))

    def clear_data(self):
        """Eliminar todos los datos existentes"""
        models_to_clear = [
            SaleBoxMovement, SaleDetail, Sale, ConsoleReservations, 
            SessionLots, Session, ConsoleMaintenance, OpeningSalesBox,
            Lots, Price, Game, Product, Category, PersonMembership,
            User, Person, MembershipType, Subsidiary, LocalSettings
        ]
        
        for model in models_to_clear:
            model.objects.all().delete()

    def create_local_settings(self):
        """Crear configuraciones locales"""
        settings = LocalSettings.objects.create(
            currency="PEN",
            minimum_time_sessions=30
        )
        self.stdout.write(f'✓ Configuración local creada: {settings}')
        return settings

    def create_subsidiaries(self, local_settings):
        """Crear sucursales"""
        subsidiaries_data = [
            {
                'name': 'GameCenter Lima Centro',
                'address': 'Av. Javier Prado 1234, San Isidro, Lima',
                'contact_number': '+51 999 123 456',
                'is_main': True
            },
            {
                'name': 'GameCenter Miraflores',
                'address': 'Av. Larco 567, Miraflores, Lima',
                'contact_number': '+51 999 654 321',
                'is_main': False
            },
            {
                'name': 'GameCenter San Borja',
                'address': 'Av. San Luis 890, San Borja, Lima',
                'contact_number': '+51 999 789 012',
                'is_main': False
            }
        ]
        
        subsidiaries = []
        for data in subsidiaries_data:
            subsidiary = Subsidiary.objects.create(
                name=data['name'],
                address=data['address'],
                contact_number=data['contact_number'],
                date_opened=date.today() - timedelta(days=random.randint(30, 365)),
                local_setting=local_settings,
                is_main=data['is_main']
            )
            subsidiaries.append(subsidiary)
            self.stdout.write(f'✓ Sucursal creada: {subsidiary.name}')
        
        return subsidiaries

    def create_membership_types(self):
        """Crear tipos de membresía"""
        membership_types_data = [
            'Membresía Básica',
            'Membresía Premium',
            'Membresía VIP',
            'Membresía Estudiante',
            'Membresía Familiar'
        ]
        
        membership_types = []
        for name in membership_types_data:
            membership_type = MembershipType.objects.create(name=name)
            membership_types.append(membership_type)
            self.stdout.write(f'✓ Tipo de membresía creado: {membership_type.name}')
        
        return membership_types

    def create_persons(self):
        """Crear personas"""
        persons_data = [
            {
                'first_name': 'Carlos',
                'last_name': 'García Pérez',
                'email': 'carlos.garcia@email.com',
                'dni': '12345678',
                'phone': '+51 999 111 222'
            },
            {
                'first_name': 'María',
                'last_name': 'López Rodríguez',
                'email': 'maria.lopez@email.com',
                'dni': '87654321',
                'phone': '+51 999 333 444'
            },
            {
                'first_name': 'José',
                'last_name': 'Martínez Silva',
                'email': 'jose.martinez@email.com',
                'dni': '11223344',
                'phone': '+51 999 555 666'
            },
            {
                'first_name': 'Ana',
                'last_name': 'Fernández Torres',
                'email': 'ana.fernandez@email.com',
                'dni': '44332211',
                'phone': '+51 999 777 888'
            },
            {
                'first_name': 'Luis',
                'last_name': 'Sánchez Morales',
                'email': 'luis.sanchez@email.com',
                'dni': '55667788',
                'phone': '+51 999 999 000'
            },
            {
                'first_name': 'Carmen',
                'last_name': 'Ruiz Vargas',
                'email': 'carmen.ruiz@email.com',
                'dni': '88776655',
                'phone': '+51 999 123 789'
            },
            {
                'first_name': 'Diego',
                'last_name': 'Herrera Castillo',
                'email': 'diego.herrera@email.com',
                'dni': '99887766',
                'phone': '+51 999 456 123'
            },
            {
                'first_name': 'Patricia',
                'last_name': 'Jiménez Ramos',
                'email': 'patricia.jimenez@email.com',
                'dni': '66554433',
                'phone': '+51 999 789 456'
            }
        ]
        
        persons = []
        for data in persons_data:
            person = Person.objects.create(**data)
            persons.append(person)
            self.stdout.write(f'✓ Persona creada: {person.first_name} {person.last_name}')
        
        return persons

    def create_person_memberships(self, persons, membership_types):
        """Crear membresías de personas"""
        for person in persons[:5]:  # Solo los primeros 5 tendrán membresía
            membership_type = random.choice(membership_types)
            PersonMembership.objects.create(
                person=person,
                membership_type=membership_type
            )
            self.stdout.write(f'✓ Membresía creada: {person.first_name} - {membership_type.name}')

    def create_users(self, persons, subsidiaries):
        """Crear usuarios del sistema"""
        users_data = [
            {
                'username': 'admin',
                'email': 'admin@gamecenter.com',
                'first_name': 'Administrador',
                'last_name': 'Sistema',
                'is_staff': True,
                'is_superuser': True
            },
            {
                'username': 'cajero1',
                'email': 'cajero1@gamecenter.com',
                'first_name': 'Roberto',
                'last_name': 'Vega'
            },
            {
                'username': 'cajero2',
                'email': 'cajero2@gamecenter.com',
                'first_name': 'Sofía',
                'last_name': 'Moreno'
            }
        ]
        
        users = []
        for i, data in enumerate(users_data):
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password='123456',
                first_name=data['first_name'],
                last_name=data['last_name'],
                is_staff=data.get('is_staff', False),
                is_superuser=data.get('is_superuser', False),
                person=persons[i] if i < len(persons) else None,
                subsidiary=subsidiaries[0] if i == 0 else random.choice(subsidiaries)
            )
            users.append(user)
            self.stdout.write(f'✓ Usuario creado: {user.username}')
        
        return users

    def create_categories(self):
        """Crear categorías"""
        categories_data = [
            {'name': 'PlayStation 5', 'group': 'dispositivos'},
            {'name': 'Xbox Series X', 'group': 'dispositivos'},
            {'name': 'Nintendo Switch', 'group': 'dispositivos'},
            {'name': 'PC Gaming', 'group': 'dispositivos'},
            {'name': 'Mandos y Controles', 'group': 'accesorios'},
            {'name': 'Audífonos Gaming', 'group': 'accesorios'},
            {'name': 'Teclados Mecánicos', 'group': 'accesorios'},
            {'name': 'Bebidas', 'group': 'comestibles'},
            {'name': 'Snacks', 'group': 'comestibles'},
            {'name': 'Dulces', 'group': 'comestibles'}
        ]
        
        categories = []
        for data in categories_data:
            category = Category.objects.create(**data)
            categories.append(category)
            self.stdout.write(f'✓ Categoría creada: {category.name}')
        
        return categories

    def create_products(self, categories):
        """Crear productos"""
        products_data = [
            # Dispositivos
            {'name': 'Consola PlayStation 5', 'category': 'dispositivos'},
            {'name': 'Consola Xbox Series X', 'category': 'dispositivos'},
            {'name': 'Nintendo Switch OLED', 'category': 'dispositivos'},
            {'name': 'PC Gaming RTX 4060', 'category': 'dispositivos'},
            {'name': 'PC Gaming RTX 4070', 'category': 'dispositivos'},
            
            # Accesorios
            {'name': 'Control DualSense PS5', 'category': 'accesorios'},
            {'name': 'Control Xbox Wireless', 'category': 'accesorios'},
            {'name': 'Pro Controller Switch', 'category': 'accesorios'},
            {'name': 'Audífonos HyperX Cloud II', 'category': 'accesorios'},
            {'name': 'Teclado Mecánico Razer', 'category': 'accesorios'},
            
            # Comestibles
            {'name': 'Coca Cola 500ml', 'category': 'comestibles'},
            {'name': 'Pepsi 500ml', 'category': 'comestibles'},
            {'name': 'Red Bull 250ml', 'category': 'comestibles'},
            {'name': 'Doritos Nacho', 'category': 'comestibles'},
            {'name': 'Pringles Original', 'category': 'comestibles'},
            {'name': 'Chocolates M&M', 'category': 'comestibles'},
            {'name': 'Galletas Oreo', 'category': 'comestibles'}
        ]
        
        products = []
        for data in products_data:
            # Buscar categoría por grupo
            category = next((c for c in categories if c.group == data['category']), categories[0])
            
            product = Product.objects.create(
                name=data['name'],
                category=category,
                image=f"https://via.placeholder.com/300x200?text={data['name'].replace(' ', '+')}"
            )
            products.append(product)
            self.stdout.write(f'✓ Producto creado: {product.name}')
        
        return products

    def create_prices(self, products):
        """Crear precios para productos"""
        prices = []
        for product in products:
            if 'consola' in product.name.lower() or 'pc gaming' in product.name.lower():
                # Precios por hora para dispositivos gaming
                price = Price.objects.create(
                    unit_measurement='hora',
                    sale_price=Decimal(str(random.uniform(8.0, 15.0))),
                    purchase_price=Decimal(str(random.uniform(5.0, 10.0)))
                )
            else:
                # Precios por unidad para accesorios y comestibles
                price = Price.objects.create(
                    unit_measurement='unidad',
                    sale_price=Decimal(str(random.uniform(3.0, 50.0))),
                    purchase_price=Decimal(str(random.uniform(1.0, 30.0)))
                )
            
            prices.append(price)
            self.stdout.write(f'✓ Precio creado: {price}')
        
        return prices

    def create_lots(self, products, prices):
        """Crear lotes de productos"""
        lots = []
        for i, product in enumerate(products):
            price = prices[i]
            
            # Crear 1-3 lotes por producto
            for j in range(random.randint(1, 3)):
                lot = Lots.objects.create(
                    product=product,
                    lot_number=f"LOT-{product.id:03d}-{j+1:02d}",
                    manufacturing_date=date.today() - timedelta(days=random.randint(1, 180)),
                    expiration_date=date.today() + timedelta(days=random.randint(30, 730)) if 'comestible' in product.category.group else None,
                    initial_stock=random.randint(5, 50),
                    current_stock=random.randint(1, 20),
                    price=price,
                    state='available',
                    entry_date=date.today() - timedelta(days=random.randint(1, 30)),
                    observations=f"Lote en perfecto estado - {product.name}"
                )
                lots.append(lot)
                self.stdout.write(f'✓ Lote creado: {lot}')
        
        return lots

    def create_games(self):
        """Crear juegos"""
        games_data = [
            {
                'name': 'The Last of Us Part II',
                'gender': 'action',
                'release_year': 2020,
                'description': 'Juego de supervivencia post-apocalíptica con elementos de acción y aventura.',
                'game_material_type': 'digital'
            },
            {
                'name': 'FIFA 24',
                'gender': 'sports',
                'release_year': 2023,
                'description': 'Simulador de fútbol con los mejores equipos del mundo.',
                'game_material_type': 'digital'
            },
            {
                'name': 'Call of Duty: Modern Warfare III',
                'gender': 'shooter',
                'release_year': 2023,
                'description': 'Shooter en primera persona con modo campaña y multijugador.',
                'game_material_type': 'digital'
            },
            {
                'name': 'Super Mario Odyssey',
                'gender': 'adventure',
                'release_year': 2017,
                'description': 'Aventura de plataformas con Mario explorando diferentes mundos.',
                'game_material_type': 'fisico'
            },
            {
                'name': 'Cyberpunk 2077',
                'gender': 'rpg',
                'release_year': 2020,
                'description': 'RPG futurista ambientado en Night City.',
                'game_material_type': 'digital'
            },
            {
                'name': 'Fortnite',
                'gender': 'shooter',
                'release_year': 2017,
                'description': 'Battle royale gratuito con construcción.',
                'game_material_type': 'digital'
            },
            {
                'name': 'Resident Evil 4',
                'gender': 'horror',
                'release_year': 2023,
                'description': 'Remake del clásico juego de terror y supervivencia.',
                'game_material_type': 'digital'
            }
        ]
        
        games = []
        for data in games_data:
            game = Game.objects.create(**data)
            games.append(game)
            self.stdout.write(f'✓ Juego creado: {game.name}')
        
        return games

    def create_console_maintenances(self, products):
        """Crear mantenimientos de consolas"""
        console_products = [p for p in products if 'consola' in p.name.lower() or 'pc gaming' in p.name.lower()]
        
        maintenances = []
        for console in console_products[:3]:  # Solo algunos mantenimientos
            maintenance = ConsoleMaintenance.objects.create(
                console=console,
                maintenance_reason=random.choice(['limpieza', 'reparación', 'actualización']),
                start_date=date.today() - timedelta(days=random.randint(1, 30)),
                end_date=date.today() - timedelta(days=random.randint(0, 5)),
                description=f"Mantenimiento preventivo para {console.name}",
                responsible="Técnico especializado",
                observations="Mantenimiento completado satisfactoriamente"
            )
            maintenances.append(maintenance)
            self.stdout.write(f'✓ Mantenimiento creado: {maintenance}')
        
        return maintenances

    def create_opening_sales_boxes(self, persons):
        """Crear aperturas de caja"""
        opening_boxes = []
        for i in range(3):  # 3 aperturas de caja
            opening_box = OpeningSalesBox.objects.create(
                user=persons[i],
                opening_amount=Decimal('100.00'),
                closing_amount=Decimal(str(random.uniform(150.0, 300.0))) if i < 2 else None,
                closing_date=date.today() - timedelta(days=i) if i < 2 else None
            )
            opening_boxes.append(opening_box)
            self.stdout.write(f'✓ Apertura de caja creada: {opening_box}')
        
        return opening_boxes

    def create_sessions(self, persons, lots):
        """Crear sesiones de juego"""
        console_lots = [l for l in lots if 'consola' in l.product.name.lower() or 'pc gaming' in l.product.name.lower()]
        
        sessions = []
        for i in range(8):  # 8 sesiones
            start_time = datetime.now() - timedelta(days=random.randint(0, 7), hours=random.randint(0, 12))
            hour_count = Decimal(str(random.uniform(1.0, 4.0)))
            
            session = Session.objects.create(
                client=random.choice(persons),
                hour_count=hour_count,
                start_time=start_time,
                end_time=start_time + timedelta(hours=float(hour_count)) if i < 6 else None,
                total_amount=hour_count * Decimal('10.00'),
                accessory_amount=Decimal(str(random.uniform(0, 15.0))),
                state='finalizado' if i < 6 else 'en curso'
            )
            sessions.append(session)
            
            # Crear SessionLots
            SessionLots.objects.create(
                session=session,
                lots=random.choice(console_lots)
            )
            
            self.stdout.write(f'✓ Sesión creada: {session}')
        
        return sessions

    def create_console_reservations(self, persons, lots):
        """Crear reservas de consolas"""
        console_lots = [l for l in lots if 'consola' in l.product.name.lower()]
        
        reservations = []
        for i in range(5):  # 5 reservas
            reservation = ConsoleReservations.objects.create(
                client=random.choice(persons),
                lots=random.choice(console_lots),
                hour_count=Decimal(str(random.uniform(2.0, 6.0))),
                start_hour=datetime.now() + timedelta(days=random.randint(0, 7), hours=random.randint(9, 20)),
                end_hour=None,
                accessory_count=random.randint(1, 4),
                state=random.choice(['reservado', 'completado', 'cancelado']),
                advance_payment=Decimal(str(random.uniform(10.0, 50.0)))
            )
            reservations.append(reservation)
            self.stdout.write(f'✓ Reserva creada: {reservation}')
        
        return reservations

    def create_sales(self, persons, sessions):
        """Crear ventas"""
        sales = []
        for i in range(10):  # 10 ventas
            sale = Sale.objects.create(
                client=random.choice(persons),
                is_anonymous=random.choice([True, False]),
                user=persons[0],  # Usuario vendedor
                session=random.choice(sessions) if random.choice([True, False]) else None,
                subtotal=Decimal(str(random.uniform(20.0, 150.0))),
                igv=Decimal('0.00'),  # Sin IGV por ahora
                total=Decimal(str(random.uniform(20.0, 150.0))),
                payment_method=random.choice(['efectivo', 'tarjeta', 'transferencia']),
                state='completado'
            )
            sales.append(sale)
            self.stdout.write(f'✓ Venta creada: {sale}')
        
        return sales

    def create_sale_details(self, sales, lots):
        """Crear detalles de venta"""
        for sale in sales:
            # Cada venta tendrá 1-3 productos
            num_products = random.randint(1, 3)
            selected_lots = random.sample(lots, min(num_products, len(lots)))
            
            for lot in selected_lots:
                amount = random.randint(1, 3)
                unit_price = lot.price.sale_price
                discount = Decimal('0.00')
                subtotal = amount * unit_price - discount
                
                SaleDetail.objects.create(
                    sale=sale,
                    lot=lot,
                    amount=amount,
                    unit_price=unit_price,
                    discount=discount,
                    subtotal=subtotal
                )
                
                self.stdout.write(f'✓ Detalle de venta creado: {sale.id} - {lot.product.name}')
