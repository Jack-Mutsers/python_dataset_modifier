
import tkinter as tk
from tkinter import Tk, Button, Checkbutton, IntVar, ttk, NORMAL
from PIL import ImageTk, Image
from glob import glob
import os
import math
import tkcap
import shutil

rows = 10
colls = 10
total_images = rows*colls
image_array = []
boxes = []
to_delete = []
loading = True
root = Tk()
tabControl = None
currentLetter = ""
cap = tkcap.CAP(root)     # master is an instance of tkinter.Tk
titleName = ""
categories = ["lowercase", "unknown", "uppercase", "number"]

special_bg = None
special_colored = [
    {"x": 2, "y": 2},
    {"x": 2, "y": 3},
    {"x": 2, "y": 4},
    {"x": 2, "y": 5},
    {"x": 2, "y": 6},
    {"x": 2, "y": 7},
    {"x": 3, "y": 7},
    {"x": 4, "y": 7},
    {"x": 5, "y": 7},
    {"x": 6, "y": 7},
    {"x": 7, "y": 7},
    {"x": 7, "y": 6},
    {"x": 7, "y": 5},
    {"x": 7, "y": 4},
    {"x": 7, "y": 3},
    {"x": 7, "y": 2},
    {"x": 6, "y": 2},
    {"x": 5, "y": 2},
    {"x": 4, "y": 2},
    {"x": 3, "y": 2},
]

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
                    delete_path = image_array[tab][i][j]["path"]
                    # print(delete_path)

                    # check if file exists
                    if os.path.isfile(delete_path):
                        to_delete.append(delete_path)

def next_selection():
    global root, loading, tabControl
    t = tabControl.index("current")
    getSelected()

    # take screenshot of window for delete evaluation to verify the correct images were removed
    take_screenshot_of_window(str(t+1))

    if loading == False and len(tabControl.children) > t+1:
        tabControl.select(t+1)
    elif loading == False:
        root.destroy()
        root = None

def premeture_delete():
    getSelected()
    remove_selected_files()

def take_screenshot_of_window(tab_number):
    global cap, titleName, categories, currentLetter

    fileName = titleName.replace("/", "_").replace(" ", "") + "-tab_" + tab_number + ".png"
    delete_path = "/".join(titleName.split("/")[:-2])
    delete_path = delete_path.replace(currentLetter, currentLetter + "/delete") + "/"

    if os.path.exists(delete_path) is False:
        os.mkdir(delete_path)

    filepath = delete_path + "." + fileName

    image_exists = os.path.isfile(filepath)
    cap.capture(filepath, image_exists)       # Capture and Save the screenshot of the tkiner window

def checkRow(y):
    global image_array, boxes, tabControl
    tab = tabControl.index("current")

    # Check if enough buttons have been selected. If so, disable the deselected indeces,
    # Otherwise set all of them to active (in case we have previously disabled them).
    index = 0
    for item in boxes[tab][y]:
        item.config(state = NORMAL)
        if (image_array[tab][y][index]["var"].get() == 1):
            item.config(background="red")
        else:
            if {"x": index, "y": y} in special_colored:
                item.config(background=special_bg)
            else:
                item.config(background="grey")
        
        index+=1

def remove_selected_files():
    global to_delete, currentLetter
    if len(to_delete) < 1:
        return

    print(to_delete)
    for filepath in to_delete:
        # skip if file has been deleted already
        if os.path.isfile(filepath) == False:
            continue

        # os.remove(filepath)
        filename = filepath.split("\\")[-1]
        path = "\\".join(filepath.split("\\")[:-1])
        delete_path = path.replace(currentLetter, currentLetter + "\\delete") + "\\"

        if os.path.exists(delete_path) is False:
            os.mkdir(delete_path)

        shutil.move(filepath, delete_path + filename)

    to_delete = []

def close_program():
    getSelected()
    remove_selected_files()
    exit()

def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb 

def scanFolder(folder_names, search_dir):
    global image_array, boxes, loading, root, tabControl, cap, titleName

    for folder_name in folder_names:
        if folder_name == "delete":
            continue

        folder_path = search_dir + folder_name + "/"

        sub_folder_names = [name for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))]
        if len(sub_folder_names) > 0:
            scanFolder(sub_folder_names, folder_path)

        image_paths = glob(folder_path+"*.png")
        max_images_per_session = 2500
        session_groups = [image_paths[x:x+max_images_per_session] for x in range(0, len(image_paths), max_images_per_session)]

        session = 0
        for session_group in session_groups:
            loading = True
            session += 1

            titleName = folder_path + " - " + str(session) + "/" + str(len(session_groups))
            root.title(titleName)
            root["bg"]='grey'

            tabControl = ttk.Notebook(root, width=colls*65)
            tabControl.grid(row=1, column=1, columnspan=colls)

            s = ttk.Style()
            s.theme_use('default')
            s.configure('TNotebook.Tab', background="grey")

            colspan = math.floor(colls/3)
            b1 = Button(root, text = "Close", command = close_program, width = 15)
            b1.grid(row=3, column=1, columnspan=colspan)

            b2 = Button(root, text = "Delete selection", command = premeture_delete, width = 15, background="darkred", foreground="white")
            b2.grid(row=3, column=colspan+1, columnspan=colspan)

            b3 = Button(root, text = "Next", command = next_selection, width = 15)
            b3.grid(row=3, column=(colspan*2)+1, columnspan=colspan)
            
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
                        btn = Checkbutton(tab)
                        btn.config(variable = image_group[y]["var"])
                        btn.config(image = image_group[y]["image"])
                        imagefile = image_group[y]["path"].split("\\")[-1]
                        imagename = imagefile.split(".")[0]
                        btn.config(text = imagename)
                        btn.config(compound= "top")

                        if {"x": x, "y": y} in special_colored:
                            btn.config(background=special_bg)
                        else:
                            btn.config(background="grey")

                        btn.config(command = lambda x = x: checkRow(x))

                        boxes[tab_count][x].append(btn)
                        boxes[tab_count][x][y].grid(row=x+1, column=y+1)

                tab_count += 1

            loading = False

            root.mainloop()

            # unset variables
            tabControl = None
            root = None
            cap = None

            # reset tkinter window
            root = Tk()
            cap = tkcap.CAP(root)     # master is an instance of tkinter.Tk

            # delete selected images
            remove_selected_files()

def create_delete_folders(delete_path, character_index):
    global categories, labelNames

    if os.path.exists(delete_path) is False:
        os.mkdir(delete_path)

    for category in categories:
        if character_index < labelNames.index("A") and category != categories[-1]:
            continue
        elif character_index > labelNames.index("9") and category == categories[-1]:
            continue

        if os.path.exists(delete_path + category) is False:
                os.mkdir(delete_path + category)

special_bg = _from_rgb((0,80,80))
for character in labelNames:
    character_index = labelNames.index(character)
    currentLetter = character

    # skip characters until desired character is reached
    if character_index < labelNames.index("S"):
        continue

    # stop looping when numbers and all letters have been ran
    if character_index > labelNames.index("Z"):
        break

    search_dir = "temp/"+character+"/"
    folder_names = [name for name in os.listdir(search_dir) if os.path.isdir(os.path.join(search_dir, name))]

    create_delete_folders(search_dir + "delete" + "/", character_index)

    scanFolder(folder_names, search_dir)

    