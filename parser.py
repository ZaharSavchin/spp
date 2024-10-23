import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import asyncio

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromiumService
from openpyxl import load_workbook
from pass_captcha import tru

urls = ['https://www.wildberries.by/catalog/0/search.aspx?sort=popular&search=iphone+16+pro+max&xsearch=true&targeturl=ST', 'https://www.wildberries.by/catalog/0/search.aspx?search=iphone+15+pro+max&targeturl=ST&xsearch=true']



async def main_search(urls):
    workbook = load_workbook(filename='wb.xlsx')
    sheet = workbook.active
    # arts = []
    # for cell in sheet['A']:
    #     arts.append(cell.value)

    options_chrome = webdriver.ChromeOptions()
    options_chrome.add_extension('guru.crx')

    price_with_spp = []
    price = []
    sold = []
    fidbacks = []
    names = []
    colors = []
    models = []
    memorys = []
    oper_memorys = []

    arts = []


    with webdriver.Chrome() as browser:
        for url in urls:

            browser.get(url)
            browser.maximize_window()
            await asyncio.sleep(5)
            hrefs = browser.find_elements(By.TAG_NAME, 'article')
            for href in hrefs:
                arts.append(href.get_attribute('data-nm-id'))
            await asyncio.sleep(5)



    def open_widget(browser):
        browser.find_element(By.CLASS_NAME, "WidgetButton_widgetButtonOpenIcon__uuM6O").click()


    with webdriver.Chrome(options=options_chrome) as browser:
        url = f'https://www.wildberries.ru/catalog/{arts[3]}/detail.aspx'
        browser.get(url)
        await asyncio.sleep(5)

        browser.switch_to.window(browser.window_handles[1])

        try:
            tru(browser)
        except Exception as err:
            print(err)

        browser.switch_to.window(browser.window_handles[0])

        browser.get(url)
        open_widget(browser)

        for art in arts[:5]:
            browser.get(f'https://www.wildberries.ru/catalog/{art}/detail.aspx')
            browser.maximize_window()
            await asyncio.sleep(5)

            try:
                price_wb = browser.find_element(By.XPATH,
                                                "/html/body/div[1]/main/div[2]/div/div[3]/div/div[3]/div[14]/div/div[1]/div[1]/div[1]/div/div/p/span/ins").text

                price_wb = ''.join(price_wb.split(' ')[:-1])
                print(f'....{price_wb}...')
                price_wb = int(price_wb)
            except Exception as err:
                price_wb = None

            try:
                price_no_spp = browser.find_element(By.XPATH,
                                                    "/html/body/div[1]/main/div[2]/div/div[3]/div/div[3]/div[14]/div/div[1]/div[1]/div[2]/div/div[2]/div[1]/span").text
                price_no_spp = ''.join(price_no_spp.split(' ')[:-1])
                price_no_spp = int(price_no_spp)
            except Exception as err:
                price_no_spp = None

            try:
                sold_out = browser.find_element(By.XPATH,
                                                '/html/body/div[1]/main/div[2]/div/div[3]/div/div[3]/div[2]/div/p/span')
                price_with_spp.append(' ')
                price.append(' ')
            except Exception as err:
                price_with_spp.append(price_wb)
                price.append(price_no_spp)

            try:
                sold_items = browser.find_element(By.XPATH, "/html/body/div[7]/div[1]/div[2]/div[3]/div[3]/b/span").text
                sold_items = ''.join(sold_items.split(' ')[:-1])
                sold.append(int(sold_items))
            except Exception as err:
                sold_items = None
                sold.append(None)

            try:
                backs = browser.find_element(By.XPATH,
                                             "/html/body/div[1]/main/div[2]/div/div[3]/div/div[4]/div[1]/ul/li[1]/button/span").text

                backs = ''.join(backs.split(' '))
                fidbacks.append(int(backs))
            except Exception as err:
                backs = None
                fidbacks.append(None)

            try:
                name = browser.find_element(By.XPATH,
                                            '/html/body/div[1]/main/div[2]/div/div[3]/div/div[3]/div[9]/div[1]/h1').text
                print(f'name = {name}')
                names.append(name)
            except Exception as err:
                name = None
                names.append(None)



            try:
                color = browser.find_element(By.XPATH,
                                             '/html/body/div[1]/main/div[2]/div/div[3]/div/div[3]/div[7]/div[2]/div/div[1]/p/span').text
                colors.append(color)
            except Exception as err:
                color = None
                print('no color')
                colors.append(None)

            try:
                model = browser.find_element(By.XPATH,
                                             '/html/body/div[1]/main/div[2]/div/div[3]/div/div[3]/div[10]/div[1]/div[2]/table/tbody/tr[2]/td').text
                models.append(model)
            except Exception as err:
                print('no model')
                model = None
                models.append(None)

            try:
                time.sleep(3)
                button = browser.find_element(By.XPATH,
                                              '/html/body/div[1]/main/div[2]/div/div[3]/div/div[3]/div[10]/button').click()
            except Exception as err:
                print('no button')

            try:
                await asyncio.sleep(3)
                memory = browser.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div[2]/table[4]/tbody/tr[1]/td').text
                memorys.append(memory)
            except Exception as err:
                memory = None
                memorys.append(None)

            try:
                oper_memory = browser.find_element(By.XPATH,
                                                   '/html/body/div[1]/div/div[1]/div[2]/table[4]/tbody/tr[2]/td').text
                oper_memorys.append(oper_memory)
            except Exception as err:
                oper_memory = None
                oper_memorys.append(None)



    for i in range(len(price_with_spp)):
        sheet.cell(row=i + 1, column=2, value=price_with_spp[i])

    for i in range(len(price)):
        sheet.cell(row=i + 1, column=3, value=price[i])

    for i in range(len(sold)):
        sheet.cell(row=i + 1, column=4, value=sold[i])

    for i in range(len(fidbacks)):
        sheet.cell(row=i + 1, column=5, value=fidbacks[i])

    for i in range(len(memorys)):
        sheet.cell(row=i + 1, column=6, value=memorys[i])

    for i in range(len(colors)):
        sheet.cell(row=i + 1, column=7, value=colors[i])

    for i in range(len(memorys)):
        sheet.cell(row=i + 1, column=8, value=memorys[i])

    for i in range(len(fidbacks)):
        sheet.cell(row=i + 1, column=9, value=fidbacks[i])

    for i in range(len(oper_memorys)):
        sheet.cell(row=i + 1, column=10, value=oper_memorys[i])

    for i in range(len(models)):
        sheet.cell(row=i + 1, column=11, value=models[i])

    for i in range(len(names)):
        sheet.cell(row=i + 1, column=12, value=names[i])

    workbook.save(filename='wb.xlsx')


async def main():
    counter = 1
    while True:
        await main_search(urls)
        print(counter)
        counter += 1
        await asyncio.sleep(120)




