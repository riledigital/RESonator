import pandas as pd
import DataPrep as dp
import XMLGenerator as xmlgen
import logging
import datetime
from pathlib import Path

outstr = datetime.datetime.today().strftime(
    '%m%d%Y') + '.log'
path = Path()
logging.basicConfig(
    # path=Path.cwd() / 'data_out' / outstr,
    filename='./data_out' + datetime.datetime.today().strftime('%m%d%Y') +
             '.log',
    level=logging.DEBUG)

from PyQt5.QtWidgets import \
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, \
    QFileDialog, QLineEdit, QHBoxLayout, QGroupBox, QComboBox, \
    QMessageBox

app = QApplication([])  ## every PyQT app needs QApplication


class RESonatorGUI:
    ## Setup class variables for files to be output
    data_lms = None
    data_eval = None
    data_meta = None
    current_lesson = None

    ## Store the paths and the as class attributes?
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
        layout_selections = QVBoxLayout()
        window.setWindowTitle("RESonator Build")

        # Create variables adjusting dimensions of a window
        self.left = 10
        self.top = 10
        self.width = 600
        self.height = 0

        # Write the directions
        layout_selections.addWidget(QLabel('SELECT FILES'))
        layout_selections.addWidget(QLabel('Select input files to process:'))

        # Add widgets to the GUI
        layout_selections.addWidget(
            self.make_filepicker_section(data_name='lms'))
        layout_selections.addWidget(
            self.make_filepicker_section(data_name='evaluation'))
        layout_selections.addWidget(
            self.make_filepicker_section(data_name='metadata'))
        layout_selections.addWidget(
            self.make_section_process())

        # lessons = QComboBox()
        # TODO: Finish writing this combobox
        # lessons.addItem('Test')
        # lessons.addItem('Test2')
        # lessons.currentIndexChanged.connect(self.change_lesson())
        # print('QComboBox currentData:' + lessons.currentData())
        # layout_selections.addWidget(lessons)

        # def change_lesson(self):
        #     '''
        #     this function is invoked when the picker changes lessons
        #     :return:
        #     '''
        #     self.current_lesson = 'TODO TESTER'
        #     print('Changing lesson,')
        #     print('QComboBox currentData:' + lessons.currentData())
        #     # TODO Refresh filter string to pass into data-prep...
        #     print('Current lesson is:')
        #     print('New lesson is:')

        window.setLayout(layout_selections)
        window.setGeometry(self.left, self.top, self.width, self.height)
        window.show()
        app.exec_()  # Run the program
        # super().__init__()

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
        horizontalGroupBox = \
            QGroupBox('Generate XML')
        layout = QHBoxLayout()  # creates a layout

        ## Choose Button
        layout_files_1 = QGroupBox('Generate XML file')
        process = QPushButton('Generate XML')
        layout.addWidget(process)
        process.clicked.connect(self.orchestrate_xml)

        horizontalGroupBox.setLayout(layout)
        return horizontalGroupBox  # return the box

    # Methods that handle events
    def update_paths(self, updated_text):
        """
        Updates the GUI to show the correct file path in the GUI
        :return nothing
        """
        ## TODO: Finish GUI part for updating file path...
        # self.paths.update( 'updated_text');
        # self.choose_path_1_edit.setText(updated_text)
        print("Updated paths in GUI")

    def open_file(self, file_name, label_to_modify):
        name = QFileDialog.getOpenFileName(
            caption='Select the .CSV file for' + file_name,
            filter="csv(*.csv)")
        new_path_str = name[0]
        new_path_dict = {file_name: str(new_path_str)}  # make new pair
        self.paths.update(new_path_dict)  # update pair to the global dict
        print('Selected ' + file_name)
        label_to_modify.setText(new_path_str)
        # self.update_paths(updated_text=new_path_str)

    def orchestrate_xml(self):
        '''
        Event that fires when clicking "Process XML"
        :return: none
        '''

        print('Started orchestrate XML...')

        # # TODO: Make a GUI option for this lesson string
        # lesson_str = 'Florida: MGT 462 '
        try:
            prep = dp.DataPrep(
                pd.read_csv(self.paths.get('lms'),
                            encoding='latin1'),
                pd.read_csv(self.paths.get('evaluation'),
                            encoding='latin1'),
                pd.read_csv(self.paths.get('metadata'),
                            encoding='latin1'))
            a_final_lms = prep.prep_data_lms()
            a_final_eval = prep.prep_data_eval()
            a_final_meta = prep.prep_data_meta()
            generator = xmlgen.XMLGenerator(a_final_lms, a_final_eval,
                                            a_final_meta)
            logging.info('Firing event generate_xml() from GUI...')
            logging.info('Starting XML compilation process')
            generator.generate_xml()
            QMessageBox.about(self.window, "Success", "Compiled XML as: " +
                              str(generator.string_output_filename))
        except:
            QMessageBox.about(self.window, "Error", "An error occurred.")

        print('Finished orchestrate_xml')


# Calling this function sets up the GUI and leaves it ready it for input
RESonatorGUI()
