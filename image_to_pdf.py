from tkinter import Tk, Toplevel, Button, Frame, Canvas, Scrollbar, filedialog, LEFT, messagebox
from PIL import Image, ImageTk
import sys, os

# -------------------- RESOURCE PATH --------------------
def resource_path(relative_path):
    """ Get absolute path to resource (works for dev and for PyInstaller exe) """
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# -------------------- SPLASH SCREEN --------------------
def show_splash(duration=2000):
    splash = Toplevel()  # separate window
    splash.overrideredirect(True)  # no title bar
    splash.geometry("500x300+{}+{}".format(
        (splash.winfo_screenwidth() - 500) // 2,
        (splash.winfo_screenheight() - 300) // 2
    ))
    splash.config(bg="white")

    # Load splash image
    img = Image.open(resource_path("splash.png"))
    tk_img = ImageTk.PhotoImage(img)
    label = Button(splash, image=tk_img, border=0, bg="white", activebackground="white")
    label.image = tk_img
    label.pack(expand=True)

    splash.update()
    return splash, duration

# -------------------- MAIN APP --------------------
app = Tk()
app.withdraw()  # hide main window initially
app.update_idletasks()

splash, splash_duration = show_splash()

def start_app():
    splash.destroy()
    app.deiconify()  # show main window

app.after(splash_duration, start_app)

app.title("Image to PDF Converter")
app.geometry("900x750")
try:
    app.iconbitmap(resource_path("app_icon.ico"))
except:
    pass  # ignore if icon missing

# -------------------- DATA --------------------
image_paths = []
thumbnail_widgets = []
thumbnails = []
drag_data = {"start_widget": None}
COLUMNS = 4   # thumbnails per row

# -------------------- SCROLLABLE AREA --------------------
canvas = Canvas(app)
scrollbar = Scrollbar(app, orient="vertical", command=canvas.yview)
scrollable_frame = Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# -------------------- BUTTONS --------------------
top_buttons = Frame(app)
top_buttons.pack(pady=10)

add_btn = Button(top_buttons, text="Add Images", command=lambda: add_images())
add_btn.pack(side=LEFT, padx=5)

clear_all_btn = Button(top_buttons, text="Clear All", command=lambda: clear_all_images())
clear_all_btn.pack(side=LEFT, padx=5)

export_btn = Button(top_buttons, text="Export to PDF", command=lambda: export_to_pdf())
export_btn.pack(side=LEFT, padx=5)

# -------------------- FUNCTIONS --------------------
def add_images():
    files = filedialog.askopenfilenames(
        title="Select Images",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
    )
    for file in files:
        image_paths.append(file)
        create_thumbnail(file)

def create_thumbnail(path):
    img = Image.open(path)
    img.thumbnail((120, 120))
    tk_img = ImageTk.PhotoImage(img)
    thumbnails.append(tk_img)  # prevent garbage collection

    frame = Frame(scrollable_frame, bd=1, relief="solid")
    frame.image_path = path
    thumbnail_widgets.append(frame)

    # IMAGE BUTTON
    label = Button(frame, image=tk_img)
    label.pack()

    # REMOVE BUTTON
    remove_btn = Button(frame, text="×", fg="red", command=lambda f=frame: remove_thumbnail(f))
    remove_btn.place(x=95, y=0)

    # DRAG EVENTS
    label.bind("<ButtonPress-1>", on_drag_start)
    label.bind("<ButtonRelease-1>", on_drag_release)

    redraw_grid()

def remove_thumbnail(frame):
    index = thumbnail_widgets.index(frame)
    thumbnail_widgets.pop(index)
    image_paths.pop(index)
    thumbnails.pop(index)
    frame.destroy()
    redraw_grid()

def clear_all_images():
    global image_paths, thumbnail_widgets, thumbnails
    for frame in thumbnail_widgets:
        frame.destroy()
    image_paths.clear()
    thumbnail_widgets.clear()
    thumbnails.clear()

def export_to_pdf():
    if not image_paths:
        messagebox.showwarning("No Images", "Please add images first.")
        return

    output_path = filedialog.asksaveasfilename(
        title="Save PDF as...",
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")]
    )

    if not output_path:
        return

    try:
        images = [Image.open(p).convert("RGB") for p in image_paths]

        if len(images) == 1:
            images[0].save(output_path, "PDF", quality=95, optimize=True)
        else:
            images[0].save(
                output_path,
                save_all=True,
                append_images=images[1:],
                quality=95,
                optimize=True
            )

        messagebox.showinfo("Success", f"PDF saved at:\n{output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")

# -------------------- DRAG LOGIC --------------------
def on_drag_start(event):
    drag_data["start_widget"] = event.widget.master
    start = drag_data["start_widget"]
    start.config(bd=3, relief="raised", highlightbackground="blue", highlightcolor="blue", bg="#e0f7ff")

def on_drag_release(event):
    start = drag_data["start_widget"]
    if not start:
        return

    start.config(bd=1, relief="solid", bg=app.cget("bg"))

    x, y = event.widget.winfo_pointerxy()
    target = event.widget.winfo_containing(x, y)

    while target and target not in thumbnail_widgets:
        target = target.master

    if target and target != start:
        swap_widgets(start, target)

    drag_data["start_widget"] = None

def swap_widgets(w1, w2):
    i1 = thumbnail_widgets.index(w1)
    i2 = thumbnail_widgets.index(w2)
    thumbnail_widgets[i1], thumbnail_widgets[i2] = thumbnail_widgets[i2], thumbnail_widgets[i1]
    image_paths[i1], image_paths[i2] = image_paths[i2], image_paths[i1]
    redraw_grid()

# -------------------- GRID REDRAW --------------------
def redraw_grid():
    for i, widget in enumerate(thumbnail_widgets):
        row = i // COLUMNS
        col = i % COLUMNS
        widget.grid(row=row, column=col, padx=10, pady=10)

# -------------------- RUN APP --------------------
app.mainloop()