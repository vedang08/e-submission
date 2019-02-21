# this is the driver that python will use to control chrome
from selenium import webdriver
# for file handling
import os
# for selecting from the dropdown
from selenium.webdriver.support.ui import Select
# this for when we need the browser object to wait
from selenium.webdriver.support.ui import WebDriverWait
# exceptions that might arise during the process
from selenium.common.exceptions import *
# these things are required for the webdriver wait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
# for making the GUI
from tkinter import *
# for the popups
from tkinter import messagebox

"""IMPORTANT!"""
"""For the uninitiated: This program uses quite a few functions so if there is a function call, you should first go 
and check it out to understand what's going on. You should also start with the create folder function at the end"""
# The three functions are to create the folders
"""this function creates the main folder, it needs the roll_no, division and year of the student"""


def make_master_directory(roll_no, division, semester, year):
    # we need to access this folder again hence we'll declare it as a global variable
    global master
    # the format in which the folder is to be named
    master_name = year + "_" + division + "_COMPS_" + roll_no
    """ here desk is the path to the user's desktop (explained later, I know its getting kind of annoying). 
    We add the name of the master directory to it"""
    master = desk + "/" + master_name
    # Create the directory if it doesn't exist
    if not os.path.exists(master):
        os.mkdir(master)
    # now to make the subject directories, call a function its return value will be stored here
    sub_dirs = make_sub_directory(roll_no, division, semester, year)
    # this function will in turn return the list of paths to subject dirs kind of like passing the baton
    return sub_dirs


""" function to create the subject directories which require the roll_no, division, semester(subject list changes based 
on the semester) and year of the student and it returns the path of each directory which we'll require later """


def make_sub_directory(roll_no, division, semester, year):
    # we need to access this subject_list later
    global subject_list
    """ here the subject lists are different based on the student's semester, there is a MISC folder where
     subjects that don't have much significance would be added"""
    if semester == "III":
        subject_list = ['DLDA', 'DS', 'DIM', 'OOPM', 'ECCF', 'MISC']
    elif semester == "IV":
        subject_list = []
    elif semester == "V":
        subject_list = ['CN', 'DBMS', 'WDL', 'MP', 'TCS', 'ELEC', 'MISC']
    elif semester == "VI":
        subject_list = []
    elif semester == "VII":
        subject_list = ['DSP', 'CSS', 'AI', 'NTAL', 'ELEC', 'MISC']
    elif semester == "VIII":
        subject_list = []
    # initialize a list for the subject directories
    subject_dir_names = []
    # loop through the subject list
    for subject in subject_list:
        # the format in which subject names need to be present in the folder
        subject_name = year + "_" + division + "_COMPS_" + roll_no + "_" + subject
        """Here master is the path to the master directory on the user's desktop(explained later). 
        We add the name of the subject to it"""
        subject_directory = master + "\\" + subject_name
        # and add it to our list of subject directories
        subject_dir_names.append(subject_directory)
        # we check if the directory already exists or not, if it doesn't we create it
        if not os.path.exists(subject_directory):
            os.mkdir(subject_directory)
        # a call a function to create the topic directories.
        make_topic_directory(subject_directory)
    # after we have created directories for each subject, return the list of paths to each directory
    return subject_dir_names


""" function to create the topic directories of which there are 3, it requires the path to the 
master directory(main folder) and subject directory in which these folders are to be made"""


def make_topic_directory(subject_directory):
    # list of topics
    topic_list = ["01 Experiments", "02 Class Tests", "03 Assignments", "04 Quiz", "05 Attendance", "06 Exit Survey",
                  "07 Certificate", "Screenshots"]
    # loop through the topic list
    for topic in topic_list:
        """  To it
         add the subject directory and the name of the topic directory"""
        path = subject_directory + "\\" + topic
        # check if this path exists and make the directory if it doesn't
        if not os.path.exists(path):
            os.mkdir(path)


# Folder Creation ends here


# The next three are simple support functions
""" this is a simple function to find if an element exists or not"""


def check_exists_by_xpath(xpath):
    # the browser tries to find the element
    try:
        browser.find_element_by_xpath(xpath)
    # if it can't then we return false
    except NoSuchElementException:
        return False
    # if it does we return true
    return True


"""another simple function to find the no. of assignments that the user has been given"""


