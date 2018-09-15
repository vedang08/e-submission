from selenium import webdriver
import os
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import re
import time


# UPDATE REQUIRED, CURRENTLY HAS ONLY THE EXPERIMENTS AND CLASS TEST FOLDER
# the next bit is to make the e-submission folder
def make_topic_directory(master_directory, subject_directory):
    topic_list = ["01_Experiments", "02_Class_Test", "Screenshots"]
    for topic in topic_list:
        path = master_directory + "\\" + subject_directory + "\\" + topic
        if not os.path.exists(path):
            os.mkdir(path)


def make_sub_directory(master_directory):
    subject_list = ['CN', 'DBMS', 'WDL', 'MP', 'TCS', 'BCE', 'MISC']
    subject_dir_names = []
    for subject in subject_list:
        subject_name = "TE_" + division + "_COMPS_" + roll_no + "_" + subject
        path = master_directory + "\\" + subject_name
        subject_dir_names.append(path)
        if not os.path.exists(path):
            os.mkdir(path)

        make_topic_directory(master_directory, subject_name)
    return subject_dir_names


def make_master_directory(roll_no, div):
    global master
    global desk
    master_name = "TE_" + div + "_COMPS_" + roll_no
    master = desk + "/" + master_name
    os.chdir(desk)
    if os.path.exists(master_name):
        for root, dirs, files in os.walk(master_name, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
    else:
        os.mkdir(master_name)
    sub_dirs = make_sub_directory(master_name)
    return sub_dirs

def login():
    # find the location of the text field where the TU id is to be entered, in this case it was named userid
    tuid_loc = browser.find_element_by_name('userid')

    # send the TU id entered by the user to be entered in the text field
    tuid_loc.send_keys(tuid)
    # the next two statements work in a similar way
    pwd_loc = browser.find_element_by_name('pass_word')
    pwd_loc.send_keys(pwd)

    # after both the user id and password have been entered

    # from the drop down select the TEC option
    select = Select(browser.find_element_by_xpath(
        '/html/body/table/tbody/tr/td[1]/table/tbody/tr[5]/td/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]/div/select'))
    # select by visible text
    select.select_by_visible_text('TEC')

    # The next section of the code is in a try block to make sure the user has not entered an incorrect id/ password or has
    # failed to select TEC, to avoid an unnecessary crash

    try:
        # find the submit button, used xpath because I was bored
        submit = browser.find_element_by_xpath(
            '/html/body/table/tbody/tr/td[1]/table/tbody/tr[5]/td/table/tbody/tr[2]/td/table/tbody/tr[5]/td/input')
        # click submit button
        submit.click()

        # the website employs frame, I observed three, header, main, footer, what we need all lies in the main frame
        # this is something that wasn't apparent, from now on pay attention to the frames and framesets present in the HTML
        browser.switch_to.frame(browser.find_element_by_name("main"))
        # now if the browser can't find the main frame for some reason, the user has made an error

    except IOError:
        print("You didn't enter the correct id/password")


# aaaand Welcome to Hell :)


# this is a function that we will use to find whether an element exists or not
def check_exists_by_xpath(xpath):
    try:
        browser.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


def find_no_of_assign():
    no_of_assign = 3
    while True:
        if check_exists_by_xpath('/html/body/table/tbody/tr/td[2]/table/tbody/tr[' + str(no_of_assign) + ']/td[9]/a/u'):
            no_of_assign = no_of_assign + 1
        else:
            break
    return no_of_assign


# UPDATE REQUIRED
# this will give us the id of the subject when we are on an individual assignment's page
def get_subject_id():
    subject_name = browser.find_element_by_xpath(
        '/html/body/table/tbody/tr/td[2]/table/tbody/tr[5]/td[2]').text

    if subject_name == 'Computer Network Lab':
        subject_id = 0
    elif subject_name == 'Database & Info. System Lab' or subject_name == 'Database Management System':
        subject_id = 1
    elif subject_name == 'Web Design Lab':
        subject_id = 2
    elif subject_name == "Microprocessor Lab":
        subject_id = 3
    elif subject_name == "Theory of Computer Science":
        subject_id = 4
    elif subject_name == "Bussiness Comm. & Ethics":
        subject_id = 5
    else:
        subject_id = 6
    return subject_id


def loop_through_assignments():
    assignments = browser.find_element_by_xpath(
        '/html/body/table/tbody/tr/td[1]/table/tbody/tr/td/table/tbody/tr[2]/td/div/table/tbody/tr[6]/td[2]/ul/li/a/span')
    assignments.click()
    no_of_assign = find_no_of_assign()
    # now we need to find the assignments, using the anchor earlier gave me a bunch of errors so I used the span present
    # inside it as the point I wish to click
    print(no_of_assign)
    sub_id = 6
    for i in range(3, no_of_assign):
        download_folder = master + r'/ERPDownloads/'
        os.chdir(download_folder)
        assignment_link = browser.find_element_by_xpath(
            '/html/body/table/tbody/tr/td[2]/table/tbody/tr[' + str(i) + ']/td[9]/a/u')
        assignment_link.click()
        title = browser.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/table/tbody/tr[2]/td[2]').text
        sub_id = get_subject_id()
        try:
            file_link = browser.find_element_by_xpath(
                '/html/body/table/tbody/tr/td[2]/table/tbody/tr[9]/td[2]/b/u/font/a')
            file_link.click()
            file_not_downloaded = True
            time_spent = 0
            while file_not_downloaded:
                list_o_files = os.listdir(download_folder)
                if len(list_o_files) == 1:
                    file_not_downloaded = False
                    time.sleep(2.5)
                    time_spent = time_spent + 2.5
                    if time_spent >= 10:
                        file_not_downloaded = False
                else:
                    pass
            list_o_files = os.listdir(download_folder)
            file_name_o = list_o_files[0]
            file_name = file_name_o
            regex = re.compile(r"(.*)(TE_(.*))")
            try:
                # the name of the actual file is in the 2nd group, ref. regex
                file_name = regex.match(str(file_name_o)).group(2)
            except:
                pass
            source = download_folder + file_name_o

            path = sub_dir_list[sub_id] + '\\' + "Screenshots"
            os.chdir(desk)
            os.chdir(path)
            # the file_name contains both the path and file name, screenshots must always be .png
            screenshot_name = 'screenshot' + str(i) + '.png'
            # use the selenium screenshot method
            browser.get_screenshot_as_file(screenshot_name)
            destination = source
            if sub_id == 0:
                subject = 'CN'
                destination = desk + "/" + sub_dir_list[0] + "/01_Experiments/" + file_name
            elif sub_id == 1:
                subject = 'DBMS'
                destination = desk + "/" + sub_dir_list[1] + "/01_Experiments/" + file_name
            elif sub_id == 2:
                subject = 'WDL'
                destination = desk + "/" + sub_dir_list[2] + "/01_Experiments/" + file_name
            elif sub_id == 3:
                subject = 'MP'
                destination = desk + "/" + sub_dir_list[3] + "/01_Experiments/" + file_name
            elif sub_id == 4:
                subject = 'TCS'
                destination = desk + "/" + sub_dir_list[4] + "/01_Experiments/" + file_name
            elif sub_id == 5:
                subject = 'BCE'
                destination = desk + "/" + sub_dir_list[5] + "/01_Experiments/" + file_name
            else:
                subject = 'MISC'
                destination = desk + "/" + sub_dir_list[6] + "/01_Experiments/" + file_name
            os.rename(source, destination)
        except NoSuchElementException:
            print("You haven't submitted " + title + " of " + subject)
        assignments = browser.find_element_by_xpath(
            '/html/body/table/tbody/tr/td[1]/table/tbody/tr/td/table/tbody/tr[2]/td/div/table/tbody/tr[6]/td[2]/ul/li/a/span')

        # we loop through all the tr since in each tr the view icon is in the same place (the part after i)
        # now we click on the anchor tag and the downloads automatically starts, if there is no anchor tag, that means we haven't submitted the assignment
        # go back to assignments
        assignments.click()
    browser.quit()


# when I analysed the HTML each individual assignment was in tr field starting from 3 the first two aren't important

# and that, my friend, was all she wrote ;)

# user inputs
division = input('Enter Division ').upper()
roll_no = input('Enter Roll No. ')
tuid = input('Enter TU Id: ')
tuid = tuid.upper()
pwd = input('Enter password: ')

master = ''
# find the location of user's desktop
desk = os.path.expanduser(r'~/Desktop')
# move to the desktop
os.chdir(desk)

sub_dir_list = make_master_directory(roll_no, division)

os.chdir(master)
# check whether the ERPDownloads folder exists, if it doesn't create it
if not os.path.exists('ERPDownloads'):
    os.mkdir('ERPDownloads')

# the location of the downloads folder
downloads = master + r"\ERPDownloads"

# this next bit is to ensure that the downloads are in our folder and not the default downloads folder
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_experimental_option("prefs", {
    "download.default_directory": downloads,
    "download.prompt_for_download": False,
    "plugins.always_open_pdf_externally": True,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

# next, we get the location of the user's chrome driver because that's what selenium will use to run chrome
try:
    chromePath = input("Paste the path for chrome driver.exe ")
    # we open the browser
    browser = webdriver.Chrome(executable_path=chromePath, port=0, chrome_options=chromeOptions, service_args=None,
                               desired_capabilities=None, service_log_path=None)

    # ask browser to first visit the terna trust login page
    browser.get('http://ternatrust.org/login')
except:
    print("Incorrect chrome driver path")
    exit()
# then click the erp icon, chose xpath since there was no other way to clearly identify the element
erp = browser.find_element_by_xpath('//*[@id="fh5co-main"]/div/div/div[1]')
# click on the erp icon that was just navigated to
erp.click()
# maximize the window
browser.maximize_window()
# erp login page opens in a new window, switch to that window
browser.switch_to.window(browser.window_handles[1])
login()
loop_through_assignments()



