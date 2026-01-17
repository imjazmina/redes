# 🐧 Broadcast & Testing

## 📌 Descripción general

Este proyecto combina **dos desafíos técnicos complementarios**:

1. **Desarrollo de una aplicación de chat en tiempo real usando sockets (broadcast)**
2. **Implementación de un sistema completo de testing (unitario + integración) sobre ese chat**
3. 
---

## 🧠 Conocimientos y habilidades trabajadas

### 🔌 Programación de Redes

* Uso de `socket.AF_INET` y `socket.SOCK_STREAM`
* Comunicación cliente-servidor mediante TCP
* Manejo de múltiples clientes concurrentes
* Implementación de lógica de **broadcast**
* Gestión de conexiones y desconexiones inesperadas
* Manejo de errores de red

### 🧵 Concurrencia

* Uso de `threading`
* Protección de recursos compartidos con `Lock`
* Envío y recepción simultánea de mensajes

### 🧪 Testing & QA

* Pruebas unitarias con `pytest`
* Separación de lógica testeable (`utils.py`)
* Casos positivos y negativos
* Aplicación del ciclo **TDD (Red → Green → Refactor)**
* Pruebas de integración reales usando sockets
* Simulación de múltiples clientes
* Validación de desconexiones abruptas
* Uso de `pytest fixtures`
* Ejecución de procesos con `subprocess`
* Análisis de **code coverage**

---

## 📂 Estructura del proyecto

```
redes/
├── server.py              # Servidor de chat con broadcast
├── client.py              # Cliente por terminal
├── utils.py               # Lógica reutilizable y validaciones
├── test/
│   ├── test_utils.py      # Pruebas unitarias
│   └── test_integration.py# Pruebas de integración
├── documentacion.txt
└── README.md
```

---

## 🚀 Funcionalidades principales

### 🧑‍💻 Servidor

* Acepta múltiples conexiones
* Mantiene una lista activa de clientes
* Reenvía mensajes a todos los clientes conectados (broadcast)
* Elimina clientes desconectados sin afectar al resto

### 🫣 Cliente

* Comunicación por terminal
* Envío y recepción simultánea de mensajes
* Manejo de cierre voluntario y forzado

---

## 🧪 Testing

### ✅ Pruebas unitarias

Ubicadas en `test/test_utils.py`.

Se validan funciones críticas como:

* mensajes válidos
* mensajes vacíos o con solo espacios
* mensajes demasiado largos
* valores inválidos (`None`)
* formateo correcto de mensajes

Estas pruebas permiten validar la lógica de forma **aislada y determinista**.

---

### 🔄 Pruebas de integración

Ubicadas en `test/test_integration.py`.

Se prueba el sistema completo como una caja negra:

* conexión cliente-servidor
* múltiples clientes conectados simultáneamente
* envío y recepción de mensajes
* envío de múltiples mensajes consecutivos
* desconexión repentina de clientes
* estabilidad del servidor ante fallos

El servidor se ejecuta en un **subproceso real**, simulando un entorno cercano a producción.

---

## 📊 Code Coverage

Se utiliza `pytest-cov` para medir cobertura:

```bash
python -m pytest --cov=utils --cov-report=term-missing
```

* `utils.py` alcanza **100% de cobertura**
* El servidor no es medido por coverage debido a que se ejecuta en un subproceso

Esto es una limitación técnica conocida y aceptada: el **comportamiento del servidor se valida mediante pruebas de integración**, no por conteo de líneas.

---

## ▶️ Cómo ejecutar el proyecto

### Levantar servidor manualmente

```bash
python server.py
```

### Ejecutar un cliente

```bash
python client.py
```

### Ejecutar todos los tests

```bash
python -m pytest
```
