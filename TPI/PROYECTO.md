# Sistema Interno de Gestión Académica ISPI Oliveros

## Descripción del proyecto

La Fundación Hospital Oliveros es una institución educativa con carreras orientadas a medicina, ubicada en Rosario.
Este proyecto: Sistema Interno de GEstión Académica está pensado para aliviar/facilitar las tareas administrativas del instituto. El alcance del mismo se extiende a gestión de alumnos, inscripción de alumnos a materias, control de pago de cuotas y registros académicos, en combinación con datos estadísticos útiles para la toma de decisiones.
El objetivo del sistema es organizar, visualizar y registrar los registros académicos de alumnos. 

## Modelo de Dominio

[Link al modelo](https://drive.google.com/file/d/1dFN4Qkw96IlSugg3RcRr6Ni13aRTl1cl/view?usp=drive_link)

## Bosquejo de Arquitectura

Definir la arquitectura del sistema y como interactuan sus diferentes componentes. Utilizar el Paquete **Office** de Draw.io o similar. [Ejemplo Online]().

## Requerimientos

### Funcionales

* REQ001: El sistema debe permitir registrar la asistencia de los alumnos a cada clase de un curso.
* REQ002: El sistema debe calcular automáticamente los recargos por demora en las cuotas vencidas y no pagadas.
* REQ003: El sistema debe generar un listado de alumnos por curso, indicando el porcentaje de asistencia de cada uno.
* REQ004: El sistema debe permitir la carga y almacenamiento de documentación digitalizada (escaneada) para cada alumno y mostrarla en una ficha.
* REQ005: El sistema debe calcular y mostrar la deuda total acumulada de cada alumno.
* REQ006: El sistema debe calcular el tiempo promedio que tardan los alumnos en completar una carrera, desde su primera inscripción hasta la aprobación de la última materia.
* REQ007: El sistema debe permitir a los usuarios (Administrativos, Docentes, Superusuarios) iniciar sesión utilizando su username y contraseña.
* REQ008: El sistema debe permitir a un usuario autenticado cerrar su sesión de forma segura.
* REQ009: El sistema debe restringir el acceso a las diferentes secciones (módulos ABM) basándose en el rol del usuario (Superusuario, Administrativo, Docente).
* REQ010: Si un usuario intenta acceder a una URL para la cual no tiene permisos (ej. un Docente intentando editar una Carrera), el sistema debe mostrar una página de error 403 (Acceso Denegado).
* REQ011: El sistema debe permitir solo al Superusuario crear nuevos registros de Docentes. Este proceso debe crear una cuenta de User (para el login) y un perfil Docente asociado.
* REQ012: El sistema debe permitir al Superusuario gestionar (crear, editar, eliminar) las cuentas de usuario con rol Administrativo.
* REQ013: El sistema debe proveer un formulario para registrar un nuevo alumno, almacenando DNI, nombre, apellido, email, fecha de nacimiento, teléfono, dirección, localidad y nacionalidad.
* REQ014: El sistema debe permitir la edición de toda la información personal de un alumno previamente registrado.
* REQ015: El sistema debe permitir la eliminación de un registro de alumno, solicitando confirmación antes de proceder.
* REQ016: El sistema debe permitir el Alta, Baja (eliminación) y Modificación de las carreras ofrecidas por el instituto (nombre, duración, titulación, resolución), solo por el SuperUsuario.
* REQ017: El sistema debe permitir el Alta, Baja y Modificación de las Materias, las cuales estan asociadas a una carrera específica.
* REQ018: El sistema debe permitir el Alta, Baja y Modificación de los Cursos (comisiones), los cuales deben estar siempre asociados a una materia específica.
* REQ019: El usuario debe poder navegar desde el listado de Carreras, seleccionar una, ver sus Materias, seleccionar una materia y ver sus Cursos.
* REQ020: Al crear o editar un Curso, el sistema debe permitir seleccionar un Docente (del listado de docentes existentes) para asignarlo a dicho curso.
* REQ021: El sistema debe mostrar un listado de todos los docentes, exhibiendo su nombre y apellido.
* REQ022: El sistema debe permitir editar los datos de un docente y eliminar el registro de un docente a los SuperUsuarios.
* REQ023: El sistema debe permitir registrar múltiples valores de cuota para una misma carrera, donde cada valor debe tener una "fecha de vigencia" que indique a partir de cuándo es válido.
* REQ024: El sistema debe ser capaz de determinar y mostrar automáticamente el "valor de cuota actual" de una carrera, basándose en el último precio registrado.

### No Funcionales

### Portability

- El sistema debe ser accesible a través de una página web desde una PC de escritorio.
- El sistema debe funcionar correctamente en los navegadores web modernos más utilizados (Chrome, Firefox, Edge).

### Security

- Todas las contraseñas de usuario deben almacenarse en la base de datos de forma encriptada (utilizando el sistema de hashing de Django).
- Las claves de API o credenciales sensibles no deben estar expuestas en el código fuente (se utilizarán variables de entorno).

### Maintainability

- El sistema debe ser desarrollado bajo la arquitectura en 3 capas.
- El código fuente será gestionado con el sistema de control de versiones GIT.
- El sistema se programará en Python 3.8 o superior.

### Reliability

- El sistema debe garantizar su funcionamiento y disponibilidad durante los días hábiles en el horario de atención del instituto (8:00hs a 19:00hs).

### Scalability

- El sistema debe soportar sesiones de usuario independientes, permitiendo el uso simultáneo desde una ventana normal y una de incógnito sin conflictos.

### Performance

- El sistema debe operar de manera fluida en un equipo de escritorio estándar de la administración.

### Usability

- La interfaz de usuario debe utilizar la paleta de colores institucional (rojo y blanco).
- El logo de la institución debe permanecer visible en la esquina superior izquierda en todas las pantallas.

### Flexibility

- El sistema utilizará una base de datos SQL para la persistencia de los datos.

## Stack Tecnológico

La selección de tecnologías se basa en la robustez, la productividad y el cumplimiento de los requisitos del proyecto.

### Capa de Datos

Base de Datos: MySQL tanto para el entorno de desarrollo como para el de producción.
¿Por qué?: Utilizar el mismo motor de base de datos en ambos entornos es una buena práctica que elimina posibles incompatibilidades o comportamientos inesperados que podrían surgir al migrar de una base de datos a otra (como de SQLite a MySQL). MySQL es un sistema de gestión de bases de datos robusto, escalable y con un rendimiento probado, ideal para las necesidades del proyecto desde el inicio del desarrollo hasta su despliegue final.

ORM: Django ORM.
¿Por qué?: Viene integrado en Django, lo que garantiza una compatibilidad perfecta. Permite interactuar con la base de datos utilizando objetos de Python en lugar de escribir SQL, lo que acelera el desarrollo, reduce errores y facilita el cambio entre SQLite y MySQL sin modificar el código de negocio.

### Capa de Negocio

Librerías: Python 3.8+ como lenguaje base. La lógica de negocio se implementará en módulos de Python puros (ej. services.py o una carpeta business dentro de las apps de Django) para mantenerla desacoplada de la web.
¿Por qué?: Separar la lógica en archivos específicos que no dependen de Django (salvo por los modelos que reciben como datos) hace que el código sea más limpio, fácil de probar y reutilizable.

Testing: Pytest.
¿Por qué?: Aunque es opcional en la checklist, es una buena práctica. Pytest es un framework de testing potente y fácil de usar en Python, ideal para crear tests unitarios que verifiquen que las reglas de negocio (ej. el cálculo de recargos) funcionan como se espera.

### Capa de Presentación

Framework: Django.
¿Por qué?: Es un framework "batteries-included" (pilas incluidas) que provee un sistema de autenticación, panel de administración, ORM y motor de plantillas de forma nativa. Su patrón MVT (Modelo-Vista-Template) se alinea perfectamente con la arquitectura de 3 capas, permitiendo un desarrollo rápido y ordenado.
