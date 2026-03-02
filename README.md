# 🖼️ Image to PDF Desktop App by Omell

A simple desktop application built with Python and Tkinter that allows users to:

- Add multiple images
- Preview thumbnails
- Drag to reorder images
- Clear added images
- Export all images into a single PDF
- Splash screen on startup
- Packaged into a Windows EXE

---

## 🚀 Features

✔ Drag-and-drop style reordering  
✔ Thumbnail preview grid   
✔ Clear all images  
✔ Export to high-quality merged PDF  
✔ Splash screen and custom app icon  

---

## 🛠️ Tech Stack

- Python
- Tkinter (GUI)
- Pillow (image processing)
- PyInstaller (packaging)

---

## ▶️ Run from source

1. Install Python 3.10+
2. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Run
```bash
python image_to_pdf.py
```

---

## 🏗️ Build EXE
```bash
pyinstaller --onefile --noconsole ^
--icon=app_icon.ico ^
--add-data "app_icon.ico;." ^
--add-data "splash.png;." ^
image_to_pdf.py
```

---

### The EXE will appear in:
```bash
dist/
```
---

## 🎯 Purpose of this project

This project was built as part of my journey to learn Python by solving real-world problems through small, practical applications.

---

## 📸 Screenshots


---

## 👨‍💻 Author - Omell Mwanza
Aspiring software developer exploring Python, Flutter, and real-world application design.