from selenium import webdriver
from time import sleep
import creds

browser = webdriver.Chrome()

def electric():
    browser.get(creds.electric_site)
    browser.find_element_by_xpath('//*[@id="loginUsername"]').send_keys(creds.electric_user)
    browser.find_element_by_xpath('//*[@id="loginPwd"]').send_keys(creds.electric_pass)
    browser.find_element_by_xpath('//*[@id="form"]/div[2]/div/button').click()
    sleep(3)
    balance = str(browser.find_element_by_xpath('/html/body/div[4]/div/div/section/article/div/div[2]/div[2]/div[2]/div[6]/div/div[6]').text)

    return balance

def student():
    browser.get()
    browser.find_element_by_path()
    browser.find_element_by_path()
    browser.find_element_by_path()
    balance = ""

    return balance

def rent():
    balance = ""

    return balance

def credit():
    balance = ""

    return balance

def all():
    print("Electric balance: " + electric())
    print("Student Loan balance: " + student())
    print("Rent balance: " + rent())
    print("Credit Card balance: " + credit())
