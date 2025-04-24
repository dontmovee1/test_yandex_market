import logging
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pytest_bdd import given, when, then
from selenium.webdriver.common.keys import Keys
from pytest_bdd import scenario

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@given("Открыт браузер Chrome на весь экран")
def open_browser(browser):
    browser.maximize_window()
    logger.info("Браузер Chrome открыт на весь экран")

@when('Я перехожу на страницу "https://market.yandex.ru"')
def navigate_to_market(browser):
    try:
        browser.get("https://market.yandex.ru")
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-zone-name='catalog']"))
        )
        logger.info("Открыта страница Яндекс.Маркет")
    except Exception as e:
        logger.error(f"Ошибка при переходе на страницу Яндекс.Маркет: {e}")
        raise

@when('В разделе "Каталог → Электроника" выбираю "Смартфоны"')
def select_smartphones(browser):
    try:
        popup = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[id='/content/popup']"))
        )
        browser.execute_script("arguments[0].remove();", popup)

        catalog_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-zone-name='catalog']"))
        )
        catalog_button.click()
        logger.info("Открыто меню каталога")
        electronics_menu = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH,
                                            "//li[contains(@class, '_12HrO')]//span[contains(@class, '_3W4t0') and text()='Электроника']"))
        )
        ActionChains(browser).move_to_element(electronics_menu).perform()
        logger.info("Курсор наведен на 'Электроника'")

        smartphones = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "//a[contains(@href, '/catalog--smartfony') and "
                                        "contains(@class, '_2re3U') and "
                                        "normalize-space(text())='Смартфоны']"))
        )
        smartphones.click()
    except:
        logger.info("Выбран раздел 'Смартфоны'")


@when('Перехожу в "Все фильтры"')
def open_filters(browser):
    try:
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Все фильтры')]"))).click()
        logger.info("Открыты все фильтры")
    except Exception as e:
        logger.error(f"Ошибка при открытии фильтров: {e}")
        raise


@when('Устанавливаю максимальную цену 20000 рублей')
def set_price_filter(browser):
    try:
        price_to = WebDriverWait(browser, 15).until(
            EC.element_to_be_clickable((By.ID, "range-filter-field-glprice_25563_max"))
        )
        price_to.click()
        price_to.clear()
        price_to.send_keys("20000")
        price_to.send_keys(Keys.ENTER)
        logger.info("Установлена максимальная цена: 20000 руб")

    except Exception as e:
        logger.error(f"Ошибка при установке цены: {e}")
        raise


@when('Устанавливаю диагональ экрана от 3 дюймов')
def set_screen_size(browser):
    try:
        screen_min = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.ID, "range-filter-field-14805766_25564_min"))
        )

        browser.execute_script("""
            const element = arguments[0];
            const headerHeight = 100;
            const elementPosition = element.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - headerHeight;

            window.scrollTo({
                top: offsetPosition,
                behavior: 'smooth'
            });
        """, screen_min)

        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.ID, "range-filter-field-14805766_25564_min"))
        )

        browser.execute_script("arguments[0].click();", screen_min)
        screen_min.clear()
        screen_min.send_keys("3")
        screen_min.send_keys(Keys.ENTER)

        logger.info("Установлена минимальная диагональ: 3 дюйма")


    except Exception as e:
        logger.error(f"Ошибка при установке диагонали: {str(e)}")
        raise

@when('Выбираю 5 производителей')
def select_manufacturers(browser):
    manufacturers = ["Xiaomi", "Samsung", "Apple", "realme", "HONOR"]
    try:
        for brand in manufacturers:
            checkbox = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//span[contains(text(), '{brand}')]/preceding-sibling::span"))
            )
            checkbox.click()
        logger.info(f"Выбраны производители: {manufacturers}")
    except Exception as e:
        logger.error(f"Ошибка при выборе производителей: {e}")
        raise

@when('Нажимаю кнопку "Показать"')
def apply_filters(browser):
    try:
        show_products_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[aria-label='Показать товары']")
            )
        )
        show_products_button.click()
        logger.info("Кнопка 'Показать товары' успешно нажата")
    except Exception as e:
        logger.error(f"Неожиданная ошибка при нажатии кнопки: {str(e)}")
        raise

@then('Я подсчитываю количество смартфонов на странице')
def count_products(browser):
    try:
        products = WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, '[data-auto="snippet-title"][itemprop="name"]')
            )
        )
        logger.info(f"Найдено смартфонов: {len(products)}")
        browser.products = products
        return len(products)
    except Exception as e:
        logger.error(f"Ошибка при подсчете смартфонов: {e}")
        raise


@then('Запоминаю последний смартфон в списке')
def remember_last_product(browser):
    try:
        WebDriverWait(browser, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-auto="snippet-title"][itemprop="name"]'))
        )
        products = browser.find_elements(By.CSS_SELECTOR, '[data-auto="snippet-title"][itemprop="name"]')

        if not products:
            raise ValueError("Список товаров пуст!")

        last_product = products[-1].text.strip()
        browser.last_product_title = last_product
        logger.info(f"Запомнен товар: {browser.last_product_title}")
        return browser.last_product_title

    except Exception as e:
        logger.error(f"Ошибка при запоминании последнего товара: {e}")
        raise


@when('Изменяю сортировку на "подороже"')
def change_sorting_to_expensive(browser):
    try:
        sort_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-zone-name="SearchSort"]'))
        )
        ActionChains(browser).move_to_element(sort_button).click().perform()

        expensive_sort = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[text()="Подороже"]'))
        )
        expensive_sort.click()

        logger.info("Сортировка изменена на 'подороже'")

    except Exception as e:
        logger.error(f"Ошибка при изменении сортировки: {e}")
        raise


@when('Нажимаю на запомненный смартфон')
def click_on_remembered_product(browser):
    try:
        remembered_title = browser.last_product_title
        logger.info(f"Ищем товар: {remembered_title}")
        product_element = WebDriverWait(browser, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, f"//*[@data-auto='snippet-title'][contains(., '{remembered_title}')]"))
        )
        browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", product_element)
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable(product_element)).click()


    except Exception as e:
        logger.error(f"Ошибка при клике на товар: {e}")
        raise


@then('Вывожу рейтинг выбранного смартфона')
def print_rating(browser):
    try:
        tabs = browser.window_handles
        browser.switch_to.window(tabs[-1])
        rating_element = WebDriverWait(browser, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'span[data-auto="ratingValue"]'))
        )
        rating = rating_element.text.strip()
        logger.info(f"Рейтинг товара '{browser.last_product_title}': {rating} из 5 ")
        return f"{rating}"

    except Exception as e:
        logger.error(f"Ошибка при получении рейтинга: {e}")
        return None

@then('Закрываю браузер')
def close_browser(browser):
    try:

        for handle in browser.window_handles:
            browser.switch_to.window(handle)
            browser.close()

        logger.info("Браузер успешно закрыт")
    except Exception as e:
        logger.error(f"Ошибка при закрытии браузера: {e}")
        raise

