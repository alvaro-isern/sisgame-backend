from django.core.management.base import BaseCommand
from gamecenter.models import (
    Person, LocalSettings, Subsidiary, Category, Product, Price, Lots, Game,
    Session, ConsoleReservations, ConsoleMaintenance, Sale, User
)


class Command(BaseCommand):
    help = 'Mostrar resumen de datos creados'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== RESUMEN DE DATOS EN LA BASE DE DATOS ===\n'))
        
        # Datos básicos
        self.stdout.write(self.style.HTTP_INFO('📊 DATOS BÁSICOS:'))
        self.stdout.write(f'  • Configuraciones locales: {LocalSettings.objects.count()}')
        self.stdout.write(f'  • Sucursales: {Subsidiary.objects.count()}')
        self.stdout.write(f'  • Personas: {Person.objects.count()}')
        self.stdout.write(f'  • Usuarios del sistema: {User.objects.count()}')
        
        # Productos y categorías
        self.stdout.write(self.style.HTTP_INFO('\n🛍️ PRODUCTOS Y CATEGORÍAS:'))
        self.stdout.write(f'  • Categorías totales: {Category.objects.count()}')
        
        for group in ['dispositivos', 'accesorios', 'comestibles']:
            count = Category.objects.filter(group=group).count()
            if count > 0:
                self.stdout.write(f'    - {group.title()}: {count}')
        
        self.stdout.write(f'  • Productos totales: {Product.objects.count()}')
        self.stdout.write(f'  • Precios configurados: {Price.objects.count()}')
        self.stdout.write(f'  • Lotes en inventario: {Lots.objects.count()}')
        
        # Gaming
        self.stdout.write(self.style.HTTP_INFO('\n🎮 GAMING:'))
        self.stdout.write(f'  • Juegos en catálogo: {Game.objects.count()}')
        
        if Game.objects.exists():
            # Mostrar algunos juegos por género
            genres = Game.objects.values_list('gender', flat=True).distinct()
            for genre in genres[:5]:  # Mostrar solo los primeros 5
                count = Game.objects.filter(gender=genre).count()
                genre_display = dict(Game._meta.get_field('gender').choices).get(genre, genre)
                self.stdout.write(f'    - {genre_display}: {count} juegos')
        
        # Dispositivos gaming
        gaming_devices = Product.objects.filter(category__group='dispositivos')
        if gaming_devices.exists():
            self.stdout.write(f'  • Dispositivos gaming: {gaming_devices.count()}')
            
            # Mostrar algunos dispositivos por categoría
            categories = gaming_devices.values_list('category__name', flat=True).distinct()
            for category in categories[:5]:
                count = gaming_devices.filter(category__name=category).count()
                self.stdout.write(f'    - {category}: {count}')
        
        # Sesiones y reservas
        self.stdout.write(self.style.HTTP_INFO('\n⏰ ACTIVIDAD:'))
        self.stdout.write(f'  • Sesiones totales: {Session.objects.count()}')
        
        if Session.objects.exists():
            active_sessions = Session.objects.filter(state='en curso').count()
            finished_sessions = Session.objects.filter(state='finalizado').count()
            self.stdout.write(f'    - En curso: {active_sessions}')
            self.stdout.write(f'    - Finalizadas: {finished_sessions}')
        
        self.stdout.write(f'  • Reservas: {ConsoleReservations.objects.count()}')
        
        if ConsoleReservations.objects.exists():
            pending_reservations = ConsoleReservations.objects.filter(state='reservado').count()
            self.stdout.write(f'    - Pendientes: {pending_reservations}')
        
        # Mantenimiento
        self.stdout.write(f'  • Mantenimientos registrados: {ConsoleMaintenance.objects.count()}')
        
        # Ventas
        sales_count = Sale.objects.count()
        if sales_count > 0:
            self.stdout.write(f'  • Ventas: {sales_count}')
        
        # Mostrar algunos datos específicos
        self.stdout.write(self.style.HTTP_INFO('\n🎯 EJEMPLOS DE DATOS:'))
        
        # Mostrar algunos gamers
        gamers = Person.objects.filter(first_name__in=['Alejandro', 'Valentina', 'Santiago', 'Isabella'])
        if gamers.exists():
            self.stdout.write('  • Gamers creados:')
            for gamer in gamers:
                self.stdout.write(f'    - {gamer.first_name} {gamer.last_name} ({gamer.email})')
        
        # Mostrar algunos productos gaming populares
        popular_devices = Product.objects.filter(
            name__icontains='PlayStation 5'
        ).union(
            Product.objects.filter(name__icontains='Xbox Series')
        ).union(
            Product.objects.filter(name__icontains='PC Gaming')
        )[:5]
        
        if popular_devices.exists():
            self.stdout.write('\n  • Dispositivos gaming disponibles:')
            for device in popular_devices:
                lot_with_price = device.lots_product.filter(price__isnull=False).first()
                if lot_with_price and lot_with_price.price:
                    price = lot_with_price.price
                    self.stdout.write(f'    - {device.name}: S/ {price.sale_price} por {price.unit_measurement}')
                else:
                    self.stdout.write(f'    - {device.name}: Sin precio configurado')
        
        # Mostrar algunos juegos
        popular_games = Game.objects.filter(
            name__in=['FIFA 24', 'Call of Duty: Modern Warfare III', 'Fortnite', 'Valorant']
        )
        if popular_games.exists():
            self.stdout.write('\n  • Juegos populares:')
            for game in popular_games:
                self.stdout.write(f'    - {game.name} ({game.release_year}) - {game.get_gender_display()}')
        
        # Mostrar configuración regional
        local_setting = LocalSettings.objects.first()
        if local_setting:
            self.stdout.write(self.style.HTTP_INFO('\n🌎 CONFIGURACIÓN REGIONAL:'))
            self.stdout.write(f'  • Moneda: {local_setting.currency}')
            self.stdout.write(f'  • Tiempo mínimo de sesión: {local_setting.minimum_time_sessions} minutos')
        
        # Mostrar sucursales
        subsidiaries = Subsidiary.objects.all()
        if subsidiaries.exists():
            self.stdout.write('\n  • Sucursales:')
            for subsidiary in subsidiaries:
                status = '(Principal)' if subsidiary.is_main else ''
                self.stdout.write(f'    - {subsidiary.name} {status}')
                self.stdout.write(f'      📍 {subsidiary.address}')
                self.stdout.write(f'      📞 {subsidiary.contact_number}')
        
        self.stdout.write(self.style.SUCCESS('\n✅ RESUMEN COMPLETADO'))
        
        if Person.objects.count() == 0:
            self.stdout.write(
                self.style.WARNING(
                    '\n⚠️  No hay datos en la base de datos. '
                    'Ejecuta uno de los seeders primero:\n'
                    '   python manage.py seed_basic\n'
                    '   python manage.py seed_gaming\n'
                    '   python manage.py seed_data'
                )
            )
