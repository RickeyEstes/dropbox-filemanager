#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import json
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox, ttk

from client import DropboxClient


class DropboxUI(DropboxClient):

    def __init__(self, master):
        # Load configurations
        self.readConfigs()
        self.master = master
        # self.font = ('',)
        # self.user_path = ''
        # self.js = {}
        self.initUI()

    def initUI(self):
        '''Create the UI, labels, window, buttons, frames'''
        self.fw = 680   # Width of frame
        self.fh = 480   # Height of the frame
        self.master.title("A dropbox File Manager")
        self.img = tk.PhotoImage(file='../icon.png')

        # Setting icon of master window
        self.master.iconphoto(False, self.img)

        self.frame = tk.Frame(self.master, width=self.fw,
                              height=self.fh, relief='raised', bg='')
        self.frame.place(x=10, y=10)
        self.style = ttk.Style(self.frame)
        self.style.configure('Treeview')

        # Centralize window
        self.centerWindow()
        self.dropboxLogo()
        self.menuBar()

        # Buttons intiliazations
        self.btnUpload()
        self.btnLoad()
        self.btnQuit()

    def centerWindow(self):
        '''Centrslizing the master window'''
        # self.master.winfo_width())  current window width
        # frame.winfo_height()  current window height
        self.w = 700
        self.h = 500
        sw = self.master.winfo_screenwidth()    # screen width size
        sh = self.master.winfo_screenheight()   # screen height size
        x = (sw - self.w) / 2
        y = (sh - self.h) / 2
        self.master.geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))

    def dropboxLogo(self):
        '''Create a welcome postgreSQL logo'''
        logo = Image.open("../logo.png")
        welcome = ImageTk.PhotoImage(logo)
        welcomeLabel = tk.Label(self.frame, image=welcome)
        welcomeLabel.image = welcome
        welcomeLabel.place(relx=0.03, rely=0.8)

    def menuBar(self):
        '''Creating the menu bar'''
        menubar = tk.Menu(self.master, font=self.font)
        self.master.config(menu=menubar)

        filemenu = tk.Menu(menubar, font=self.font, tearoff=0)
        filemenu.add_command(label='Upload Files', command=self.openFiles)
        filemenu.add_command(label='Load Files', command=self.loadFiles)
        filemenu.add_separator()
        filemenu.add_command(label='Quit', command=self.quit)
        menubar.add_cascade(label='File', menu=filemenu)

        editmenu = tk.Menu(menubar, font=self.font, tearoff=0)
        editmenu.add_command(label='Settings', command=self.settings)
        menubar.add_cascade(label='Edit', menu=editmenu)

        helpmenu = tk.Menu(menubar, font=self.font, tearoff=0)
        helpmenu.add_command(label='License', command='')
        helpmenu.add_command(label='About', command='')
        menubar.add_cascade(label='Help', menu=helpmenu)

    def btnUpload(self):
        '''Hnadle upload button'''
        btn = tk.Button(self.frame, text='Upload files', width=10,
                        height=2, relief='raised', bd=2,
                        font=self.font, command=self.openFiles)
        btn.place(relx=0.5, rely=0.3, anchor='center')

    def btnLoad(self):
        '''Handle load button'''
        btn = tk.Button(self.frame, text='Load files', width=10,
                        height=2, relief='raised', bd=2,
                        font=self.font, command=self.loadFiles)
        btn.place(relx=0.5, rely=0.45, anchor='center')

    def btnQuit(self):
        '''Handle load button'''
        btn = tk.Button(self.frame, text='Quit', width=6,
                        height=1, relief='raised', bd=2,
                        font=self.font, fg='white', bg='grey',
                        command=self.quit)
        btn.place(relx=0.92, rely=0.93, anchor='center')

    def openFiles(self):
        '''Choosing files for uploading'''
        filenames = filedialog.askopenfilenames(
                                                initialdir=f'{self.user_path}',
                                                multiple=True,
                                                title='Select files',
                                                filetypes=[
                                                    ('all files', ['*.*'])]
                                                )
        if filenames:
            # Connect to the dropbbox account
            self.connect_to_account()
            # Upload files to the  dropbox acount
            self.upload(filenames)
            self.msgBoxInfo('Uploading files', 'Uploading finished!')

    def loadFiles(self):
        '''Loading files from dropbox accound'''
        # Connect to the dropbbox account
        self.connect_to_account()
        self.window_loadFiles = tk.Toplevel()
        self.window_loadFiles.title('Load files')
        self.window_loadFiles.iconphoto(False, self.img)

        # Get the files from the dropbox account
        metadata = self.list_files()
        # Creating a tree view table
        self.tree = ttk.Treeview(self.window_loadFiles,
                                 columns=('Date', 'Size', 'Type'))
        self.tree.configure(height=20)

        # Creating the headings
        self.tree.heading('#0', text='Name')
        self.tree.heading('#1', text='Date')
        self.tree.heading('#2', text='Size')
        self.tree.heading('#3', text='Type')

        # Creating the columns
        self.tree.column('#0', stretch='yes')
        self.tree.column('#1', stretch='yes')
        self.tree.column('#2', stretch='yes')

        folders, current_folder = '', ''
        for item in metadata:
            # Spliting the metadata by category
            folder = os.path.dirname(item.split(',')[0])
            file = item.split(',')[1]
            date = item.split(',')[2]
            size = item.split(',')[3]
            ftype = item.split(',')[1].split('.')[-1]

            # Fixed files in the root directory
            if folder == '/':
                self.tree.insert('', 'end', text=file,
                                 values=(date, size, ftype + ' file'),
                                 tags='T')
                continue

            # Checking if the folder changing name
            if folder != current_folder:
                folders = self.tree.insert('', 'end', text=folder, tags='T')
                current_folder = folder

            # Store data into the table
            self.tree.insert(folders, 'end', text=file,
                             values=(date, size, ftype + ' file'), tags='T')
        self.tree.tag_configure('T', font=self.font)
        self.tree.pack(fill='both', expand=True)

        btnRemove = tk.Button(self.window_loadFiles, text='Delete',
                              height=1, relief='raised', bd=1,
                              font=self.font, fg='red',
                              command='')
        btnRemove.place(relx=0.65, rely=0.92, anchor='center')

        btnDownload = tk.Button(self.window_loadFiles, text='Download',
                                height=1, relief='raised', bd=1,
                                font=self.font,
                                command='')
        btnDownload.place(relx=0.79, rely=0.92, anchor='center')

        btnCancel = tk.Button(self.window_loadFiles, text='Cancel',
                              height=1, relief='raised', bd=1,
                              font=self.font,
                              command=self.window_loadFiles.destroy)
        btnCancel.place(relx=0.92, rely=0.92, anchor='center')

    def settings(self):
        '''Set applications settings'''
        self.window_settings = tk.Toplevel()
        self.window_settings.resizable(0, 0)
        self.window_settings.title('Settings')
        self.window_settings.iconphoto(False, self.img)
        self.window_settings.config(width=620, height=400)

        labelAppKey = tk.Label(self.window_settings, text='APP KEY',
                               font=self.font)
        labelAppKey.place(relx=0.05, rely=0.11)

        # Enter a APP KEY
        entryAppKey = tk.Entry(self.window_settings, bd=2,
                               font=self.font, width=47)
        if self.app_key:
            entryAppKey.insert(0, self.app_key)
        entryAppKey.place(relx=0.2, rely=0.1)

        labelPath = tk.Label(self.window_settings, text='User PATH',
                             font=self.font)
        labelPath.place(relx=0.05, rely=0.21)

        # Enter the user path
        entryPath = tk.Entry(self.window_settings, bd=2,
                             font=self.font, width=30)
        if self.user_path:
            entryPath.insert(0, self.user_path)
        entryPath.place(relx=0.2, rely=0.2)

        # Label for radio button font name
        labelFonts = tk.Label(self.window_settings, text='Font',
                              font=self.font)
        labelFonts.place(relx=0.05, rely=0.4)

        # Radio buttons for font name control
        default_name = {
            'Arial': 1,
            'Tahoma': 2,
            'DejaVu Sans': 3
        }

        var1 = tk.IntVar(None, default_name[self.config['font_name']])
        radioBtn1 = tk.Radiobutton(self.window_settings, text='Arial',
                                   variable=var1, value=1, indicator=1,
                                   font=self.font,
                                   command=self.updateConfigs)
        radioBtn1.place(relx=0.2, rely=0.4)

        radioBtn2 = tk.Radiobutton(self.window_settings, text='Tahoma',
                                   variable=var1, value=2, indicator=1,
                                   font=self.font,
                                   command=self.updateConfigs)

        radioBtn2.place(relx=0.32, rely=0.4)

        radioBtn3 = tk.Radiobutton(self.window_settings, text='DejaVu Sans',
                                   variable=var1, value=3, indicator=1,
                                   font=self.font,
                                   command=self.updateConfigs)

        radioBtn3.place(relx=0.5, rely=0.4)

        # Label for radio button font size
        labelFonts = tk.Label(self.window_settings, text='Size',
                              font=self.font)
        labelFonts.place(relx=0.05, rely=0.5)

        # Radio buttons for font size control

        default_size = {
            10: 1,
            12: 2
        }

        var2 = tk.IntVar(None, default_size[self.config['font_size']])
        radioBtn4 = tk.Radiobutton(self.window_settings, text='10',
                                   variable=var2, value=1, indicator=1,
                                   font=self.font,
                                   command=self.updateConfigs)
        radioBtn4.place(relx=0.2, rely=0.5)

        radioBtn5 = tk.Radiobutton(self.window_settings, text='12',
                                   variable=var2, value=2, indicator=1,
                                   font=self.font,
                                   command=self.updateConfigs)
        radioBtn5.place(relx=0.32, rely=0.5)

        # Buttons for save settings or cancel
        btnApply = tk.Button(self.window_settings, text='Apply', width=5,
                            height=1, relief='raised', bd=2,
                            font=self.font, command=self.updateConfigs)
        btnApply.place(relx=0.75, rely=0.9, anchor='center')

        btnClose = tk.Button(self.window_settings, text='Close', width=5,
                              height=1, relief='raised', bd=2,
                              font=self.font,
                              command=self.window_settings.destroy)
        btnClose.place(relx=0.9, rely=0.9, anchor='center')

        self.entryAppKey = entryAppKey
        self.entryPath = entryPath
        self.var1 = var1
        self.var2 = var2

    def updateConfigs(self):
        '''Get values from settings and update config dictionary'''
        font_name_dict = {
            0: '',
            1: 'Arial',
            2: 'Tahoma',
            3: 'DejaVu Sans'}

        font_size_dict = {
            0: '',
            1: 10,
            2: 12
        }

        fname = font_name_dict[self.var1.get()]
        fsize = font_size_dict[self.var2.get()]
        self.app_key = self.entryAppKey.get()
        self.user_path = self.entryPath.get()

        self.config = {
            'app_key': self.app_key,
            'user_path': self.user_path,
            'font_size': fsize,
            'font_name': fname
            }
        self.saveConfigs()

    def configs(self):
        '''Default app setting'''
        self.config = {
            'app_key': '',
            'user_path': '/home',
            'font_size': 12,
            'font_name': 'Arial'
            }
        self.publicConfigs()

    def publicConfigs(self):
        '''Public the configurations'''
        self.app_key = self.config['app_key']
        self.user_path = self.config['user_path']
        self.font = (self.config['font_name'], self.config['font_size'])

    def readConfigs(self):
        '''Read the configuration file'''
        if os.path.isfile('config.json'):
            with open('config.json') as config_file:
                self.config = json.load(config_file)
            self.publicConfigs()
        else:
            self.saveConfigs()

    def saveConfigs(self):
        '''Save the configuration to a json file'''
        if not os.path.isfile('config.json'):
            self.configs()
        js = json.dumps(self.config)
        with open('config.json', 'w') as f:
            f.write(js)

    def msgBoxInfo(self, title, message):
        '''info message box'''
        messagebox.showinfo(title, message)

    def msgBoxWarning(self, title, message):
        '''Warning message box'''
        messagebox.showwarning(title, message)

    def connect_to_account(self):
        '''Checking if connected to the account by APP KEY'''
        if self.app_key:
            self.connect(self.app_key)
        else:
            self.msgBoxWarning('Warning', 'An APP KEY required to connect to your acount')

    def quit(self):
        '''Destroy master window and quit'''
        self.master.destroy()

    def test(self):
        pass

def main():

    root = tk.Tk()
    root.resizable(0, 0)
    root.bind("<Escape>", exit)
    app = DropboxUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()