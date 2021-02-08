import os, tkinter
from tkinter import Tk, ttk, filedialog, messagebox
filePart1 = ""; filePart2 = ""
readSize = 1000000

mainWindow = Tk()
mainWindow.title("Genesect")
mainWindow.resizable(False, False)

def checkMerge():
    if file1Path.get() and file2Path.get(): mergeButton.config(state = "normal")
    else: mergeButton.config(state = "disabled")

def displayMerge(mergePart, mergeTotal):
    mergeProgress["value"] += readSize
    mergeFraction = (mergePart / mergeTotal)
    mergeFraction = int(str(round(mergeFraction * 100, 0))[:-2])
    if mergeFraction > 100: mergeFraction = 100
    mergeButton.config(text = f"Merge in Progress ({mergeFraction}%)")

def fileSelect1():
    filePart1 = filedialog.askopenfilename(title = "Select ISO Part 1", filetypes = (("Disc Image File","*.iso"),))
    if filePart1 == "": raise Exception("No file was selected!")
    file1Path.config(state = "normal")
    file1Path.delete(0, "end"); file1Path.insert(0, filePart1)
    file1Path.config(state = "readonly"); checkMerge()

def fileSelect2():
    filePart2 = filedialog.askopenfilename(title = "Select ISO Part 2", filetypes = (("Disc Image File","*.iso"),))
    if filePart2 == "": raise Exception("No file was selected!")
    file2Path.config(state = "normal")
    file2Path.delete(0, "end"); file2Path.insert(0, filePart2)
    file2Path.config(state = "readonly"); checkMerge()

def fileMergeData():
    fileProduct = filedialog.asksaveasfilename(title = "Save Merged ISO Parts", filetypes = (("Disc Image File","*.iso"),))
    if not fileProduct.endswith(".iso"): fileProduct = fileProduct + ".iso"
    pickFile1.config(state = "disabled"); pickFile2.config(state = "disabled")
    mergeButton.config(text = "Merge in Progress", state = "disabled")
    mergeTotal = os.stat(file1Path.get()).st_size + os.stat(file2Path.get()).st_size
    mergeProgress["maximum"] = mergeTotal
    with open(fileProduct, "wb+") as mergeProduct, open(file1Path.get(), "rb") as filePart1, open(file2Path.get(), "rb") as filePart2:
        while True:
            dataPart1 = filePart1.read(readSize)
            if dataPart1 == b"": break
            else:
                mergeProduct.write(dataPart1)
                displayMerge(mergeProgress["value"], mergeTotal)
                mainWindow.update()
        while True:
            dataPart2 = filePart2.read(readSize)
            if dataPart2 == b"": break
            else:
                mergeProduct.write(dataPart2)
                displayMerge(mergeProgress["value"], mergeTotal)
                mainWindow.update()
    if os.stat(fileProduct).st_size == mergeTotal: messagebox.showinfo("Genesect", "The files have been merged successfully!")
    else: messagebox.showwarning("Genesect", "The files might be merged improperly! Please try again.")
    mergeButton.config(text = "Merge Split ISO Files", state = "normal")
    pickFile1.config(state = "normal"); pickFile2.config(state = "normal")
    mergeProgress["value"] = 0

file1Label = tkinter.Label(mainWindow, text = "ISO File Part 1")
file1Label.grid(row = 1)
file1Path = tkinter.Entry(mainWindow, state = "readonly", width = 40, border = 5)
file1Path.grid(row = 2)
pickFile1 = tkinter.Button(mainWindow, text = "Select Part 1", textvariable = filePart1, border = 5, command = fileSelect1)
pickFile1.grid(row = 3); pickFile1.config(height = 1, width = 35)

file2Label = tkinter.Label(mainWindow, text = "ISO File Part 2")
file2Label.grid(row = 4, pady = (5, 0))
file2Path = tkinter.Entry(mainWindow, state = "readonly", width = 40, border = 5)
file2Path.grid(row = 5)
pickFile2 = tkinter.Button(mainWindow, text = "Select Part 2", textvariable = filePart2, border = 5, command = fileSelect2)
pickFile2.grid(row = 6); pickFile2.config(height = 1, width = 35)

buttonSeparator = ttk.Separator(mainWindow, orient = "horizontal")
buttonSeparator.grid(row=7, sticky = "ew", pady = 10)

mergeProgress = ttk.Progressbar(mainWindow, orient = "horizontal")
mergeProgress.grid(row = 8); mergeProgress.config(length = 260)
mergeButton = tkinter.Button(mainWindow, text = "Merge Split ISO Files", border = 5, command = fileMergeData)
mergeButton.grid(row = 9, pady = (10, 5)); mergeButton.config(height = 2, width = 35)

creditLabel = tkinter.Label(mainWindow, text = "Created by NoahAbc12345", width = 40)
creditLabel.grid(row = 10)

checkMerge(); mainWindow.mainloop()