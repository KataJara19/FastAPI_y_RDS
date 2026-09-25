# API de Productos y Pedidos

API RESTful construida con FastAPI y SQLModel para la gestión de un inventario de productos y el registro de pedidos.

El proyecto utiliza SQLite como base de datos local y está diseñado bajo una arquitectura modular, separando los modelos, esquemas, operaciones CRUD, rutas y configuración de la base de datos.

## Tecnologías Utilizadas

- Python 3.10+
- FastAPI
- SQLModel
- SQLite
- FastAPI CLI / Uvicorn

## Estructura del Proyecto

```text
backend/
├── src/
│   ├── crud/
│   │   ├── pedido_crud.py
│   │   └── producto_crud.py
│   │
│   ├── database/
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── pedido_model.py
│   │   └── producto_model.py
│   │
│   ├── routers/
│   │   ├── pedido_router.py
│   │   └── producto_router.py
│   │
│   ├── schemas/
│   │   ├── pedido_schema.py
│   │   └── producto_schema.py
│   │
│   └── main.py
│
├── venv/
├── .gitignore
├── requirements.txt
└── productos_pedidos.db
```

### Descripción de las carpetas

- `crud/`: contiene las operaciones relacionadas con la base de datos.
- `database/`: contiene la configuración de conexión y las sesiones de SQLite.
- `models/`: contiene los modelos de las tablas creados con SQLModel.
- `routers/`: contiene los endpoints y controladores de la API.
- `schemas/`: contiene los esquemas utilizados para la validación de datos.
- `main.py`: archivo principal para ejecutar la aplicación.
- `requirements.txt`: contiene las dependencias necesarias para ejecutar el proyecto.
- `productos_pedidos.db`: base de datos SQLite generada automáticamente.

---

# Instalación y Configuración

## 1. Abrir la terminal en la carpeta principal

Asegúrate de estar ubicado dentro de la carpeta `backend/` del proyecto.

```bash
cd backend
```

## 2. Crear el entorno virtual

En Linux o WSL:

```bash
python3 -m venv venv
```

## 3. Activar el entorno virtual

```bash
source venv/bin/activate
```

Cuando el entorno virtual se encuentre activo, normalmente aparecerá `(venv)` al inicio de la terminal.

Ejemplo:

```text
(venv) usuario@equipo:~/backend$
```

## 4. Instalar las dependencias

Instala las dependencias utilizando el archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

El proyecto utiliza principalmente:

- FastAPI
- SQLModel
- Uvicorn
- FastAPI CLI

## 5. Ejecutar el servidor

Levanta la aplicación en modo desarrollo utilizando:

```bash
fastapi dev
```

La aplicación estará disponible normalmente en:

```text
http://127.0.0.1:8000
```

La base de datos `productos_pedidos.db` se creará automáticamente cuando se inicialice la aplicación.

Si necesitas ejecutar la aplicación en un puerto específico, puedes indicar el puerto correspondiente.

Por ejemplo:

```bash
fastapi dev --port 8085
```

En este caso, la aplicación estaría disponible en:

```text
http://127.0.0.1:8085
```

---

# Documentación Interactiva de la API

FastAPI genera automáticamente documentación interactiva mediante Swagger UI.

Una vez que el servidor se encuentre en ejecución, abre en el navegador:

```text
http://127.0.0.1:8000/docs
```

Desde Swagger UI puedes visualizar y probar directamente los endpoints disponibles.

---

# Resumen de Endpoints

## General

### Verificar la API

```http
GET /
```

Retorna un mensaje de bienvenida y permite verificar que la API se encuentra funcionando.

### Verificar el estado del servidor

```http
GET /health
```

Permite comprobar el estado de salud del servidor.

---

# Productos

Los endpoints relacionados con productos utilizan la ruta:

```text
/productos
```

## Obtener todos los productos

```http
GET /productos/
```

Obtiene la lista completa de productos registrados en la base de datos.

## Obtener un producto por ID

```http
GET /productos/{id}
```

