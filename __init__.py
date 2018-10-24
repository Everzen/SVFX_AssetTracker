import sys, os, pprint, time
from PySide.QtCore import *
from PySide.QtGui import *
import qdarkstyle
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from operator import itemgetter
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import widgets
import googleSheet
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
app = QApplication(sys.argv)
app.setStyleSheet(qdarkstyle.load_stylesheet())
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~






# print ("COURSE DATA")
# print ("Course Name : " + root.get('Textbox12'))
# print ("Course Code : " + root.get('Textbox4'))
# print ("Course Tutor : " + root.get('Textbox16'))
# print ("Module Semester 1 : " + root.get('Textbox23'))
# print ("Module Year : " + root.get('Textbox20'))


print ("\nSTUDENT LIST\n")
staffList = [{"name":"Gwyn Carlisle", "gmail":"gwynnethcarville@gmail.com"},
            {"name":"Jim Costello", "gmail":"unknown"},
            {"name":"Richard Jones", "gmail":"3dframework@gmail.com"},
            {"name":"Matt Lilley", "gmail":"mattpaullilley@gmail.com"},
            {"name":"Richard McEvoy-Crompton", "gmail":"fabrikbouche@gmail.com"},
            {"name":"Claire Minehane", "gmail":"unknown"},
            {"name":"Jack Myers", "gmail":"jacko83@gmail.com"},
            {"name":"Sam Taylor", "gmail":"samtaylorsfx@gmail.com"},
            {"name":"Mark Whyte", "gmail":"mark1virtual@gmail.com"},
            {"name":"Natalie Woods", "gmail":"njwoods87@hotmail.co.uk"}]



courseList = [{"name":"BDes(Hons) Special Effects for Film and Television", "code":"CRT022-F-UOB-SX", "shortName":"SFX"},
              {"name":"BSc (Hons) Visual Effects for Film and Television", "code":"CRT021-F-UOB-SX", "shortName":"VFX"},
              {"name":"BDes(H) Special Make Up Effects for Film and TV", "code":"CRT002-F-UOB-SX", "shortName":"SMUFX"},
              {"name":"BDes(Hons) Special Effects Modelmaking for Film and Television", "code":"CRT007-F-UOB-SX", "shortName":"MMFX"}] 



# loanList = [studentList[0], studentList[1]]


