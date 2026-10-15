from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


TIEMPO_ESPERA = 5


def login(driver, username="standard_user", password="secret_sauce"):

    wait = WebDriverWait(driver, TIEMPO_ESPERA)

    driver.get("https://www.saucedemo.com")

    # Espero que el campo de usuario sea visible
    username_input = wait.until(
        EC.visibility_of_element_located(
            (By.ID, "user-name")
        )
    )

    # Espero que el campo de password sea visible
    password_input = wait.until(
        EC.visibility_of_element_located(
            (By.ID, "password")
        )
    )

    # Espero que el boton de login se pueda presionar
    login_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'input[type="submit"]')
        )
    )

    username_input.send_keys(username)
    password_input.send_keys(password)

    login_button.click()


def verificar_url(driver, ruta):

    wait = WebDriverWait(driver, TIEMPO_ESPERA)

    # Espero que se produzca la redireccion
    wait.until(
        EC.url_contains(ruta)
    )

    assert ruta in driver.current_url, \
        f"No se redirigió correctamente a {ruta}"


def verificar_titulo(driver, titulo):

    wait = WebDriverWait(driver, TIEMPO_ESPERA)

    # Espero que el titulo del head sea el esperado
    wait.until(
        EC.title_is(titulo)
    )

    assert driver.title == titulo, \
        f"Titulo inesperado en el <head>. Se esperaba {titulo}"


def obtener_productos(driver):

    wait = WebDriverWait(driver, TIEMPO_ESPERA)

    # Espero que los productos sean visibles
    productos = wait.until(
        EC.visibility_of_all_elements_located(
            (
                By.CSS_SELECTOR,
                ".inventory_list .inventory_item"
            )
        )
    )

    assert len(productos) > 0, \
        "No se encontraron productos visibles"

    return productos


def agregar_primer_producto(driver):

    wait = WebDriverWait(driver, TIEMPO_ESPERA)

    # Espero que el primer producto sea visible
    first_product = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".inventory_item")
        )
    )

    first_product_name = first_product.find_element(
        By.CSS_SELECTOR,
        ".inventory_item_name"
    ).text

    # Espero que el boton del primer producto se pueda presionar
    add_button = wait.until(
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                ".inventory_item:first-child button"
            )
        )
    )

    add_button.click()

    return first_product_name