#lab3front.py - Bhaasita

import tkinter as tk
from tkinter import messagebox
import sqlite3


'''main window class'''

class MainWin(tk.Tk):

    #constructor for main window
    def __init__(self):
        super().__init__()
        self.geometry("+100+100")
        self.entryText = tk.StringVar()
        self.L = tk.Label(self,text="Enter first letter of country name: ")  # create label for prompt
        self.L.grid()
        self.E = tk.Entry(self, textvariable=self.entryText)
        self.E.grid(row=0, column=1) # create entry for user input
        self.E.bind("<Return>", self.fct)
        self.LBL = tk.Label(self, text="Select a country name: ").grid(row=1, column=0, sticky ="w")
        self.LB = tk.Listbox(self, height=10, width=50, selectmode="extended")
        self.LB.grid(row=2, column=0, columnspan=2)
        self.LB.bind("<<ListboxSelect>>", self.displayNames)

    def fct(self, event):  # callback function
        self.inputText = self.entryText.get()
        self.inputText = self.inputText.strip()
        self.countryList = []
        if self.inputText.__len__() == 1:
            if self.inputText.isalpha():
                conn = sqlite3.connect('regionalDataDB.sqlite')
                cur = conn.cursor()
                sqlQuery= "SELECT countryName FROM CommonNames WHERE countryName LIKE " + "\'" +self.inputText +"%\' ORDER BY countryName ASC"
                cur.execute(sqlQuery)
                self.rows = cur.fetchall()
                if(self.rows != []):
                    if self.LB.size() != 0:
                        self.LB.delete(0, tk.END)

                    for name in self.rows:
                        self.LB.insert(tk.END, name[0])
                    conn.close()
                else:
                    errorMessage = "No country in database starting with letter " + self.inputText
                    messagebox.showerror("Error", errorMessage)
            else:
                messagebox.showerror("Error", "Enter a letter only")
        else:
            messagebox.showerror("Error", "Enter only one letter")


    def displayNames(self, event):  # callback function
        items = self.LB.curselection()
        for x in items:
            keyValue = self.rows[x][0]
        top = DialogWin(self, keyValue)


'''Dialog window class'''
class DialogWin(tk.Toplevel):

    # constructor for display window
    def __init__(self, master, keyValue):
        super().__init__(master)
        self.geometry("+100+100")
        self.keyValue = keyValue
        self.focus_set()
        self.grab_set()
        self.S = tk.Scrollbar(master)
        self.LB = tk.Listbox(self, height=10, width=50, selectmode="extended", yscrollcommand=self.S.set)
        self.LB.grid(row=1, column=0, columnspan=2)
        self.LB.bind("<Enter>", self.displayCommonNames)
        self.S.config(command=self.LB.yview)

    def displayCommonNames(self, event): # callback function
        self.listBoxLabel = tk.Label(self, text="Most popular names for "+self.keyValue).grid(row=0, column=0,sticky ="w")
        conn = sqlite3.connect('regionalDataDB.sqlite')
        cur = conn.cursor()
        sqlQuery = "SELECT * FROM CommonNames WHERE countryName is "+"\"" +self.keyValue+"\""
        cur.execute(sqlQuery)
        self.row = cur.fetchone()
        tups = self.row[1:]
        for val in range(len(tups)):
            self.LB.insert(0, tups[val])
        conn.close()


app = MainWin()
app.mainloop()
