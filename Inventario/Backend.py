from datetime import datetime
from typing import List, Optional
from enum import Enum
from dataclasses import dataclass
from flask import request, jsonify, Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Esto permite peticiones CORS desde cualquier origen

class CategoriaProducto(Enum):
    PAPELERIA = "Papelería"
    MORRALES = "Morrales"
    ESCRITURA = "Escritura"
    ACCESORIOS = "Accesorios"
    CONTENEDORES = "Contenedores"
    ROPA = "Ropa"
    TECNOLOGIA = "Tecnología"
    PROTECCION = "Protección"

class Talla(Enum):
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"
    XXL = "XXL"
    UNICA = "Única"

class Color(Enum):
    BLANCO = "Blanco"
    NEGRO = "Negro"
    NARANJA = "Naranja"
    GRIS = "Gris"
    VERDE = "Verde"
    DORADO = "Dorado"
    CAFE = "Café"
    MULTICOLOR = "Multicolor"

class TipoMovimiento(Enum):
    ENTRADA = "Entrada"
    SALIDA = "Salida"

class Ubicacion(Enum):
    MEDELLIN = "Medellín"
    BOGOTA = "Bogotá"

@dataclass
class ProductoBase:
    id: int
    nombre: str
    categoria: CategoriaProducto
    precio: float = 0.0
    cantidad: int = 0

@dataclass
class MovimientoInventario:
    id: int
    producto_id: int
    tipo: TipoMovimiento
    ubicacion: Ubicacion
    cantidad: int
    fecha: datetime = datetime.now()
    descripcion: str = ""

# Lista de productos predefinidos
PRODUCTOS_INVENTARIO = [
    # Papelería
    ProductoBase(1, "Cuaderno Sofka", CategoriaProducto.PAPELERIA, cantidad=126),
    ProductoBase(2, "Cuaderno Liderazgo", CategoriaProducto.PAPELERIA, cantidad=-7),
    ProductoBase(3, "Cuaderno Valtica", CategoriaProducto.PAPELERIA, cantidad=3),
    ProductoBase(4, "Cuaderno Temporal de Sticker", CategoriaProducto.PAPELERIA, cantidad=30),
    
    # Morrales
    ProductoBase(5, "Morral Negro Sofka", CategoriaProducto.MORRALES, cantidad=-113),
    ProductoBase(6, "Morral Negro Valtica", CategoriaProducto.MORRALES, cantidad=18),
    ProductoBase(7, "Morral Colores Sofka", CategoriaProducto.MORRALES, cantidad=21),
    
    # Escritura
    ProductoBase(8, "Esfero Hibot", CategoriaProducto.ESCRITURA, cantidad=1),
    ProductoBase(9, "Esfero Naranja Sofka Kit", CategoriaProducto.ESCRITURA, cantidad=63),
    ProductoBase(10, "Esfero Gris Sofka Kit", CategoriaProducto.ESCRITURA, cantidad=5),
    ProductoBase(11, "Esfero Sofka VIP", CategoriaProducto.ESCRITURA, cantidad=85),
    ProductoBase(12, "Esfero Pertrinum", CategoriaProducto.ESCRITURA, cantidad=0),
    
    # Contenedores
    ProductoBase(13, "Termo Térmico", CategoriaProducto.CONTENEDORES, cantidad=102),
    ProductoBase(14, "Vaso Cafe Sofka", CategoriaProducto.CONTENEDORES, cantidad=21),
    ProductoBase(15, "Lonchera Negra", CategoriaProducto.CONTENEDORES, cantidad=3),
    ProductoBase(16, "Lonchera Cafe", CategoriaProducto.CONTENEDORES, cantidad=-4),
    ProductoBase(17, "Lonchera Colores", CategoriaProducto.CONTENEDORES, cantidad=2),
    ProductoBase(18, "Mug Sofka", CategoriaProducto.CONTENEDORES, cantidad=-7),
    ProductoBase(19, "Mug Liderazgo", CategoriaProducto.CONTENEDORES, cantidad=8),
    ProductoBase(20, "Mug Sofka Navideño", CategoriaProducto.CONTENEDORES, cantidad=0),
    
    # Accesorios
    ProductoBase(21, "Gorra Negra Sofka", CategoriaProducto.ACCESORIOS, cantidad=11),
    ProductoBase(22, "Gorra Pertrinum", CategoriaProducto.ACCESORIOS, cantidad=0),
    ProductoBase(23, "Canguro - Riñonera", CategoriaProducto.ACCESORIOS, cantidad=27),
    
    # Tecnología
    ProductoBase(24, "USB", CategoriaProducto.TECNOLOGIA, cantidad=24),
    
    # Protección
    ProductoBase(25, "Tapabocas", CategoriaProducto.PROTECCION, cantidad=34),
]

