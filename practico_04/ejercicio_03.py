"""Base de Datos SQL - Baja"""

import datetime

from practico_04.ejercicio_01 import reset_tabla
from practico_04.ejercicio_02 import agregar_persona
import sqlite3

def borrar_persona(id_persona):
    """Implementar la funcion borrar_persona, que elimina un registro en la 
    tabla Persona. Devuelve un booleano en base a si encontro el registro y lo 
    borro o no."""
    conexion = sqlite3.connect("basededatos.db")
    cursor = conexion.cursor()
    cursor.execute('''
        DELETE FROM Persona
        WHERE IdPersona = ?;
    ''', (id_persona,)) 
    conexion.commit()
    filas_afectadas = cursor.rowcount
    conexion.close()
    if filas_afectadas == 0:
        return False
    return True

# NO MODIFICAR - INICIO
@reset_tabla
def pruebas():
    assert borrar_persona(agregar_persona('juan perez', datetime.datetime(1988, 5, 15), 32165498, 180))
    assert borrar_persona(12345) is False

if __name__ == '__main__':
    pruebas()
# NO MODIFICAR - FIN
