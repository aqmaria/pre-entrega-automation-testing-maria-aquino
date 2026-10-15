# Pre-entrega para el curso de Automation Testing de Talento Tech 

## Proposito del proyecto

Este proyecto implementa pruebas automatizadas sobre la aplicacion web SauceDemo.

El objetivo es validar funcionalidades principales de la aplicacion, incluyendo:

- Inicio de sesion.
- Visualizacion del catalogo de productos.
- Validacion de nombre y precio de los productos.
- Agregado de productos al carrito.
- Validacion del contador del carrito.
- Validacion de que el producto agregado se encuentre correctamente en el carrito.

Las pruebas Selenium se encuentran separadas para evitar que la falla de un caso de prueba afecte la ejecucion de los demas.

## Tecnologias utilizadas

- Python
- Selenium WebDriver
- Microsoft Edge
- Pytest
- unittest.mock para las pruebas unitarias de las funciones auxiliares

## Estructura del proyecto

```text
proyecto/
├── tests/
│   ├── test.py
│   └── utils_test.py
├── utils/
│   └── utils.py
├── reports/
│   ├── test_reports.html
│   └── utils_test_reports.html
└── pytest.ini
```

## Instalación de dependencias

Instalar las dependencias necesarias:

```bash
pip install selenium pytest
```

## Ejecucion de las pruebas

### Ejecutar todas las pruebas

```bash
python -m pytest -v
```

### Generar reporte de las pruebas funcionales

```bash
python -m pytest tests/test.py -v --html=reports/test_reports.html
```

### Generar reporte de las pruebas de Utils

```bash
python -m pytest tests/utils_test.py -v --html=reports/utils_test_reports.html
```

## Consideraciones

- Microsoft Edge debe estar instalado en el equipo para ejecutar las pruebas Selenium configuradas con `webdriver.Edge()`.
- Las interacciones con la interfaz utilizan esperas explicitas mediante `WebDriverWait` y `expected_conditions`.
- Cada prueba Selenium debe preparar su propio estado para mantener la independencia entre casos de prueba.
- La falla de una prueba no debe impedir que Pytest ejecute las restantes.
