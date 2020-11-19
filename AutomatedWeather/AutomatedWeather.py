# Goal: Make an automated historic weather data collector. Inspired by a friend collecting this data manually for a student job at PSU. Expecting to use Selenium (only?). Need to use Weather Underground's site, which provides all required criteria listed below.

# Deliverable: CSV containing the past month's worth of weather data below where the only input arguments needed are the location's ZIP code and month desired.

# Required Criteria:
# Date, High Temp (F), Historic Avg. High Temp (F), Low Temp (F), Historic Avg. Low Temp (F), Day Avg. Temp (F), Historic Avg. Day Avg. Temp (F), Max Wind Speed (MPH), Rain, Dominant Condition

# After Action Report:
# Implementing ZIP code functionality would require more clicking and text entry. Probably not much, but enough to leave it as is.
# Only had to use one module from the time package, so I was almost right on only using Selenium
# Ran into A LOT of problems with "refreshing" different XPATHs and elements. See code for how messy it ended up being. Still don't know why it was such a struggle

########## PREP WORK ##########

from selenium import webdriver
from time import sleep

# Make a dictionary for months of the year to convert to at the end of the script
monthtonum = {
                "January" : "01",
                "February" : "02",
                "March" : "03",
                "April" : "04",
                "May" : "05",
                "June" : "06",
                "July" : "07",
                "August" : "08",
                "September" : "09",
                "October" : "10",
                "November" : "11",
                "December" : "12"
}

# Ask user which month to record stats for
reqmonth = input("What month would you like to gather data from? ")

# Open the browser and browse to the State College month's tab
# If you would like to change this, find your own location's month page and replace the string in browser.get() with it
browser = webdriver.Chrome()
browser.get("https://www.wunderground.com/history/daily/us/pa/state-college/KUNV/date/2020-11-11")
sleep(3)

# Find the full XPATH for the month selector list
monthxpath = browser.find_element_by_xpath("/html/body/app-root/app-history/one-column-layout/wu-header/sidenav/mat-sidenav-container/mat-sidenav-content/div/section/div[2]/div[1]/div[1]/div[1]/div/lib-date-selector/div/select[1]")

# Search the month options for the requested month
for month in monthxpath.find_elements_by_tag_name("option"):
    if month.text == reqmonth:
        print(f"Found {reqmonth}")
        month.click()

# Find the full XPATH for the day list
dayxpath = browser.find_element_by_xpath("/html/body/app-root/app-history/one-column-layout/wu-header/sidenav/mat-sidenav-container/mat-sidenav-content/div/section/div[2]/div[1]/div[1]/div[1]/div/lib-date-selector/div/select[2]")

# Store the options for day list
dayoptions = dayxpath.find_elements_by_tag_name("option")

# Find the first day and click on it, then proceed without assessing the rest of the list
for day in dayoptions:
    if day.text == "1":
        day.click()
        break

# Find the view button full XPATH and click on it
view = browser.find_element_by_xpath("/html/body/app-root/app-history/one-column-layout/wu-header/sidenav/mat-sidenav-container/mat-sidenav-content/div/section/div[2]/div[1]/div[1]/div[1]/div/lib-date-selector/div/input")
view.click()

sleep(2)

########## BEGIN DATA COLLECTION ##########

