from tkinter import filedialog as fd, Canvas, Tk, Button, Label, font, OptionMenu, StringVar, IntVar, Text
from tkinter.colorchooser import askcolor
from PIL import Image, ImageTk, ImageDraw, ImageFont
import matplotlib.font_manager as fm


class WaterMark():
    def __init__(self):
        FONT_NAME = "Nirmala UI"
        GREEN = "#00C5CD"
        bg = "#ABBFB6"
        self.font_name = "Nirmala UI"
        self.water_size_list = range(1, 21, 1)
        self.position_list = ["bottomright", "bottomleft", "topright", "topleft", "center"]
        self.opacity_list = range(0, 16)
        self.font_color = 'black'
        font_list = fm.findSystemFonts(fontpaths=None, fontext='ttf')
        self.fonts_list = [font.split("\\")[-1].split('.')[0] for font in font_list]
        self.font_size_list = range(5, 50, 5)
        self.window = Tk()
        self.window.title("Watermarker")
        self.window.config(padx=50, pady=50, bg=bg)

        # ----------------- Canvas ---------------------------------
        self.canvas = Canvas(width=800, height=500, bg=bg, highlightthickness=0)
        self.canvas.grid(column=2, row=1, columnspan=2, rowspan=8)

        # ----------------- Text -----------------------------------
        self.text = Text(width=15, height=3)
        self.text.insert('end', "Fred Herbert")
        self.text.grid(column=1, row=5, padx=10)

        self.font_size_var = IntVar(self.window)
        self.font_size_var.set(self.font_size_list[2])
        self.font_size_menu = OptionMenu(self.window, self.font_size_var, * self.font_size_list)
        self.font_size_menu.grid(column=1, row=6)

        self.sizes_var = IntVar(self.window)
        self.sizes_var.set(self.water_size_list[9])
        self.size_menu = OptionMenu(self.window, self.sizes_var, * self.water_size_list)
        self.size_menu.grid(column=1, row=2, padx=10)

        self.font_var = StringVar(self.window)
        self.font_var.set(self.fonts_list[0])
        self.font_menu = OptionMenu(self.window, self.font_var, * self.fonts_list)
        self.font_menu.grid(column=1, row=7)

        self.posi_var = StringVar(self.window)
        self.posi_var.set(self.position_list[-1])
        self.posi_menu = OptionMenu(self.window, self.posi_var, * self.position_list)
        self.posi_menu.grid(column=1, row=3, padx=10)

        self.opacity_var = IntVar(self.window)
        self.opacity_var.set(self.opacity_list[-1])
        self.opacity_menu = OptionMenu(self.window, self.opacity_var, * self.opacity_list)
        self.opacity_menu.grid(column=1, row=4)

        self.text_box_lab = Label(text="Enter Text:", bg=bg, font=(FONT_NAME, 15, "bold"))
        self.text_box_lab.grid(column=0, row=5)

        self.font_size_lab = Label(text="Font Size:", bg=bg, font=(FONT_NAME, 15, "bold"))
        self.font_size_lab.grid(column=0, row=6)

        self.font_style_lab = Label(text="Font Style:", bg=bg, font=(FONT_NAME, 15, "bold"))
        self.font_style_lab.grid(column=0, row=7)

        self.font_color_lab = Label(text='Font Color:', bg=bg, font=(FONT_NAME, 15, "bold"))
        self.font_color_lab.grid(column=0, row=8)

        self.title_label = Label(text="Luke's Water Marker", fg=GREEN, bg=bg, font=(FONT_NAME, 45, "bold"))
        self.title_label.grid(column=2, row=0, columnspan=2)

        self.size_label = Label(text="Size:", bg=bg, font=(FONT_NAME, 15, "bold"))
        self.size_label.grid(column=0, row=2)

        self.position_label = Label(text="Position:", bg=bg, font=(FONT_NAME, 15, "bold"))
        self.position_label.grid(column=0, row=3)

        self.opacity_label = Label(text="Transparancy:", bg=bg, font=(FONT_NAME, 15, "bold"))
        self.opacity_label.grid(column=0, row=4)

        #- ---------------------- INIT PHOTO ------------
        self.filename = 'Images/default_im.jpg'
        self.im = Image.open(self.filename)
        self.watername = 'Images/default_mark.jpg'
        self.water = Image.open(self.watername)
        self.resize_im()
        self.PI = ImageTk.PhotoImage(self.im)
        self.photo = self.canvas.create_image(self.width // 2, self.height // 2, image=self.PI)
        self.add_water()


        # ------------------------ Buttons -------------------------
        self.color_butt = Button(
            text="Font Color",
            command=self.change_color
        )
        self.color_butt.grid(column=1, row=8)

        self.apply_butt = Button(
            text="Apply Changes",
            command=self.add_water
        )
        self.apply_butt.grid(column=0, row=9)

        self.open_button = Button(
            text='Open an Image File',
            command=self.select_file,

        )
        self.open_button.grid(column=2, row=9, pady=10)

        self.open_water = Button(
            text='Open a Watermark File',
            command=self.select_water
        )
        self.open_water.grid(column=3, row=9, pady=10)


    def change_color(self):
        color_choice = askcolor(title="Choose font color")
        self.font_color = color_choice[0]


    def resize_im(self):
        self.width = self.im.size[0]
        self.height = self.im.size[1]
        if self.width > 1400 or self.height > 500:
            self.width = 500 * self.width//self.height
            self.height = 500
        self.im = self.im.resize((self.width, self.height))

    def select_water(self):
        self.watername = fd.askopenfilename(
            title='Open an image',
            initialdir='/',
        )
        self.add_water()


    def resize_water(self):
        water_size = self.sizes_var.get() / 20
        self.w_width = round(water_size*self.water.size[0])
        self.w_height = round(water_size*self.water.size[1])
        self.water = self.water.resize((self.w_width, self.w_height))



    def select_file(self):
        self.filename = fd.askopenfilename(
            title='Open an image',
            initialdir='/'
        )
        self.im = Image.open(self.filename).convert("RGBA")
        self.resize_im()
        self.configure_im()

    def saveas(self):
        file = fd.asksaveasfile(
            title="Save As",
            initialdir='/',
            filetypes=(('PNG', '*.png'),
                       ('JPG', '*.jpg')),
            initialfile=f'{self.filename.split("/")[-1].split(".")[0]}-watermarked',
            defaultextension='*.png',
            mode='w'
        )
        if file:
            self.im.save(file.name)


    def configure_im(self):
        self.PI = ImageTk.PhotoImage(self.im)
        self.canvas.itemconfig(self.photo, image=self.PI)
        self.canvas.config(height=self.height, width=self.width)
        self.canvas.coords(self.photo, self.width // 2, self.height // 2)

    def add_text(self):
        self.font_name = f'C:\\\\Windows\\\\Fonts\\\\{self.font_var.get()}.ttf'
        self.font_size = self.font_size_var.get()
        self.img_font = ImageFont.truetype(self.font_name, self.font_size)
        TEXT_INPUT = self.text.get('1.0', 'end')
        self.draw = ImageDraw.Draw(self.water)
        w = self.img_font.getlength(TEXT_INPUT)
        self.draw.multiline_text(((self.w_width - w) // 2, self.w_height // 2), TEXT_INPUT, self.font_color, font=self.img_font, align='center', )

    def position_water(self):
        position_dict = {
            "topleft": (0, 0),
            "topright": (self.width - self.w_width, 0),
            "bottomleft": (0, self.height - self.w_height),
            "bottomright": (self.width - self.w_width, self.height - self.w_height),
            "center": ((self.width - self.w_width) // 2, (self.height - self.w_height) // 2)
        }
        position = self.posi_var.get()
        self.im.paste(self.water, position_dict[position], self.water)
        self.canvas.coords(position_dict[position][0], position_dict[position][1])

    def change_opacity(self):
        opacity = self.opacity_var.get()
        self.water.putalpha(17 * opacity)

    def add_water(self):
        self.im = Image.open(self.filename).convert("RGBA")
        self.water = Image.open(self.watername).convert("RGBA")
        self.resize_im()
        self.resize_water()
        self.add_text()
        self.change_opacity()
        self.position_water()
        self.configure_im()
