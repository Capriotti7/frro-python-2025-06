# Sistema Interno de Gestión Académica ISPI Oliveros

## Descripción del proyecto

La Fundación Hospital Oliveros es una institución educativa con carreras orientadas a medicina, ubicada en Rosario.
Este proyecto: Sistema Interno de GEstión Académica está pensado para aliviar/facilitar las tareas administrativas del instituto. El alcance del mismo se extiende a gestión de alumnos, inscripción de alumnos a materias, control de pago de cuotas y registros académicos, en combinación con datos estadísticos útiles para la toma de decisiones.
El objetivo del sistema es organizar, visualizar y registrar los registros académicos de alumnos. 

## Modelo de Dominio

Insertar el modelo de dominio aquí.

## Bosquejo de Arquitectura

Definir la arquitectura del sistema y como interactuan sus diferentes componentes. Utilizar el Paquete **Office** de Draw.io o similar. [Ejemplo Online]().

## Requerimientos

REQ001: El sistema debe registrar la asistencia de los alumnos.
REQ002: El sistema debe calcular el recargo de las cuotas no pagadas.
REQ003: El sistema debe poder calcular en un listado el porcentaje de asistencias de los alumnos.
REQ004: El sistema debe funcionar en una página web y solo se accederá desde una PC (puede estar sujeto a modificaciones en el futuro).
REQ008: El sistema debe poder escanear la documentacion de los alumnos y almacenarla en la BD.
REQ009: El sistema debe calcular deuda total de cada alumno.
REQ010: El sistema debe calcular el tiempo promedio de los alumnos en recibirse.

REQ005: El sistema debe usar los colores del instituto rojo y blanco.
REQ006: El sistema debe tener un logo siempre arriba izquierda.
REQ007: El sistema debe estar funcional por completo los días hábiles durante el horario de atención (8:00hs a 19:00hs)

### Funcionales

Listado y descripción breve de los requerimientos funcionales.

### No Funcionales

Listado y descripción breve de los requerimientos no funcionales. Utilizar las categorias dadas:

### Portability

**Obligatorios**

- El sistema debe funcionar correctamente en múltiples navegadores (Sólo Web).
- El sistema debe ejecutarse desde un único archivo .py llamado app.py (Sólo Escritorio).

### Security

**Obligatorios**

- Todas las contraseñas deben guardarse con encriptado criptográfico (SHA o equivalente).
- Todas los Tokens / API Keys o similares no deben exponerse de manera pública.

### Maintainability

**Obligatorios**

- El sistema debe diseñarse con la arquitectura en 3 capas. (Ver [checklist_capas.md](checklist_capas.md))
- El sistema debe utilizar control de versiones mediante GIT.
- El sistema debe estar programado en Python 3.8 o superior.

### Reliability

### Scalability

**Obligatorios**

- El sistema debe funcionar desde una ventana normal y una de incógnito de manera independiente (Sólo Web).
  - Aclaración: No se debe guardar el usuario en una variable local, deben usarse Tokens, Cookies o similares.

### Performance

**Obligatorios**

- El sistema debe funcionar en un equipo hogareño estándar.

### Reusability

### Flexibility

**Obligatorios**

- El sistema debe utilizar una base de datos SQL o NoSQL

## Stack Tecnológico

Definir que tecnologías se van a utilizar en cada capa y una breve descripción sobre por qué se escogió esa tecnologia.

### Capa de Datos

Definir que base de datos, ORM y tecnologías se utilizaron y por qué.

### Capa de Negocio

Definir que librerías e integraciones con terceros se utilizaron y por qué. En caso de consumir APIs, definir cúales se usaron.

### Capa de Presentación

Definir que framework se utilizó y por qué.
