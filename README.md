# API de Productos y Pedidos

API RESTful construida con **FastAPI** y **SQLModel** para la gestión de inventario de productos y el registro de pedidos, desplegada en la nube utilizando una instancia **Amazon EC2** y persistencia en una base de datos relacional gestionada **Amazon RDS (PostgreSQL)**.

El proyecto está diseñado bajo una arquitectura modular y desacoplada, separando modelos, esquemas, operaciones CRUD, controladores y la configuración de conexión mediante variables de entorno, bajo el principio de mínimo privilegio.

---

## Tecnologías Utilizadas

- Python 3.10+
- FastAPI
- SQLModel
- PostgreSQL
- Amazon RDS
- Amazon EC2
- PM2 (Process Manager)
- psycopg2-binary
- python-dotenv
- FastAPI CLI / Uvicorn

---

## Estructura del Proyecto

```text
TareaEC2yRDS/
└── productos-pedidos-api/
    └── backend/
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
        ├── .env
        ├── .env.example
        ├── .gitignore
        ├── requirements.txt
        └── README.md
```

### Descripción de las carpetas

- **`crud/`**: contiene las operaciones de persistencia y consultas CRUD (Create, Read, Update, Delete) en la base de datos.
- **`database/`**: contiene la configuración del motor de base de datos (`create_engine`), la gestión de sesiones (`get_session`) y la inicialización de tablas en Amazon RDS PostgreSQL.
- **`models/`**: contiene los modelos de datos y la definición de tablas creados con SQLModel.
- **`routers/`**: contiene las rutas, controladores y endpoints de la API.
- **`schemas/`**: contiene los esquemas Pydantic utilizados para la validación de entrada y transferencia de datos.
- **`main.py`**: punto de entrada principal para levantar y configurar la aplicación FastAPI.
- **`.env`**: almacena las variables de entorno y credenciales de acceso a Amazon RDS. Este archivo no debe subirse al repositorio.
- **`.env.example`**: plantilla pública con la estructura de las variables necesarias, sin credenciales sensibles.
- **`requirements.txt`**: contiene la lista de librerías y dependencias necesarias para ejecutar la aplicación.

---

# Configuración de Seguridad en AWS

El despliegue aplica el **principio de mínimo privilegio**, aislando la base de datos de accesos públicos y restringiendo las conexiones a las entidades autorizadas.

## 1. Security Group de la Instancia EC2

**Nombre:** `api-ec2-sg`

Controla el tráfico de red entrante hacia el servidor donde se ejecuta la API.

| Tipo | Protocolo | Puerto | Origen | Propósito |
|---|---|---:|---|---|
| SSH | TCP | 22 | `0.0.0.0/0` o My IP | Acceso remoto administrativo a la instancia |
| Custom TCP | TCP | 8085 | `0.0.0.0/0` | Acceso público a la API y Swagger UI |

## 2. Security Group de Amazon RDS

**Nombre:** `rds-postgres-sg`

Aísla la base de datos y permite únicamente conexiones entrantes autorizadas.

| Tipo | Protocolo | Puerto | Origen | Propósito |
|---|---|---:|---|---|
| PostgreSQL | TCP | 5432 | ID del Security Group de EC2 | Conexión desde la API desplegada en EC2 |
| PostgreSQL | TCP | 5432 | My IP (`/32`) | Administración local y consultas mediante cliente SQL o VS Code |

---

# Variables de Entorno

El proyecto desacopla las credenciales de la base de datos utilizando **python-dotenv** y `urllib.parse.quote_plus`, evitando almacenar credenciales directamente en el código fuente.

Crea un archivo `.env` en la raíz de `backend/` y, de acuerdo con la configuración actual del proyecto, una copia en `backend/src/`.

Ejemplo:

```env
DB_USER=postgres
DB_PASSWORD=tu_contrasena_rds
DB_HOST=tu-endpoint-de-rds.xxxxxx.us-east-1.rds.amazonaws.com
DB_PORT=5432
DB_NAME=postgres
```

> **Importante:** El archivo `.env` contiene información sensible y no debe subirse al repositorio Git.

---

# Instalación y Despliegue en Amazon EC2

