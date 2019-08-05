from PyQt5.QtWidgets import \
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, \
    QFileDialog, QLineEdit, QHBoxLayout, QGroupBox

app = QApplication([])  ## every PyQT app needs QApplication


class RESonatorGUI():
    ## Store the paths as class attributes?
    paths = {
        'lms': '',
        'evaluation': '',
        'metadata': ''}

    def __init__(self) -> None:
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

        window.setLayout(layout_selections)
        window.setGeometry(self.left, self.top, self.width, self.height)
        window.show()
        app.exec_()  # Run the program
        # super().__init__()

    ## make_filepicker_section
    ## Creates a line representing file inputs
    def make_filepicker_section(self, data_name):
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
        new_path_dict = {file_name: name[0]}  # make new pair
        new_path_str = name[0]
        self.paths.update(new_path_dict)  # update pair to the global dict
        print('Selected ' + file_name)
        self.update_paths(updated_text=new_path_str)

    # This will start the data processing program
    def orchestrate_xml(self):
        print('orchestrate_xml')


# Calling this function sets up the GUI and leaves it ready it for input
RESonatorGUI()
