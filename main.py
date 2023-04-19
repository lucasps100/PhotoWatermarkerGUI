from tkinter import filedialog as fd, Canvas, Tk, Button, Label, font, OptionMenu, StringVar, IntVar, Text
from tkinter.colorchooser import askcolor
from PIL import Image, ImageTk, PSDraw, ImageDraw, ImageFont
import matplotlib.font_manager as fm

# ------------------- Constants --------------------------
FONT_NAME = "Nirmala UI"
GREEN = "#00C5CD"
bg = "#ABBFB6"

water_size_list = range(1, 21, 1)
position_list = ["bottomright", "bottomleft", "topright", "topleft", "center"]
opacity_list = range(0, 16)
color = 'black'

font_list = fm.findSystemFonts(fontpaths=None, fontext='ttf')
fonts_list = [font.split("\\")[-1].split('.')[0] for font in font_list]

font_size_list = range(5, 50, 5)


# ------------------- Functions ------------------------
def change_color():
    global color
    color_choice = askcolor(title="Choose font color")
    color = color_choice[0]


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
    global water_im, w_width, w_height
    water_size = sizes_var.get() / 20
    w_width = round(water_size*water_im.size[0])
    w_height = round(water_size*water_im.size[1])
    water_im = water_im.resize((w_width, w_height))



def select_file():
    global filename, im
    filename = fd.askopenfilename(
        title='Open an image',
        initialdir='/'
    )
    im = Image.open(filename).convert("RGBA")
    resize_im()
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
        im.save(file.name)


def configure_im():
    global im, photo, new_photo, width, height
    new_photo = ImageTk.PhotoImage(im)
    canvas.itemconfig(photo, image=new_photo)
    canvas.config(height=height, width=width)
    canvas.coords(photo, width // 2, height // 2)

def add_text():
    global water_im, text, color, draw, IMG_FONT, w_width, w_height
    FONT_NAME = f'C:\\\\Windows\\\\Fonts\\\\{font_var.get()}.ttf'
    FONT_SIZE = font_size_var.get()
    IMG_FONT = ImageFont.truetype(FONT_NAME, FONT_SIZE)
    TEXT_INPUT = text.get('1.0', 'end')
    draw = ImageDraw.Draw(water_im)
    w, h = draw.textsize(TEXT_INPUT, font=IMG_FONT)
    draw.multiline_text(((w_width - w) // 2, (w_height - h) // 2), TEXT_INPUT, color, font=IMG_FONT, align='center', )

def position_water():
    global width, height, w_width, w_height, im, water_im
    position_dict = {
        "topleft": (0, 0),
        "topright": (width - w_width, 0),
        "bottomleft": (0, height - w_height),
        "bottomright": (width - w_width, height - w_height),
        "center": ((width - w_width) // 2, (height - w_height) // 2)
    }
    position = posi_var.get()
    im.paste(water_im, position_dict[position], water_im)
    canvas.coords(position_dict[position][0], position_dict[position][1])

def change_opacity():
    global water_im
    opacity = opacity_var.get()
    water_im.putalpha(17 * opacity)

def add_water():
    global water_im, im, watername, filename
    im = Image.open(filename).convert("RGBA")
    water_im = Image.open(watername).convert("RGBA")
    resize_im()
    resize_water()
    add_text()
    change_opacity()
    position_water()
    configure_im()








# ---------------------------------------- UI ------------------------------------
window = Tk()
window.title("Watermarker")
window.config(padx=50, pady=50, bg=bg)



# ----------------- Canvas ---------------------------------
canvas = Canvas(width=800, height=500, bg=bg, highlightthickness=0)
canvas.grid(column=2, row=1, columnspan=2, rowspan=8)
# ----------------- Text -----------------------------------
text = Text(width=15, height=3)
text.insert('end', "Fred Herbert")
text.grid(column=1, row=5, padx=10)

#------------------ Menus ----------------------------------

font_size_var = IntVar(window)
font_size_var.set(font_size_list[2])
font_size_menu = OptionMenu(window, font_size_var, *font_size_list)
font_size_menu.grid(column=1, row=6)

sizes_var = IntVar(window)
sizes_var.set(water_size_list[9])
size_menu = OptionMenu(window, sizes_var, *water_size_list)
size_menu.grid(column=1, row=2, padx=10)

font_var = StringVar(window)
font_var.set(fonts_list[0])
font_menu = OptionMenu(window, font_var, *fonts_list)
font_menu.grid(column=1, row=7)

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
text_box_lab = Label(text="Enter Text:", bg=bg, font=(FONT_NAME, 15, "bold"))
text_box_lab.grid(column=0, row=5)

font_size_lab = Label(text="Font Size:", bg=bg, font=(FONT_NAME, 15, "bold"))
font_size_lab.grid(column=0, row=6)

font_style_lab = Label(text="Font Style:", bg=bg, font=(FONT_NAME, 15, "bold"))
font_style_lab.grid(column=0, row=7)

font_color_lab = Label(text='Font Color:', bg=bg, font=(FONT_NAME, 15, "bold"))
font_color_lab.grid(column=0, row=8)

title_label = Label(text="Luke's Water Marker", fg=GREEN, bg=bg, font=(FONT_NAME, 45, "bold"))
title_label.grid(column=2, row=0, columnspan=2)


size_label = Label(text="Size:", bg=bg, font=(FONT_NAME, 15, "bold"))
size_label.grid(column=0, row=2)

position_label = Label(text="Position:", bg=bg, font=(FONT_NAME, 15, "bold"))
position_label.grid(column=0, row=3)

opacity_label = Label(text="Transparancy:", bg=bg, font=(FONT_NAME, 15, "bold"))
opacity_label.grid(column=0, row=4)

# ------------------------ Buttons -------------------------
color_butt = Button(
    text="Font Color",
    command=change_color
)
color_butt.grid(column=1, row=8)
apply_butt = Button(
    text="Apply Changes",
    command=add_water
)
apply_butt.grid(column=0, row=9)

open_button = Button(
    text='Open an Image File',
    command=select_file,

)

open_button.grid(column=2, row=9, pady=10)

open_water = Button(
    text='Open a Watermark File',
    command=select_water
)
open_water.grid(column=3, row=9, pady=10)

save_button = Button(
    text="Save As",
    command=saveas
)
save_button.grid(row=9, column=1)


window.mainloop()

#TODO: Organize code with class objects.
