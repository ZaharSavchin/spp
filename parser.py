import time
from selenium import webdriver
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromiumService
from openpyxl import load_workbook
from pass_captcha import tru


workbook = load_workbook(filename='wb.xlsx')
sheet = workbook.active
arts = []
for cell in sheet['A']:
    arts.append(cell.value)

options_chrome = webdriver.ChromeOptions()
options_chrome.add_extension('guru.crx')

price_with_spp = []
price = []
sold = []
fidbacks = []


def open_widget(browser):
    browser.find_element(By.CLASS_NAME, "WidgetButton_widgetButtonOpenIcon__uuM6O").click()


with webdriver.Chrome(options=options_chrome) as browser:
    url = f'https://www.wildberries.ru/catalog/{arts[3]}/detail.aspx'
    browser.get(url)
    time.sleep(5)

    browser.switch_to.window(browser.window_handles[1])

    try:
        tru(browser)
    except Exception as err:
        print(err)

    browser.switch_to.window(browser.window_handles[0])

    browser.get(url)
    open_widget(browser)
    for art in arts:
            browser.get(f'https://www.wildberries.ru/catalog/{art}/detail.aspx')
            browser.maximize_window()
            time.sleep(5)

            try:
                price_wb = browser.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/div[3]/div/div[3]/div[14]/div/div[1]/div[1]/div[1]/div/div/p/span/ins").text

                price_wb = ''.join(price_wb.split(' ')[:-1])
                print(f'....{price_wb}...')
                price_wb = int(price_wb)
            except Exception as err:
                price_wb = None

            try:
                price_no_spp = browser.find_element(By.CLASS_NAME, "SppWidget_sppWidget__boldPrice__0J7RF").text
                price_no_spp = ''.join(price_no_spp.split(' ')[:-1])
                price_no_spp = int(price_no_spp)
            except Exception as err:
                price_no_spp = None

            try:
                sold_out = browser.find_element(By.CLASS_NAME, 'sold-out-product')
                price_with_spp.append(' ')
                price.append(' ')
            except Exception as err:
                price_with_spp.append(price_wb)
                price.append(price_no_spp)

            try:
                sold_items = browser.find_element(By.CLASS_NAME, "ShortWidgetStat_shortWidgetStatColumn__nzQOE").text
                sold_items = ''.join(sold_items.split(' ')[:-1])
                sold.append(int(sold_items))
            except Exception as err:
                sold_items = None
                sold.append(None)

            try:
                backs = browser.find_element(By.CLASS_NAME, "user-activity__count").text
                fidbacks.append(int(backs))
            except Exception as err:
                backs = None
                fidbacks.append(None)

            print(f'{art} = {price_wb}, {price_no_spp}р, {sold_items}, {backs}')


for i in range(len(price_with_spp)):
    sheet.cell(row=i+1, column=2, value=price_with_spp[i])

for i in range(len(price)):
    sheet.cell(row=i+1, column=3, value=price[i])

for i in range(len(sold)):
    sheet.cell(row=i+1, column=4, value=sold[i])

for i in range(len(fidbacks)):
    sheet.cell(row=i+1, column=5, value=fidbacks[i])

workbook.save(filename='wb.xlsx')
