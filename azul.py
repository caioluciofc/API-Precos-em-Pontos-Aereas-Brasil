from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as cond
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from threading import *
import time


class AzulGrabber(Thread):

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
        my_driver.get('https://www.voeazul.com.br/')
        wait.until(cond.presence_of_element_located((By.NAME, 'origin1')))
        time.sleep(3)
        my_driver.find_element_by_name('origin1').send_keys(origem)
        my_driver.find_element_by_name('origin1').send_keys(Keys.ENTER)
        my_driver.find_element_by_name('destination1').send_keys(destino)
        my_driver.find_element_by_name('destination1').send_keys(Keys.ENTER)

        my_driver.find_element_by_name('departure1').send_keys(data)
        my_driver.find_element_by_name('departure1').send_keys(Keys.ENTER)

        my_driver.find_element_by_name('arrival').send_keys(data)
        my_driver.find_element_by_name('arrival').send_keys(Keys.ENTER)
        time.sleep(1)

        my_driver.find_element_by_xpath('//*[@id="TCSS__tabbox-shopping"]/div[5]/div[2]/div/span[3]/input').click()
        time.sleep(1)
        my_driver.find_element_by_id('searchTicketsButton').click()
        wait.until(cond.element_to_be_clickable((By.CLASS_NAME, 'outer-circle')))
        time.sleep(2)
        todos_voos_ida = my_driver.find_element_by_id('tbl-depart-flights')
        voos_ida = todos_voos_ida.find_elements_by_class_name('flight-item')

        voos = []

        for voo in voos_ida:
            departure = voo.find_element_by_class_name('dep-time').text
            arrival = voo.find_element_by_class_name('arr-time').text
            duration = voo.find_element_by_class_name('flight-duration-info').text
            try:
                points_price = voo.find_element_by_class_name('price-points').text
                voos.append(('AZUL',origem,destino,data,departure,arrival,points_price))
            except:
                continue

        todos_voos_volta = my_driver.find_element_by_id('box-return-flights')
        voos_volta = todos_voos_volta.find_elements_by_class_name('flight-item')

        for voo in voos_volta:
            departure = voo.find_element_by_class_name('dep-time').text
            arrival = voo.find_element_by_class_name('arr-time').text
            duration = voo.find_element_by_class_name('flight-duration-info').text
            try:
                points_price = voo.find_element_by_class_name('price-points').text
                voos.append(('AZUL',destino,origem,data,departure,arrival,points_price))
            except:
                continue

        my_driver.close()
        return voos