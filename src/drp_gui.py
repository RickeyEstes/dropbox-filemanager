#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox, ttk

from client import DropboxClient


class DropboxUI(DropboxClient):

    def __init__(self, master):
        self.master = master
        self.font = "ArialBold"
        self.home_dir = os.getenv('HOME')
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
        # self.master.winfo_width())  #current window width
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
        menubar = tk.Menu(self.master, font=(self.font, 12))
        self.master.config(menu=menubar)

        filemenu = tk.Menu(menubar, font=(self.font, 12), tearoff=0)
        filemenu.add_command(label='Upload Files', command=self.openFiles)
        filemenu.add_command(label='Load Files', command=self.loadFiles)
        filemenu.add_separator()
        filemenu.add_command(label='Quit', command=self.quit)
        menubar.add_cascade(label='File', menu=filemenu)

        editmenu = tk.Menu(menubar, font=(self.font, 12), tearoff=0)
        editmenu.add_command(label='Settings', command='')
        menubar.add_cascade(label='Edit', menu=editmenu)

    def btnUpload(self):
        '''Hnadle upload button'''
        btn = tk.Button(self.frame, text='Upload files', width=10,
                        height=2, relief='raised', bd=2,
                        font=(self.font, 12), command=self.openFiles)
        btn.place(relx=0.5, rely=0.3, anchor='center')

    def btnLoad(self):
        '''Handle load button'''
        btn = tk.Button(self.frame, text='Load files', width=10,
                        height=2, relief='raised', bd=2,
                        font=(self.font, 12), command=self.loadFiles)
        btn.place(relx=0.5, rely=0.45, anchor='center')

    def btnQuit(self):
        '''Handle load button'''
        btn = tk.Button(self.frame, text='Quit', width=6,
                        height=2, relief='raised', bd=2,
                        font=(self.font, 10), fg='red', command=self.quit)
        btn.place(relx=0.92, rely=0.93, anchor='center')

    def openFiles(self):
        '''Choosing files for uploading'''
        filenames = filedialog.askopenfilenames(
                                                initialdir=f'{self.home_dir}',
                                                multiple=True,
                                                title='Select files',
                                                filetypes=[
                                                    ('all files', ['*.*'])]
                                                )
        # Connect to the dropbbox account
        if filenames:
            self.connect()
        # Upload files to the  dropbox acount
        self.upload(filenames)

    def loadFiles(self):
        '''Loading files from dropbox accound'''
        # Connect to the dropbbox account
        self.new_top_window = tk.Toplevel()
        self.new_top_window.iconphoto(False, self.img)
        self.connect()
        # Get the files from the dropbox account
        metadata = self.list_files()
        # Creating a tree view table
        self.tree = ttk.Treeview(self.new_top_window,
                                 columns=('Date', 'Size', 'Type'))
        self.tree.config(height=20)
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
        self.tree.tag_configure('T', font=(self.font, 12))
        self.tree.pack(fill='both', expand=True)

    def wDestroy(self, widget):
        '''Widget distroyer'''
        widget.destroy()

    def msgBoxInfo(self, title, message):
        '''Message box'''
        messagebox.showinfo(title, message)

    def quit(self):
        '''Destroy master window'''
        self.master.destroy()


def main():

    root = tk.Tk()
    root.resizable(0, 0)
    root.bind("<Escape>", exit)
    app = DropboxUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()