## 1. Abrir la terminal en la carpeta principal

Asegúrate de estar ubicado dentro de la carpeta `backend/` del proyecto:

```bash
cd backend
```

---

## 2. Crear el entorno virtual

En Linux o WSL:

```bash
python3 -m venv venv
```

---

## 3. Activar el entorno virtual

```bash
source venv/bin/activate
```

Cuando el entorno virtual se encuentre activo, aparecerá `(venv)` al inicio de la terminal:

```text
(venv) ubuntu@ip-172-31-28-191:~/productos-pedidos-api/backend$
```

---

## 4. Instalar las dependencias

Instala las dependencias necesarias:

```bash
pip install -r requirements.txt
```

El proyecto utiliza principalmente:

- FastAPI
- SQLModel
- psycopg2-binary
- python-dotenv
- Uvicorn / FastAPI CLI

---

## 5. Ejecutar el servidor

### Modo Desarrollo

Levanta la aplicación utilizando:

```bash
fastapi dev src/main.py --port 8085
```

La aplicación estará disponible localmente en:

```text
http://127.0.0.1:8085
```

---

### Modo Producción con PM2 en Amazon EC2

Para mantener el servidor ejecutándose de manera continua en segundo plano y permitir su reinicio automático ante fallos:

```bash
cd src
pm2 start "../venv/bin/fastapi run main.py --port 8085" --name api
pm2 save
```

La aplicación estará accesible mediante la dirección IP pública de la instancia EC2:

```text
http://<TU_IP_PUBLICA_EC2>:8085
```

Para verificar el estado del proceso:

```bash
pm2 status
```

---

# Documentación Interactiva de la API

FastAPI genera automáticamente documentación interactiva mediante **Swagger UI**.

Una vez que el servidor se encuentre en ejecución, abre en el navegador:

```text
http://<TU_IP_PUBLICA_EC2>:8085/docs
```

Desde Swagger UI es posible visualizar, probar y verificar directamente las operaciones CRUD realizadas contra Amazon RDS.

---

# Resumen de Endpoints

## General

### Verificar la API

```http
GET /
```

Retorna un mensaje de bienvenida y permite comprobar que la API se encuentra funcionando.

### Verificar el estado del servidor

```http
GET /health
```

Permite comprobar el estado de salud del servidor y la conexión a los servicios.

---

# Productos

Los endpoints relacionados con productos utilizan la ruta base:

```text
/productos
```

## Obtener todos los productos

```http
GET /productos/
```

Obtiene la lista completa de productos registrados en Amazon RDS.

---

## Obtener un producto por ID

```http
GET /productos/{id}
```

Obtiene la información de un producto específico mediante su identificador.

Ejemplo:

```http
GET /productos/1
```

---

## Crear un producto

```http
POST /productos/
```

Registra un nuevo producto en la base de datos PostgreSQL.

---

## Actualizar un producto

```http
PUT /productos/{id}
```

Actualiza la información de un producto existente.

Ejemplo:

```http
PUT /productos/1
```

---

## Eliminar un producto

```http
DELETE /productos/{id}
```

Elimina un producto de la base de datos mediante su identificador.

Ejemplo:

```http
DELETE /productos/1
```

---

# Pedidos

Los endpoints relacionados con pedidos utilizan la ruta base:

```text
/pedidos
```

## Obtener todos los pedidos

```http
GET /pedidos/
```

Obtiene la lista completa de pedidos registrados.

---

## Obtener un pedido por ID

```http
GET /pedidos/{id}
```

Obtiene la información de un pedido específico mediante su identificador.

Ejemplo:

```http
GET /pedidos/1
```

---

## Crear un pedido

```http
POST /pedidos/
```

Registra un nuevo pedido y lo asocia con un producto existente.

---

## Actualizar un pedido

```http
PUT /pedidos/{id}
```

Permite actualizar la información de un pedido, como estado, dirección o cantidad.

Ejemplo:

```http
PUT /pedidos/1
```

---

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

Los siguientes ejemplos pueden utilizarse directamente desde **Swagger UI** para probar los endpoints `POST` y `PUT`.

## Crear un Producto

**Endpoint:**

```http
POST /productos/
```

