import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from .processor import Processor
import os

class Ui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Skintils")
        self.root.geometry("400x320")
        self.root.resizable(False, False)
        self.root.minsize(350, 250)
        self.center_window()
        
        self.osu_path = None
        self.selected_skin = None
        self.skin_path = None
        
        self.setup()
        self.processor = Processor()
        self.find_osu_directory()
        self.root.mainloop()

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def setup(self):
        self.root.columnconfigure(0, weight=1)
        
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N))
        main_frame.columnconfigure(0, weight=1)
        
        dir_frame = ttk.LabelFrame(main_frame, text="osu! Directory", padding="10")
        dir_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        dir_frame.columnconfigure(0, weight=1)
        
        dir_content_frame = ttk.Frame(dir_frame)
        dir_content_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        dir_content_frame.columnconfigure(0, weight=1)
        
        self.osu_label = ttk.Label(dir_content_frame, text="Not found", foreground="red")
        self.osu_label.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(dir_content_frame, text="Browse Directory", 
                  command=self.browse_osu_directory).grid(row=0, column=1)
        
        skin_frame = ttk.LabelFrame(main_frame, text="Skin Selection", padding="10")
        skin_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        skin_frame.columnconfigure(0, weight=1)
        
        self.skin_var = tk.StringVar()
        self.skin_dropdown = ttk.Combobox(skin_frame, textvariable=self.skin_var, 
                                         state="readonly")
        self.skin_dropdown.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        self.skin_dropdown.bind('<<ComboboxSelected>>', self.on_skin_selected)

        actions_frame = ttk.LabelFrame(main_frame, text="Actions", padding="10")
        actions_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        actions_frame.columnconfigure(0, weight=1)
        
        self.triplestack_btn = ttk.Button(actions_frame, text="Triplestack Circles", 
                                         command=self.triplestack_circles, state="disabled")
        self.triplestack_btn.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        self.instafade_btn = ttk.Button(actions_frame, text="Instafade Circles", 
                                       command=self.instafade_circles, state="disabled")
        self.instafade_btn.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        self.font_btn = ttk.Button(actions_frame, text="Apply Font File", 
                                  command=self.apply_font_file, state="disabled")
        self.font_btn.grid(row=2, column=0, sticky=(tk.W, tk.E))

    def find_osu_directory(self):
        localappdata = os.environ.get('LOCALAPPDATA')
        if localappdata and os.path.exists(os.path.join(localappdata, 'osu!')):
            self.osu_path = os.path.join(localappdata, 'osu!')
            display_path = self.osu_path
            if len(display_path) > 50:
                display_path = "..." + display_path[-47:]
                
            self.osu_label.config(text=display_path, foreground="green")
            self.load_skins()

    def browse_osu_directory(self):
        directory = filedialog.askdirectory(title="Select osu! Directory")
        if directory and os.path.exists(os.path.join(directory, 'Skins')):
            self.osu_path = directory
            display_path = directory
            if len(display_path) > 50:
                display_path = "..." + display_path[-47:]
                
            self.osu_label.config(text=display_path, foreground="green")
            self.load_skins()
        elif directory:
            messagebox.showerror("Error", "Invalid osu! directory. Skins folder not found.")

    def load_skins(self):
        if not self.osu_path:
            return
        
        skins_path = os.path.join(self.osu_path, 'Skins')
        if os.path.exists(skins_path):
            skins = [d for d in os.listdir(skins_path) if os.path.isdir(os.path.join(skins_path, d))]
            self.skin_dropdown['values'] = skins
            if skins:
                self.skin_dropdown.current(0)
                self.on_skin_selected()

    def on_skin_selected(self, event=None):
        if self.skin_var.get():
            self.selected_skin = self.skin_var.get()
            self.skin_path = os.path.join(self.osu_path, 'Skins', self.selected_skin)
            self.enable_buttons()

    def enable_buttons(self):
        self.triplestack_btn.config(state="normal")
        self.instafade_btn.config(state="normal")
        self.font_btn.config(state="normal")

    def triplestack_circles(self):
        try:
            self.processor.triplestack_circles(self.skin_path)
            messagebox.showinfo("Success", "Triplestack circles applied successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply triplestack circles: {str(e)}")

    def instafade_circles(self):
        try:
            self.processor.instafade_circles(self.skin_path)
            messagebox.showinfo("Success", "Instafade circles applied successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply instafade circles: {str(e)}")

    def apply_font_file(self):
        try:
            font_path = filedialog.askopenfilename(title="Select Font File", filetypes=[("Font files", "*.ttf *.otf *.woff *.woff2")])
            if not font_path:
                return
            self.processor.apply_font_file(self.skin_path, font_path)
            messagebox.showinfo("Success", "Font applied successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply font: {str(e)}")