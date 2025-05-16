"""Base de Datos - ORM"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from practico_05.ejercicio_01 import Base, Socio

from typing import List, Optional

class DatosSocio():

    def __init__(self):
        
        self.engine = create_engine('sqlite:///socios.db') #Crea la base de datos 
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def buscar(self, id_socio: int) -> Optional[Socio]:
        """Devuelve la instancia del socio, dado su id. Devuelve None si no 
        encuentra nada.
        """

        socio = self.session.query(Socio).filter(Socio.id == id_socio).first()        # Busca el socio por su id
        return socio

    def buscar_dni(self, dni_socio: int) -> Optional[Socio]:
        """Devuelve la instancia del socio, dado su dni. Devuelve None si no 
        encuentra nada.
        """
        socio = self.session.query(Socio).filter(Socio.dni == dni_socio).first()        # Busca el socio por su dni
        return socio
        
    def todos(self) -> List[Socio]:
        """Devuelve listado de todos los socios en la base de datos."""
        socios = self.session.query(Socio).all()        # Devuelve todos los socios
        return socios

    def borrar_todos(self) -> bool:
        """Borra todos los socios de la base de datos. Devuelve True si el 
        borrado fue exitoso.
        """
        try:
            self.session.query(Socio).delete()
            self.session.commit()
            return True
        except Exception as err:
            print(f"Error al borrar todos los socios: {err}") #Si no se logran borrar todos los socios, se imprime el error
            self.session.rollback()                         # y se deshace la transacción para evitar inconsistencias
            return False

    def alta(self, socio: Socio) -> Socio:
        """Agrega un nuevo socio a la tabla y lo devuelve"""
        try:
            self.session.add(socio)
            self.session.commit()
            return socio
        except Exception as err:
            print(f"Error al agregar el socio: {err}")
            self.session.rollback()                         # Si no se logra agregar el socio, se imprime el error
            return None

    def baja(self, id_socio: int) -> bool:
        """Borra el socio especificado por el id. Devuelve True si el borrado 
        fue exitoso.
        """
        try:
            socio = self.buscar(id_socio)
            if socio:
                self.session.delete(socio)
                self.session.commit()
                return True
            else:
                print(f"No se encontró un socio con el id: {id_socio}")
                return False
        except Exception as err:
            print(f"Error al borrar el socio: {err}")
            self.session.rollback()                         # Si no se logra borrar el socio, se imprime el error
            return False

    def modificacion(self, socio: Socio) -> Socio:
        """Guarda un socio con sus datos modificados. Devuelve el Socio 
        modificado.
        """
        try:
            socio_modificado = self.buscar(socio.id)
            if socio_modificado:
                socio_modificado.dni = socio.dni
                socio_modificado.nombre = socio.nombre
                socio_modificado.apellido = socio.apellido
                self.session.commit()
                return socio_modificado
            else:
                print(f"No se encontró un socio con el id: {socio.id}")
                return None
        except Exception as err:
            print(f"Error al modificar el socio: {err}")
            self.session.rollback()                         # Si no se logra modificar el socio, se imprime el error
            return None
    
    def contarSocios(self) -> int:
        """Devuelve el total de socios que existen en la tabla"""
        try:
            total_socios = self.session.query(Socio).count()        # Cuenta el total de socios
            return total_socios
        except Exception as err:
            print(f"Error al contar los socios: {err}")            # Si no se logra contar los socios, se imprime el error
            return 0



# NO MODIFICAR - INICIO

# Test Creación
datos = DatosSocio()

# Test Alta
socio = datos.alta(Socio(dni=12345678, nombre='Juan', apellido='Perez'))
assert socio.id > 0

# Test Baja
assert datos.baja(socio.id) == True

# Test Consulta
socio_2 = datos.alta(Socio(dni=12345679, nombre='Carlos', apellido='Perez'))
assert datos.buscar(socio_2.id) == socio_2

# Test Buscar DNI
socio_2 = datos.alta(Socio(dni=12345670, nombre='Carlos', apellido='Perez'))
assert datos.buscar_dni(socio_2.dni) == socio_2

# Test Modificación
socio_3 = datos.alta(Socio(dni=12345680, nombre='Susana', apellido='Gimenez'))
socio_3.nombre = 'Moria'
socio_3.apellido = 'Casan'
socio_3.dni = 13264587
datos.modificacion(socio_3)
socio_3_modificado = datos.buscar(socio_3.id)
assert socio_3_modificado.id == socio_3.id
assert socio_3_modificado.nombre == 'Moria'
assert socio_3_modificado.apellido == 'Casan'
assert socio_3_modificado.dni == 13264587

# Test Conteo
assert len(datos.todos()) == 3

# Test Delete
datos.borrar_todos()
assert len(datos.todos()) == 0

# NO MODIFICAR - FIN