from selenium import webdriver
from selenium.webdriver.chrome.options import Options

XPATH_PRODUCTS = r'//div[@class="category"]//div[@class="productsCont productList list"]//ul[@class="productColumns"]//li[@class="product"]'
XPATH_STOCK = r'//div[@class="priceAvailability"]//div[@class="rightColumn"]//span[@class="in stock"]'


def setup_chrome_driver(url: str):
    chrome_options = Options()
    chrome_options.headless = True

    driver = webdriver.Chrome("chromedriver.exe", options=chrome_options)
    driver.get(url)

    return driver


def serialize_product_element(product_element) -> dict:
    return {
        "title": product_element.get_attribute("data-description"),
        "price": product_element.get_attribute("data-price"),
    }


def get_stocked_products(driver) -> [dict]:
    result = []
    product_list = driver.find_elements_by_xpath(XPATH_PRODUCTS)

    for product_element in product_list:
        is_in_stock = len(product_element.find_elements_by_xpath(XPATH_STOCK)) > 0
        if is_in_stock:
            details = serialize_product_element(product_element)
            result.append(details)
            print(details)

    return result


if __name__ == '__main__':
    URL = r"https://www.scan.co.uk/shop/computer-hardware/gpu-nvidia/geforce-rtx-3060-ti-graphics-cards"

    driver = setup_chrome_driver(url=URL)
    products = get_stocked_products(driver)
