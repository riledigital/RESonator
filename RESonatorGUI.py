import sys
import os
import pandas as pd
import DataPrep
import XMLGenerator
import logging
import datetime
from pathlib import Path

# from PyQt5.QtCore import *
# from PyQt5.QtGui import *

from PyQt5.QtWidgets import \
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, \
    QFileDialog, QLineEdit, QHBoxLayout, QGroupBox, QComboBox, \
    QMessageBox

# set the version number...
# __version__: str = '0.1'

# Setup file paths for saving and loading files...
path = Path()
home = Path.home()

path_cwd:Path = os.getcwd()
print('current cwd is + ' + str(path_cwd))

# Setup logging output
logging_output = str(datetime.datetime.today().strftime('%m%d%Y') + '.log')
logging_path = os.path.join(home, logging_output)
if not os.path.exists(logging_path):
    open(logging_path, 'w')

# logging_output: str = str(datetime.datetime.strftime("%Y-%m-%d_%H-%M-%S") +
#                           '.log'

logging.basicConfig(
    filename=os.path.join(home, logging_output),
    level=logging.DEBUG)

# logging.info('RESonator version: ' + str(__version__))
logging.info('New session started on ' + str(datetime.datetime.now()))
app = QApplication([])  ## every PyQT app needs QApplication
app.setQuitOnLastWindowClosed(True)

