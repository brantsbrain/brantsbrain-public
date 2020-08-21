# See https://pypi.org/project/selenium/ for how to install Selenium and the accompanying webdriver
from selenium import webdriver
# Import the sleep module to pause script
from time import sleep
# Create creds.py and add user and password string variables with your username and password
import creds, datetime

# Create webdriver
browser = webdriver.Chrome()

# Create voting method
def vote():
    print("Began voting at " + str(datetime.datetime.now()))
    # Declare counter to keep track of how many votes your instance has submitted
    counter = 1
    # Navigate to Jake's babies' website
    browser.get("https://www.babyvote.com/may20//harper-carter-amelia-mooney-sullivan#_=_")
    # Wait three seconds
    sleep(3)
    # Click on the vote button
    browser.find_element_by_xpath("/html/body/div[5]/div/div[1]/div/div[2]/div/div/div/form/button").click()
    # Wait three seconds to let the page load
    sleep(3)
    # Enter username from creds.py
    browser.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[1]/form/div/div[1]/input").send_keys(creds.user)
    # Enter password from creds.py
    browser.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[1]/form/div/div[2]/input").send_keys(creds.password)
    # Click on the login button
    browser.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[1]/form/div/div[3]/button").click()
    # Print first vote
    print("Voted " + str(counter) + " time - " + str(datetime.datetime.now()))

    # Run this loop indefinitely since True is always True
    while True:
        # You're only allowed to vote once every ten minutes, so wait ten minutes and ten seconds to allow a margin of error
        sleep(610)
        # Refresh the browser
        browser.refresh()
        # Click on the vote button
        browser.find_element_by_xpath("/html/body/div[5]/div/div[1]/div/div[2]/div/div/div/form/button").click()
        # Increase your counter by one
        counter += 1
        # Print the latest count
        print("Voted " + str(counter) + " times - " + str(datetime.datetime.now()))

# Start the vote method
vote()
