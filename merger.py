import os, tkinter
from tkinter import Tk, ttk, filedialog, messagebox
filePart1 = ""; filePart2 = ""
mainWindow = Tk()
mainWindow.title("Genesect")
mainWindow.resizable(False, False)

def buttonCheck():
    if file1Path.get() and file2Path.get(): mergeButton.config(text = "Merge Split ISO Files", state = "normal")
    else: mergeButton.config(text = "Merge Split ISO Files", state = "disabled")

def fileSelect1():
    filePart1 = filedialog.askopenfilename(title = "Select ISO Part 1", filetypes = (("Disc Image File","*.iso"),))
    if filePart1 == "": raise Exception("No file was selected!")
    file1Path.config(state = "normal")
    file1Path.delete(0, "end"); file1Path.insert(0, filePart1)
    file1Path.config(state = "readonly"); buttonCheck()

def fileSelect2():
    filePart2 = tkinter.filedialog.askopenfilename(title = "Select ISO Part 2", filetypes = (("Disc Image File","*.iso"),))
    if filePart2 == "": raise Exception("No file was selected!")
    file2Path.config(state = "normal")
    file2Path.delete(0, "end"); file2Path.insert(0, filePart2)
    file2Path.config(state = "readonly"); buttonCheck()

def fileMergeData():
    fileProduct = filedialog.asksaveasfilename(title = "Save Merged ISO Parts", filetypes = (("Disc Image File","*.iso"),))
    if not fileProduct.endswith(".iso"): fileProduct = fileProduct + ".iso"
    mergeButton.config(text = "Merging... Please wait for completion.", state = "disabled")
    with open(fileProduct, "wb+") as mergeProduct, open(file1Path.get(), "rb") as filePart1, open(file2Path.get(), "rb") as filePart2:
        while True:
            dataPart1 = filePart1.read(1000000)
            if dataPart1 == b"": break
            else: mergeProduct.write(dataPart1)
        while True:
            dataPart2 = filePart2.read(1000000)
            if dataPart2 == b"": break
            else: mergeProduct.write(dataPart2)
    tkinter.messagebox.showinfo("Genesect","The files have been merged successfully!")
    mergeButton.config(text = "Merge Split ISO Files", state = "normal")

file1Label = tkinter.Label(mainWindow, text = "ISO File Part 1")
file1Label.grid(row = 1)

file1Path = tkinter.Entry(mainWindow, state = "readonly", width = 40, border = 5)
file1Path.grid(row = 2)

pickFile1 = tkinter.Button(mainWindow, text = "Select Part 1", textvariable = filePart1, border = 5, command = fileSelect1)
pickFile1.config(height = 1, width = 35); pickFile1.grid(row = 3)

file2Label = tkinter.Label(mainWindow, text = "ISO File Part 2")
file2Label.grid(row = 4, pady = (10, 0))

file2Path = tkinter.Entry(mainWindow, state = "readonly", width = 40, border = 5)
file2Path.grid(row = 5)

pickFile2 = tkinter.Button(mainWindow, text = "Select Part 2", textvariable = filePart2, border = 5, command = fileSelect2)
pickFile2.config(height = 1, width = 35); pickFile2.grid(row = 6)

buttonSeparator = tkinter.ttk.Separator(mainWindow, orient = "horizontal")
buttonSeparator.grid(row=7, sticky = "ew", pady = 10)

mergeButton = tkinter.Button(mainWindow, text = "Merge Split ISO Files", border = 5, command = fileMergeData)
mergeButton.config(height = 2, width = 35); mergeButton.grid(row = 8)
buttonCheck()

creditLabel = tkinter.Label(mainWindow, text = "Created by: NoahAbc12345", width = 40)
creditLabel.grid(row = 9, pady = 5)

mainWindow.mainloop()