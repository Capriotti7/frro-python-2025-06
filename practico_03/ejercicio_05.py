"""Propiedades"""


class Auto:
    def __init__(self, nombre: str, precio: float = 0.0):
        self._nombre = nombre
        self._precio = precio

    @property
    def nombre(self) -> str:
        return self._nombre.capitalize() # Devuelve la primera letra

    @property
    def precio(self) -> float:
        return round(self._precio, 2)
    
    @precio.setter
    def precio(self, nuevo_precio: float) -> None:
        if nuevo_precio < 0:
            raise ValueError("El precio no puede ser negativo")
        self._precio = nuevo_precio

# NO MODIFICAR - INICIO
auto = Auto("Ford", 12_875.456)

assert auto.nombre == "Ford"
assert auto.precio == 12_875.46
auto.precio = 13_874.349
assert auto.precio == 13_874.35

try:
    auto.nombre = "Chevrolet"
    assert False
except AttributeError:
    assert True
# NO MODIFICAR - FIN


###############################################################################


from dataclasses import dataclass

@dataclass
class Auto:
    """Re-Escribir utilizando DataClasses"""
    _nombre: str
    _precio: float = 0.0

    @property
    def nombre(self) -> str:
        return self._nombre.capitalize()

    @nombre.setter
    def nombre(self, nuevo_nombre: str):
        raise AttributeError("No se puede modificar el nombre del auto")

    @property
    def precio(self) -> float:
        return round(self._precio, 2)

    @precio.setter
    def precio(self, nuevo_precio: float):
        if nuevo_precio < 0:
            raise ValueError("El precio no puede ser negativo")
        self._precio = nuevo_precio

# NO MODIFICAR - INICIO
auto = Auto("Ford", 12_875.456)

assert auto.nombre == "Ford"
assert auto.precio == 12_875.46
auto.precio = 13_874.349
assert auto.precio == 13_874.35

try:
    auto.nombre = "Chevrolet"
    assert False
except AttributeError:
    assert True
# NO MODIFICAR - FIN
