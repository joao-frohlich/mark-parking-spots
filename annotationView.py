import tkinter as tk
from PIL import ImageTk, Image
import os
import jsonProcessing
import imageProcessing

def set_image(image_path, image_data, image_id, im_width, im_height):
    global my_image
    global image_frame
    global bg_label
    global checkboxes
    global vars
    global aux_centers
    aux_centers = {}
    centers = imageProcessing.drawMasks(image_path, '/tmp/aux.jpg', image_data)
    my_image = ImageTk.PhotoImage(Image.open('/tmp/aux.jpg').resize((800,600), Image.ANTIALIAS))
    bg_label = tk.Label(image_frame, image=my_image)
    bg_label.place(x=0,y=0)
    vars = {}
    checkboxes = {}
    for center in centers:
        vars[center[0]] = tk.IntVar()
        checkboxes[center[0]] = tk.Checkbutton(
            image_frame,
            variable=vars[center[0]],
            onvalue=2,
            offvalue=1,
            bd=0,
            padx=0,
            pady=0
        )
        aux_centers[center[0]] = [int(center[1]*(800/im_width)), int(center[2]*(600/im_height))]
        vars[center[0]].set(center[3])
        checkboxes[center[0]].place(x = aux_centers[center[0]][0], y = aux_centers[center[0]][1], height=7, width=7)
        # vars[center[0]].set(center[3])
        # checkboxes[center[0]].place(x = int(center[1]*(800/im_width)), y = int(center[2]*(600/im_height)), height=7, width=7)

def prev_image(num_images, json_path, save):
    global data
    global imgs_path
    global current_image
    global status_frame
    global status_label
    if save:
        save_image(json_path)
    if (current_image > 1):
        current_image-=1
        image_id = current_image
        set_image(imgs_path+'/'+data[image_id]['image_info']['path'], data[image_id]['parkingSpaces_info'], image_id, data[image_id]['image_info']['width'], data[image_id]['image_info']['height'])
        status_label.forget()
        status_label = tk.Label(
            status_frame,
            text='Image ' + str(current_image) + ' of ' + str(num_images),
            border = 1,
            background = '#1c1c1c',
            foreground = '#c1c1c1',
            highlightbackground = "#c1c1c1",
            highlightcolor = "#c1c1c1",
            highlightthickness = 1,
            anchor = tk.E,
        )
        status_label.pack(expand=True, fill='both')

def save_image(json_path):
    global vars
    global json_data
    global data
    global current_image
    global imgs_path
    for i in vars:
        json_data['parkingSpaces'][i-1]['status_id'] = vars[i].get()
    jsonProcessing.saveJson(json_data, json_path)
    json_data, data = jsonProcessing.openJson(json_path)
    image_id = current_image
    set_image(imgs_path+'/'+data[image_id]['image_info']['path'], data[image_id]['parkingSpaces_info'], image_id, data[image_id]['image_info']['width'], data[image_id]['image_info']['height'])

def next_image(num_images, json_path, save):
    global data
    global imgs_path
    global current_image
    global status_frame
    global status_label
    if save:
        save_image(json_path)
    if (current_image < num_images):
        current_image+=1
        image_id = current_image
        set_image(imgs_path+'/'+data[image_id]['image_info']['path'], data[image_id]['parkingSpaces_info'], image_id, data[image_id]['image_info']['width'], data[image_id]['image_info']['height'])
        status_label.forget()
        status_label = tk.Label(
            status_frame,
            text='Image ' + str(current_image) + ' of ' + str(num_images),
            border = 1,
            background = '#1c1c1c',
            foreground = '#c1c1c1',
            highlightbackground = "#c1c1c1",
            highlightcolor = "#c1c1c1",
            highlightthickness = 1,
            anchor = tk.E,
        )
        status_label.pack(expand=True, fill='both')

def save_undefined(tmp_window, json_path):
    tmp_window.destroy()
    save_image(json_path)

