import time
from selenium import webdriver
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromiumService
from openpyxl import load_workbook
mail = 'pasechnik.pchelovod@mail.ru'


workbook = load_workbook(filename='wb.xlsx')
sheet = workbook.active
arts = []
for cell in sheet['A']:
    arts.append(cell.value)

options_chrome = webdriver.ChromeOptions()
options_chrome.add_extension('guru.crx')

price = []


with webdriver.Chrome(service=ChromiumService(ChromeDriverManager().install()), options=options_chrome) as browser:
    url = 'https://www.wildberries.ru/'
    browser.get(url)
    time.sleep(60)
    for art in arts:
        try:
            browser.get(f'https://www.wildberries.ru/catalog/{art}/detail.aspx')
            time.sleep(5)
            price_no_spp = browser.find_element(By.CLASS_NAME, "SppWidget_sppWidget__boldPrice__0J7RF").text
            price_no_spp = ''.join(price_no_spp.split(' ')[:-1])
            price.append(int(price_no_spp))
            print(f'{art} = {price_no_spp}р')
        except Exception as err:
            price.append(None)
            print(f'{art} = problem')


for i in range(len(price)):
    sheet.cell(row=i+1, column=2, value=price[i])

workbook.save(filename='wb.xlsx')


