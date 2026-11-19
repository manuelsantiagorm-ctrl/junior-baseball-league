# Junior Baseball League

Proyecto Django con PostgreSQL. Base de datos: `junior_baseball_league`.

## Modelos

- `Team`: id automático, name, city y category (Infantil o Juvenil).
- `Player`: id automático, name, number, position, birth_date y team.
- Un equipo tiene muchos jugadores. La columna `team_id` referencia al equipo.
- Al eliminar un equipo se eliminan sus jugadores asociados.

Las categorías son opciones iniciales porque la imagen no especifica sus valores.
Pueden editarse en `apps/league/models.py`.

## Ejecutar en PowerShell

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py createsuperuser
.\.venv\Scripts\python.exe manage.py runserver
```

Abrir http://127.0.0.1:8000/admin/ para gestionar equipos y jugadores.
El superusuario de Django se crea con el comando anterior; es una cuenta distinta
del usuario PostgreSQL que se utiliza desde pgAdmin.

## Páginas HTML del CRUD

- Inicio: http://127.0.0.1:8000/league/
- Equipos: http://127.0.0.1:8000/league/equipos/
- Jugadores: http://127.0.0.1:8000/league/jugadores/

Cada listado permite crear, consultar, editar y eliminar registros. La ficha de
un equipo muestra su plantilla y permite agregar jugadores con ese equipo
preseleccionado. La eliminación requiere confirmar mediante un formulario;
eliminar un equipo también elimina sus jugadores.

Todas las páginas del CRUD requieren una sesión de administrador activo
(superusuario con acceso al panel). Se utiliza el mismo inicio de sesión de
`/admin/login/`. Los visitantes son redirigidos al acceso y los usuarios sin
permisos de administrador reciben una respuesta 403. El inicio permanece público.

Ejecutar las pruebas (requiere permisos para crear una base temporal en PostgreSQL):

```powershell
.\.venv\Scripts\python.exe manage.py test apps.league.tests --noinput
```

La conexión local está configurada en `jbl_project/settings.py`. Se puede
sobrescribir mediante las variables de entorno `PGDATABASE`, `PGUSER`,
`PGPASSWORD`, `PGHOST` y `PGPORT`. No se requiere un archivo `.env`.
