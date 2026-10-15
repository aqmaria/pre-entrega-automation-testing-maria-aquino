import pytest

from unittest.mock import MagicMock
from selenium.common.exceptions import TimeoutException

import utils


#############################################################################################################
###                                              FIXTURES                                                 ###
#############################################################################################################

@pytest.fixture
def driver():

    # Creo un driver simulado
    return MagicMock()


@pytest.fixture
def wait_mock(monkeypatch):

    # Creo una espera explicita simulada
    wait = MagicMock()

    # Reemplazo WebDriverWait dentro de utils
    webdriver_wait_mock = MagicMock(
        return_value=wait
    )

    monkeypatch.setattr(
        utils,
        "WebDriverWait",
        webdriver_wait_mock
    )

    return wait


@pytest.fixture
def elementos_login():

    # Creo los elementos simulados del login
    username_input = MagicMock()
    password_input = MagicMock()
    login_button = MagicMock()

    return username_input, password_input, login_button


@pytest.fixture
def primer_producto():

    # Creo los elementos simulados del primer producto
    producto = MagicMock()
    nombre_producto = MagicMock()
    boton_agregar = MagicMock()

    # Simulo el nombre del producto
    nombre_producto.text = "Sauce Labs Backpack"

    # Simulo la busqueda del nombre dentro del producto
    producto.find_element.return_value = nombre_producto

    return producto, nombre_producto, boton_agregar


#############################################################################################################
###                                                LOGIN                                                  ###
#############################################################################################################

@pytest.mark.login
@pytest.mark.parametrize(
    "username, password",
    [
        pytest.param(
            "standard_user",
            "secret_sauce",
            id="standard-user"
        ),
        pytest.param(
            "problem_user",
            "secret_sauce",
            id="problem-user"
        ),
        pytest.param(
            "performance_glitch_user",
            "secret_sauce",
            id="performance-user"
        )
    ]
)
def test_login_completa_credenciales_y_presiona_boton(
    driver,
    wait_mock,
    elementos_login,
    username,
    password
):

    username_input, password_input, login_button = elementos_login

    # Configuro los elementos devueltos por las esperas
    wait_mock.until.side_effect = [
        username_input,
        password_input,
        login_button
    ]

    # Realizo el login
    utils.login(
        driver,
        username,
        password
    )

    # Verifico que se haya ingresado a SauceDemo
    driver.get.assert_called_once_with(
        "https://www.saucedemo.com"
    )

    # Verifico que se hayan realizado las tres esperas
    assert wait_mock.until.call_count == 3

    # Verifico que se hayan ingresado las credenciales
    username_input.send_keys.assert_called_once_with(
        username
    )

    password_input.send_keys.assert_called_once_with(
        password
    )

    # Verifico que se haya presionado el boton
    login_button.click.assert_called_once()


@pytest.mark.login
@pytest.mark.parametrize(
    "elementos_encontrados",
    [
        pytest.param(
            [],
            id="campo-usuario-no-encontrado"
        ),
        pytest.param(
            [MagicMock()],
            id="campo-password-no-encontrado"
        ),
        pytest.param(
            [MagicMock(), MagicMock()],
            id="boton-login-no-encontrado"
        )
    ]
)
def test_login_genera_error_si_falta_un_elemento(
    driver,
    wait_mock,
    elementos_encontrados
):

    # Configuro las esperas realizadas antes del error
    wait_mock.until.side_effect = [
        *elementos_encontrados,
        TimeoutException(
            "Elemento de login no encontrado"
        )
    ]

    # Verifico que la espera genere TimeoutException
    with pytest.raises(TimeoutException):

        utils.login(
            driver,
            "standard_user",
            "secret_sauce"
        )


#############################################################################################################
###                                         VERIFICACION DE URL                                           ###
#############################################################################################################

@pytest.mark.validacion_url
@pytest.mark.parametrize(
    "url_actual, ruta_esperada",
    [
        pytest.param(
            "https://www.saucedemo.com/inventory.html",
            "/inventory.html",
            id="inventario"
        ),
        pytest.param(
            "https://www.saucedemo.com/cart.html",
            "/cart.html",
            id="carrito"
        ),
        pytest.param(
            "https://www.saucedemo.com/checkout-step-one.html",
            "/checkout-step-one.html",
            id="checkout"
        )
    ]
)
def test_verificar_url_acepta_ruta_correcta(
    driver,
    wait_mock,
    url_actual,
    ruta_esperada
):

    # Simulo la URL actual
    driver.current_url = url_actual

    # Simulo que se cumple la espera
    wait_mock.until.return_value = True

    # Verifico que la funcion acepte la ruta
    utils.verificar_url(
        driver,
        ruta_esperada
    )

    # Verifico que se haya realizado la espera
    wait_mock.until.assert_called_once()


@pytest.mark.validacion_url
@pytest.mark.parametrize(
    "url_actual, ruta_esperada",
    [
        pytest.param(
            "https://www.saucedemo.com/",
            "/inventory.html",
            id="no-redirige-al-inventario"
        ),
        pytest.param(
            "https://www.saucedemo.com/inventory.html",
            "/cart.html",
            id="no-redirige-al-carrito"
        ),
        pytest.param(
            "https://www.saucedemo.com/cart.html",
            "/checkout-step-one.html",
            id="no-redirige-al-checkout"
        )
    ]
)
def test_verificar_url_genera_error_si_no_se_produce_redireccion(
    driver,
    wait_mock,
    url_actual,
    ruta_esperada
):

    # Simulo la URL actual
    driver.current_url = url_actual

    # Simulo que la redireccion no se produce
    wait_mock.until.side_effect = TimeoutException(
        "No se produjo la redireccion"
    )

    # Verifico que la espera genere TimeoutException
    with pytest.raises(TimeoutException):

        utils.verificar_url(
            driver,
            ruta_esperada
        )


