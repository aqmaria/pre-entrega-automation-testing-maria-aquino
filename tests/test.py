import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import utils

@pytest.fixture
def driver():

    # Creo una instancia nueva del navegador para cada test
    driver = webdriver.Edge()

    yield driver

    # Cierro el navegador al finalizar cada test
    driver.quit()


@pytest.fixture
def wait(driver):

    # Creo una espera explicita de hasta 5 segundos
    return WebDriverWait(driver, 5)


#############################################################################################################
###                                             TEST DE LOGIN                                             ###
#############################################################################################################

@pytest.mark.login
def test_login(driver):

    # Realizo el login
    utils.login(driver)

    # Verifico redireccion al inventario
    utils.verificar_url(driver, "/inventory.html")

    # Verifico titulo del head
    utils.verificar_titulo(driver, "Swag Labs")


#############################################################################################################
###                                          TEST DE CATALOGO                                             ###
#############################################################################################################

@pytest.mark.catalogo
def test_catalogo(driver, wait):

    # Realizo el login
    utils.login(driver)

    # Verifico posicion en el inventario
    utils.verificar_url(driver, "/inventory.html")

    # Espero que el titulo de la seccion sea visible
    titulo_catalogo = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "header .title")
        )
    )

    # Verifico titulo de la seccion
    assert titulo_catalogo.text == "Products", \
        "Titulo inesperado para el header"

    # Verifico productos visibles
    productos = utils.obtener_productos(driver)

    assert len(productos) > 0, \
        "No se encontraron productos visibles"

    # Verifico datos del primer producto visible
    assert productos[0].find_element(
        By.CLASS_NAME,
        "inventory_item_name"
    ).text.strip(), "El item no tiene nombre"

    assert productos[0].find_element(
        By.CLASS_NAME,
        "inventory_item_price"
    ).text.strip(), "El item no tiene precio"

    # Verifico existencia de ordenador de productos
    ordenador = wait.until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "product_sort_container")
        )
    )

    assert ordenador.is_displayed(), \
        "Ordenador de productos no encontrado"

    # Verifico existencia del carrito
    carrito = wait.until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "shopping_cart_link")
        )
    )

    assert carrito.is_displayed(), \
        "Carrito no encontrado"

    # Verifico existencia del menu
    menu = wait.until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, "bm-menu")
        )
    )

    assert menu, \
        "Menu no encontrado"


#############################################################################################################
###                                           TEST DE CARRITO                                             ###
#############################################################################################################

@pytest.mark.carrito
def test_carrito(driver, wait):

    # Realizo el login
    utils.login(driver)

    # Verifico posicion en el inventario
    utils.verificar_url(driver, "/inventory.html")

    # Agrego el primer producto del inventario al carrito
    first_product_name = utils.agregar_primer_producto(driver)

    # Espero que aparezca el contador del carrito
    badge = wait.until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "shopping_cart_badge")
        )
    )

    # Confirmo que el contador del carrito muestra 1
    assert badge.text == "1", \
        "Contador de carrito no incrementado"

    # Espero que el carrito se pueda presionar
    shopping_cart = wait.until(
        EC.element_to_be_clickable(
            (By.CLASS_NAME, "shopping_cart_link")
        )
    )

    # Ingreso al carrito
    shopping_cart.click()

    # Espero que aparezca el producto agregado
    cart_product = wait.until(
        EC.visibility_of_element_located(
            (
                By.CSS_SELECTOR,
                ".cart_item .inventory_item_name"
            )
        )
    )

    # Verifico que el producto del carrito sea el producto agregado
    assert cart_product.text == first_product_name, \
        "El nombre del producto del carrito no coincide con el del producto que fue agregado"