# Definición de camisetas con sus variantes
CAMISETAS_BASE = [
    ("Eventos", Color.MULTICOLOR, 7),
    ("Valtica", Color.MULTICOLOR, 33),
    ("8 Años", Color.MULTICOLOR, 0),
    ("Hibot Verde", Color.VERDE, 0),
    ("10 Años", Color.MULTICOLOR, 0),
    ("Gris Sofka U", Color.GRIS, 0),
]

# Diccionario de cantidades iniciales para camisetas por modelo, género y talla
CANTIDADES_CAMISETAS = {
    "Sofkiana Blanca": {
        "Hombre": {"S": 22, "M": 4, "L": 0, "XL": 19, "XXL": 32},
        "Mujer": {"S": 16, "M": 36, "L": 39, "XL": 26, "XXL": 25}
    },
    "Sofkiana Naranja": {
        "Hombre": {"S": 31, "M": 10, "L": 22, "XL": -4, "XXL": 10},
        "Mujer": {"S": 11, "M": 12, "L": 7, "XL": 20, "XXL": 8}
    },
    "Sofkiana Negra": {
        "Hombre": {"S": 16, "M": 3, "L": -2, "XL": 6, "XXL": 23},
        "Mujer": {"S": 13, "M": 23, "L": 35, "XL": 14, "XXL": 15}
    },
    "Sofkiana Negra Dorada": {
        "Hombre": {"S": 10, "M": 21, "L": 24, "XL": 8, "XXL": 5},
        "Mujer": {"S": 15, "M": 10, "L": 9, "XL": 15, "XXL": 6}
    }
}

# Generador de productos de camisetas
def generar_camisetas():
    id_actual = len(PRODUCTOS_INVENTARIO) + 1
    camisetas = []
    
    # Primero las camisetas con tallas
    for nombre_base, color, _ in CAMISETAS_BASE:
        if nombre_base in ["Eventos", "Valtica", "8 Años", "Hibot Verde", "10 Años", "Gris Sofka U"]:
            cantidad = next((c for n, _, c in CAMISETAS_BASE if n == nombre_base), 0)
            camisetas.append(
                ProductoBase(
                    id=id_actual,
                    nombre=f"Camiseta {nombre_base} Todas las tallas",
                    categoria=CategoriaProducto.ROPA,
                    cantidad=cantidad
                )
            )
            id_actual += 1
            continue

        if nombre_base in CANTIDADES_CAMISETAS:
            for genero in ["Hombre", "Mujer"]:
                for talla in Talla:
                    if talla != Talla.UNICA:
                        cantidad = CANTIDADES_CAMISETAS[nombre_base][genero][talla.value]
                        camisetas.append(
                            ProductoBase(
                                id=id_actual,
                                nombre=f"Camiseta {nombre_base} {genero} {talla.value}",
                                categoria=CategoriaProducto.ROPA,
                                cantidad=cantidad
                            )
                        )
                        id_actual += 1
    
    return camisetas

# Agregar las camisetas a la lista de productos
PRODUCTOS_INVENTARIO.extend(generar_camisetas())

class Producto:
    def __init__(self, 
                 id: int,
                 nombre: str, 
                 descripcion: str,
                 cantidad: int,
                 categoria: CategoriaProducto):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.categoria = categoria
        self.fecha_creacion = datetime.now()
        self.fecha_actualizacion = datetime.now()

