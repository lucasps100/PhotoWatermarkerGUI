from tkinter import filedialog as fd, Canvas, Tk, Button, Label, font, OptionMenu, StringVar, IntVar
from PIL import Image, ImageTk, PSDraw

# ------------------- Constants --------------------------
FONT_NAME = "Nirmala UI"
GREEN = "#00C5CD"
bg = "#ABBFB6"

water_size_list = range(1, 21, 1)
position_list = ["bottomright", "bottomleft", "topright", "topleft", "center"]
opacity_list = range(0, 16)

# ------------------- Functions ------------------------

def resize_im():
    global im, width, height
    width = im.size[0]
    height = im.size[1]
    if width > 1400 or height > 500:
        width = 500*width//height
        height = 500
    im = im.resize((width, height))

def select_water():
    global water_im, watername
    watername = fd.askopenfilename(
        title='Open an image',
        initialdir='/',
    )
    add_water()


def resize_water():
    global water_im, sizes_var, w_width, w_height
    water_size = sizes_var.get() / 20
    w_width = round(water_size*water_im.size[0])
    w_height = round(water_size*water_im.size[1])
    water_im = water_im.resize((w_width, w_height))



def select_file():
    global filename
    filename = fd.askopenfilename(
        title='Open an image',
        initialdir='/'
    )
    configure_im()

def saveas():
    global im
    file = fd.asksaveasfile(
        title="Save As",
        initialdir='/',
        filetypes=(('PNG', '*.png'),
                   ('JPG', '*.jpg')),
        initialfile=f'{filename.split("/")[-1].split(".")[0]}-watermarked',
        defaultextension='*.png',
        mode='w'
    )
    if file:
        im.convert('L').save(file.name)


def configure_im():
    global im, photo, new_photo
    im = Image.open(filename).convert("RGBA")
    resize_im()
    new_photo = ImageTk.PhotoImage(im)
    canvas.itemconfig(photo, image=new_photo)
    canvas.config(height=im.size[1], width=im.size[0])
    canvas.coords(photo, im.size[0] // 2, im.size[1] // 2)

def add_water():
    global im, w_width, w_height, posi_var, opacity_var, new_photo
    global water_im, watername
    global photo
    opacity = opacity_var.get()
    position = posi_var.get()
    water_im = Image.open(watername).convert("RGBA")
    resize_water()
    position_dict = {
        "topleft": (0, 0),
        "topright": (width - w_width, 0),
        "bottomleft": (0, height - w_height),
        "bottomright": (width - w_width, height - w_height),
        "center": ((width-w_width) // 2, (height-w_height) // 2)
    }
    configure_im()
    water_im.putalpha(17*opacity)
    im.paste(water_im, position_dict[position], water_im)
    new_photo = ImageTk.PhotoImage(im)
    canvas.itemconfig(photo, image=new_photo)





# ---------------------------------------- UI ------------------------------------
window = Tk()
window.title("Watermarker")
window.config(padx=50, pady=50, bg=bg)

fonts_list = list(font.families())
print(fonts_list)
# ----------------- Canvas ---------------------------------
canvas = Canvas(width=800, height=500, bg=bg, highlightthickness=0)
canvas.grid(column=2, row=1, columnspan=2, rowspan=6)


#------------------ Menus ----------------------------------
sizes_var = IntVar(window)
sizes_var.set(water_size_list[9])
size_menu = OptionMenu(window, sizes_var, *water_size_list)
size_menu.grid(column=1, row=2, padx=10)

posi_var = StringVar(window)
posi_var.set(position_list[-1])
posi_menu = OptionMenu(window, posi_var, *position_list)
posi_menu.grid(column=1, row=3, padx=10)

opacity_var = IntVar(window)
opacity_var.set(opacity_list[-1])
opacity_menu = OptionMenu(window, opacity_var, *opacity_list)
opacity_menu.grid(column=1, row=4)
#------------------------- Initialize --------------------------
filename = 'Images/default_im.jpg'
im = Image.open(filename)
watername = 'Images/default_mark.jpg'
water_im = Image.open(watername)
resize_im()
PI = ImageTk.PhotoImage(im)
photo = canvas.create_image(width//2, height//2, image=PI)
add_water()

# -------------------------- Labels ------------------------------------

title_label = Label(text="Luke's Water Marker", fg=GREEN, bg=bg, font=(FONT_NAME, 45, "bold"))
title_label.grid(column=2, row=0, columnspan=2)

size_label = Label(text="Size:", bg=bg, font=(FONT_NAME, 15, "bold"))
size_label.grid(column=0, row=2)

position_label = Label(text="Position:", bg=bg, font=(FONT_NAME, 15, "bold"))
position_label.grid(column=0, row=3)

opacity_label = Label(text="Transparancy:", bg=bg, font=(FONT_NAME, 15, "bold"))
opacity_label.grid(column=0, row=4)

# ------------------------ Buttons -------------------------
apply_butt = Button(
    text="Apply Changes",
    command=add_water
)
apply_butt.grid(column=0, row=5, columnspan=2)

open_button = Button(
    text='Open an Image File',
    command=select_file,

)

open_button.grid(column=2, row=7, pady=10)

open_water = Button(
    text='Open a Watermark File',
    command=select_water
)
open_water.grid(column=3, row=7, pady=10)

save_button = Button(
    text="Save As",
    command=saveas
)
save_button.grid(row=7, column=0)


window.mainloop()

#TODO: Add watermark designing functionality(text/drawing/filters)