#############################################################################################################
###                                       VERIFICACION DE TITULO                                          ###
#############################################################################################################

@pytest.mark.validacion_titulo
@pytest.mark.parametrize(
    "titulo",
    [
        pytest.param(
            "Swag Labs",
            id="swag-labs"
        ),
        pytest.param(
            "Products",
            id="products"
        ),
        pytest.param(
            "Your Cart",
            id="your-cart"
        )
    ]
)
def test_verificar_titulo_acepta_titulo_correcto(
    driver,
    wait_mock,
    titulo
):

    # Simulo el titulo actual
    driver.title = titulo

    # Simulo que se cumple la espera
    wait_mock.until.return_value = True

    # Verifico que la funcion acepte el titulo
    utils.verificar_titulo(
        driver,
        titulo
    )


@pytest.mark.validacion_titulo
@pytest.mark.parametrize(
    "titulo_actual, titulo_esperado",
    [
        pytest.param(
            "Titulo incorrecto",
            "Swag Labs",
            id="titulo-diferente"
        ),
        pytest.param(
            "",
            "Swag Labs",
            id="titulo-vacio"
        ),
        pytest.param(
            "Products",
            "Your Cart",
            id="titulo-de-otra-seccion"
        )
    ]
)
def test_verificar_titulo_genera_error_si_no_es_el_esperado(
    driver,
    wait_mock,
    titulo_actual,
    titulo_esperado
):

    # Simulo el titulo actual
    driver.title = titulo_actual

    # Simulo que el titulo esperado no aparece
    wait_mock.until.side_effect = TimeoutException(
        "Titulo esperado no encontrado"
    )

    # Verifico que la espera genere TimeoutException
    with pytest.raises(TimeoutException):

        utils.verificar_titulo(
            driver,
            titulo_esperado
        )


#############################################################################################################
###                                         OBTENER PRODUCTOS                                             ###
#############################################################################################################

@pytest.mark.catalogo
@pytest.mark.parametrize(
    "cantidad_productos",
    [
        pytest.param(1, id="un-producto"),
        pytest.param(2, id="dos-productos"),
        pytest.param(6, id="seis-productos")
    ]
)
def test_obtener_productos_devuelve_productos_visibles(
    driver,
    wait_mock,
    cantidad_productos
):

    # Creo los productos simulados
    productos_simulados = [
        MagicMock()
        for _ in range(cantidad_productos)
    ]

    # Simulo los productos devueltos por la espera
    wait_mock.until.return_value = productos_simulados

    # Obtengo los productos visibles
    productos = utils.obtener_productos(driver)

    # Verifico que se haya realizado la espera
    wait_mock.until.assert_called_once()

    # Verifico que se devuelvan los productos encontrados
    assert productos == productos_simulados
    assert len(productos) == cantidad_productos


@pytest.mark.catalogo
def test_obtener_productos_genera_error_si_catalogo_esta_vacio(
    driver,
    wait_mock
):

    # Simulo que no aparecen productos
    wait_mock.until.side_effect = TimeoutException(
        "No se encontraron productos"
    )

    # Verifico que la espera genere TimeoutException
    with pytest.raises(TimeoutException):

        utils.obtener_productos(driver)


#############################################################################################################
###                                    AGREGAR PRIMER PRODUCTO                                            ###
#############################################################################################################

@pytest.mark.carrito
def test_agregar_primer_producto_presiona_boton_y_devuelve_nombre(
    driver,
    wait_mock,
    primer_producto
):

    producto, nombre_producto, boton_agregar = primer_producto

    # Simulo el producto y el boton devueltos por las esperas
    wait_mock.until.side_effect = [
        producto,
        boton_agregar
    ]

    # Agrego el primer producto al carrito
    resultado = utils.agregar_primer_producto(driver)

    # Verifico que se hayan realizado dos esperas
    assert wait_mock.until.call_count == 2

    # Verifico que se haya presionado el boton
    boton_agregar.click.assert_called_once()

    # Verifico que se devuelva el nombre
    assert resultado == "Sauce Labs Backpack"


@pytest.mark.carrito
@pytest.mark.parametrize(
    "elementos_encontrados",
    [
        pytest.param(
            [],
            id="producto-no-encontrado"
        ),
        pytest.param(
            [MagicMock()],
            id="boton-no-encontrado"
        )
    ]
)
def test_agregar_primer_producto_genera_error_si_falla_una_espera(
    driver,
    wait_mock,
    elementos_encontrados
):

    # Configuro las esperas realizadas antes del error
    wait_mock.until.side_effect = [
        *elementos_encontrados,
        TimeoutException(
            "Elemento del producto no encontrado"
        )
    ]

    # Verifico que la espera genere TimeoutException
    with pytest.raises(TimeoutException):

        utils.agregar_primer_producto(driver)