def find_no_of_assign():
    # in the current erp setup(Sept/Oct 2018) the first 2 rows of the table don't have any useful information
    # the actual assignments start at row 3
    no_of_assign = 3
    # now we create a loop
    while True:
        """ call to a function, we keep incrementing the table rows, once there are no rows left the function will 
        return false and the then value of no_of_assign is the no. of assignments the user has been given"""
        if check_exists_by_xpath('/html/body/table/tbody/tr/td[2]/table/tbody/tr[' + str(no_of_assign) + ']/td[9]/a/u'):
            no_of_assign = no_of_assign + 1
        else:
            break
    return no_of_assign


"""This function finds which subject a particular assignment belongs to"""


def get_subject_id():
    # we find the name of the subject for the given assignment
    subject_name = browser.find_element_by_xpath(
        '/html/body/table/tbody/tr/td[2]/table/tbody/tr[5]/td[2]').text
    # the next few lines are self evident but as a hint, check the subject lists we created in the master directory
    if subject_name == 'Computer Network Lab' or subject_name == 'Computer Network' or \
            subject_name == 'Digital Signal Processing' \
            or subject_name == 'Digital Logic Design and Analysis' or subject_name == 'Digital System Lab':
        subject_id = 0
    elif subject_name == 'Database & Info. System Lab' or subject_name == 'Database Management System' or \
            subject_name == "Cryptography and System Security" \
            or subject_name == 'Data Structures' or subject_name == 'Data structure Lab':
        subject_id = 1
    elif subject_name == 'Web Design Lab' or subject_name == "Artificial Intelligence" \
            or subject_name == "Discrete Mathematics":
        subject_id = 2
    elif subject_name == "Microprocessor Lab" or subject_name == "Microprocessor" or \
            subject_name == "Network Threats and Attacks Laboratory" or \
            subject_name == "OOPM(Java)" or subject_name == "OOPM(Java) Lab":
        subject_id = 3
    elif subject_name == "Theory of Computer Science" \
            or subject_name == "Electronic Circuits and Communication Fundamentals" or "Elective" in subject_name \
            or subject_name == "Basic Electronics Lab ":
        subject_id = 4
    else:
        subject_id = 5
    return subject_id


"""This function finds chromedriver.exe"""


def find_chrome():
    # initially, we set the chrome path to blank
    chrome_path = ""
    # this is a list of possible directories where chromedriver.exe should exist
    possible_dirs = [os.path.expanduser(r"~\Desktop"), os.path.expanduser(r"~\Downloads"),
                     os.path.expanduser(r"~\Documents")]
    # loop through these directories
    for root_folder in possible_dirs:
        # this function goes through the root folder and lists all the files in the folder and in the directories within
        for root_name, dirs, files in os.walk(root_folder):
            # we search through the lis tof files
            for f in files:
                # we find chromedriver.exe we set the chrome path to be the path to the file
                if f == "chromedriver.exe":
                    chrome_path = os.path.join(root_name, f)
                    break
    return chrome_path


"""Now we need to login for which we need the id and password"""


def login(tuid, pwd):
    # we declare that we are referencing the global error flag variable
    global error_flag
    # to handle the situations where erp might be down, we wait for 5 seconds, if no response we assume the worst
    try:
        # we find the location of the tuid element which is named userid
        tuid_loc = WebDriverWait(browser, 5).until(ec.presence_of_element_located((By.NAME, "userid")))
        # enter the tuid
        tuid_loc.send_keys(tuid)
        # same as above
        pwd_loc = browser.find_element_by_name('pass_word')
        pwd_loc.send_keys(pwd)
        # find the dropdown menu
        select = Select(browser.find_element_by_xpath(
            '/html/body/table/tbody/tr/td[1]/table/tbody/tr[5]/td/table/tbody/tr[2]/td/table/tbody/'
            'tr[3]/td[2]/div/select'))
        # select TEC from the dropdown
        select.select_by_visible_text('TEC')
    except TimeoutException:
        error_flag = True
        error = "ERP seems to be down, try again later"
        browser.quit()
        messagebox.showerror("Error!", error)
    # now we try to submit the entered info
    try:
        # find the submit button, used xpath because I was bored
        submit = browser.find_element_by_xpath(
            '/html/body/table/tbody/tr/td[1]/table/tbody/tr[5]/td/table/tbody/tr[2]/td/table/tbody/tr[5]/td/input')
        # click submit button
        submit.click()
        # when the user has logged in the frame changes
        browser.switch_to.frame(browser.find_element_by_name("main"))
        # now if there is an alert that comes up, the user has made an error
    except UnexpectedAlertPresentException:
        error_flag = True
        # update the global error statement
        error = "You didn't enter the correct id/password"
        # quit the browser
        browser.quit()
        # display the error
        messagebox.showerror("Error!", error)


