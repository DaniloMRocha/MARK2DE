from tkinter import Tk, Frame as TkFrame, Button, LEFT, BOTH, TOP, PhotoImage, Label
from PIL import Image, ImageTk
from annotation_tab import AnnotationTab
from combine3_tab import CombineSamplesTab
from triplicates_tab import CombineTriplicatesTab

import os

class RNAseqToolkit:
    def __init__(self, root):
        self.root = root
        self.root.title("MARK2DE")
        self.root.geometry("1000x750")
        self.root.configure(bg='white')

        self.create_layout()

    def create_layout(self):
        # Left side (menu)
        self.sidebar = TkFrame(self.root, width=260, bg='white')
        self.sidebar.pack(side=LEFT, fill='y')

        # Content area
        self.content_frame = TkFrame(self.root, bg='white')
        self.content_frame.pack(side=LEFT, fill=BOTH, expand=True)

        self.create_sidebar()
        self.load_frame("annotation")

    def create_sidebar(self):
        
        # Path to main.py
        base_dir = os.path.dirname(__file__)
        logo_path = None
        # Logo
        for fname in os.listdir(base_dir):
            if fname.lower().startswith("mark2de_logo"):
                logo_path = os.path.join(base_dir, fname)
                break

        if logo_path is None:
            raise FileNotFoundError("'Mark2DE_logo' not found.")
        logo_image = Image.open(logo_path).resize((80, 80))
        logo_photo = ImageTk.PhotoImage(logo_image)
        logo_label = Label(self.sidebar, image=logo_photo, bg='white')
        logo_label.image = logo_photo
        logo_label.pack(pady=(20, 5))

        # Title
        Label(self.sidebar, text="MARK2DE", font=("Segoe UI", 16, "bold"), fg="#2e8b8d", bg='white').pack(anchor='center')

        # Subtitle
        subtitle = (
            "Merging and Annotation\n"
            "of RNA for Quantification\n"
            "and Differential Expression analysis"
        )

        Label(
            self.sidebar,
            text=subtitle,
            font=("Segoe UI", 9),
            fg="gray",
            bg='white',
            justify='center'
        ).pack(pady=(0, 20), anchor='center')
        
        # Nabegation
        Button(self.sidebar, text="1. Annotation and Quantification", width=26, bg="#2e8b8d", fg="white", command=lambda: self.load_frame("annotation")).pack(pady=5)
        Button(self.sidebar, text="2. Combine Files to Triplicates", width=26, bg="#2e8b8d", fg="white", command=lambda: self.load_frame("combine")).pack(pady=5)
        Button(self.sidebar, text="3. Combine Triplicates to DE", width=26, bg="#2e8b8d", fg="white", command=lambda: self.load_frame("triplicates")).pack(pady=5)

    def load_frame(self, name):
        # Remove last content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Add corresponding frame
        if name == "annotation":
            AnnotationTab(self.content_frame).pack(fill=BOTH, expand=True)
        elif name == "combine":
            CombineSamplesTab(self.content_frame).pack(fill=BOTH, expand=True)
        elif name == "triplicates":
            CombineTriplicatesTab(self.content_frame).pack(fill=BOTH, expand=True)

if __name__ == "__main__":
    root = Tk()
    app = RNAseqToolkit(root)
    root.mainloop()
