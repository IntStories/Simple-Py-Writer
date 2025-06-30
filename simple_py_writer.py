import tkinter as tk
from tkinter import filedialog, font, simpledialog, messagebox
import os

class SimpleWriter:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Writer")

        self.font_family = "Arial"
        self.font_size = 12
        self.dark_mode = False
        self.fullscreen = False

        self.setup_toolbar()

        self.text = tk.Text(root, wrap="word", undo=True)
        self.text.pack(expand=1, fill="both")

        self.update_font()
        self.set_theme("light")

        # Bindings
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)
        self.text.bind("<Control-BackSpace>", self.delete_prev_word)

    def setup_toolbar(self):
        self.toolbar = tk.Frame(self.root)
        self.toolbar.pack(side="top", fill="x")

        tk.Button(self.toolbar, text="Open", command=self.open_file).pack(side="left")
        tk.Button(self.toolbar, text="Save", command=self.save_file).pack(side="left")
        tk.Button(self.toolbar, text="A+", command=self.increase_font).pack(side="left")
        tk.Button(self.toolbar, text="A–", command=self.decrease_font).pack(side="left")
        tk.Button(self.toolbar, text="Font", command=self.change_font).pack(side="left")
        tk.Button(self.toolbar, text="Slider", command=self.show_slider).pack(side="left")
        tk.Button(self.toolbar, text="TTF", command=self.load_custom_font).pack(side="left")
        tk.Button(self.toolbar, text="Dark", command=self.toggle_theme).pack(side="left")
        tk.Button(self.toolbar, text="Fullscreen", command=self.toggle_fullscreen).pack(side="left")

    # === Core functionality ===

    def open_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if filepath:
            with open(filepath, "r", encoding="utf-8") as f:
                self.text.delete(1.0, tk.END)
                self.text.insert(tk.END, f.read())

    def save_file(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Text Files", "*.txt")])
        if filepath:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(self.text.get(1.0, tk.END).rstrip())

    def update_font(self):
        new_font = font.Font(family=self.font_family, size=self.font_size)
        self.text.config(font=new_font)

    def increase_font(self):
        self.font_size += 2
        self.update_font()

    def decrease_font(self):
        self.font_size -= 2
        self.update_font()

    def show_slider(self):
        top = tk.Toplevel(self.root)
        top.title("Adjust Font Size")

        slider = tk.Scale(top, from_=8, to=48, orient="horizontal", length=300,
                          label="Font Size", command=self.set_font_size)
        slider.set(self.font_size)
        slider.pack(padx=10, pady=10)

    def set_font_size(self, value):
        self.font_size = int(value)
        self.update_font()

    def change_font(self):
        fonts = list(font.families())
        fonts.sort()
        selected = simpledialog.askstring("Font", "Enter font name:", initialvalue=self.font_family)
        if selected in fonts:
            self.font_family = selected
            self.update_font()
        else:
            messagebox.showerror("Error", "Font not found.")

    def load_custom_font(self):
        file_path = filedialog.askopenfilename(filetypes=[("TrueType Font", "*.ttf")])
        if file_path and os.path.isfile(file_path):
            try:
                font_name = os.path.basename(file_path).split(".")[0]
                font.Font(name=font_name, file=file_path)
                self.font_family = font_name
                self.update_font()
            except Exception as e:
                messagebox.showerror("Error", f"Could not load font: {e}")

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.set_theme("dark" if self.dark_mode else "light")

    def set_theme(self, theme):
        if theme == "dark":
            self.text.config(bg="#1e1e1e", fg="white", insertbackground="white")
        else:
            self.text.config(bg="white", fg="black", insertbackground="black")

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)

    def exit_fullscreen(self, event=None):
        if self.fullscreen:
            self.fullscreen = False
            self.root.attributes("-fullscreen", False)

    def delete_prev_word(self, event=None):
        index = self.text.index(tk.INSERT)
        line, char = map(int, index.split("."))
        if char == 0 and line == 1:
            return "break"
        start = self.text.search(r"\s", index, backwards=True, regexp=True)
        if not start:
            start = "1.0"
        self.text.delete(start, index)
        return "break"


if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleWriter(root)
    root.mainloop()