"""This is the function that does the brunt of the work"""


def loop_through_assignments(sel_year, division, roll_no):
    # we declare that we are referencing the global error flag variable
    global error_flag
    # an empty list where we'll add the assignments that the user has not submitted
    not_submitted = "You haven't submitted: \n\n"
    list_not_downloaded = "These files couldn't be downloaded, they have to be done manually: \n\n"
    # after logging in we first find the assignments tab and move to the assignments section
    # try block because erp can be down, again the same principle as the previous one
    try:
        assignments = WebDriverWait(browser, 5).until(ec.presence_of_element_located((By.XPATH,
                                                                                      '/html/body/table/tbody/tr/td[1]/'
                                                                                      'table/tbody/tr/td/table/tbody/'
                                                                                      'tr[2]/td/div/table/tbody/tr[6]/'
                                                                                      'td[2]/ul/li/a/span')))
        assignments.click()
    except TimeoutException:
        error_flag = True
        error = "ERP seems to be down, try again later"
        browser.quit()
        messagebox.showerror("Error!", error)
    # call to a function
    no_of_assign = find_no_of_assign()
    # again the first 2 rows aren't of much use to us, we start looping over each assignment which begin at row 3
    for i in range(3, no_of_assign):
        # now we move to the downloads folder where all the assignments would be initially downloaded
        download_folder = master + r'/ERPDownloads/'
        os.chdir(download_folder)
        # find the link to each assignment, this would change each time when the loop executes
        assignment_link = browser.find_element_by_xpath(
            '/html/body/table/tbody/tr/td[2]/table/tbody/tr[' + str(i) + ']/td[9]/a/u')
        assignment_link.click()
        # this is the name of the assignment given at the top
        title = browser.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/table/tbody/tr[2]/td[2]').text
        # call to a function
        sub_id = get_subject_id()
        try:
            # we try to find the name of the file the user has submitted, if he has submitted it
            file_name_o = browser.find_element_by_xpath(
                '/html/body/table/tbody/tr/td[2]/table/tbody/tr[9]/td[2]/b/u/font/a').text
            # Now we find the number of the given assignment, for eg. Experiment 2, Assignment No.1
            try:
                title_no = str(re.search(r"\d+(?: \(\w\)|\(\w\)|{\w}|\[\w\]|)", title).group())
                """if there is no number for the given assignment the group() function will fail as it returns the 
                matched part of the string and it won't find any matches"""
            except AttributeError:
                title_no = ""
            """a rudimentary way of finding whether a given assignment is an Experiment, if you're reading this at some
            point in the future where things have improved, you can optimize this"""
            if "exp" in title.lower():
                fol_name = "/01 Experiments/"
                # here we change the value of the title variable to what it should be
                title = "EXP_" + title_no
            # for class tests
            elif re.search(r"(?:(?:unit|class) test|[cu]t)", title.lower()) and "project" not in title.lower():
                fol_name = "/02 Class Tests/"
                title = "CT_" + title_no
            # similar to what's been done above
            elif "assign" in title.lower():
                fol_name = "/03 Assignments/"
                title = "ASSIGN_" + title_no
            else:
                fol_name = "/03 Assignments/"
            no_ext_flag = False
            dot_list = file_name_o.split(".")
            ext = "pdf"
            if dot_list[-1] in ["doc", "docx", "pdf", "jpg", "jpeg", "xlxs", "zip", "xml", "txt", "ppt"]:
                ext = dot_list[-1]
            else:
                no_ext_flag = True
            # setting the name for the file in a proper format
            file_name = sel_year + '_' + division + "_" + roll_no + "_" + title + "_" + subject_list[sub_id] + "." + ext
            """ now we decide the destination of the file because we'll have to check whether the file we are downloading
            already exists or not"""
            destination = sub_dir_list[sub_id] + fol_name + file_name
            # check if the file already exists or not
            if not os.path.exists(destination):
                # we try to find the link to the file, if the user has submitted it, then we'll be able to click on it
                file_link = browser.find_element_by_xpath(
                    '/html/body/table/tbody/tr/td[2]/table/tbody/tr[9]/td[2]/b/u/font/a')
                file_link.click()
                # initially, when the file has not been downloaded we set the file_not_downloaded flag to true
                file_not_downloaded = True
                # this loop will run until the file is downloaded
                while file_not_downloaded:
                    # first get the list of files in the download folder
                    list_o_files = os.listdir(download_folder)
                    # if there is a file present in the download folder we need to check some things
                    if len(list_o_files) == 1:
                        """the way chrome downloads files is that once we start the download it creates a .tmp, once it gets
                         the exact name of the file it renames it to .crdownload and once the download is complete it 
                         renames it to whatever its supposed to be, so we check for both of those things in the file"""
                        if ".tmp" not in list_o_files[0]:
                            if ".crdownload" not in list_o_files[0]:
                                remove_flag = False
                                if no_ext_flag:
                                    if list_o_files[0].split(".")[-1] in ["doc", "docx", "pdf", "jpg", "jpeg", "xlxs",
                                                                          "zip", "xml", "txt", "ppt"]:
                                        ext = list_o_files[0].split(".")[-1]
                                        # setting the name for the file in a proper format
                                        file_name_o = list_o_files[0]
                                        file_name = sel_year + '_' + division + "_" + roll_no + "_" + title + "_" + \
                                                    subject_list[sub_id] + "." + ext
                                        destination = sub_dir_list[sub_id] + fol_name + file_name
                                    else:
                                        remove_flag = True
                                        list_not_downloaded = list_not_downloaded + subject_list[
                                            sub_id] + " " + title + "\n"
                                # only when the download is complete we set the file_not_downloaded to false
                                file_not_downloaded = False
                # GETTING THE SCREENSHOT
                # now we find the path to the current subject directory and then move to its screenshots folder
                path = sub_dir_list[sub_id] + '\\' + "Screenshots"
                os.chdir(path)
                # the name for every screenshot has to be unique
                screenshot_name = sel_year + "_" + division + "_" + roll_no + "_" + title + "_" + subject_list[
                    sub_id] + '.png'
                # take the screenshot
                try:
                    browser.get_screenshot_as_file(screenshot_name)
                except FileExistsError:
                    pass
                # thus the screenshot for this assignment is done
                # now to move the file, we first get its current path
                source = download_folder + file_name_o
                # move the file from its source to destination, here rename stands for renaming the path to a file
                if not remove_flag:
                    try:
                        os.rename(source, destination)
                    except FileExistsError:
                        os.remove(source)
                else:
                    os.remove(source)
            else:
                pass
            # if the browser couldn't click on the link it means it doesn't exist and
            # the user hasn't submitted a particular file
        except NoSuchElementException:
            subject = subject_list[sub_id]
            # add the name of the file to our string of not submitted files
            not_submitted = not_submitted + title + " of " + subject + "\n"
        # now click on the assignments link again and the cycle will continue till we've exhausted all the assignments
        assignments = browser.find_element_by_xpath(
            '/html/body/table/tbody/tr/td[1]/table/tbody/tr/'
            'td/table/tbody/tr[2]/td/div/table/tbody/tr[6]/td[2]/ul/li/a/span')
        assignments.click()
    browser.quit()
    # now if the value of the variable has not been changed then it means that the user has submitted everything
    if not_submitted == "You haven't submitted: \n\n":
        messagebox.showinfo("Done!", "Good job mate!")
    # otherwise we show this warning
    else:
        messagebox.showinfo("Submit These First!", not_submitted)
    if list_not_downloaded == "These files couldn't be downloaded, they have to be done manually: \n\n":
        pass
    else:
        messagebox.showinfo("Unable to download", list_not_downloaded)


