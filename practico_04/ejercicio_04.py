"""Base de Datos SQL - Búsqueda"""

import datetime

from practico_04.ejercicio_01 import reset_tabla
from practico_04.ejercicio_02 import agregar_persona
import sqlite3


def buscar_persona(id_persona):
    conexion = sqlite3.connect('basededatos.db')
    cursor = conexion.cursor()

    cursor.execute('''
        SELECT * FROM Persona
        WHERE IdPersona = ?;
    ''', (id_persona,)) 

    fila = cursor.fetchone()
    conexion.close()

    if fila:
        # fila[2] es la fecha, que viene como string tipo '1988-05-15'
        fecha_nacimiento = datetime.datetime.strptime(fila[2], '%Y-%m-%d')
        return (fila[0], fila[1], fecha_nacimiento, fila[3], fila[4])
    else:
        return False

# NO MODIFICAR - INICIO
@reset_tabla
def pruebas():
    juan = buscar_persona(agregar_persona('juan perez', datetime.datetime(1988, 5, 15), 32165498, 180))
    '''print(juan)
    print((1, 'juan perez', datetime.datetime(1988, 5, 15), 32165498, 180))''' #prints añadidos para verificar

    assert juan == (1, 'juan perez', datetime.datetime(1988, 5, 15), 32165498, 180)
    assert buscar_persona(12345) is False

if __name__ == '__main__':
    pruebas()
# NO MODIFICAR - FIN
