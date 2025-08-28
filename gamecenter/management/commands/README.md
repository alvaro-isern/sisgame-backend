# Seeders para GameCenter

Este directorio contiene varios comandos de Django para crear datos de prueba en español para el sistema GameCenter.

## Comandos disponibles

### 1. `seed_basic` - Datos básicos mínimos
Crea los datos esenciales para pruebas rápidas:
- 1 configuración local
- 1 sucursal principal
- 3 personas básicas
- 5 categorías fundamentales
- 5 productos con precios y lotes
- 3 juegos básicos

```bash
python manage.py seed_basic
```

### 2. `seed_gaming` - Datos específicos de gaming
Crea un conjunto completo de datos enfocados en gaming:
- 4 gamers con perfiles específicos
- Categorías detalladas por consolas y PC
- 17+ productos gaming (PS5, Xbox, Nintendo, PC)
- 13 juegos populares
- 15 sesiones de gaming realistas
- 8 reservas futuras
- Mantenimientos de equipos

```bash
python manage.py seed_gaming
```

### 3. `seed_data` - Conjunto completo de datos
Crea un dataset completo para pruebas exhaustivas:
- Configuraciones locales
- 3 sucursales (Lima Centro, Miraflores, San Borja)
- 5 tipos de membresía
- 8 personas con datos completos
- 3 usuarios del sistema con roles
- 10 categorías (dispositivos, accesorios, comestibles)
- 17 productos variados
- 7 juegos populares
- Sesiones, reservas, ventas y mantenimientos

```bash
python manage.py seed_data
```

**Opciones adicionales:**
```bash
# Eliminar datos existentes antes de crear nuevos
python manage.py seed_data --clear
```

## Orden recomendado de ejecución

1. **Para pruebas rápidas:**
   ```bash
   python manage.py seed_basic
   ```

2. **Para datos de gaming completos:**
   ```bash
   python manage.py seed_basic
   python manage.py seed_gaming
   ```

3. **Para dataset completo:**
   ```bash
   python manage.py seed_data
   ```

## Datos en español incluidos

### Personas
- Nombres típicos en español: Carlos, María, José, Ana, Luis, Carmen, Diego, Patricia
- Apellidos compuestos: García Pérez, López Rodríguez, Martínez Silva
- DNIs válidos y teléfonos con formato peruano (+51)
- Emails de prueba con dominios .com

### Ubicaciones
- Sucursales en Lima: San Isidro, Miraflores, San Borja
- Direcciones reales de Lima con avenidas principales
- Teléfonos con código de país peruano

### Productos Gaming
- **Consolas:** PlayStation 5, Xbox Series X, Nintendo Switch
- **PC Gaming:** Configuraciones High-End y Mid-Range con especificaciones reales
- **Accesorios:** Controles, headsets, teclados mecánicos de marcas conocidas
- **Precios:** En soles peruanos (PEN) con tarifas realistas por hora

### Juegos Populares
- FIFA 24, Call of Duty: Modern Warfare III
- Fortnite, League of Legends, Valorant
- The Last of Us Part II, Spider-Man: Miles Morales
- Super Mario Odyssey, Zelda: Breath of the Wild

### Categorías
- **Dispositivos:** PlayStation, Xbox, Nintendo, PC Gaming
- **Accesorios:** Controles, headsets, teclados, mouse
- **Comestibles:** Bebidas, snacks, dulces

### Configuración Regional
- **Moneda:** PEN (Soles Peruanos)
- **Tiempo mínimo de sesión:** 30 minutos
- **Horarios realistas:** Sesiones entre 14:00 y 22:00
- **Métodos de pago:** Efectivo, tarjeta, transferencia

## Estructura de precios

- **Consolas nuevas (PS5, Xbox Series X):** 14-15 soles/hora
- **Consolas anteriores (PS4, Xbox One):** 9-12 soles/hora
- **PC Gaming High-End:** 18-20 soles/hora
- **PC Gaming Mid-Range:** 12-15 soles/hora
- **Nintendo Switch:** 10-13 soles/hora
- **Accesorios:** 22-40 soles por alquiler
- **Comestibles:** 3-5 soles por unidad

## Datos de sesiones realistas

- **Duración típica:** 1-6 horas
- **Horarios populares:** 14:00 - 22:00
- **Estados:** En curso, finalizado
- **Costos adicionales:** Snacks, bebidas (0-25 soles)
- **Reservas:** Con adelanto del 30%

## Validación de datos

Todos los seeders incluyen:
- Validación de datos únicos (emails, DNIs)
- Relaciones consistentes entre modelos
- Fechas realistas y coherentes
- Stocks y precios lógicos
- Estados válidos según las opciones del modelo

## Troubleshooting

### Error: "Modelo no encontrado"
Asegúrate de que las migraciones estén aplicadas:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Error: "Datos duplicados"
Usa la opción `--clear` para limpiar antes de crear:
```bash
python manage.py seed_data --clear
```

### Error: "No module named gamecenter"
Verifica que estés en el directorio correcto del proyecto y que la app esté en INSTALLED_APPS.