def select_undefined(json_path):
    global vars
    global checkboxes2
    global aux_values
    checkboxes2 = {}
    aux_values = {}
    tmp_window = tk.Toplevel()
    tmp_window.configure(bg = "#1c1c1c")
    tmp_window.geometry("800x630")
    global my_image2
    my_image2 = ImageTk.PhotoImage(Image.open('/tmp/aux.jpg').resize((800,600), Image.ANTIALIAS))
    bg_label2 = tk.Label(tmp_window, image=my_image2)
    bg_label2.place(x=0,y=0)
    for i in vars:
        aux_values[i] = vars[i].get()
        checkboxes2[i] = tk.Checkbutton(
            tmp_window,
            variable=vars[i],
            onvalue=3,
            offvalue=aux_values[i],
            bd=0,
            padx=0,
            pady=0
        )
        checkboxes2[i].place(x=aux_centers[i][0], y=aux_centers[i][1], height=7, width=7)
    confirm_button = tk.Button(tmp_window, text = "Confirm", bg="#1c1c1c", fg="#c1c1c1", activebackground = "#3c3c3c", pady=10, command = lambda: save_undefined(tmp_window, json_path))
    confirm_button.place(x=360,y=605,width=80, height=20)
    tmp_window.bind("<Return>", lambda x: save_undefined(tmp_window, json_path))

def change_image(tmp_window, num_images):
    global entry1
    global data
    global imgs_path
    global current_image
    global status_frame
    global status_label
    aux = entry1.get()
    if aux.isnumeric():
        aux = int(aux)
        if aux > 0 and aux <= num_images:
            current_image = aux
            image_id = current_image
            set_image(imgs_path+'/'+data[image_id]['image_info']['path'], data[image_id]['parkingSpaces_info'], image_id, data[image_id]['image_info']['width'], data[image_id]['image_info']['height'])
            status_label.forget()
            status_label = tk.Label(
                status_frame,
                text='Image ' + str(current_image) + ' of ' + str(num_images),
                border = 1,
                background = '#1c1c1c',
                foreground = '#c1c1c1',
                highlightbackground = "#c1c1c1",
                highlightcolor = "#c1c1c1",
                highlightthickness = 1,
                anchor = tk.E,
            )
            status_label.pack(expand=True, fill='both')
    tmp_window.destroy()

def select_image(num_images):
    tmp_window = tk.Toplevel()
    tmp_window.configure(padx = 20, pady = 20, bg = "#1c1c1c")
    label3 = tk.Label(tmp_window, text = "Insert image id", bg="#1c1c1c", fg="#c1c1c1")
    label3.grid(row=0,column=0,padx=10)
    global entry1
    entry1 = tk.Entry(tmp_window)
    entry1.grid(row=0, column=1)
    confirm_button = tk.Button(tmp_window, text = "Confirm", bg="#1c1c1c", fg="#c1c1c1", activebackground = "#3c3c3c", command = lambda:change_image(tmp_window,num_images))
    confirm_button.grid(row=1, column=0, pady=10)
    tmp_window.bind("<Return>", lambda x: change_image(tmp_window, num_images))