**JSON de ejemplo:**

```json
{
  "nombre": "Laptop ASUS Vivobook X1605VA",
  "descripcion": "Laptop con Intel Core i9, ideal para desarrollo y virtualización.",
  "precio": 1150.00,
  "stock": 10
}
```

---

## Crear un Pedido

**Endpoint:**

```http
POST /pedidos/
```

> **Nota:** Antes de registrar un pedido, asegúrate de que el valor enviado en `producto_id` corresponda a un producto existente en la base de datos.

**JSON de ejemplo:**

```json
{
  "producto_id": 1,
  "cantidad": 2,
  "direccion_envio": "Av. Simón Bolívar, Quito"
}
```

---

## Actualizar un Pedido

**Endpoint:**

```http
PUT /pedidos/{id}
```

**JSON de ejemplo:**

```json
{
  "estado": "Completado"
}
```

---

# Flujo Básico de Pruebas y Verificación en RDS

Para validar el funcionamiento completo de la solución:

1. Iniciar el servicio en la instancia EC2 y comprobar que PM2 se encuentre activo:

   ```bash
   pm2 status
   ```

2. Abrir Swagger UI:

   ```text
   http://<TU_IP_PUBLICA_EC2>:8085/docs
   ```

3. Crear un producto mediante:

   ```http
   POST /productos/
   ```

4. Consultar el producto creado mediante:

   ```http
   GET /productos/{id}
   ```

5. Crear un pedido asociado al producto mediante:

   ```http
   POST /pedidos/
   ```

6. Modificar el pedido mediante:

   ```http
   PUT /pedidos/{id}
   ```

7. Verificar la persistencia ejecutando consultas SQL directamente en Amazon RDS mediante un cliente SQL o una extensión de VS Code:

   ```sql
   SELECT * FROM producto;
   SELECT * FROM pedido;
   ```

8. Eliminar un registro mediante:

   ```http
   DELETE /pedidos/{id}
   ```

9. Comprobar en PostgreSQL que el registro haya sido eliminado correctamente.

---

# Notas Importantes

- El entorno virtual `venv/` no debe subirse al repositorio Git.
- El archivo `.env` contiene credenciales sensibles y tampoco debe versionarse.
- Se recomienda mantener `.env` incluido dentro del archivo `.gitignore`.
- El archivo `.env.example` puede mantenerse en el repositorio como plantilla, siempre que no incluya credenciales reales.
- Las tablas en PostgreSQL se crean automáticamente al iniciar la API mediante la función `create_database()` definida en `database.py`.
- Las conexiones externas hacia Amazon RDS requieren SSL habilitado.
- El puerto utilizado por la API es `8085`.
- PostgreSQL utiliza el puerto `5432`.
- Para detener temporalmente el servicio administrado por PM2:

```bash
pm2 stop api
```

- Para eliminar completamente el proceso de PM2:

```bash
pm2 delete api
```

- Para volver a consultar el estado de los procesos:

```bash
pm2 status
```

---

# Arquitectura General

El flujo principal de comunicación de la aplicación es:

```text
Cliente / Swagger UI
        │
        │ HTTP :8085
        ▼
Amazon EC2
        │
        │ FastAPI
        ▼
Routers
        │
        ▼
CRUD
        │
        ▼
SQLModel
        │
        │ PostgreSQL :5432
        ▼
Amazon RDS
```

La instancia **EC2** aloja y ejecuta la API, mientras que **Amazon RDS** proporciona la persistencia de datos mediante PostgreSQL. La comunicación entre ambos servicios se controla mediante Security Groups y las credenciales se administran mediante variables de entorno.

---

## Seguridad

Las credenciales reales utilizadas para conectarse a Amazon RDS **nunca deben almacenarse directamente en el repositorio**.

El repositorio únicamente debe incluir una plantilla:

```text
.env.example
```

Los siguientes elementos deben permanecer excluidos mediante `.gitignore`:

```gitignore
.env
venv/
__pycache__/
*.pyc
```

---

## Autor

Proyecto desarrollado como parte de una implementación práctica de una **API REST con FastAPI, Amazon EC2 y Amazon RDS PostgreSQL**.
