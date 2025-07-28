import pandas as pd
import os
from tkinter import filedialog, Button, Label, messagebox, Entry, StringVar, Frame as TkFrame
from tkinter.ttk import Frame
from scrollbar import with_scrollable_container

class CombineSamplesTab(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.setup_variables()
        self.create_widgets()
        
    def setup_variables(self):
        self.file1_var = StringVar()
        self.file2_var = StringVar()
        self.file3_var = StringVar()
        self.output_folder_var = StringVar()
        
    def create_widgets(self):
        scrollable = with_scrollable_container(self)
        container = TkFrame(scrollable)
        container.pack(padx=20, pady=20, anchor="n")

        # Title
        Label(container, text="2. Combine Files to Triplicates",
            font=("Segoe UI", 12, "bold"), fg="#2e8b8d", justify="center").grid(
            row=0, column=0, columnspan=4, pady=(0, 5))

        # Description
        Label(container, text="Select three output files from '1. Annotation and Quantification' and name each sample",
            font=("Segoe UI", 10), fg="#2e8b8d", wraplength=600, justify="center").grid(
            row=1, column=0, columnspan=4, pady=(0, 5))

        # Instruction
        Label(container, text="Use the buttons below to select replicates from a same speacies/treatment",
            font=("Segoe UI", 10, "bold"), fg="black", justify="center").grid(
            row=2, column=0, columnspan=4, pady=(0, 15))

        # File 1
        Button(container, text="Select File 1", command=lambda: self.select_file(self.file1_var, self.file1_label)).grid(row=3, column=0, sticky="e")
        self.file1_label = Label(container, text="No file selected", fg="blue")
        self.file1_label.grid(row=3, column=1, columnspan=3, sticky="w")

        # File 2
        Button(container, text="Select File 2", command=lambda: self.select_file(self.file2_var, self.file2_label)).grid(row=4, column=0, sticky="e")
        self.file2_label = Label(container, text="No file selected", fg="blue")
        self.file2_label.grid(row=4, column=1, columnspan=3, sticky="w")

        # File 3
        Button(container, text="Select File 3", command=lambda: self.select_file(self.file3_var, self.file3_label)).grid(row=5, column=0, sticky="e")
        self.file3_label = Label(container, text="No file selected", fg="blue")
        self.file3_label.grid(row=5, column=1, columnspan=3, sticky="w")

        # Sample names
        Label(container, text="Sample 1 name:").grid(row=6, column=0, sticky="e", pady=(15, 2))
        self.sample1_entry = Entry(container, width=30)
        self.sample1_entry.grid(row=6, column=1, columnspan=2, pady=(15, 2), sticky="w")

        Label(container, text="Sample 2 name:").grid(row=7, column=0, sticky="e", pady=2)
        self.sample2_entry = Entry(container, width=30)
        self.sample2_entry.grid(row=7, column=1, columnspan=2, pady=2, sticky="w")

        Label(container, text="Sample 3 name:").grid(row=8, column=0, sticky="e", pady=2)
        self.sample3_entry = Entry(container, width=30)
        self.sample3_entry.grid(row=8, column=1, columnspan=2, pady=2, sticky="w")

        # Output Section
        output_frame = Frame(container)
        output_frame.grid(row=9, column=0, columnspan=4, pady=(20, 10))

        Label(output_frame, text="Select output folder:", font=("Segoe UI", 10, "bold")).pack()
        Button(output_frame, text="Browse", command=self.select_output_folder).pack()
        self.output_folder_label = Label(output_frame, text="No folder selected", fg="blue")
        self.output_folder_label.pack()

        Label(output_frame, text="Output filename (without extension):", font=("Segoe UI", 10, "bold")).pack(pady=(10, 0))
        self.output_name_entry = Entry(output_frame, width=30)
        self.output_name_entry.pack()

        Label(output_frame, text="The file will be saved with .tabular extension", fg="gray").pack()

        Button(output_frame, text="Combine Files", command=self.combine_files,
            bg="#2e8b8d", fg="white", font=("Segoe UI", 10, "bold")).pack(pady=20)

    def select_file(self, entry_var, label_widget):
        file = filedialog.askopenfilename(title="Select output file from blastRNAnotate", 
                                        filetypes=[("Tabular files", "*.tabular")])
        if file:
            entry_var.set(file)
            label_widget.config(text=os.path.basename(file))

    def select_output_folder(self):
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            self.output_folder_var.set(folder)
            self.output_folder_label.config(text=folder)

    def combine_files(self):
        # Get file paths
        file1 = self.file1_var.get()
        file2 = self.file2_var.get()
        file3 = self.file3_var.get()
        output_folder = self.output_folder_var.get()
        output_name = self.output_name_entry.get().strip()
        
        # Get sample names
        sample1 = self.sample1_entry.get().strip()
        sample2 = self.sample2_entry.get().strip()
        sample3 = self.sample3_entry.get().strip()
        
        # Validate inputs
        if not all([file1, file2, file3]):
            messagebox.showerror("Error", "Please select all three input files")
            return
        
        if not output_folder:
            messagebox.showerror("Error", "Please select an output folder")
            return
        
        if not output_name:
            messagebox.showerror("Error", "Please provide an output filename")
            return
        
        if not all([sample1, sample2, sample3]):
            messagebox.showerror("Error", "Please provide names for all three samples")
            return
        
        # Check for duplicate sample names
        sample_names = [sample1, sample2, sample3]
        if len(sample_names) != len(set(sample_names)):
            messagebox.showerror("Error", "Sample names must be unique")
            return
        
        try:
            # Read files with tab separator
            df1 = pd.read_csv(file1, sep='\t')
            df2 = pd.read_csv(file2, sep='\t')
            df3 = pd.read_csv(file3, sep='\t')
            
            # Verify required columns exist
            for i, df in enumerate([df1, df2, df3], 1):
                if 'NCBI GeneID' not in df.columns:
                    raise ValueError(f"File {i} is missing 'NCBI GeneID' column")
                if 'Counts-FeatureCounts' not in df.columns:
                    raise ValueError(f"File {i} is missing 'Counts-FeatureCounts' column")
            
            # Create merged dataframe
            merged = pd.DataFrame()
            merged['GeneID'] = df1['NCBI GeneID']
            
            # Verify GeneIDs match
            if not (merged['GeneID'].equals(df2['NCBI GeneID']) and 
                    merged['GeneID'].equals(df3['NCBI GeneID'])):
                raise ValueError("Gene IDs do not match across all files")
            
            # Add counts with custom names
            merged[sample1] = df1['Counts-FeatureCounts']
            merged[sample2] = df2['Counts-FeatureCounts']
            merged[sample3] = df3['Counts-FeatureCounts']
            
            # Ensure the filename has .tabular extension
            if not output_name.lower().endswith('.tabular'):
                output_name += '.tabular'
            
            # Create output path
            output_path = os.path.join(output_folder, output_name)
            
            # Check if file exists and ask for confirmation
            if os.path.exists(output_path):
                if not messagebox.askyesno("Warning", f"File {output_name} already exists. Overwrite?"):
                    return
            
            # Save output as tabular file
            merged.to_csv(output_path, sep='\t', index=False)
            
            messagebox.showinfo("Success", f"File successfully created:\n{output_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")