def annotation_view(images_path, json_path, image_id, root):
    top = tk.Toplevel()
    top.title("Annotation")
    top.geometry("1000x620")

    global image_frame
    global data
    global imgs_path
    global current_image
    global json_data
    current_image = image_id
    imgs_path = images_path
    json_data, data = jsonProcessing.openJson(json_path)
    num_images = len(json_data['images'])
    if image_id > num_images:
        image_id = num_images

    image_frame = tk.Frame(top)
    image_frame.place(x=0,y=0, width=800, height=600)

    set_image(images_path+'/'+data[image_id]['image_info']['path'], data[image_id]['parkingSpaces_info'], image_id, data[image_id]['image_info']['width'], data[image_id]['image_info']['height'])

    side_menu = tk.Frame(
        top,
        bg = '#1c1c1c',
    )
    side_menu.place(x=800,y=0, width=200, height=600)

    prev_image_button = tk.Button(
        side_menu,
        text = "Previous Image",
        bg = "#1c1c1c",
        activebackground = "#3c3c3c",
        fg = "#c1c1c1",
        command = lambda: prev_image(num_images, json_path, True)
    )
    prev_image_button.place(x=15,y=20, width=170, height=25)

    save_image_button = tk.Button(
        side_menu,
        text = "Save Image",
        bg = "#1c1c1c",
        activebackground = "#3c3c3c",
        fg = "#c1c1c1",
        command = lambda: save_image(json_path)
    )
    save_image_button.place(x=15,y=65, width=170, height=25)

    next_image_button = tk.Button(
        side_menu,
        text = "Next Image",
        bg = "#1c1c1c",
        activebackground = "#3c3c3c",
        fg = "#c1c1c1",
        command = lambda: next_image(num_images, json_path, True)
    )
    next_image_button.place(x=15,y=110, width=170, height=25)

    prev_image_no_save_button = tk.Button(
        side_menu,
        text = "Previous Image No Save",
        bg = "#1c1c1c",
        activebackground = "#3c3c3c",
        fg = "#c1c1c1",
        command = lambda: prev_image(num_images, json_path, False)
    )
    prev_image_no_save_button.place(x=15,y=265, width=170, height=25)

    next_image_no_save_button = tk.Button(
        side_menu,
        text = "Next Image No Save",
        bg = "#1c1c1c",
        activebackground = "#3c3c3c",
        fg = "#c1c1c1",
        command = lambda: next_image(num_images, json_path, False)
    )
    next_image_no_save_button.place(x=15,y=310, width=170, height=25)

    close_program_button = tk.Button(
        side_menu,
        text = "Close Program",
        bg = "#1c1c1c",
        activebackground = "#3c3c3c",
        fg = "#c1c1c1",
        command = root.destroy
    )
    close_program_button.place(x=15,y=465, width=170, height=25)

    select_undefined_button = tk.Button(
        side_menu,
        text = "Select Undefined",
        bg = "#1c1c1c",
        activebackground = "#3c3c3c",
        fg = "#c1c1c1",
        command = lambda: select_undefined(json_path)
    )
    select_undefined_button.place(x=15,y=510, width=170, height=25)

    select_image_button = tk.Button(
        side_menu,
        text = "Select Image",
        bg = "#1c1c1c",
        activebackground = "#3c3c3c",
        fg = "#c1c1c1",
        command = lambda: select_image(num_images)
    )
    select_image_button.place(x=15,y=555, width=170, height=25)

    global status_frame
    status_frame = tk.Frame(top, bg= "#1c1c1c")
    status_frame.place(x=0,y=600,height=20, width=1000)

    global status_label
    status_label = tk.Label(
        status_frame,
        text='Image ' + str(current_image) + ' of ' + str(num_images),
        border = 1,
        background = '#1c1c1c',
        foreground = '#c1c1c1',
        highlightbackground = "#c1c1c1",
        highlightcolor = "#c1c1c1",
        highlightthickness = 1,
        anchor = tk.E,
    )
    status_label.pack(expand=True, fill='both')

    top.bind("<Control-q>", lambda x: prev_image(num_images, json_path, True))
    top.bind("<Control-s>", lambda x: save_image(json_path))
    top.bind("<Control-e>", lambda x: next_image(num_images, json_path, True))
    top.bind("<Control-p>", lambda x: prev_image(num_images, json_path, False))
    top.bind("<Control-n>", lambda x: next_image(num_images, json_path, False))
    top.bind("<Control-a>", lambda x: select_undefined(json_path))
    top.bind("<Control-f>", lambda x: select_image(num_images))
    top.bind("<Escape>", lambda x: root.destroy())


    # return top