class GestorInventario:
    def __init__(self):
        self.productos = []
        self.movimientos = []
        self._ultimo_id_movimiento = 0
        self.inicializar_inventario()
    
    def inicializar_inventario(self):
        """Inicializa el inventario con los productos predefinidos"""
        for producto_base in PRODUCTOS_INVENTARIO:
            self.productos.append(Producto(
                id=producto_base.id,
                nombre=producto_base.nombre,
                descripcion="",  # Puedes agregar descripciones después
                cantidad=producto_base.cantidad,
                categoria=producto_base.categoria
            ))

    def obtener_productos_por_categoria(self, categoria: CategoriaProducto) -> List[Producto]:
        """Retorna todos los productos de una categoría específica"""
        return [p for p in self.productos if p.categoria == categoria]

    def agregar_producto(self, 
                        nombre: str, 
                        descripcion: str, 
                        cantidad: int) -> Producto:
        self._ultimo_id += 1
        nuevo_producto = Producto(
            id=self._ultimo_id,
            nombre=nombre,
            descripcion=descripcion,
            cantidad=cantidad
        )
        self.productos.append(nuevo_producto)
        return nuevo_producto

    def buscar_producto_por_id(self, id: int) -> Optional[Producto]:
        for producto in self.productos:
            if producto.id == id:
                return producto
        return None

    def actualizar_cantidad(self, id: int, nueva_cantidad: int) -> bool:
        producto = self.buscar_producto_por_id(id)
        if producto:
            producto.cantidad = nueva_cantidad
            producto.fecha_actualizacion = datetime.now()
            return True
        return False

    def registrar_movimiento(self, 
                           producto_id: int, 
                           tipo: TipoMovimiento, 
                           ubicacion: Ubicacion,
                           cantidad: int, 
                           descripcion: str = "") -> bool:
        """Registra un movimiento de entrada o salida en el inventario"""
        producto = self.buscar_producto_por_id(producto_id)
        if not producto:
            return False
            
        if tipo == TipoMovimiento.SALIDA and producto.cantidad < cantidad:
            return False  # No hay suficiente stock
            
        # Actualizar cantidad
        nueva_cantidad = (producto.cantidad + cantidad 
                         if tipo == TipoMovimiento.ENTRADA 
                         else producto.cantidad - cantidad)
        
        # Registrar el movimiento
        self._ultimo_id_movimiento += 1
        movimiento = MovimientoInventario(
            id=self._ultimo_id_movimiento,
            producto_id=producto_id,
            tipo=tipo,
            ubicacion=ubicacion,
            cantidad=cantidad,
            descripcion=descripcion
        )
        self.movimientos.append(movimiento)
        
        # Actualizar el producto
        self.actualizar_cantidad(producto_id, nueva_cantidad)
        return True

    def obtener_movimientos_producto(self, producto_id: int) -> List[MovimientoInventario]:
        """Obtiene el historial de movimientos de un producto"""
        return [m for m in self.movimientos if m.producto_id == producto_id]

    def obtener_movimientos_por_ubicacion(self, ubicacion: Ubicacion) -> List[MovimientoInventario]:
        """Obtiene el historial de movimientos de una ubicación específica"""
        return [m for m in self.movimientos if m.ubicacion == ubicacion]

# Crear el gestor de inventario
gestor = GestorInventario()

# Obtener todos los productos de una categoría
camisetas = gestor.obtener_productos_por_categoria(CategoriaProducto.ROPA)
papeleria = gestor.obtener_productos_por_categoria(CategoriaProducto.PAPELERIA)

# Buscar un producto específico
producto = gestor.buscar_producto_por_id(1)  # Retornará el Cuaderno Sofka

# Agregar las rutas al final del archivo
@app.route('/movimientos', methods=['POST'])
def registrar_movimiento():
    datos = request.json
    
    try:
        tipo = TipoMovimiento.ENTRADA if datos['tipo'] == 'entrada' else TipoMovimiento.SALIDA
        ubicacion = Ubicacion.MEDELLIN if datos['ubicacion'] == 'medellin' else Ubicacion.BOGOTA
        
        exito = gestor.registrar_movimiento(
            producto_id=datos['producto_id'],
            tipo=tipo,
            ubicacion=ubicacion,
            cantidad=datos['cantidad'],
            descripcion=datos['descripcion']
        )
        
        if exito:
            return jsonify({"message": "Movimiento registrado exitosamente"}), 200
        else:
            return jsonify({"message": "No hay suficiente stock o el producto no existe"}), 400
            
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@app.route('/movimientos/<ubicacion>', methods=['GET'])
def obtener_movimientos_ubicacion(ubicacion):
    try:
        ubicacion_enum = Ubicacion.MEDELLIN if ubicacion.lower() == 'medellin' else Ubicacion.BOGOTA
        movimientos = gestor.obtener_movimientos_por_ubicacion(ubicacion_enum)
        return jsonify([{
            'id': m.id,
            'producto_id': m.producto_id,
            'tipo': m.tipo.value,
            'ubicacion': m.ubicacion.value,
            'cantidad': m.cantidad,
            'fecha': m.fecha.isoformat(),
            'descripcion': m.descripcion
        } for m in movimientos]), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