# Open a writeable file to record data in
with open(f"{reqmonth}2020_HistoricData.csv", "w") as writer:
    # Write first line, which will be requried headers for the CSV
    writer.write("Date, High Temp (F), Historic Avg. High Temp (F), Low Temp (F), Historic Avg. Low Temp (F), Day Avg. Temp (F), Historic Avg. Day Avg. Temp (F), Max Wind Speed (MPH), Rain, Dominant Condition\n")

    # Refresh XPATH location for the day variable
    dayxpath = browser.find_element_by_xpath("/html/body/app-root/app-history/one-column-layout/wu-header/sidenav/mat-sidenav-container/mat-sidenav-content/div/section/div[2]/div[1]/div[1]/div[1]/div/lib-date-selector/div/select[2]")
    # Refresh options list for the day variable
    dayoptions = dayxpath.find_elements_by_tag_name("option")

    # Set current day to 0 to begin list
    currentdaynum = 0
    for day in dayoptions:
        # The following chunk of logic was difficult to figure out, but was required for the script to work. I believe it had something to do with invalid elements or "old" elements appearing, which had to be refreshed. The error I kept getting was "StaleElementException"
        print("Trying to refresh day object...")
        day = browser.find_element_by_xpath("/html/body/app-root/app-history/one-column-layout/wu-header/sidenav/mat-sidenav-container/mat-sidenav-content/div/section/div[2]/div[1]/div[1]/div[1]/div/lib-date-selector/div/select[2]").find_elements_by_tag_name("option")[currentdaynum]
        view = browser.find_element_by_xpath("/html/body/app-root/app-history/one-column-layout/wu-header/sidenav/mat-sidenav-container/mat-sidenav-content/div/section/div[2]/div[1]/div[1]/div[1]/div/lib-date-selector/div/input")
        currentdaynum = int(day.text)

        print("Trying to click on day and view")
        day.click()
        sleep(0.5)
        view.click()
        sleep(0.5)

        # Had to refresh the day variable again without modifying the REAL current day
        day = browser.find_element_by_xpath("/html/body/app-root/app-history/one-column-layout/wu-header/sidenav/mat-sidenav-container/mat-sidenav-content/div/section/div[2]/div[1]/div[1]/div[1]/div/lib-date-selector/div/select[2]").find_elements_by_tag_name("option")[currentdaynum - 1]

        ########## RECORD/WRITE NEEDED VARIABLES ##########

        actualhigh = browser.find_element_by_xpath("/html/body/app-root/app-history/one-column-layout/wu-header/sidenav/mat-sidenav-container/mat-sidenav-content/div/section/div[2]/div[1]/div[3]/div[1]/div/lib-city-history-summary/div/div[2]/table/tbody[1]/tr[1]/td[1]").text

        histavghigh = browser.find_element_by_xpath("/html/body/app-root/app-history/one-column-layout/wu-header/sidenav/mat-sidenav-container/mat-sidenav-content/div/section/div[2]/div[1]/div[3]/div[1]/div/lib-city-history-summary/div/div[2]/table/tbody[1]/tr[1]/td[2]").text

        actuallow = browser.find_element_by_xpath("/html/body/app-root/app-history/one-column-layout/wu-header/sidenav/mat-sidenav-container/mat-sidenav-content/div/section/div[2]/div[1]/div[3]/div[1]/div/lib-city-history-summary/div/div[2]/table/tbody[1]/tr[2]/td[1]").text

        histavglow = browser.find_element_by_xpath("/html/body/app-root/app-history/one-column-layout/wu-header/sidenav/mat-sidenav-container/mat-sidenav-content/div/section/div[2]/div[1]/div[3]/div[1]/div/lib-city-history-summary/div/div[2]/table/tbody[1]/tr[2]/td[2]").text

        avgday = browser.find_element_by_xpath("/html/body/app-root/app-history/one-column-layout/wu-header/sidenav/mat-sidenav-container/mat-sidenav-content/div/section/div[2]/div[1]/div[3]/div[1]/div/lib-city-history-summary/div/div[2]/table/tbody[1]/tr[3]/td[1]").text

        histavgday = browser.find_element_by_xpath("/html/body/app-root/app-history/one-column-layout/wu-header/sidenav/mat-sidenav-container/mat-sidenav-content/div/section/div[2]/div[1]/div[3]/div[1]/div/lib-city-history-summary/div/div[2]/table/tbody[1]/tr[3]/td[2]").text

        maxwind = browser.find_element_by_xpath("/html/body/app-root/app-history/one-column-layout/wu-header/sidenav/mat-sidenav-container/mat-sidenav-content/div/section/div[2]/div[1]/div[3]/div[1]/div/lib-city-history-summary/div/div[2]/table/tbody[4]/tr[1]/td[1]").text

        rain = browser.find_element_by_xpath("/html/body/app-root/app-history/one-column-layout/wu-header/sidenav/mat-sidenav-container/mat-sidenav-content/div/section/div[2]/div[1]/div[3]/div[1]/div/lib-city-history-summary/div/div[2]/table/tbody[2]/tr/td[1]").text

        # The rain value is a string, so all we care about is whether or not it's "0.00" or different, then reassign the value to Yes or No
        if rain == "0.00":
            rain = "No"
        else:
            rain = "Yes"

        # Find the number of rows in the dominant condition column/table
        numrows = len(browser.find_elements_by_xpath("/html/body/app-root/app-history/one-column-layout/wu-header/sidenav/mat-sidenav-container/mat-sidenav-content/div/section/div[2]/div[1]/div[5]/div[1]/div/lib-city-history-observation/div/div[2]/table/tbody/tr"))

        # Declare the domcondition dictionary, then iterate through the column and only add an entry if it isn't already in the dictionary. Otherwise, increase that entry's value by one
        domcondition = {}
        for cell in range(numrows):
            try:
                for key in browser.find_elements_by_xpath("/html/body/app-root/app-history/one-column-layout/wu-header/sidenav/mat-sidenav-container/mat-sidenav-content/div/section/div[2]/div[1]/div[5]/div[1]/div/lib-city-history-observation/div/div[2]/table/tbody/tr[" + str(cell) + "]/td[10]"):
                    if key.text not in domcondition.keys():
                        domcondition[key.text] = 1
                    else:
                        domcondition[key.text] += 1
            except Exception as e:
                print(f"Caught {e}")

        # Sort the dictionary into a list by highest values
        sorted_domcondition = sorted(domcondition.items(), key=lambda x: x[1], reverse=True)

        # Write all the gathered data to the CSV then end with a \n to prep for the next row. Only write the first entry of the sorted domcondition list
        writer.write(f"{monthtonum[reqmonth]}/{day.text}/2020,{actualhigh},{histavghigh},{actuallow},{histavglow},{avgday},{histavgday},{maxwind},{rain},{sorted_domcondition[0][0]}\n")
