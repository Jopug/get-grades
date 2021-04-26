from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from getpass import getpass
import time
from win10toast import ToastNotifier

option = webdriver.ChromeOptions()

option.add_argument('headless')

toast = ToastNotifier()

PATH = "C:\Program Files (x86)\chromedriver.exe"

def getGrades(user, pwd):
    driver = webdriver.Chrome(PATH, options=option)

    driver.get("https://epprd.mcmaster.ca/psp/prepprd/?cmd=login")

    UID_Field = driver.find_element_by_id("userid")
    UID_Field.send_keys(user) 

    PWD_Field = driver.find_element_by_id("pwd")
    PWD_Field.send_keys(pwd)

    PWD_Field.send_keys(Keys.RETURN)

    time.sleep(3)

    driver.get("https://csprd.mcmaster.ca/psc/prcsprd_2/EMPLOYEE/SA/c/SA_LEARNER_SERVICES.SSR_SSENRL_GRADE.GBL?Page=SSR_SSENRL_GRADE&PortalActualURL=https%3a%2f%2fcsprd.mcmaster.ca%2fpsc%2fprcsprd_2%2fEMPLOYEE%2fSA%2fc%2fSA_LEARNER_SERVICES.SSR_SSENRL_GRADE.GBL%3fPage%3dSSR_SSENRL_GRADE&PortalContentURL=https%3a%2f%2fcsprd.mcmaster.ca%2fpsc%2fprcsprd%2fEMPLOYEE%2fSA%2fc%2fSA_LEARNER_SERVICES.SSR_SSENRL_GRADE.GBL%3fPage%3dSSR_SSENRL_GRADE&PortalContentProvider=SA&PortalCRefLabel=Grades&PortalRegistryName=EMPLOYEE&PortalServletURI=https%3a%2f%2fepprd.mcmaster.ca%2fpsp%2fprepprd_2%2f&PortalURI=https%3a%2f%2fepprd.mcmaster.ca%2fpsc%2fprepprd_2%2f&PortalHostNode=EMPL&NoCrumbs=yes&PortalKeyStruct=yes")
    driver.find_element_by_id("#ICOK").click()

    grades = {}

    i=2

    while True:
        try:
            row = '/html/body/form/div[5]/table/tbody/tr/td/div/table/tbody/tr[8]/td[2]/div/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/div/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[' + str(i) + ']'
            namePath = row + '/td[2]/div/span'
            gradePath = row + '/td[5]/div/span'
            name = driver.find_elements_by_xpath(namePath)[0].text
            grade = driver.find_elements_by_xpath(gradePath)[0].text
            grades[name] = grade
            #print("Class: " + str(name) + " - Grade: " + str(grade))
            i += 1
        except Exception:
            break

    return grades

user = input("User Name: ")
pwd = getpass()

baseLineGrades = getGrades(user, pwd)
print("Baseline Grades")
for key in baseLineGrades:
    print(str(key) + " - " + str(baseLineGrades[key]))

while True:
    newGrades = getGrades(user, pwd)
    for key in newGrades:
        if baseLineGrades[key] != newGrades[key] :
            print("NEW GRADE RELEASED")
            toast.show_toast("Grade Released", (str(key) + " - " + str(newGrades[key])) ,duration=20)
            print(newGrades)
            print("NEW GRADE RELEASED")
    time.sleep(300)