from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as cond
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from threading import *
import datetime


class SmilesGrabber(Thread):

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
        data_passagem_epoch = str(int(datetime.datetime(int(data.split('/')[2]),int(data.split('/')[1]),int(data.split('/')[0]),10,0).timestamp())) + '000'
        my_driver.get(f'https://www.smiles.com.br/emissao-com-milhas?tripType=2&originAirport={origem}&destinationAirport={destino}&departureDate={data_passagem_epoch}&returnDate=&adults=1&children=0&infants=0&searchType=g3&segments=1&isElegible=false&originCity=Belo%20Horizonte&originCountry=Brasil&destinCity=Fortaleza&destinCountry=Brasil&originAirportIsAny=false&destinationAirportIsAny=false&isFlexibleDateChecked=false&cabin=ECONOMIC&fromSearchMilesBalance=')
        wait.until(cond.presence_of_element_located((By.CLASS_NAME,'flightsArticle')))
        voos_info = my_driver.find_elements_by_class_name('flightsArticle')
        voos = []
        for voo in voos_info:
            times = voo.find_elements_by_class_name('travel__date-info')
            departure = times[0].text
            arrival = times[1].text
            points_price = my_driver.find_elements_by_class_name('flightlb')[1].text
            voos.append(("SMILES", origem, destino, data, departure, arrival, points_price))
        return voos