class SVFX_AssetTrackerUI(QDialog):
    def __init__(self, parent=None):
        super(SVFX_AssetTrackerUI, self).__init__(parent)
        self.assignmentDetails = {} #A dict to contain information about the assignments, once the marking module sheet is setup.
        self.studentFolders = []

        self.folderLabel = QLabel("Path to be displayed here...")  #Define Folder label early so that it can be passed to the list widget
        # self.folderLabel.setText("moo")

        userLeftLayout = QVBoxLayout()
        self.userListTV = widgets.userTV(courseList, self.folderLabel)
        self.setMinimumSize(400,800)
        self.setMaximumSize(1150,800)
        self.tabWidget = QTabWidget()
        self.tabWidget.addTab(self.userListTV, "Module Box Creation")
        # self.tabWidget.addTab(QWidget(), "Relative")
        # self.tabWidget.addTab(QWidget(), "Questions")
        # self.tabWidget.addTab(QWidget(), "Quest Specific")

        moduleFolderLayout = QHBoxLayout()
        foldernameLabel = QLabel("MARKING FOLDER:")
        foldernameLabel.setMaximumWidth(95)
        # self.folderLabel = QLabel("Path to be displayed here...")
        
        moduleFolderLayout.addWidget(foldernameLabel)
        moduleFolderLayout.addWidget(self.folderLabel)

        userLeftLayout.addLayout(moduleFolderLayout)
        userLeftLayout.addWidget(self.tabWidget)


        moduleSettingsLayout = QVBoxLayout()
        moduleSettingsLayout.setAlignment(Qt.AlignTop)

        userColumnWidth = 250
        userTabWidth = 400
        
        #Setup regarding List - This is going to dictate who the message is about
        courseLabel = QLabel("Filter by Courses")
        self.courseListLW =  QListWidget()
        self.courseListLW.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.courseListLW.setMaximumHeight(19*len(courseList))
        for c in courseList:
            newCourse = QListWidgetItem(c["shortName"])
            self.courseListLW.addItem(newCourse)

        courseFilterButton = QPushButton("Apply Course Filter")
        courseFilterButton.clicked.connect(self.filterCourses)
        courseFilterButton.setMinimumHeight(25)
        # regardingListLW.insertItems(0, regardingList)

        firstMarkerLabel = QLabel("First Marker")
        self.firstMarkerCombo = QComboBox(self)
        self.firstMarkerCombo.addItem("Choose First Marker...")  
        self.firstMarkerCombo.activated[str].connect(self.firstMarkerComboSel)       
        for s in staffList:
            self.firstMarkerCombo.addItem(s["name"])
        self.firstMarkerEmail = QLineEdit()
        self.firstMarkerEmail.setReadOnly(True)


        secondMarkerLabel = QLabel("Second Marker")
        self.secondMarkerCombo = QComboBox(self)
        self.secondMarkerCombo.addItem("Choose Second Marker...")
        self.secondMarkerCombo.activated[str].connect(self.secondMarkerComboSel)       

        for s in staffList:
            self.secondMarkerCombo.addItem(s["name"])
        self.secondMarkerEmail = QLineEdit()
        self.secondMarkerEmail.setReadOnly(True)


        yearLayout = QHBoxLayout()
        yearLabel = QLabel("Select Academic Year:")
        self.yearCombo = QComboBox(self)
        self.yearCombo.addItems(["2017-18","2018-19","2019-20","2020-21", "2021-22","2022-23"])    #HARDCODED year dates

        yearLayout.addWidget(yearLabel)
        yearLayout.addWidget(self.yearCombo)

        prepDateLabel = QLabel("Module Preparation Date:")
        self.prepDate = QCalendarWidget(self)
        reviewDateLabel = QLabel("Module Review Date:")
        self.reviewDate = QCalendarWidget(self)

        moduleSettingsLayout.addWidget(courseLabel)
        moduleSettingsLayout.addWidget(self.courseListLW)
        moduleSettingsLayout.addWidget(courseFilterButton)
        moduleSettingsLayout.addWidget(firstMarkerLabel)
        moduleSettingsLayout.addWidget(self.firstMarkerCombo)
        moduleSettingsLayout.addWidget(self.firstMarkerEmail)
        moduleSettingsLayout.addWidget(secondMarkerLabel)
        moduleSettingsLayout.addWidget(self.secondMarkerCombo)
        moduleSettingsLayout.addWidget(self.secondMarkerEmail)
        moduleSettingsLayout.addLayout(yearLayout)
        moduleSettingsLayout.addWidget(prepDateLabel)
        moduleSettingsLayout.addWidget(self.prepDate)
        moduleSettingsLayout.addWidget(reviewDateLabel)
        moduleSettingsLayout.addWidget(self.reviewDate)

        activationLayout = QVBoxLayout()
        activationLayout.setAlignment(Qt.AlignTop)

        moduleBoxDocButton = QPushButton("Build Module Box Document")
        moduleBoxDocButton.clicked.connect(self.buildModuleBox)
        moduleBoxDocButton.setMinimumHeight(400)
        moduleBoxDocButton.setMinimumWidth(300)

        self.markingFolderButton = QPushButton("Create Marking Folders")
        self.markingFolderButton.clicked.connect(self.createMarkingFolders)
        self.markingFolderButton.setEnabled(False)
        self.markingFolderButton.setMinimumHeight(100)
        # self.markingFolderButton.setMinimumWidth(100)
        self.sortAssignmentsLabel = QLabel("Sort Assignments")
        self.sortAssignmentsLabel.setEnabled(False)

        assignmentSortLayout = QHBoxLayout()
        self.assignmentCombo = QComboBox(self)
        self.assignmentCombo.addItem("No Assignment info")
        self.assignmentCombo.setEnabled(False)
        self.sortAssignmentsButton = QPushButton("Sort Assignments") 
        self.sortAssignmentsButton.clicked.connect(self.sortAssignmentFiles)
        self.sortAssignmentsButton.setEnabled(False)

        assignmentSortLayout.addWidget(self.assignmentCombo)
        assignmentSortLayout.addWidget(self.sortAssignmentsButton)

        exportFeedbackButton = QPushButton("Export Feedback")
        exportFeedbackButton.setMinimumHeight(215)
        # exportFeedbackButton.setMinimumWidth(100)
        exportFeedbackButton.setEnabled(False)

        activationLayout.addWidget(moduleBoxDocButton)
        activationLayout.addWidget(self.markingFolderButton)
        activationLayout.addWidget(self.sortAssignmentsLabel)
        activationLayout.addLayout(assignmentSortLayout)
        activationLayout.addWidget(exportFeedbackButton)

        mainLayout = QHBoxLayout()
        mainLayout.addLayout(userLeftLayout)
        mainLayout.addLayout(moduleSettingsLayout)
        mainLayout.addLayout(activationLayout)

        # mainLayout.addWidget(tabWidget)
        # mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("The Rubrics Cube")

    def filterCourses(self):
        #Grab the selection state of the Course List widget
        selCourses = self.courseListLW.selectedItems()
        selCourseArr = []
        if len(selCourses) == 0: selCourseArr = ["SFX", "VFX", "SMUFX", "MMFX"]  #No course is selected, so no filter is applied
        else:
            for c in selCourses: selCourseArr.append(c.text())
        print("Selected Courses: " + str(selCourseArr))
        self.userListTV.filterbyCourse(selCourseArr)
        print(str(self.prepDate.selectedDate().day()) + "/" + str(self.prepDate.selectedDate().month()) + "/" + str(self.prepDate.selectedDate().year()))
        print(str(self.reviewDate.selectedDate().day()) + "/" + str(self.reviewDate.selectedDate().month()) + "/" + str(self.reviewDate.selectedDate().year()))

    def firstMarkerComboSel(self, text):
        gmail = ""
        for s in staffList:
            if text == s["name"]: gmail = s["gmail"]
        self.firstMarkerEmail.setText(gmail)

    def secondMarkerComboSel(self, text):
        gmail = ""
        for s in staffList:
            if text == s["name"]: gmail = s["gmail"]
        self.secondMarkerEmail.setText(gmail)

    def buildModuleBox(self):
        #We need to build all the data into a dictionary to pass to the relevant function that will build the google sheet
        moduleData = {}
        markingUserList = self.userListTV.getUserList()
        markingUserList = sorted(markingUserList, key=lambda k: k['surname']) #Sort the list into alphabetical by surname
        moduleData["students"] = markingUserList
        moduleData["code"] = self.userListTV.getModuleCode()
        moduleData["year"] = self.yearCombo.currentText()
        moduleData["prepDate"] = str(self.prepDate.selectedDate().day()) + "/" + str(self.prepDate.selectedDate().month()) + "/" + str(self.prepDate.selectedDate().year())
        moduleData["reviewDate"] = str(self.reviewDate.selectedDate().day()) + "/" + str(self.reviewDate.selectedDate().month()) + "/" + str(self.reviewDate.selectedDate().year())
        moduleData["firstMarker"] = self.firstMarkerCombo.currentText()
        moduleData["secondMarker"] = self.secondMarkerCombo.currentText()
        pprint.pprint(moduleData)
        self.assignmentDetails = googleSheet.buildMarkSheet(moduleData)
        #Now that we have the assessment details, we can add the items to the combo box
        self.assignmentCombo.removeItem(0)
        self.assignmentCombo.addItem("Specify assignment...")
        for i in range(0, self.assignmentDetails["number"]):
            self.assignmentCombo.addItem(self.assignmentDetails["titles"][i])
        #Now activate the rest of the UI
        self.markingFolderButton.setEnabled(True)


    def buildModuleBoxFolders(self):
    	markingFolder = self.userListTV.getMarkingDirectory()
    	modulefolderName = self.userListTV.getModuleCode() + "_" + self.userListTV.getModuleTitle()
    	os.mkdir(markingFolder + "//_ModuleBox")
    	os.mkdir(markingFolder + "//_ModuleBox" + "//" +  modulefolderName)
    	os.mkdir(markingFolder + "//_ModuleBox" + "//" +  modulefolderName + "//" + "1.0 Module Guide")
    	os.mkdir(markingFolder + "//_ModuleBox" + "//" +  modulefolderName + "//" + "2.0 Assessments & Assessment Moderation")
    	os.mkdir(markingFolder + "//_ModuleBox" + "//" +  modulefolderName + "//" + "3.0 Sample of Work")
    	os.mkdir(markingFolder + "//_ModuleBox" + "//" +  modulefolderName + "//" + "4.0 Module Evaluation")


    def createMarkingFolders(self):
    	self.buildModuleBoxFolders() #Build the standard modulebox Template
        folderStudents = self.userListTV.getUserList()
        markingFolder = self.userListTV.getMarkingDirectory()
        self.studentFolders = []
        for s in folderStudents:
			studentFolderDetails = {}
			folderName = s['surname'] + "_" + s['forename'] + "_ID_" + s['id']
			studentFolderDetails['id'] = s['id']
			studentFolderDetails['folder'] = (markingFolder + "//" + folderName)
			self.studentFolders.append(studentFolderDetails)
			os.mkdir(markingFolder + "//" + folderName)
			for i in range(0, self.assignmentDetails["number"]):
			    os.mkdir(markingFolder + "//" + folderName + "//" + self.assignmentDetails['titles'][i])
			self.sortAssignmentsLabel.setEnabled(True)
			self.assignmentCombo.setEnabled(True)
			self.sortAssignmentsButton.setEnabled(True)

    def sortAssignmentFiles(self):
    	assignmentFolder = self.assignmentCombo.currentText()
    	markingFolder = self.userListTV.getMarkingDirectory()
    	if (assignmentFolder == "No Assignment info") or ((assignmentFolder == "Specify assignment...")): 
    		print "Error - No Assignment Names Listed"
    		return 0
    	else:
    		dirFiles = [f for f in os.listdir(markingFolder) if os.path.isfile(os.path.join(markingFolder, f))]
    		print("Directory Files: " + str(dirFiles))
    		#Now loop through all the student IDs and match up the files
    		for s in self.studentFolders:
    			for f in dirFiles:
    				if s['id'] in f:
    					# print("Found: " + s['id'] + " in " + str(f))
    					filename = os.path.split(f)  #This priduces an arra
    					print ("Split : " + str(filename))
    					print("The File: " + str(f))
    					print("The Location: " + str(s['folder'] + "//" + assignmentFolder + "//" + filename[1]))
    					os.rename((markingFolder + "//" + f), (s['folder'] + "//" + assignmentFolder + "//" + filename[1])) #Renameing is the way that windows moves files from one folder to another




#######################################Load Program#######################################################
reg = SVFX_AssetTrackerUI()
reg.show()
# view.show()
sys.exit(app.exec_())
# ~~~~~~~~~~~~~~~~~~~~~~~~~

