
import tkinter as tk
from tkinter import Tk, Button, Checkbutton, IntVar, ttk, NORMAL, DISABLED
from PIL import ImageTk, Image
from glob import glob
import os
import math

rows = 10
colls = 10
total_images = rows*colls
image_array = []
boxes = []
to_delete = []
loading = True
root = Tk()
tabControl = None

labelNames = "0123456789"
labelNames += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
labelNames += "abcdefghijklmnopqrstuvwxyz"
labelNames = [l for l in labelNames]

def loadImages(image_paths):
    loaded_images = {}
    index = 0
    for image_path in image_paths:
        image = Image.open(image_path)
        glb_img = ImageTk.PhotoImage(image)

        loaded_images[index] = {}
        loaded_images[index]["path"] = image_path
        loaded_images[index]["image"] = glb_img
        loaded_images[index]["var"] = IntVar()
        loaded_images[index]["var"].set(0)
        index += 1

    return loaded_images

def getSelected():
    global image_array, to_delete, tabControl
    tab = tabControl.index("current")

    for i in range(len(image_array[tab])):
        for j in range(len(image_array[tab][i])):
            if image_array[tab][i][j]["var"].get() == 1:
                if image_array[tab][i][j]["path"] not in to_delete:
                    to_delete.append(image_array[tab][i][j]["path"])

def next_selection():
    global root, loading, tabControl
    t = tabControl.index("current")
    getSelected()

    if loading == False and len(tabControl.children) > t+1:
        tabControl.select(t+1)
    elif loading == False:
        root.destroy()
        root = None

def checkRow(tab_index, x, y):
    global image_array, boxes

    row = image_array[tab_index][x]
    deselected = []

    # Loop through row that was changed, check which items were not selected 
    # (so that we know which indeces to disable in the event that 2 have been selected)

    for j in range(len(row)):
        if row[j]["var"].get() == 0:
            deselected.append(j)

    # Check if enough buttons have been selected. If so, disable the deselected indeces,
    # Otherwise set all of them to active (in case we have previously disabled them).

    if len(deselected) == (len(row)):
        for j in deselected:
            boxes[tab_index][x][j].config(state = DISABLED)
    else:
        for item in boxes[tab_index][x]:
            item.config(state = NORMAL)

def remove_selected_files():
    global to_delete
    if len(to_delete) < 1:
        return

    print(to_delete)
    for filepath in to_delete:
        os.remove(filepath)

    to_delete = []

def close_program():
    getSelected()
    remove_selected_files()
    exit()

def scanFolder(folder_names, search_dir):
    global image_array, boxes, loading, root, tabControl

    for folder_name in folder_names:
        folder_path = search_dir + folder_name

        sub_folder_names = [name for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))]
        if len(sub_folder_names) > 0:
            scanFolder(sub_folder_names, folder_path)
        
        image_paths = glob(folder_path+"/*.png")
        max_images_per_session = 2500
        session_groups = [image_paths[x:x+max_images_per_session] for x in range(0, len(image_paths), max_images_per_session)]

        for session_group in session_groups:
            loading = True

            root.title(folder_path)
            root["bg"]='grey'

            tabControl = ttk.Notebook(root, width=colls*65)
            tabControl.grid(row=1, column=1, columnspan=colls)

            s = ttk.Style()
            s.theme_use('default')
            s.configure('TNotebook.Tab', background="grey")

            colspan = math.floor(colls/2)
            b1 = Button(root, text = "Close", command = close_program, width = 15)
            b1.grid(row=3, column=1, columnspan=colspan)

            b2 = Button(root, text = "Next", command = next_selection, width = 15)
            b2.grid(row=3, column=colspan+1, columnspan=colspan)
            
            image_path_groups = [session_group[x:x+total_images] for x in range(0, len(session_group), total_images)]

            tab_count = 0
            image_array = []
            boxes = []
            for image_path_group in image_path_groups:
                images = loadImages(image_path_group)

                image_array.append([])
                for y in range(0, math.ceil(len(images) / colls)):
                    image_array[tab_count].append([])

                row = 0
                i = 0
                for image_index in images:
                    image = images[image_index]
                    image_array[tab_count][row].append(image)

                    i += 1
                    if len(image_array[tab_count][row]) % colls == 0:
                        row += 1
                        i = 0
                
                tab = tk.Frame(tabControl, background="grey")
                tabControl.add(tab, text=str(tab_count+1))

                boxes.append([])
                for x in range(len(image_array[tab_count])):

                    image_group = image_array[tab_count][x]
                    boxes[tab_count].append([])
                    for y in range(len(image_group)):
                        var = image_group[y]["var"]
                        image = image_group[y]["image"]
                        command = lambda x = x: checkRow(tab_count, x, y)
                        boxes[tab_count][x].append(Checkbutton(tab, variable = var, image = image, command = command, background="grey"))
                        boxes[tab_count][x][y].grid(row=x+1, column=y+1)

                tab_count += 1

            loading = False

            root.mainloop()

            # unset variables
            tabControl = None
            root = None

            # reset tkinter window
            root = Tk()
            
            # delete selected images
            remove_selected_files()




for character in labelNames:
    character_index = labelNames.index(character)

    # skip characters until desired character is reached
    if character_index < labelNames.index("C"):
        continue

    # stop looping when numbers and all letters have been ran
    if character_index > labelNames.index("Z"):
        break

    search_dir = "temp/"+character+"/"
    folder_names = [name for name in os.listdir(search_dir) if os.path.isdir(os.path.join(search_dir, name))]

    scanFolder(folder_names, search_dir)

    