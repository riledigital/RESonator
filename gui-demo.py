#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Currently used for figuring out the GUI for RESonator

import wx

## create a class for the app
from wx import FilePickerCtrl


class AppInterface(wx.Frame):
    ## Instantiation
    def __init__(self, *args, **kwargs):
        super(AppInterface, self).__init__(*args, **kwargs)

        self.InitUI()  # on instantiation, create the UI picker...

    def InitUI(self):
        # instruction_1 = 'Select the LMS data file:'
        # instruction_2 = 'Select the ZipGrade data file:'
        # instruction_3 = 'Select the hand-prepared metadata file:'

        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fileItem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        # menubar.Append(fileMenu, '&File')
        # self.SetMenuBar(menubar)

        # self.Bind(wx.EVT_MENU, self.OnQuit, fileItem)
        # setting up event handling

        self.SetSize((600, 450))
        panel1 = wx.Panel(self)  # set up a panel
        vbox = wx.BoxSizer(wx.VERTICAL)  # BoxSizer
        top_row = wx.BoxSizer(wx.HORIZONTAL)
        panel1.SetSizer(vbox)  # set up a sizer for layout...

        font = wx.Font(13, wx.DEFAULT, wx.NORMAL, wx.DEFAULT)

        # instance the widgets
        in_picker_1: FilePickerCtrl = wx.FilePickerCtrl()
        top_row.Add(in_picker_1)
        st1 = wx.StaticText(panel1, label=instruction_1, style=wx.ALIGN_LEFT)
        st2 = wx.StaticText(panel1, label=instruction_2, style=wx.ALIGN_LEFT)
        st3 = wx.StaticText(panel1, label=instruction_3, style=wx.ALIGN_LEFT)

        # button_choose_1 \
        #     = wx.Button(
        #     panel1,
        #     label='Choose file')
        # button_choose_1.Bind(wx.EVT_BUTTON, self.FilePick1)
        #
        # st1.SetFont(font)

        # Add the widgets to boxsizer>panel>Frame
        vbox.Add(st1, flag=wx.ALL, border=15)
        vbox.Add(top_row)
        vbox.Add(st2, flag=wx.ALL, border=15)
        vbox.Add(st3, flag=wx.ALL, border=15)
        # oddly enough, adding the button picker crashes
        # the app with a segfault
        vbox.Add(in_picker_1, flag=wx.LEFT)

        self.SetTitle('RESonator')
        self.Centre()

    def FilePick1(self, one):
        print(self)
        print(one)
        print('Ran file picker')

    def OnQuit(self, e):  # event for closing app
        self.Close()


def main():
    app = wx.App()  # instantiate the gui + logic
    ex = AppInterface(None)  # create an instance of the app
    ex.Show()  # draw it to the screen
    app.MainLoop()  # start the event loop


if __name__ == '__main__':  # Check if the module name is the same
    main()
