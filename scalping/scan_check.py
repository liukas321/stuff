import pyttsx3
from time import sleep
from queue import Empty
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from helpers.ui import ui_worker

XPATH_PRODUCTS = r'//div[@class="category"]//div[@class="productsCont productList list"]//ul[@class="productColumns"]//li[@class="product"]'
XPATH_STOCK = r'//div[@class="priceAvailability"]//div[@class="rightColumn"]//span[@class="in stock"]'


def setup_chrome_driver(headless: bool = False):
    chrome_options = Options()
    chrome_options.headless = headless

    driver = webdriver.Chrome("chromedriver.exe", options=chrome_options)
    return driver


def serialize_product_element(product_element) -> dict:
    return {
        "title": product_element.get_attribute("data-description"),
        "price": product_element.get_attribute("data-price"),
        "in_stock": product_element.find_element_by_xpath(XPATH_STOCK).text == "IN STOCK",
    }


def get_stocked_products(driver, url: str) -> [dict]:
    result = []

    driver.get(url)
    product_list = driver.find_elements_by_xpath(XPATH_PRODUCTS)

    for product_element in product_list:
        product_details = serialize_product_element(product_element)
        if product_details["in_stock"]:
            result.append(product_details)
            print(product_details)

    return result


def speak_products(speech_engine, products: [dict]):
    for product in products:
        s = f"GPU available on Scan for {product['price']} pounds"
        speech_engine.say(s)

    speech_engine.runAndWait()


def main(url: str):
    speech_engine = pyttsx3.init()  # singleton - will use existing instance if available
    driver = setup_chrome_driver(headless=True)

    _, q = ui_worker()

    while True:
        # Check if user initiated script stoppage
        try:
            q.get(False)
        except Empty:
            pass
        else:
            print("Script stopped by user")
            break

        # get products that are in stock
        products = get_stocked_products(driver, url)
        if products:
            speak_products(speech_engine, products)

        sleep(10)

    # Cleanup
    driver.quit()
    speech_engine.stop()


if __name__ == '__main__':
    # URL = r"https://www.scan.co.uk/shop/computer-hardware/gpu-nvidia/nvidia-geforce-rtx-2080-ti-graphics-cards"   # test link
    URL = r"https://www.scan.co.uk/shop/computer-hardware/gpu-nvidia/geforce-rtx-3060-ti-graphics-cards"

    main(URL)
