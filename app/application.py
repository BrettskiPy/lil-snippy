from tkinter import *
from tkinter import colorchooser, filedialog
from snip_tools import SnipRectangle, bounded_screenshot
from PIL import Image, ImageTk
import os

class Application:
    def __init__(self, master: Tk) -> None:
        self.master = master

        self.master.geometry("300x100+200+300")
        self.master.title("Lil Snippy")
        self.master.resizable(False, False)

        self.snip_border_width = 2
        self.snip_border_size_window = None
        self.snip_save_directory = os.path.join(os.path.expanduser('~'), 'Desktop')
        self.snip_coordinates_toggle = True

        self.add_menu_bar()
        self.menu_frame = Frame(self.master, background='black')
        self.menu_frame.pack(fill=BOTH, expand=YES)
        self.add_main_menu_buttons()

        self.outside_snip_color = ["#a0a0a0"]
        self.snip_border_color = ["#FF0000"]

    def add_main_menu_buttons(self) -> None:
        self.menu_button_bar = Frame(self.menu_frame, bg='grey10')
        self.menu_button_bar.pack(padx=10, pady=6)

        self.photo = PhotoImage(file="app/assets/camera_icon.png")
        self.snipButton = Button(
            self.menu_button_bar,
            height=30,
            width=30,
            command=self.create_snipping_environment,
            image=self.photo
        )
        self.snipButton.pack(side='left', padx=10, pady=6)


    def add_menu_bar(self) -> None:
        self.menu_bar = Menu(self.master)
        self.master.config(menu=self.menu_bar)

        file_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(
            label="Set Save Location", command=self.set_save_directory
        )
        file_menu.add_command(label="Quit", command=self.master.quit)


        self.options_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Customize", menu=self.options_menu)
        self.options_menu.add_command(
            label="Background Color", command=self.open_outside_snip_color_window
        )
        self.options_menu.add_command(
            label="Rectangle Color", command=self.open_snip_border_color_window
        )
        self.options_menu.add_command(
            label="Snip Border Size", command=self.open_snip_border_size_window
        )
        self.options_menu.add_command(
            label="Snip Coordinates: On", command=self.toggle_snip_coordinates
        )

        about_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="About", menu=about_menu)
        about_menu.add_command(label="Info", command=self.master.quit)
    
    def toggle_snip_coordinates(self):
        if self.snip_coordinates_toggle:
            self.snip_coordinates_toggle = False
            self.options_menu.entryconfig(4, label="Snip Coordinates: Off")
        else:
            self.snip_coordinates_toggle = True
            self.options_menu.entryconfig(4, label="Snip Coordinates: On")

    def set_save_directory(self):
        self.snip_save_directory = filedialog.askdirectory(initialdir = "app")
    
    def open_outside_snip_color_window(self):
        self.outside_snip_color = colorchooser.askcolor()

    def open_snip_border_color_window(self):
        self.snip_border_color = colorchooser.askcolor()

    def open_snip_border_size_window(self):
        if self.snip_border_size_window:
            self.snip_border_size_window.destroy()

        self.snip_border_size_window = Toplevel()
        self.snip_border_size_window.resizable = False
        self.snip_border_size_window.geometry("200x100")
        self.snip_border_size_window.attributes("-topmost", True)

        size_scale = Scale(
            self.snip_border_size_window, from_=1, to=5, orient=HORIZONTAL, length=150
        )
        size_scale.pack(pady=10)

        apply_button = Button(
            self.snip_border_size_window,
            text="Apply",
            command=lambda: self.set_snip_border_size(size_scale.get(), self.snip_border_size_window),
        )
        apply_button.pack()

    def set_snip_border_size(self, size, snip_border_size_window):
        self.snip_border_width = size
        snip_border_size_window.destroy()
        self.snip_border_size_window_open = False

    def create_snipping_environment(self) -> None:
        self.master.withdraw()
        self.master.lower()

        # Create base snip screen and frame
        self.base_snip_screen = Toplevel(self.master)
        self.base_snip_screen.attributes("-fullscreen", True)
        self.base_snip_screen.attributes("-alpha", 0.5)

        # Colors must match to become transparent
        self.base_snip_screen.attributes("-transparent", "maroon3")
        self.snip_frame = Frame(self.base_snip_screen, background="maroon3")
        self.snip_frame.pack(fill=BOTH, expand=YES)

        # Create snipping surface (everything outside of the snip square)
        self.snip_surface = Canvas(
            self.snip_frame, cursor="cross", bg=self.outside_snip_color[-1]
        )
        self.snip_surface.pack(fill=BOTH, expand=YES)
        # Create snipping coordinates
        if self.snip_coordinates_toggle:
            self.coords_label_window = Toplevel()
            self.coords_label_window.attributes("-topmost", True)
            self.coords_label_window.overrideredirect(True)
            self.coords_label = Label(
                self.coords_label_window, background="white", foreground="black"
            )
            self.coords_label.pack()
            self.coords_label_window.withdraw()

        self.snip_surface.bind("<ButtonPress-1>", self.on_snip_button_press)
        self.snip_surface.bind("<B1-Motion>", self.on_snip_drag)
        self.snip_surface.bind("<ButtonRelease-1>", self.on_drag_release)

    def on_snip_button_press(self, event: Event) -> None:
        "Saves the inital position of the rectangle on the screan"
        self.rect = SnipRectangle(x1=event.x, y1=event.y)
        self.snip_surface.create_rectangle(0, 0, 1, 1,
            outline=self.snip_border_color[-1],
            width=self.snip_border_width,
            fill="maroon3",
        )

    def on_snip_drag(self, event: Event) -> None:
        self.rect.x2, self.rect.y2 = (event.x, event.y)
        self.snip_surface.coords(
            1, self.rect.x1, self.rect.y1, self.rect.x2, self.rect.y2
        )
        if self.snip_coordinates_toggle:
            self.coords_label_window.deiconify()
            x, y = self.snip_surface.winfo_pointerxy()
            self.coords_label_window.geometry(f"+{x}+{y}")
            self.coords_label.config(text=f"X:{self.rect.x2} Y:{self.rect.y2}")

    def on_drag_release(self, event: Event) -> None:
        self.snip_surface.destroy()
        if self.snip_coordinates_toggle:
            self.coords_label_window.destroy()
        self.base_snip_screen.withdraw()
        bounded_screenshot(self.snip_save_directory, self.rect.bounds)
        self.master.deiconify()
        return event
