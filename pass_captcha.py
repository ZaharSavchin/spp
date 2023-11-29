import time
import pydub

import requests
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import speech_recognition as sr

name_audio_file = 'audio_captcha.mp3'
login = '*************'
password = '************'


def write_audio(url):
    response = requests.get(url)
    with open(f'{name_audio_file}', 'wb') as file:
        file.write(response.content)


def audio_to_text():
    with open(f"{name_audio_file}", 'rb') as file:
        path_to_mp3 = name_audio_file
        path_to_wav = 'audio_file.wav'
        sound = pydub.AudioSegment.from_file(path_to_mp3, 'mp3')
        sound.export(path_to_wav, 'wav')
        sample_audio = sr.AudioFile(path_to_wav)
        r = sr.Recognizer()
        with sample_audio as source:
            audio = r.record(source)
        key = r.recognize_google(audio)
        return key


def tru(browser):
    time.sleep(5)
    browser.find_element(By.CLASS_NAME, "header-nav__buttons").find_element(By.TAG_NAME, 'a').click()
    # browser.find_element(By.XPATH, '/html/body/app-root/app-extension/div/app-extension-main/div/div/div/div[1]/div[3]/div/a[2]').click()
    # browser.find_element(By.CLASS_NAME, "btn btn-dark").click()
    # time.sleep(5)
    # time.sleep(10)
    # WebDriverWait(browser, 10).until(EC.frame_to_be_available_and_switch_to_it(
    #     (By.CSS_SELECTOR, f"iframe[title='Виджет, содержащий вызов безопасности Cloudflare']")))
    # time.sleep(10)
    # WebDriverWait(browser, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-extension/div/app-extension-main/div/div/div/div[1]/div[3]/div/a[2]'))).click()
    # time.sleep(10)
    # browser.implicitly_wait(10)
    # time.sleep(10)
    time.sleep(3)
    browser.find_element(By.ID, "email").send_keys(login)
    time.sleep(3)
    browser.find_element(By.XPATH, '/html/body/app-root/app-auth-layout/div[1]/div[2]/div/app-signin/form/div[2]/mg-input-password/mg-input-primitive/div/div[2]/input').send_keys(password)
    time.sleep(3)
    browser.find_element(By.CLASS_NAME, "w-100").click()
    time.sleep(5)
    # WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, "onetrust-reject-all-handler"))).click()
    # WebDriverWait(browser, 10).until(
    #     EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, f"iframe[title='reCAPTCHA']")))
    #
    # WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, 'recaptcha-anchor'))).click()
    # time.sleep(10)
    #
    # browser.implicitly_wait(10)
    #
    # browser.switch_to.default_content()
    WebDriverWait(browser, 10).until(EC.frame_to_be_available_and_switch_to_it(
        (By.CSS_SELECTOR, f"iframe[title='текущую проверку reCAPTCHA можно пройти в течение ещё двух минут']")))

    browser.find_element(By.ID, 'recaptcha-audio-button').click()
    time.sleep(5)
    src = browser.find_element(By.ID, "audio-source").get_attribute("src")
    print(f"[INFO] Audio src: {src}")
    write_audio(src)
    key = audio_to_text()
    print(key)

    time.sleep(5)

    browser.find_element(By.CSS_SELECTOR, 'input[id="audio-response"]').send_keys(key.lower())
    time.sleep(5)
    browser.find_element(By.ID, "audio-response").send_keys(Keys.ENTER)
    time.sleep(5)
