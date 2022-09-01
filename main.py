from tkinter import *
from dataclasses import dataclass
import pyautogui

import datetime


@dataclass()
class Rectangle:
    x1: int = 0
    y1: int = 0
    x2: int = 0
    y2: int = 0
    
    def display_position(self) -> None:
        print(self.x1)
        print(self.y1)
        print(self.x2)
        print(self.y2)


def take_bounded_screenshot(x1, y1, x2, y2):
    image = pyautogui.screenshot(region=(x1, y1, x2, y2))
    file_name = datetime.datetime.now().strftime("%f")
    image.save("snips/" + file_name + ".png")


def calc_screenshot_bounds(r: Rectangle):
    if r.x1 <= r.x2 and r.y1 <= r.y2:
        print("right down")
        take_bounded_screenshot(r.x1, r.y1, r.x2 - r.x1, r.y2 - r.y1)

    elif r.x1 >= r.x2 and r.y1 <= r.y2:
        print("left down")
        take_bounded_screenshot(r.x2, r.y1, r.x1 - r.x2, r.y2 - r.y1)

    elif r.x1 <= r.x2 and r.y1 >= r.y2:
        print("right up")
        take_bounded_screenshot(r.x1, r.y2, r.x2 - r.x1, r.y1 - r.y2)

    elif r.x1 >= r.x2 and r.y1 >= r.y2:
        print("left up")
        take_bounded_screenshot(r.x2, r.y2, r.x1 - r.x2, r.y1 - r.y2)


class Application:
    def __init__(self, master):
        self.coords_label = None
        self.snip_surface = None
        self.master = master
        self.rect = Rectangle()

        root.geometry("400x50+200+200")  # set new geometry
        root.title("Lil Snippy")

        self.menu_frame = Frame(master)
        self.menu_frame.pack(fill=BOTH, expand=YES, padx=1, pady=1)

        self.buttonBar = Frame(self.menu_frame, bg="")
        self.buttonBar.pack()

        self.snipButton = Button(
            self.buttonBar,
            width=5,
            height=5,
            command=self.create_screen_canvas,
            background="green",
        )
        self.snipButton.pack()

        self.master_screen = Toplevel(root)
        self.master_screen.withdraw()
        self.master_screen.attributes("-transparent", "maroon3")
        self.picture_frame = Frame(self.master_screen, background="maroon3")
        self.picture_frame.pack(fill=BOTH, expand=YES)

    def create_screen_canvas(self):
        self.master_screen.deiconify()
        root.withdraw()

        self.master_screen.attributes("-fullscreen", True)
        self.master_screen.attributes("-alpha", 0.5)
        self.master_screen.lift()
        self.master_screen.attributes("-topmost", True)

        self.snip_surface = Canvas(self.picture_frame, cursor="cross", bg="grey11")
        self.snip_surface.pack(fill=BOTH, expand=YES)
        self.coords_label = Label(self.snip_surface)

        self.snip_surface.bind("<ButtonPress-1>", self.on_snip_button_press)
        self.snip_surface.bind("<B1-Motion>", self.on_snip_drag)
        self.snip_surface.bind("<ButtonRelease-1>", self.on_drag_release)

    def on_drag_release(self, event):
        self.rect.display_position()
        self.snip_surface.destroy()
        self.master_screen.withdraw()
        calc_screenshot_bounds(self.rect)
        root.deiconify()
        return event

    def on_snip_button_press(self, event):
        # save mouse drag start position
        self.rect.x1 = int(self.snip_surface.canvasx(event.x))
        self.rect.y1 = int(self.snip_surface.canvasy(event.y))
        self.snip_surface.create_rectangle(
            0, 0, 1, 1, outline="red", width=3, fill="maroon3"
        )

    def on_snip_drag(self, event):
        self.rect.x2, self.rect.y2 = (event.x, event.y)
        # expand rectangle as you drag the mouse
        self.snip_surface.coords(
            1, self.rect.x1, self.rect.y1, self.rect.x2, self.rect.y2
        )
        self.coords_label.place(x=self.rect.x2, y=self.rect.y2)
        self.coords_label.config(text=f"X:{self.rect.x2} Y:{self.rect.y2}")
        self.rect.display_position()


if __name__ == "__main__":
    root = Tk()
    app = Application(root)
    root.mainloop()
