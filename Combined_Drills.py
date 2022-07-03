# Modules

from tkinter import *
import tkinter as tk
from tkinter import filedialog
import os
import glob
import time
import sqlite3

# Main Loop

class ParentWindow(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

# Create database and add table

        conn = sqlite3.connect('myDatabase.db')

        with conn:
            cur = conn.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS tbl_txtFiles \
            (ID INTEGER PRIMARY KEY AUTOINCREMENT, col_txtFile TEXT, col_dateModified TEXT)")
            conn.commit()
        conn.close()

# Main window size & config

        self.master = master
        self.master.minsize(500, 200)
        self.master.maxsize(500, 200)
        self.master.title("Folder Selector")
        self.master.configure(bg="lightgray")

# File explorer buttons & entry fields
        
        self.btn_FileExplorer_1 = tk.Button(self.master, command=self.getDir_1, width=12, bg="#e5e5e5", text="From:")
        self.btn_FileExplorer_1.grid(row=1, column=0, padx=(15,0), pady=(35,0), sticky=W)

        self.txtBox_1 = tk.Text(self.master, height=1, width = 40)
        self.txtBox_1.grid(row=1, column=1, padx=(15,0), pady=(35,0), sticky=W)

        self.btn_FileExplorer_2 = tk.Button(self.master, command=self.getDir_2, width=12, bg="#e5e5e5", text="To:")
        self.btn_FileExplorer_2.grid(row=2, column=0, padx=(15,0), pady=(15,0), sticky=W)

        self.txtBox_2 = tk.Text(self.master, height=1, width = 40)
        self.txtBox_2.grid(row=2, column=1, padx=(15,0), pady=(15,0), sticky=W)

# File search button

        self.btn_Submit = tk.Button(self.master, command=self.scanDirectory, height=2, width=12, bg="#e5e5e5", text="Submit")
        self.btn_Submit.grid(row=3, column=0, padx=(15,0), pady=(25,0), sticky=W)
        
# Retrieve file path

    def getDir_1(self):
        self.Directory_1 = filedialog.askdirectory(initialdir = "c:\\", title='Please select a directory')
        self.txtBox_1.insert('1.0', self.Directory_1)

    def getDir_2(self):
        self.Directory_2 = filedialog.askdirectory(initialdir = "c:\\", title='Please select a directory')
        self.txtBox_2.insert('1.0', self.Directory_2)

# Gather all .txt files in list, convert individual list elements to a string path

    def scanDirectory(self):
        conn = sqlite3.connect('myDatabase.db')
        
        os.chdir(self.Directory_1)
        txtFiles = glob.glob('*.txt')

# Combine strings to form fromPath and toPath
# os.rename fromPath -> toPath
# get the Modification time of each text file
# Insert text file name and modification time into database
        
        i = 0
        while i < len(txtFiles):
            txtFileString = "".join(txtFiles[i])
            
            fromPath = self.Directory_1 + "/" + txtFileString

            toPath = self.Directory_2 + "/" + txtFileString

            os.rename(fromPath, toPath)

            modTimesinceEpoc = os.path.getmtime(toPath)
            modificationTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modTimesinceEpoc))
            
            cur = conn.cursor()
            cur.execute("INSERT INTO tbl_txtFiles(col_txtFile, col_dateModified) VALUES (?, ?)", (txtFileString, modificationTime))
            conn.commit()

            print(txtFileString + " was last modified on " + modificationTime)
                
            i += 1

        conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    App = ParentWindow(root)
    root.mainloop()
