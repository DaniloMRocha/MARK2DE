import pandas as pd
import os
from tkinter import filedialog, Button, Label, messagebox, Entry, StringVar, Frame as TkFrame
from tkinter.ttk import Frame
from scrollbar import with_scrollable_container

class CombineTriplicatesTab(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.setup_variables()
        self.create_widgets()

    def setup_variables(self):
        self.file1_var = StringVar()
        self.file2_var = StringVar()
        self.output_file_var = StringVar()

    def create_widgets(self):
        scrollable = with_scrollable_container(self)
        container = TkFrame(scrollable)
        container.pack(padx=20, pady=20, anchor="n")

        Label(container, text="3. Combine Triplicates to DE", font=("Segoe UI", 12, "bold"), fg="#2e8b8d").pack(pady=(10, 0))

        Label(container, text="Combine triplicates of different samples/treatments from '2. Combine Files to Triplicates' to generate an output ready for Differential Expression",
              font=("Segoe UI", 10), fg="#2e8b8d", wraplength=600, justify="center").pack(pady=(0, 15))

        Button(container, text="Select First Triplicate File", command=lambda: self.select_file(self.file1_var, self.file1_label)).pack()
        self.file1_label = Label(container, text="No file selected", fg="blue")
        self.file1_label.pack()

        Button(container, text="Select Second Triplicate File", command=lambda: self.select_file(self.file2_var, self.file2_label)).pack()
        self.file2_label = Label(container, text="No file selected", fg="blue")
        self.file2_label.pack()

        Label(container, text="Group 1 name (First Triplicate):").pack(pady=(10, 0))
        self.group1_entry = Entry(container, width=30)
        self.group1_entry.pack()

        Label(container, text="Group 2 name (Second Triplicate):").pack(pady=(5, 0))
        self.group2_entry = Entry(container, width=30)
        self.group2_entry.pack()

        Label(container, text="Select output folder:", font=("Segoe UI", 10, "bold")).pack(pady=(15, 0))
        Button(container, text="Browse", command=self.select_output_folder).pack()
        self.output_folder_label = Label(container, text="No folder selected", fg="blue")
        self.output_folder_label.pack()

        Label(container, text="Output filename (without extension):", font=("Segoe UI", 10, "bold")).pack(pady=(10, 0))
        self.output_name_entry = Entry(container, width=30)
        self.output_name_entry.pack()
        Label(container, text="The file will be saved with .tabular extension", fg="gray").pack()

        Button(container, text="Combine Triplicates", command=self.combine_triplicates, bg="#2e8b8d", fg="white",
               font=('Segoe UI', 10, 'bold')).pack(pady=20)

    def select_file(self, entry_var, label_widget):
        file = filedialog.askopenfilename(title="Select counts file", 
                                          filetypes=[("Tabular files", "*.tabular")])
        if file:
            entry_var.set(file)
            label_widget.config(text=os.path.basename(file))

    def select_output_folder(self):
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            self.output_file_var.set(folder)
            self.output_folder_label.config(text=folder)

    def combine_triplicates(self):
        file1 = self.file1_var.get()
        file2 = self.file2_var.get()
        output_folder = self.output_file_var.get()
        output_name = self.output_name_entry.get().strip()

        if not output_folder:
            messagebox.showerror("Error", "Please select an output folder")
            return
        if not output_name:
            messagebox.showerror("Error", "Please provide an output filename")
            return

        output_file = os.path.join(output_folder, output_name + ".tabular")
        group1 = self.group1_entry.get().strip()
        group2 = self.group2_entry.get().strip()

        if not all([file1, file2]):
            messagebox.showerror("Error", "Please select both input files")
            return

        if not output_file:
            messagebox.showerror("Error", "Please select an output file")
            return

        if not all([group1, group2]):
            messagebox.showerror("Error", "Please provide names for both groups")
            return

        try:
            df1 = pd.read_csv(file1, sep='\t')
            df2 = pd.read_csv(file2, sep='\t')

            for i, df in enumerate([df1, df2], 1):
                if 'GeneID' not in df.columns:
                    raise ValueError(f"File {i} is missing 'GeneID' column")
                if df.shape[1] < 4:
                    raise ValueError(f"File {i} doesn't contain triplicate data (needs GeneID + 3 sample columns)")

            if not df1['GeneID'].equals(df2['GeneID']):
                raise ValueError("Gene IDs do not match between the two files")

            samples1 = df1.columns[1:4]
            samples2 = df2.columns[1:4]

            merged = pd.DataFrame()
            merged['GeneID'] = df1['GeneID']

            for i, col in enumerate(samples1, 1):
                merged[f"{group1}{i}"] = df1[col]

            for i, col in enumerate(samples2, 1):
                merged[f"{group2}{i}"] = df2[col]

            if os.path.exists(output_file):
                if not messagebox.askyesno("Warning", f"File {os.path.basename(output_file)} already exists. Overwrite?"):
                    return

            merged.to_csv(output_file, sep='\t', index=False)
            messagebox.showinfo("Success", f"File successfully created:\n{output_file}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