class RESonatorGUI:
    """
    RESonatorGUI spawns the GUI for the app
    and handles main logic, delegating the
    specifics to XMLGenerator and to DataPrep.
    """
    ## Setup class variables for files to be output
    # We can initialize these as None's but they
    # will need to be changed later...
    data_lms = None
    data_eval = None
    data_meta = None
    lesson_list = None  # Lesson list for populating lesson list
    layout_selections = QComboBox()
    current_lesson = None

    ## Store the paths and the as class attributes in a dict
    paths = {
        'lms': '',
        'evaluation': '',
        'metadata': ''}

    window = QWidget()  # creates a window

    def __init__(self) -> None:
        """
        init function doesn't need to take inputs yet
        """
        # setup a vertical layout for the window
        # of which we add other horizontal layouts to...
        window = QWidget()  # creates a window
        self.layout_selections = QVBoxLayout()
        window.setWindowTitle("RESonator Build")

        # Create variables adjusting dimensions of a window
        self.left = int(10)
        self.top = int(10)
        self.width = int(600)
        self.height = int(0)

        # Write the directions
        self.layout_selections.addWidget(QLabel('SELECT FILES'))
        self.layout_selections.addWidget(
            QLabel('Select input files to process:'))

        # Add widgets to the GUI
        self.layout_selections.addWidget(
            self.make_filepicker_section(data_name='lms'))

        self.lessons = QComboBox()
        self.lessons.currentIndexChanged.connect(
            lambda: self.change_lesson())
        print('QComboBox currentData:' + self.lessons.currentText())
        self.layout_selections.addWidget(self.lessons)

        self.layout_selections.addWidget(
            self.make_filepicker_section(data_name='evaluation'))
        self.layout_selections.addWidget(
            self.make_filepicker_section(data_name='metadata'))
        self.layout_selections.addWidget(
            self.make_section_process())
        window.setLayout(self.layout_selections)
        window.setGeometry(self.left, self.top, self.width, self.height)
        window.show()
        app.exec_()
        sys.exit(app.exec_())

    def change_lesson(self):
        """
        Takes in a current lesson QComboBox and changes the global current_lesson variable
        """
        self.current_lesson = self.lessons.currentText()
        logging.info('Changed lesson:' + self.current_lesson)

    def make_filepicker_section(self, data_name):
        '''
        make_filepicker_section
        Creates a line representing file inputs
        :param data_name: name of data field to create filepicker for
        :return:
        '''
        self.horizontalGroupBox = \
            QGroupBox('Select input file for ' + str(data_name))
        lt = QHBoxLayout()  # creates a layout
        ## Start edit section
        # choose_path_1_edit = QLineEdit()
        # lt.addWidget(self.choose_path_1_edit)
        data_label = ''

        # Update the data_label
        # if self.paths[data_name] != '':
        #     data_label = self.paths[data_name]
        label_pathname = QLabel(self.paths[data_name])
        lt.addWidget(label_pathname)

        ## Choose Button
        layout_files_1 = QGroupBox('Choose the file below')
        choose_1 = QPushButton('Choose')
        lt.addWidget(choose_1)
        choose_1.clicked.connect(
            lambda:
            self.open_file(
                file_name=data_name, label_to_modify=label_pathname))

        self.horizontalGroupBox.setLayout(lt)
        return self.horizontalGroupBox
        # layout_files_1
        #     choose_1

    def make_section_process(self):
        horizontal_group_box = QGroupBox('Generate XML')
        layout = QHBoxLayout()  # creates a layout

        ## Choose Button
        layout_files_1 = QGroupBox('Generate XML file')
        process = QPushButton('Generate XML')
        layout.addWidget(process)
        process.clicked.connect(self.orchestrate_xml)
        horizontal_group_box.setLayout(layout)
        return horizontal_group_box  # return the box

    # Methods that handle events
    def update_paths(self, updated_text):
        """
        Updates the GUI to show the correct file path in the GUI
        :return nothing
        """
        # self.paths.update( 'updated_text');
        # self.choose_path_1_edit.setText(updated_text)
        print("Updated paths in GUI")

    def open_file(self, file_name, label_to_modify):
        try:
            name = QFileDialog.getOpenFileName(
                caption='Select the .CSV file for' + file_name,
                filter="csv(*.csv)")
        except:
            QMessageBox.about(self.window, "File error", "Error opening file.")

        new_path_str = name[0]
        new_path_dict = {file_name: str(new_path_str)}  # make new pair
        self.paths.update(new_path_dict)  # update pair to the global dict
        print('Selected ' + file_name)
        label_to_modify.setText(new_path_str)

        # If its the LMS file, read it immediately
        # and report a list of lessons
        if file_name == "lms":
            try:
                logging.info('Reading in lms file to get list of lessons')
                temp_lms = pd.read_csv(self.paths.get('lms'), encoding='latin1')
                # Make a list of all the lessons?
                self.lesson_list = temp_lms['Lesson'].unique().tolist()
                logging.info('List of Lessons: ' + str(self.lesson_list))
                # self.lessons.addItems(self.lesson_list)
                for item in self.lesson_list:
                    logging.info('adding item: ' + str(str(item)))
                    self.lessons.addItem(str(item))
            except Exception as e:
                Exception('ERROR: Error occurred while reading list of '
                          'lessons: ' + str(e))
        # self.update_paths(updated_text=new_path_str)

    def orchestrate_xml(self):
        '''
        Event that fires when clicking "Process XML"
        :return: none
        '''
        logging.info('Started orchestrate XML...')

        try:
            if self.current_lesson == 'DEFAULT_INITIALIZED':
                QMessageBox.about(
                    self.window,
                    "No lesson chosen to filter by",
                    "Please choose a lesson to filter by.")
                raise Exception("No lesson defined!")

            prep = DataPrep.DataPrep(
                pd.read_csv(self.paths.get('lms'),
                            encoding='latin1'),
                pd.read_csv(self.paths.get('evaluation'),
                            encoding='latin1'),
                self.paths.get('metadata'),
                self.current_lesson)
            a_final_lms = prep.prep_data_lms()
            a_final_eval = prep.prep_data_eval()
            a_final_meta = prep.prep_data_meta()
            generator = \
                XMLGenerator.XMLGenerator(
                    a_final_lms, a_final_eval, a_final_meta)
            logging.info('Firing event generate_xml() from GUI...')
            logging.info('TEST: List of Lessons:' + str(
                prep.get_lessons_list()))
            logging.info('Starting XML compilation process')
            try:  # Add try/except every time a major thing can error
                generator.generate_xml()
            except Exception as e:
                logging.error("Error: Couldn't generate XML. " + str(e))
                QMessageBox.about(
                    self.window, "Error", "Couldn't generate XML. " +
                                           str(e))
            # Successfully compiled XML
            QMessageBox.about(
                self.window, "Success", "Compiled XML as: " +
                                        str(generator.string_output_file_path))
        except Exception as e:
            logging.error('Error: ' + str(e))
            QMessageBox.about(
                self.window,
                "Error",
                "Error generating output XML. "
                "Exception: " + str(e))

        print('Finished orchestrate_xml')


#app.exec_()  # Run the program
# Calling this function sets up the GUI and leaves it ready it for input

## Check if running in a bundle or from source
# https://pyinstaller.readthedocs.io/en/stable/runtime-information.html#run-time-information
try:
    if getattr(sys, 'frozen') and hasattr(sys, '_MEIPASS'):
        print('running in a PyInstaller bundle')
    else:
        print('running in a normal Python process')
        print('_MEIPASS is ' + str(sys._MEIPASS))
except Exception as e:
    print('Exception: ' + str(e))

RESonatorGUI()
#ret = app.exec_()
#sys.exit(ret)
## TODO test if exit code works here as well