"""this is sort of the main function which calls the other important functions and which is executed when the user 
clicks the create folder button"""


def create_folder():
    # we declare that we are trying to access the global variables with the following names
    global sub_dir_list
    global desk
    global master
    global error_flag
    # now as the button is pressed we need to get the current value for each field
    # we obtain the value of the radiobuttons from the dropdown and set division accordingly
    division = div.get()
    # since division returns a numeric value assign it a proper alphabet
    if division == 1:
        division = "A"
    elif division == 2:
        division = "B"
    else:
        division = "C"
    # similarly we get the other values
    roll_no = rno.get()
    tuid = tid.get()
    tuid = tuid.upper()
    pwd = p.get()
    semester = sem.get()
    if semester == "III" or semester == "IV":
        year = "SE"
    elif semester == "V" or semester == "VI":
        year = "TE"
    else:
        year = "BE"

    if str(roll_no) == "" or str(tuid) == "" or str(pwd) == "":
        messagebox.showinfo("Empty Fields", "You haven't filled all the required information")
    else:
        # ACTUAL LOGIC STARTS HERE!
        # we initialize the path to master directory(main folder)
        master = ''
        # here we find the path to the user's desktop and move to it
        desk = os.path.expanduser(r'~/Desktop')
        os.chdir(desk)
        # call to a function
        sub_dir_list = make_master_directory(roll_no, division, semester, year)
        # now once the master directory is created we move to it
        os.chdir(master)
        # inside the master directory we check if there is a folder named ERPDownloads, if there isn't, we make one
        if not os.path.exists('ERPDownloads'):
            os.mkdir('ERPDownloads')
        # we set the location of the downloads as this folder
        downloads = master + r"\ERPDownloads"
        # we first initialize a variable to store the options with which we wish to open chrome
        chrome_options = webdriver.ChromeOptions()
        # we add these options to it
        chrome_options.add_experimental_option("prefs", {
            # we specify the default download directory
            "download.default_directory": downloads,
            # we disable the prompt that appears for download
            "download.prompt_for_download": False,
            # we say that chrome shouldn't open pdfs on its own
            "plugins.always_open_pdf_externally": True,
            # we say that we have updated the download directory
            "download.directory_upgrade": True,
            "safebrowsing.enabled": False
        })
        # we try to open up a browser
        try:
            # now we declare browser as a global variable because its going to used throughout the program
            global browser
            # we find the exact path to the chrome driver which should be in the downloads directory
            chrome_path = find_chrome()
            # we open the browser
            browser = webdriver.Chrome(executable_path=chrome_path, port=0, chrome_options=chrome_options,
                                       service_args=None,
                                       desired_capabilities=None, service_log_path=None)
        except OSError:
            # if we can't that means that there is no chromedriver downloaded by the user
            error_flag = True
            error = "Unable to find chromedriver.exe. Please ensure that it is somewhere in the desktop directory"
            # we show the error in a popup
            messagebox.showerror("Error!", error)
            # we quit the execution of the program
            # exit()
        try:
            # ask browser to first visit the terna trust login page
            browser.get('http://ternatrust.org/login')
            erp = browser.find_element_by_xpath('//*[@id="fh5co-main"]/div/div/div[1]')
            # click on the erp icon that was just navigated to
            erp.click()
            # maximize the window
            browser.maximize_window()
            # erp login page opens in a new window, switch to that window
            browser.switch_to.window(browser.window_handles[1])
        except NoSuchElementException:
            error_flag = True
            # if it can't, then it means that there is no network
            error = "No Network"
            # we quit the browser
            browser.quit()
            messagebox.showerror("Error!", error)
        # call to functions
        try:
            # we first login where we need the tuid and password
            login(tuid, pwd)
            attendance_link = browser.find_element_by_xpath(
                r"/html/body/table/tbody/tr/td[1]/table/tbody/tr/td[1]/table/tbody/tr[2]/td/div/table/tbody/tr[3]/"
                r"td[2]/ul/li/a/span")
            attendance_link.click()
            course_wise_link = browser.find_element_by_xpath(
                r'/html/body/table/tbody/tr/td[2]/table[1]/tbody/tr/td[2]/a')
            course_wise_link.click()
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            file_name = year + "_" + division + "_ATTENDANCE_" + roll_no + ".png"
            for subject in sub_dir_list:
                attendance_path = subject + r"\05 Attendance"
                os.chdir(attendance_path)
                try:
                    browser.get_screenshot_as_file(file_name)
                except FileExistsError:
                    pass
            # and then we loop through assignments
            loop_through_assignments(year, division, roll_no)
            os.chdir(master)
            os.rmdir("ERPDownloads")
        except:
            if error_flag is not True:
                error_flag = True
                messagebox.showerror("Error!", "Something went wrong, try again later")
            else:
                pass


