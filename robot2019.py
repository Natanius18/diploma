from time import sleep, time

import winsound
from openpyxl import Workbook
from selenium.webdriver import Chrome, Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By


chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

browser = Chrome(options=chrome_options)
browser.maximize_window()
browser.implicitly_wait(3)

url = 'https://vstup2019.edbo.gov.ua/offers/'
license_path = "//*[contains(text(), 'Ліцензійний обсяг:')]"
derj_order = '//*[text() = "Обсяг держзамовлення: "]'
browser.get(url)

wb = Workbook()
ws = wb.active
ws.append(["Університет", "Спеціальність", "Спеціалізація", "Форма навчання", "Макс. обсяг держзамовлення", "Середні бали ЗНО", "Ліцензійний обсяг",
           "Точно бакалавр?", "Регіональний коефіцієнт"])

def check_and_close_error_message():
    if browser.find_elements(By.CLASS_NAME, 'ui-dialog-buttonset'):
        sleep(2)
        browser.find_element(By.CLASS_NAME, 'ui-button').click()


def close_last_tab():
    browser.close()
    browser.switch_to.window(window_name=browser.window_handles[0])


def find_derj_value():
    if browser.find_elements(By.CLASS_NAME, 'max-order'):
        return browser.find_element(By.CLASS_NAME, 'max-order').find_element(By.TAG_NAME, 'div').text
    else:
        elements = browser.find_element(By.ID, 'offer-wrapper').find_elements(By.TAG_NAME, 'label')
        for e in elements:
            if e.text.__contains__("держзамовлення"):
                return e.find_element(By.XPATH, "..").find_element(By.TAG_NAME, 'div').text


def read_info():
    browser.switch_to.window(window_name=browser.window_handles[-1])
    speciality = browser.find_element(By.CLASS_NAME, 'speciality-name').text
    max_order = find_derj_value()
    if browser.find_elements(By.CLASS_NAME, 'avg-konkurs-value'):
        avg_konkurs_value = browser.find_element(By.CLASS_NAME, 'avg-konkurs-value').find_element(By.TAG_NAME, 'div').text
    else:
        avg_konkurs_value = "-"
    if browser.find_elements(By.CLASS_NAME, 'specialization'):
        specialization = browser.find_element(By.CLASS_NAME, 'specialization').find_element(By.TAG_NAME, 'div').text
    else:
        specialization = "-"
    education_form = browser.find_element(By.CLASS_NAME, 'education-form').find_element(By.TAG_NAME, 'div').text
    if browser.find_elements(By.CLASS_NAME, 'regional-coeff'):
        regional_coeff = browser.find_element(By.CLASS_NAME, 'regional-coeff').find_element(By.TAG_NAME, 'div').text
    else:
        regional_coeff = "-"
    qualification = browser.find_element(By.CLASS_NAME, 'qualification').text
    if browser.find_elements(By.XPATH, license_path):
        license_value = browser.find_element(By.XPATH, license_path).find_element(By.XPATH, '..').find_element(By.TAG_NAME, 'div').text
    else:
        license_value = "-"
    print("uni_name:", uni_name,
          "\nspeciality:", speciality,
          "\nqualification:", qualification,
          "\nspecialization:", specialization,
          "\neducation_form:", education_form,
          "\nmax_order:", max_order,
          "\navg_konkusrs_value:", avg_konkurs_value,
          "\nlicense_value:", license_value,
          "\nregional_coeff:", regional_coeff, "\n\n\n")

    sleep(6)
    close_last_tab()

    ws.append([uni_name, speciality, specialization, education_form, max_order, avg_konkurs_value, license_value,
               qualification, regional_coeff, button_num])
    wb.save("testlim.xlsx")
    sleep(7)


input_speciality = browser.find_element(By.ID, 'offers-search-ft-q')
input_speciality.send_keys("Бакалавр")
input_speciality.send_keys(Keys.ENTER)
browser.implicitly_wait(5)
buttons = browser.find_elements(By.CLASS_NAME, 'button-offer-university')


def scrap_page():
    global button_num, uni_name, i
    try:
        for button_num in range(0, len(buttons)):
            check_and_close_error_message()
            button = buttons[button_num]

            actions = ActionChains(browser)
            actions.move_to_element(button).perform()
            sleep(3)
            button.click()
            print("button:", button_num, "/", len(buttons))
            sleep(2)
            offer_path = "//div[@class='offer-university'][" + (button_num + 1).__str__() + "]"
            offers = browser.find_element(By.XPATH, offer_path).find_elements(By.CLASS_NAME, 'offer-wrapper')

            uni_name = browser.find_element(By.XPATH, offer_path).find_element(By.TAG_NAME, 'h2').text
            browser.implicitly_wait(0)
            sleep(2)
            for offer_num in range(len(offers)):
                offer = offers[offer_num]
                if offer.find_elements(By.CLASS_NAME, 'offer-type'):
                    offer_type = offer.find_element(By.CLASS_NAME, 'offer-type').find_element(By.TAG_NAME, 'div').text
                    if offer_type.__contains__('із вказанням пріоритетності'):
                        actions.move_to_element(offer).perform()
                        sleep(8)
                        offer.find_element(By.CLASS_NAME, 'button').click()
                        sleep(5)
                        read_info()

            check_and_close_error_message()
            actions.move_to_element(button).perform()
            sleep(1)
            button.click()
            sleep(1)
    except:
        for i in range(5):
            winsound.MessageBeep(winsound.SND_NOWAIT)
            sleep(1.5)


scrap_page()
