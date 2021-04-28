#!/usr/bin/env python

from includes import *

class site:

    def __init__(self, name, loginURL, tableData, usr, pwd, gradesURL, *args):

        if platform == "win32":
            self.PATH = "C:\Program Files (x86)\chromedriver.exe"
        elif platform == "linux" or platform == "linux2":
            self.PATH = "/usr/bin/chromedriver"
        self.grades = {}

        self.name = name
        self.loginURL = loginURL
        self.tableData = tableData
        self.usr = usr
        self.pwd = pwd
        self.gradesURL = gradesURL
        self.additional = {}

        for i in args :
            self.additional[i[0]] = i[1]

        # We can give the entries in self.additional keys of when the step occurs and execute them if we have additional steps that must occur

    def getGrades(self):
        
        step = 0

        # step 0
        if step in self.additional:
            eval(self.additional[step])

        #if step in self.additional:
        #    self.additional[step][0](self.additional[step][1:])

        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        driver = webdriver.Chrome(self.PATH, options=option)

        step += 1

        # Step 1
        if step in self.additional:
            eval(self.additional[step])

        driver.get(self.loginURL)

        step += 1

        # Step 2
        if step in self.additional:
            eval(self.additional[step]) 

        UID_Field = driver.find_element_by_id(self.usr[0])
        UID_Field.send_keys(self.usr[1]) 
        PWD_Field = driver.find_element_by_id(self.pwd[0])
        PWD_Field.send_keys(self.pwd[1])
        PWD_Field.send_keys(Keys.RETURN)

        step += 1

        # Step 3 (for mosaic this would be time.sleep(3) )
        if step in self.additional:
            eval(self.additional[step])

        if str(driver.current_url) == self.loginURL :
            print("Error... Incorrect Login Info\n")
            return None

        step += 1

        # Step 4
        if step in self.additional:
            eval(self.additional[step]) 
        
        driver.get(self.gradesURL)

        step += 1

        # Step 5 (for mosaic click ok goes here)
        if step in self.additional:
            eval(self.additional[step]) 

        # tableData[0, 1, 2, 3] = first row xpath (except final "<row>]" ), first grade offset, class name field, grade field

        i=self.tableData[1]

        while True:
            try:
                row = self.tableData[0] + str(i) + ']'
                namePath = row + self.tableData[2]
                gradePath = row + self.tableData[3]
                name = driver.find_elements_by_xpath(namePath)[0].text
                grade = driver.find_elements_by_xpath(gradePath)[0].text
                self.grades[name] = grade
                #print("Class: " + str(name) + " - Grade: " + str(grade))
                i += 1
            except Exception:
                break
        driver.quit()

        step += 1

        # Step 6
        if step in self.additional:
            eval(self.additional[step])         

        return self.grades

        



class grades:

    def __init__(self):

        self.grades = {}
        self.sites = []

    def addSite(self, *args):

        pass

def mosaic():

    # tableData[0, 1, 2, 3] = first row xpath (except final "<row>]" ), first grade offset, class name field, grade field
    tableData = [] 
    tableData.append('/html/body/form/div[5]/table/tbody/tr/td/div/table/tbody/tr[8]/td[2]/div/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/div/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[')
    tableData.append(2)
    tableData.append('/td[2]/div/span')
    tableData.append('/td[5]/div/span')

    # usr[0, 1] = username field identifier, username
    usr = []
    usr.append("userid")
    usr.append(input("User Name: "))

    # pwd[0, 1] = password field identifier, password
    pwd = []
    pwd.append("pwd")
    pwd.append(getpass())

    # Grades URL once logged in
    gradesURL = "https://csprd.mcmaster.ca/psc/prcsprd_2/EMPLOYEE/SA/c/SA_LEARNER_SERVICES.SSR_SSENRL_GRADE.GBL?Page=SSR_SSENRL_GRADE&PortalActualURL=https%3a%2f%2fcsprd.mcmaster.ca%2fpsc%2fprcsprd_2%2fEMPLOYEE%2fSA%2fc%2fSA_LEARNER_SERVICES.SSR_SSENRL_GRADE.GBL%3fPage%3dSSR_SSENRL_GRADE&PortalContentURL=https%3a%2f%2fcsprd.mcmaster.ca%2fpsc%2fprcsprd%2fEMPLOYEE%2fSA%2fc%2fSA_LEARNER_SERVICES.SSR_SSENRL_GRADE.GBL%3fPage%3dSSR_SSENRL_GRADE&PortalContentProvider=SA&PortalCRefLabel=Grades&PortalRegistryName=EMPLOYEE&PortalServletURI=https%3a%2f%2fepprd.mcmaster.ca%2fpsp%2fprepprd_2%2f&PortalURI=https%3a%2f%2fepprd.mcmaster.ca%2fpsc%2fprepprd_2%2f&PortalHostNode=EMPL&NoCrumbs=yes&PortalKeyStruct=yes"

    # Time wait after log in
    timeWait = [3, "time.sleep(3)"]

    # Click ok on grades page
    #clickOk = [5, 'driver.find_element_by_id("#ICOK").click()']
    #clickOk = [5, 'print("hi")']

    website = site('mosaic', "https://epprd.mcmaster.ca/psp/prepprd/?cmd=login", tableData, usr, pwd, gradesURL, timeWait)#, clickOk)

    recGrades = website.getGrades()

    for key in recGrades :
        print(str(key) + " - " + str(recGrades[key]))

    return recGrades

mosaic()