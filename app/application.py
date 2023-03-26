from tkinter import *
from tkinter import colorchooser
from screenshot_tools import SnipRectangle, bounded_screenshot


class Application:
    def __init__(self, master: Tk) -> None:
        self.master = master

        self.master.geometry("400x50+200+200")
        self.master.title("Lil Snippy")

        self.add_menu_bar()
        self.menu_frame = Frame(master)
        self.menu_frame.pack(fill=BOTH, expand=YES, padx=1, pady=1)
        self.add_menu_buttons()

        self.outside_snip_color = ["#a0a0a0"]

    def add_menu_buttons(self) -> None:
        self.menu_button_bar = Frame(self.menu_frame)
        self.menu_button_bar.pack()

        self.snipButton = Button(
            self.menu_button_bar,
            width=5,
            height=5,
            command=self.create_snipping_environment,
            background="green",
        )
        self.snipButton.pack()

    def add_menu_bar(self) -> None:
        self.menu_bar = Menu(self.master)
        self.master.config(menu=self.menu_bar)

        file_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Quit", command=self.master.quit)

        options_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Customize", menu=options_menu)
        options_menu.add_command(label="Colors", command=self.open_color_window)

        about_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="About", menu=about_menu)
        about_menu.add_command(label="Info", command=self.master.quit)

    def open_color_window(self):
        self.outside_snip_color = colorchooser.askcolor()

    def close_slider_window(self, slider_window):
        slider_window.destroy()
        self.slider_window_open = False

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
        """Saves the inital position of the rectangle on the screan"""
        self.rect = SnipRectangle(x1=event.x, y1=event.y)
        self.snip_surface.create_rectangle(
            0, 0, 1, 1, outline="red", width=3, fill="maroon3"
        )

    def on_snip_drag(self, event: Event) -> None:
        self.coords_label_window.deiconify()
        self.rect.x2, self.rect.y2 = (event.x, event.y)
        self.snip_surface.coords(
            1, self.rect.x1, self.rect.y1, self.rect.x2, self.rect.y2
        )
        x, y = self.snip_surface.winfo_pointerxy()
        self.coords_label_window.geometry(f"+{x}+{y}")
        self.coords_label.config(text=f"X:{self.rect.x2} Y:{self.rect.y2}")

    def on_drag_release(self, event: Event) -> None:
        self.snip_surface.destroy()
        self.coords_label_window.destroy()
        self.base_snip_screen.withdraw()
        bounded_screenshot(self.rect.bounds)
        self.master.deiconify()
        return event
