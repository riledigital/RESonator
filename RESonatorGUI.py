import pandas as pd
import DataPrep as dp
import XMLGenerator as xmlgen

from PyQt5.QtWidgets import \
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, \
    QFileDialog, QLineEdit, QHBoxLayout, QGroupBox, QComboBox

app = QApplication([])  ## every PyQT app needs QApplication


class RESonatorGUI():
    ## Setup class variables for files to be output
    data_lms = None
    data_eval = None
    data_meta = None
    current_lesson = None

    ## Store the paths and the as class attributes?
    paths = {
        'lms': './data_in2/2019-07-18-12-32-33_d43o0sted3.csv',
        'evaluation': './data_in2/quiz-Eval-full.csv',
        'metadata': './data_in2/meta-template.csv'}

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
        if self.paths[data_name] != '':
            data_label = self.paths[data_name]
        lt.addWidget(QLabel('File selected: ' + data_label))

        ## Choose Button
        layout_files_1 = QGroupBox('Choose the file below')
        choose_1 = QPushButton('Choose')
        lt.addWidget(choose_1)
        choose_1.clicked.connect(lambda:
                                 self.open_file(
                                     file_name=data_name))

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
        process.clicked.connect(
            lambda: self.orchestrate_xml())

        horizontalGroupBox.setLayout(layout)
        return horizontalGroupBox  # return the box

    # Methods that handle events
    def update_paths(self, updated_text):
        # self.choose_path_1_edit.setText(updated_text)
        print("Updated paths in GUI")

    def open_file(self, file_name):
        name = QFileDialog.getOpenFileName(
            caption='Select the .CSV file for' + file_name,
            filter="csv(*.csv)")
        new_path_str = name[0]
        new_path_dict = {file_name: str(new_path_str)}  # make new pair
        self.paths.update(new_path_dict)  # update pair to the global dict
        print('Selected ' + file_name)
        self.update_paths(updated_text=new_path_str)

    def orchestrate_xml(self):
        '''
        Event that fires when clicking "Process XML"
        :return: none
        '''
        print('Started orchestrate XML...')
        # TODO: set these DF's using the class variable list
        # retrieve them also
        # lms_df = pd.read_csv(lms_path, encoding='latin1')
        # eval_df = pd.read_csv(path_eval, encoding='latin1')
        # meta_df = pd.read_csv(path_meta, encoding='latin1')
        # # TODO: Make a GUI option for this lesson string
        # lesson_str = 'Florida: MGT 462 '
        #

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
        generator.generate_xml()
        print('Finished orchestrate_xml')


# Calling this function sets up the GUI and leaves it ready it for input
RESonatorGUI()
