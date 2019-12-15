import os

import tkinter as tk
from tkinter import filedialog, ttk

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

        # Buttons intiliazations
        self.btnUpload()
        self.btnLoad()

    def centerWindow(self):
        # self.master.winfo_width())  #current window width
        # frame.winfo_height()  current window height
        self.w = 700
        self.h = 500
        sw = self.master.winfo_screenwidth()    # screen width size
        sh = self.master.winfo_screenheight()   # screen height size
        x = (sw - self.w) / 2
        y = (sh - self.h) / 2
        self.master.geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))

    def btnUpload(self):
        btn = tk.Button(self.frame, text='Upload files', width=10,
                        height=2, relief='raised', bd=2,
                        font=(self.font, 12), command=self.selectFiles)
        btn.place(relx=0.5, rely=0.3, anchor='center')

    def btnLoad(self):
        btn = tk.Button(self.frame, text='Load files', width=10,
                        height=2, relief='raised', bd=2,
                        font=(self.font, 12), command=self.loadFiles)
        btn.place(relx=0.5, rely=0.45, anchor='center')

    def selectFiles(self):
        filenames = filedialog.askopenfilenames(
                                                initialdir='/home/dslackw/     Downloads/',
                                                multiple=True,
                                                title='Select files',
                                                filetypes=[
                                                    ('all files', ['*.*'])]
                                                )
        # Connect to the dropbbox account
        self.connect()
        # Upload files to the  dropbox acount
        self.upload(filenames)

    def loadFiles(self):
        # Connect to the dropbbox account
        self.connect()
        self.new_window = tk.Toplevel()
        self.new_window.iconphoto(False, self.img)

        # Get the files from the dropbox account
        metadata = self.list_files()
        # Creating a tree view table
        self.tree = ttk.Treeview(self.new_window,
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
        self.tree.column('#2' , stretch='yes')

        folders, current_folder = '', ''
        for item in metadata:
            # Spliting the metadata by category
            folder = os.path.dirname(item.split(',')[0])
            file = item.split(',')[1]
            date = item.split(',')[2]
            size = item.split(',')[3]
            ftype = item.split(',')[1].split('.')[-1]

            if folder == '/':
                self.tree.insert('', 'end', text=file,
                                 values=(date, size, ftype + ' file'),
                                 tags='T')
                continue

            # Checking if the folder change name
            if folder != current_folder:
                folders = self.tree.insert('', 'end', text=folder, tags='T')
                current_folder = folder

            # Store data into the table
            self.tree.insert(folders, 'end', text=file,
                             values=(date, size, ftype + ' file'), tags='T')
        self.tree.tag_configure('T', font=(self.font, 12))
        self.tree.pack(fill='both', expand=True)


def main():

    root = tk.Tk()
    root.resizable(0, 0)
    root.bind("<Escape>", exit)
    app = DropboxUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()