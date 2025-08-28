from django.core.management.base import BaseCommand
from django.db import transaction
from decimal import Decimal
from datetime import date, datetime, timedelta
import random

from gamecenter.models import (
    LocalSettings, Subsidiary, Category, Product, Price, Lots, Game, Person,
    Session, SessionLots, ConsoleReservations, ConsoleMaintenance
)


class Command(BaseCommand):
    help = 'Crear datos específicos de gaming con consolas, juegos y sesiones'

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write(self.style.SUCCESS('Creando datos específicos de gaming...'))
            
            # Verificar que existen datos básicos
            if not LocalSettings.objects.exists():
                self.stdout.write(self.style.WARNING('Creando configuración básica...'))
                local_settings = LocalSettings.objects.create(
                    currency="PEN",
                    minimum_time_sessions=30
                )
                
                Subsidiary.objects.create(
                    name='GameCenter Principal',
                    address='Av. Gaming 123, Lima',
                    contact_number='+51 999 123 456',
                    date_opened=date.today(),
                    local_setting=local_settings,
                    is_main=True
                )
            
            # Crear gamers específicos
            gamers_data = [
                {
                    'first_name': 'Alejandro',
                    'last_name': 'Pro Gamer',
                    'email': 'alejandro.progamer@gaming.com',
                    'dni': '12345001',
                    'phone': '+51 999 001 001'
                },
                {
                    'first_name': 'Valentina',
                    'last_name': 'Esports',
                    'email': 'valentina.esports@gaming.com',
                    'dni': '12345002',
                    'phone': '+51 999 002 002'
                },
                {
                    'first_name': 'Santiago',
                    'last_name': 'Casual Player',
                    'email': 'santiago.casual@gaming.com',
                    'dni': '12345003',
                    'phone': '+51 999 003 003'
                },
                {
                    'first_name': 'Isabella',
                    'last_name': 'Streamer',
                    'email': 'isabella.streamer@gaming.com',
                    'dni': '12345004',
                    'phone': '+51 999 004 004'
                }
            ]
            
            gamers = []
            for data in gamers_data:
                gamer, created = Person.objects.get_or_create(
                    dni=data['dni'],
                    defaults=data
                )
                gamers.append(gamer)
                if created:
                    self.stdout.write(f'✓ Gamer creado: {gamer.first_name} {gamer.last_name}')
            
            # Categorías gaming específicas
            gaming_categories = [
                {'name': 'PlayStation 5', 'group': 'dispositivos'},
                {'name': 'PlayStation 4', 'group': 'dispositivos'},
                {'name': 'Xbox Series X/S', 'group': 'dispositivos'},
                {'name': 'Xbox One', 'group': 'dispositivos'},
                {'name': 'Nintendo Switch', 'group': 'dispositivos'},
                {'name': 'PC Gaming High-End', 'group': 'dispositivos'},
                {'name': 'PC Gaming Mid-Range', 'group': 'dispositivos'},
                {'name': 'Controles Gaming', 'group': 'accesorios'},
                {'name': 'Headsets Gaming', 'group': 'accesorios'},
                {'name': 'Teclados Mecánicos', 'group': 'accesorios'},
                {'name': 'Mouse Gaming', 'group': 'accesorios'}
            ]
            
            categories = []
            for cat_data in gaming_categories:
                category, created = Category.objects.get_or_create(
                    name=cat_data['name'],
                    group=cat_data['group']
                )
                categories.append(category)
                if created:
                    self.stdout.write(f'✓ Categoría gaming creada: {category.name}')
            
            # Productos gaming específicos
            gaming_products = [
                # Consolas PlayStation
                {'name': 'PlayStation 5 Standard', 'category': 'PlayStation 5', 'price_hour': 15.00},
                {'name': 'PlayStation 5 Digital', 'category': 'PlayStation 5', 'price_hour': 14.00},
                {'name': 'PlayStation 4 Pro', 'category': 'PlayStation 4', 'price_hour': 12.00},
                {'name': 'PlayStation 4 Slim', 'category': 'PlayStation 4', 'price_hour': 10.00},
                
                # Consolas Xbox
                {'name': 'Xbox Series X', 'category': 'Xbox Series X/S', 'price_hour': 15.00},
                {'name': 'Xbox Series S', 'category': 'Xbox Series X/S', 'price_hour': 12.00},
                {'name': 'Xbox One X', 'category': 'Xbox One', 'price_hour': 11.00},
                {'name': 'Xbox One S', 'category': 'Xbox One', 'price_hour': 9.00},
                
                # Nintendo
                {'name': 'Nintendo Switch OLED', 'category': 'Nintendo Switch', 'price_hour': 13.00},
                {'name': 'Nintendo Switch Lite', 'category': 'Nintendo Switch', 'price_hour': 10.00},
                
                # PC Gaming
                {'name': 'PC Gaming RTX 4080 + i7', 'category': 'PC Gaming High-End', 'price_hour': 20.00},
                {'name': 'PC Gaming RTX 4070 + i5', 'category': 'PC Gaming High-End', 'price_hour': 18.00},
                {'name': 'PC Gaming RTX 3060 + i5', 'category': 'PC Gaming Mid-Range', 'price_hour': 15.00},
                {'name': 'PC Gaming GTX 1660 + i3', 'category': 'PC Gaming Mid-Range', 'price_hour': 12.00},
                
                # Accesorios
                {'name': 'Control DualSense PS5', 'category': 'Controles Gaming', 'price_unit': 35.00},
                {'name': 'Control Xbox Wireless', 'category': 'Controles Gaming', 'price_unit': 32.00},
                {'name': 'Pro Controller Nintendo', 'category': 'Controles Gaming', 'price_unit': 40.00},
                {'name': 'HyperX Cloud Alpha', 'category': 'Headsets Gaming', 'price_unit': 25.00},
                {'name': 'SteelSeries Arctis 7', 'category': 'Headsets Gaming', 'price_unit': 30.00},
                {'name': 'Razer BlackWidow V3', 'category': 'Teclados Mecánicos', 'price_unit': 28.00},
                {'name': 'Logitech G Pro X', 'category': 'Mouse Gaming', 'price_unit': 22.00}
            ]
            
            products = []
            for prod_data in gaming_products:
                # Buscar categoría
                category = next((c for c in categories if c.name == prod_data['category']), None)
                if not category:
                    continue
                
                product, created = Product.objects.get_or_create(
                    name=prod_data['name'],
                    category=category,
                    defaults={'image': f"https://via.placeholder.com/400x300?text={prod_data['name'].replace(' ', '+')}"}
                )
                
                if created:
                    # Crear precio
                    if 'price_hour' in prod_data:
                        unit_measurement = 'hora'
                        sale_price = Decimal(str(prod_data['price_hour']))
                    else:
                        unit_measurement = 'unidad'
                        sale_price = Decimal(str(prod_data['price_unit']))
                    
                    price = Price.objects.create(
                        unit_measurement=unit_measurement,
                        sale_price=sale_price,
                        purchase_price=sale_price * Decimal('0.6')
                    )
                    
                    # Crear lote
                    lot = Lots.objects.create(
                        product=product,
                        lot_number=f"GAMING-{product.id:03d}",
                        initial_stock=random.randint(3, 8),
                        current_stock=random.randint(1, 5),
                        price=price,
                        state='available',
                        entry_date=date.today() - timedelta(days=random.randint(1, 60)),
                        observations=f"Equipo gaming de alta calidad - {product.name}"
                    )
                    
                    products.append(product)
                    self.stdout.write(f'✓ Producto gaming creado: {product.name}')
            
            # Juegos populares
            popular_games = [
                {
                    'name': 'FIFA 24',
                    'gender': 'sports',
                    'release_year': 2023,
                    'description': 'El simulador de fútbol más realista con todos los equipos y ligas oficiales.',
                    'game_material_type': 'digital'
                },
                {
                    'name': 'Call of Duty: Modern Warfare III',
                    'gender': 'shooter',
                    'release_year': 2023,
                    'description': 'El shooter más intenso con modos multijugador y campaña épica.',
                    'game_material_type': 'digital'
                },
                {
                    'name': 'Fortnite',
                    'gender': 'shooter',
                    'release_year': 2017,
                    'description': 'Battle Royale gratuito con construcción y eventos especiales.',
                    'game_material_type': 'digital'
                },
                {
                    'name': 'Grand Theft Auto V',
                    'gender': 'action',
                    'release_year': 2013,
                    'description': 'Mundo abierto de acción con modo online masivo.',
                    'game_material_type': 'digital'
                },
                {
                    'name': 'League of Legends',
                    'gender': 'strategy',
                    'release_year': 2009,
                    'description': 'MOBA competitivo con torneos profesionales.',
                    'game_material_type': 'digital'
                },
                {
                    'name': 'Valorant',
                    'gender': 'shooter',
                    'release_year': 2020,
                    'description': 'Shooter táctico 5v5 con habilidades únicas.',
                    'game_material_type': 'digital'
                },
                {
                    'name': 'Apex Legends',
                    'gender': 'shooter',
                    'release_year': 2019,
                    'description': 'Battle Royale con leyendas y habilidades especiales.',
                    'game_material_type': 'digital'
                },
                {
                    'name': 'The Last of Us Part II',
                    'gender': 'action',
                    'release_year': 2020,
                    'description': 'Aventura post-apocalíptica con narrativa emotiva.',
                    'game_material_type': 'digital'
                },
                {
                    'name': 'Spider-Man: Miles Morales',
                    'gender': 'action',
                    'release_year': 2020,
                    'description': 'Aventura de superhéroes en Nueva York.',
                    'game_material_type': 'digital'
                },
                {
                    'name': 'Cyberpunk 2077',
                    'gender': 'rpg',
                    'release_year': 2020,
                    'description': 'RPG futurista en la ciudad de Night City.',
                    'game_material_type': 'digital'
                },
                {
                    'name': 'Rocket League',
                    'gender': 'sports',
                    'release_year': 2015,
                    'description': 'Fútbol con coches - deporte del futuro.',
                    'game_material_type': 'digital'
                },
                {
                    'name': 'Super Mario Odyssey',
                    'gender': 'adventure',
                    'release_year': 2017,
                    'description': 'Aventura de plataformas con Mario y Cappy.',
                    'game_material_type': 'fisico'
                },
                {
                    'name': 'The Legend of Zelda: Breath of the Wild',
                    'gender': 'adventure',
                    'release_year': 2017,
                    'description': 'Aventura épica en mundo abierto de Hyrule.',
                    'game_material_type': 'fisico'
                }
            ]
            
            games = []
            for game_data in popular_games:
                game, created = Game.objects.get_or_create(
                    name=game_data['name'],
                    defaults=game_data
                )
                games.append(game)
                if created:
                    self.stdout.write(f'✓ Juego creado: {game.name}')
            
            # Crear sesiones de gaming realistas
            console_lots = [lot for lot in Lots.objects.filter(
                product__category__group='dispositivos'
            )]
            
            if console_lots and gamers:
                for i in range(15):  # 15 sesiones de gaming
                    gamer = random.choice(gamers)
                    console_lot = random.choice(console_lots)
                    
                    # Horarios realistas de gaming
                    days_ago = random.randint(0, 30)
                    hour = random.choice([14, 15, 16, 17, 18, 19, 20, 21, 22])  # Horarios populares
                    start_time = datetime.now().replace(hour=hour, minute=0, second=0) - timedelta(days=days_ago)
                    
                    # Duración realista (1-6 horas)
                    hour_count = Decimal(str(random.choice([1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0])))
                    end_time = start_time + timedelta(hours=float(hour_count))
                    
                    # Calcular costos
                    base_cost = hour_count * console_lot.price.sale_price
                    accessory_cost = Decimal(str(random.uniform(0, 25.0)))  # Snacks, bebidas, etc.
                    
                    session = Session.objects.create(
                        client=gamer,
                        number_hours=int(hour_count),
                        start_time=start_time,
                        end_time=end_time if i < 12 else None,  # Algunas sesiones en curso
                        total_amount=base_cost + accessory_cost,
                        accessory_amount=accessory_cost,
                        state='finalizado' if i < 12 else 'en curso'
                    )
                    
                    # Asociar la consola usada
                    SessionLots.objects.create(
                        session=session,
                        lots=console_lot
                    )
                    
                    self.stdout.write(f'✓ Sesión gaming creada: {gamer.first_name} - {console_lot.product.name} ({hour_count}h)')
            
            # Crear reservas futuras
            if console_lots and gamers:
                for i in range(8):  # 8 reservas
                    gamer = random.choice(gamers)
                    console_lot = random.choice(console_lots)
                    
                    # Reservas para los próximos días
                    days_ahead = random.randint(0, 7)
                    hour = random.choice([15, 16, 17, 18, 19, 20, 21])
                    start_hour = datetime.now().replace(hour=hour, minute=0, second=0) + timedelta(days=days_ahead)
                    
                    hour_count = Decimal(str(random.choice([2.0, 3.0, 4.0, 5.0])))
                    advance_payment = console_lot.price.sale_price * hour_count * Decimal('0.3')  # 30% adelanto
                    
                    reservation = ConsoleReservations.objects.create(
                        client=gamer,
                        lots=console_lot,
                        hour_count=hour_count,
                        start_hour=start_hour,
                        accessory_count=random.randint(2, 4),
                        state='reservado',
                        advance_payment=advance_payment
                    )
                    
                    self.stdout.write(f'✓ Reserva creada: {gamer.first_name} - {console_lot.product.name}')
            
            # Crear algunos mantenimientos
            gaming_devices = Product.objects.filter(category__group='dispositivos')[:5]
            for device in gaming_devices:
                maintenance = ConsoleMaintenance.objects.create(
                    console=device,
                    maintenance_reason=random.choice(['limpieza', 'actualización', 'reparación']),
                    start_date=date.today() - timedelta(days=random.randint(1, 90)),
                    end_date=date.today() - timedelta(days=random.randint(0, 10)),
                    description=f"Mantenimiento preventivo para optimizar rendimiento de {device.name}",
                    responsible="Técnico Gaming Especializado",
                    observations="Mantenimiento completado. Sistema funcionando óptimamente."
                )
                self.stdout.write(f'✓ Mantenimiento creado: {device.name}')
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Datos de gaming creados exitosamente:\n'
                    f'  - {len(gamers)} gamers\n'
                    f'  - {len([c for c in categories if c.group == "dispositivos"])} categorías de dispositivos\n'
                    f'  - {len(products)} productos gaming\n'
                    f'  - {len(games)} juegos populares\n'
                    f'  - {Session.objects.count()} sesiones de gaming\n'
                    f'  - {ConsoleReservations.objects.count()} reservas\n'
                    f'  - {ConsoleMaintenance.objects.count()} mantenimientos'
                )
            )
