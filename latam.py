from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as cond
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from threading import *
import time


class LatamGrabber(Thread):

    def __init__(self):
        pass

    def grab_info(self, origem, destino, data):
        options = webdriver.ChromeOptions()
        options.add_argument("window-size=1500,800")
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        options.add_argument('headless')
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                             "(KHTML, like Gecko) Chrome/90.0.4412.3 Safari/537.36")
        chrome_path = 'C:/Users/caiol/Downloads/chromedriver_win32/chromedriver.exe'
        my_driver = webdriver.Chrome(executable_path=chrome_path, options=options)
        wait = WebDriverWait(my_driver, 20)
        my_driver.get(f'https://www.latam.com/pt_br/apps/personas/booking?fecha1_dia={data.split("/")[0]}&fecha1_anomes={data.split("/")[2]}-{data.split("/")[1]}&from_city1={origem}&to_city1={destino}&ida_vuelta=ida&cabina=Y&nadults=1&nchildren=0&ninfants=0&application=lanpass#/')
        # time.sleep(50000)
        wait.until(cond.presence_of_element_located((By.CLASS_NAME, 'value')))
        voos_site = my_driver.find_elements_by_class_name('flight')
        voos = []
        for voo in voos_site:
            points_price = voo.find_element_by_class_name('value').text
            saida = voo.find_element_by_class_name('departure').text
            chegada = voo.find_element_by_class_name('arrival').text
            voos.append(("LATAM",origem, destino,data, "".join(saida.split('\n')[0:3]), "".join(chegada.split('\n')[0:3]), points_price))
        my_driver.close()
        return voos