Obtiene la información de un producto específico utilizando su identificador.

Ejemplo:

```http
GET /productos/1
```

## Crear un producto

```http
POST /productos/
```

Registra un nuevo producto en la base de datos.

## Actualizar un producto

```http
PUT /productos/{id}
```

Actualiza la información de un producto existente.

Ejemplo:

```http
PUT /productos/1
```

## Eliminar un producto

```http
DELETE /productos/{id}
```

Elimina un producto de la base de datos utilizando su identificador.

Ejemplo:

```http
DELETE /productos/1
```

---

# Pedidos

Los endpoints relacionados con pedidos utilizan la ruta:

```text
/pedidos
```

## Obtener todos los pedidos

```http
GET /pedidos/
```

Obtiene la lista completa de pedidos registrados.

## Obtener un pedido por ID

```http
GET /pedidos/{id}
```

Obtiene la información de un pedido específico utilizando su identificador.

Ejemplo:

```http
GET /pedidos/1
```

## Crear un pedido

```http
POST /pedidos/
```

Registra un nuevo pedido y lo asocia con un producto existente.

## Actualizar un pedido

```http
PUT /pedidos/{id}
```

Permite actualizar información de un pedido, como:

- Estado.
- Dirección de envío.
- Cantidad.

Ejemplo:

```http
PUT /pedidos/1
```

## Eliminar un pedido

```http
DELETE /pedidos/{id}
```

Elimina un pedido registrado en la base de datos.

Ejemplo:

```http
DELETE /pedidos/1
```

---

# Ejemplos de Datos JSON para Pruebas

Los siguientes ejemplos pueden utilizarse directamente desde Swagger UI para probar los endpoints `POST` y `PUT`.

## Crear un Producto

Endpoint:

```http
POST /productos/
```

JSON de ejemplo:

```json
{
  "nombre": "Laptop ASUS Vivobook X1605VA",
  "descripcion": "Laptop con Intel Core i9, ideal para desarrollo.",
  "precio": 1150.00,
  "stock": 10
}
```

---

## Crear un Pedido

Endpoint:

```http
POST /pedidos/
```

Antes de registrar un pedido, asegúrate de que el valor enviado en `producto_id` corresponda a un producto que exista previamente en la base de datos.

JSON de ejemplo:

```json
{
  "producto_id": 1,
  "cantidad": 1,
  "direccion_envio": "Av. Simón Bolívar, Quito"
}
```

---

## Actualizar un Pedido

Endpoint:

```http
PUT /pedidos/{id}
```

Para actualizar un pedido, se pueden enviar únicamente los campos que se desean modificar.

Por ejemplo, para cambiar el estado del pedido:

```json
{
  "estado": "Completado"
}
```

---

# Flujo Básico de Pruebas

Para comprobar el funcionamiento general de la API desde Swagger UI, se puede seguir el siguiente orden:

1. Ejecutar el servidor:

```bash
fastapi dev
```

2. Abrir Swagger UI:

```text
http://127.0.0.1:8000/docs
```

3. Crear un producto utilizando:

```http
POST /productos/
```

4. Consultar el producto creado:

```http
GET /productos/{id}
```

5. Crear un pedido asociado al producto:

```http
POST /pedidos/
```

6. Consultar el pedido:

```http
GET /pedidos/{id}
```

7. Actualizar el estado del pedido:

```http
PUT /pedidos/{id}
```

8. Comprobar todos los productos y pedidos registrados:

```http
GET /productos/
GET /pedidos/
```

---

# Notas

- El entorno virtual `venv/` no debe subirse al repositorio.
- La base de datos SQLite puede incluirse en `.gitignore` si no se desea mantenerla dentro del repositorio.
- Antes de crear un pedido, el producto indicado mediante `producto_id` debe existir.
- Swagger UI permite probar todos los endpoints sin necesidad de utilizar herramientas externas.
- Para detener el servidor se puede utilizar `Ctrl + C` en la terminal donde se está ejecutando FastAPI.# MiprimerApi_EC2