error_flag = False
"""ignore my tkinter shenanigans. The next part creates the GUI, where, if you press the create folder button,
 the above function executes"""
# this the setup for the GUI
# we create our app
root = Tk()
# the configure method is mostly used for aesthetic purposes
root.configure(background="gray17")
# the root should not be resizable
root.resizable(False, False)
# we set the size of the main frame
root.geometry("500x280")
# we create four frames that will contain different things
frame1 = Frame(root)
frame1.configure(background="gray17")
frame1.pack()
frame2 = Frame(root)
frame2.configure(background="gray17")
frame2.pack()
frame3 = Frame(root)
frame3.configure(background="gray17")
frame3.pack()
frame4 = Frame(root)
frame4.configure(background="gray17")
frame4.pack(side=RIGHT)
# we set the title to our app
root.title("E-Submission")
# we setup variables for the division and year
div = IntVar()
div.set(1)
sem = StringVar()
# the options for year, the default is set to SE
options = ["III", "IV", "V", "VI", "VII", "VIII"]
sem.set(options[0])
# we create a label and an adjoining entry field for tuid, password, and roll no. and place it on various rows
l1 = Label(frame1, text="TU ID: ", fg="gray75")
l1.grid(row=0, column=6, pady=(20, 4))
l1.configure(background="gray17")
tid = Entry(frame1, bg="gray35", fg="gray85")
tid.grid(row=0, column=9, sticky=E, pady=(20, 4))
l2 = Label(frame1, text="Password: ", fg="gray75")
l2.grid(row=2, column=6, pady=4)
l2.configure(background="gray17")
p = Entry(frame1, show="*", bg="gray35", fg="gray85")
p.grid(row=2, column=9, sticky=E, pady=4)
l3 = Label(frame1, text="Roll Number: ", fg="gray75")
l3.grid(row=4, column=6, pady=4)
l3.configure(background="gray17")
rno = Entry(frame1, bg="gray35", fg="gray85")
rno.grid(row=4, column=9, sticky=E, pady=4)
# we create a label for the division, since all of them are packed to the left, they appear in a straight line
l4 = Label(frame2, text="Division: ", fg="gray75")
l4.pack(side=LEFT, padx=15, pady=(8, 5))
l4.configure(background="gray17")
# we create three radiobuttons for the divisions
r1 = Radiobutton(frame2, text="A", variable=div, value=1)
r1.pack(side=LEFT, padx=5, pady=(10, 5))
r1.configure(background="gray17", fg="gray75", selectcolor="gray25")
r2 = Radiobutton(frame2, text="B", variable=div, value=2)
r2.pack(side=LEFT, padx=5, pady=(10, 5))
r2.configure(background="gray17", fg="gray75", selectcolor="gray25")
r3 = Radiobutton(frame2, text="C", variable=div, value=3)
r3.configure(background="gray17", fg="gray75", selectcolor="gray25")
r3.pack(side=LEFT, padx=5, pady=(10, 5))
# we create a dropdown for year
option_label = Label(frame3, text="Semester:", fg="gray75")
option_label.pack(side=TOP)
option_label.configure(background="gray17")
o = OptionMenu(frame3, sem, *options)
o.pack(pady=5)
o.configure(background="gray25", highlightthickness=0, bd=1, fg="gray75")
# THIS IS WHAT YOU NEED TO FOCUS ON!, when the button is pressed the following create_folder button is executed
b = Button(frame3, text="Create Folder", command=create_folder, fg="gray75")
b.pack(padx=10, pady=5, side=TOP)
b.configure(background="gray35", highlightthickness=0, bd=1)
l5 = Label(frame3, text="To quit, exit the browser", fg="gray75")
l5.pack(side=BOTTOM, padx=10)
l5.configure(background="gray17")
# and for a little bit of credit
l6 = Label(frame4, text="~By Vean", font=("TkDefaultFont", 10, "italic"), fg="gray75")
l6.pack(side=RIGHT, padx=10, )
l6.configure(background="gray17")
root.mainloop()
# and that, my friend, was all she wrote. I've also realized that the program has just crossed 500 lines, I have no life
