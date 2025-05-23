# practico_07/app.py

from flask import Flask, render_template, request, redirect, url_for, flash
import sys
import os

# Añadimos los directorios padre al path para importar los modulos de practico_05 y practico_06
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from practico_06.capa_negocio import NegocioSocio, DniRepetido, LongitudInvalida, MaximoAlcanzado
from practico_05.ejercicio_01 import Socio

app = Flask(__name__)
app.secret_key = 'your_secret_key' # Needed for flash messages
negocio_socio = NegocioSocio()

@app.route('/')
def index():
    socios = negocio_socio.todos()
    return render_template('index.html', socios=socios)

@app.route('/alta', methods=['GET', 'POST'])
def alta_socio():
    if request.method == 'POST':
        dni = request.form['dni']
        nombre = request.form['nombre']
        apellido = request.form['apellido']

        try:
            # Convert dni to int, as it's stored as Integer in the database
            dni = int(dni)
            nuevo_socio = Socio(dni=dni, nombre=nombre, apellido=apellido)
            if negocio_socio.alta(nuevo_socio):
                flash('Socio dado de alta exitosamente.', 'success')
                return redirect(url_for('index'))
            else:
                # If alta returns False, it means an exception was caught internally and printed
                flash('Error al dar de alta el socio. Verifique los datos.', 'danger')
        except ValueError:
            flash('El DNI debe ser un número entero.', 'danger')
        except DniRepetido:
            flash('Error: El DNI ingresado ya está en uso.', 'danger')
        except LongitudInvalida:
            flash('Error: El nombre y apellido deben tener entre 3 y 15 caracteres.', 'danger')
        except MaximoAlcanzado:
            flash('Error: Se ha alcanzado el máximo de socios permitidos.', 'danger')
        except Exception as e:
            flash(f'Error inesperado: {e}', 'danger')

    return render_template('socio_form.html', title='Alta de Socio', socio=None)

@app.route('/baja/<int:id_socio>')
def baja_socio(id_socio):
    if negocio_socio.baja(id_socio):
        flash('Socio dado de baja exitosamente.', 'success')
    else:
        flash('Error al dar de baja el socio.', 'danger')
    return redirect(url_for('index'))

@app.route('/modificar/<int:id_socio>', methods=['GET', 'POST'])
def modificar_socio(id_socio):
    socio_a_modificar = negocio_socio.buscar(id_socio)
    if not socio_a_modificar:
        flash('Socio no encontrado.', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        dni = request.form['dni']
        nombre = request.form['nombre']
        apellido = request.form['apellido']

        try:
            dni = int(dni)
            socio_a_modificar.dni = dni
            socio_a_modificar.nombre = nombre
            socio_a_modificar.apellido = apellido

            if negocio_socio.modificacion(socio_a_modificar):
                flash('Socio modificado exitosamente.', 'success')
                return redirect(url_for('index'))
            else:
                flash('Error al modificar el socio. Verifique los datos.', 'danger')
        except ValueError:
            flash('El DNI debe ser un número entero.', 'danger')
        except LongitudInvalida:
            flash('Error: El nombre y apellido deben tener entre 3 y 15 caracteres.', 'danger')
        except Exception as e:
            flash(f'Error inesperado: {e}', 'danger')

    return render_template('socio_form.html', title='Modificar Socio', socio=socio_a_modificar)

if __name__ == '__main__':
    # Ensure the database is clean for consistent testing
    datos = negocio_socio.datos
    datos.borrar_todos()
    app.run(debug=True)
