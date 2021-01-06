import tkinter as tk

def fct(event):  # callback function that:
    print("Hi,", entryText.get())  # - prints Hi and user input name
    # E.delete(0, tk.END)

win = tk.Tk()
entryText = tk.StringVar()
L = tk.Label(win,text="Enter first letter of country name: ")  # create label for prompt
L.grid()
E = tk.Entry(win, textvariable=entryText)# create entry for user input
E.grid(row=0, column=1)
E.bind("<Return>", fct)


win.mainloop()
