import pandas as pd
import re
import os
from tkinter import filedialog, Button, Label, messagebox, Entry, StringVar, Toplevel, Frame as TkFrame, Text
from tkinter.ttk import Frame
from tooltip import ToolTip
from scrollbar import with_scrollable_container

class AnnotationTab(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.setup_variables()
        self.create_widgets()

    def setup_variables(self):
        self.blast_file = StringVar()
        self.genelist_file = StringVar()
        self.stringtie_file = StringVar()
        self.featurecounts_file = StringVar()
        self.output_folder = StringVar()

    def create_widgets(self):
        scrollable = with_scrollable_container(self)
        container = TkFrame(scrollable)
        container.pack(padx=20, pady=20, anchor="n")

        # Title and description
        Label(container, text="1. Annotation and Quantification",
              font=("Segoe UI", 12, "bold"), fg="#2e8b8d", justify="center").pack(pady=(0, 5))

        Label(container, text="Select files for Gene Annotation by Similarity and Quantification",
              font=("Segoe UI", 10), fg="#2e8b8d", wraplength=600, justify="center").pack(pady=(0, 20))

        def labeled_row(parent, label_text, tooltip_text):
            row_frame = TkFrame(parent)
            row_frame.pack(anchor='center', pady=(5, 0))
            label = Label(row_frame, text=label_text, font=("Segoe UI", 10, "bold"))
            label.pack(side="left")
            tooltip_icon = Label(row_frame, text=" 🔍", fg="blue")
            tooltip_icon.pack(side="left")
            ToolTip(tooltip_icon, tooltip_text)

        #Gene list, BLAST, StringTie, FeatureCounts and output folder selection
        labeled_row(container, "Gene list file:", "Select a standard NCBI genelist tabular file of the genes you used for BLAST")
        Button(container, text="Select Gene List File (.tabular)", command=self.select_genelist_file).pack()
        self.genelist_label = Label(container, text="No file selected", fg="blue")
        self.genelist_label.pack()

        labeled_row(container, "BLAST output file:", "Select a standard tabular BLAST output file with 25 columns")
        Button(container, text="Select BLAST Output File (.tabular)", command=self.select_blast_file).pack()
        self.blast_label = Label(container, text="No file selected", fg="blue")
        self.blast_label.pack()

        labeled_row(container, "StringTie output file (optional):", "Select the 'Gene Abundance Estimation' output file from StringTie")
        Button(container, text="Select StringTie File (.tabular)", command=self.select_stringtie_file).pack()
        self.stringtie_label = Label(container, text="No file selected", fg="blue")
        self.stringtie_label.pack()

        labeled_row(container, "FeatureCounts output file (optional):", "Select the standard output file from FeatureCounts")
        Button(container, text="Select FeatureCounts File (.tabular)", command=self.select_featurecounts_file).pack()
        self.featurecounts_label = Label(container, text="No file selected", fg="blue")
        self.featurecounts_label.pack()

        Label(container, text="Select output folder:", font=("Segoe UI", 10, "bold"), justify="center").pack(pady=(10, 0))
        Button(container, text="Select Output Folder", command=self.select_output_folder).pack()
        self.output_folder_label = Label(container, text="No folder selected", fg="blue")
        self.output_folder_label.pack()

        Label(container, text="Output filename (without extension):", font=("Segoe UI", 10, "bold"), justify="center").pack(pady=(10, 0))
        self.output_filename_entry = Entry(container, width=40)
        self.output_filename_entry.pack()
        Label(container, text="The file will be saved with .tabular extension", fg="gray").pack()

        Button(container, text="Start Annotation", command=self.start_annotation,
               bg="#2e8b8d", fg="white", font=("Segoe UI", 10, "bold")).pack(pady=20)
        
        # Logbox
        self.log_box = Text(container, height=10, wrap="word", bg="#f8f8f8", fg="black")
        self.log_box.pack(fill="x", expand=False, padx=5, pady=(0, 10))
        self.log_box.insert("end", "Log messages will appear here.\n")
        self.log_box.config(state="disabled")

    def select_blast_file(self):
        file = filedialog.askopenfilename(title="Select BLAST output file", 
                                        filetypes=[("Tabular files", "*.tabular")])
        if file:
            self.blast_file.set(file)
            self.blast_label.config(text=file)

    def select_genelist_file(self):
        file = filedialog.askopenfilename(title="Select gene list file", 
                                        filetypes=[("Tabular files", "*.tabular")])
        if file:
            self.genelist_file.set(file)
            self.genelist_label.config(text=file)

    def select_stringtie_file(self):
        file = filedialog.askopenfilename(title="Select StringTie output file", 
                                        filetypes=[("Tabular files", "*.tabular")])
        if file:
            self.stringtie_file.set(file)
            self.stringtie_label.config(text=file)

    def select_featurecounts_file(self):
        file = filedialog.askopenfilename(title="Select FeatureCounts output file", 
                                        filetypes=[("Tabular files", "*.tabular")])
        if file:
            self.featurecounts_file.set(file)
            self.featurecounts_label.config(text=file)

    def select_output_folder(self):
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            self.output_folder.set(folder)
            self.output_folder_label.config(text=folder)

    def log(self, message):
        self.log_box.config(state="normal")
        self.log_box.insert("end", message + "\n")
        self.log_box.see("end")
        self.log_box.config(state="disabled")

    def prepare_blast(self, blast_file):
        print("🔄 Preparing the BLAST file...")
        self.log("Preparing the BLAST file...")
        try:
            df = pd.read_csv(blast_file, delimiter="\t", header=None)
            def extract_geneid(text):
                match = re.search(r"GeneID=(\d+)", str(text))
                return match.group(1) if match else None
            df['GeneID'] = df[24].apply(extract_geneid)
            df['Simplified_Transcript'] = df[0].apply(lambda x: re.sub(r"\.\d+$", "", x))
            df_result = df[['Simplified_Transcript', 2, 'GeneID']]
            df_result.columns = ['Transcript', 'Identity', 'GeneID']
            df_max_identity = df_result.loc[df_result.groupby('Transcript')['Identity'].idxmax()]
            print("✅ BLAST file prepared successfully!")
            self.log("BLAST file prepared successfully!")
            return df_max_identity
        except Exception as e:
            print(f"❌ Error preparing the BLAST file: {e}")
            self.log(f"Error preparing the BLAST file: {e}")
            return None

    def merge_genelist(self, genelist_file, blast_df):
        print("🔄 Merging BLAST with the gene list...")
        self.log("Merging BLAST with the gene list...")
        try:
            genelist_df = pd.read_csv(genelist_file, sep="\t")
            genelist_df["NCBI GeneID"] = genelist_df["NCBI GeneID"].astype(str)
            blast_df["GeneID"] = blast_df["GeneID"].astype(str)
            merged_df = pd.merge(genelist_df, blast_df, how='left', left_on='NCBI GeneID', right_on='GeneID')
            print("✅ BLAST merged with the gene list! ", merged_df.shape[0], " records.")
            self.log(f"BLAST merged with the gene list! {merged_df.shape[0]} records.")
            return merged_df
        except Exception as e:
            print(f"❌ Error merging BLAST with gene list: {e}")
            self.log(f"Error merging BLAST with gene list: {e}")
            return None

    def merge_stringtie(self, df, stringtie_file):
        print("🔄 Merging with StringTie...")
        self.log("Merging with StringTie...")
        try:
            stringtie_df = pd.read_csv(stringtie_file, sep="\t")
            if "TPM" in stringtie_df.columns:
                stringtie_df["TPM"] = pd.to_numeric(stringtie_df["TPM"], errors="coerce").fillna(0)
            df = pd.merge(df, stringtie_df, how='left', left_on='Transcript', right_on='Gene ID')
            print("✅ Table merged with StringTie! ", df.shape[0], " records.")
            self.log(f"Table merged with StringTie! {df.shape[0]} records.")
            return df
        except Exception as e:
            print(f"❌ Error merging with StringTie: {e}")
            self.log(f"Error merging with StringTie: {e}")
            return df

    def merge_featurecounts(self, df, featurecounts_file):
        print("🔄 Merging with FeatureCounts...")
        self.log("Merging with FeatureCounts...")
        try:
            featurecounts_df = pd.read_csv(featurecounts_file, sep="\t", header=None, names=["Transcript", "Count"])
            featurecounts_df["Count"] = pd.to_numeric(featurecounts_df["Count"], errors="coerce").fillna(0)
            df = pd.merge(df, featurecounts_df, how='left', left_on='Transcript', right_on='Transcript')
            print("✅ Table merged with FeatureCounts! ", df.shape[0], " records.")
            self.log(f"Table merged with FeatureCounts! {df.shape[0]} records.")
            return df
        except Exception as e:
            print(f"❌ Error merging with FeatureCounts: {e}")
            self.log(f"Error merging with FeatureCounts: {e}")
            return df

    def start_annotation(self):
        if not self.blast_file.get() or not self.genelist_file.get() or not self.output_folder.get() or not self.output_filename_entry.get():
            messagebox.showerror("Error", "Please select BLAST output, gene list, output folder, and provide a filename.")
            return

        try:
            blast_df = self.prepare_blast(self.blast_file.get())
            if blast_df is None:
                return

            merged_df = self.merge_genelist(self.genelist_file.get(), blast_df)
            if merged_df is None:
                return

            if self.stringtie_file.get():
                merged_df = self.merge_stringtie(merged_df, self.stringtie_file.get())

            if self.featurecounts_file.get():
                merged_df = self.merge_featurecounts(merged_df, self.featurecounts_file.get())

            merged_df.fillna(0, inplace=True)

            try:
                agg_functions = {
                    "Transcript": lambda x: ", ".join(sorted(set(x.astype(str)))) if any(x.notna()) else "0",
                    "Description": "first"
                }
                if self.stringtie_file.get():
                    agg_functions["TPM"] = "sum"
                if self.featurecounts_file.get():
                    agg_functions["Count"] = "sum"

                grouped_df = merged_df.groupby("NCBI GeneID", as_index=False).agg(agg_functions)

                if self.stringtie_file.get():
                    grouped_df = grouped_df.rename(columns={"TPM": "TPM-StringTie"})
                if self.featurecounts_file.get():
                    grouped_df = grouped_df.rename(columns={"Count": "Counts-FeatureCounts"})

                columns = ["NCBI GeneID", "Description", "Transcript"]
                if self.stringtie_file.get():
                    columns.append("TPM-StringTie")
                if self.featurecounts_file.get():
                    columns.append("Counts-FeatureCounts")
                grouped_df = grouped_df[columns]

                if self.stringtie_file.get():
                    grouped_df["TPM-StringTie"] = grouped_df["TPM-StringTie"].round(6)

                grouped_df["NCBI GeneID"] = pd.to_numeric(grouped_df["NCBI GeneID"], errors="coerce")
                grouped_df = grouped_df.sort_values(by="NCBI GeneID", ascending=True)

                print("✅ Data grouped and consolidated!")
            except Exception as e:
                messagebox.showerror("Error", f"Error grouping data: {str(e)}")
                return

            output_file = os.path.join(self.output_folder.get(), self.output_filename_entry.get())
            if not output_file.lower().endswith('.tabular'):
                output_file += '.tabular'

            if os.path.exists(output_file):
                if not messagebox.askyesno("Warning", f"File {os.path.basename(output_file)} exists. Overwrite?"):
                    return
                os.remove(output_file)

            grouped_df.to_csv(output_file, sep="\t", index=False)
            messagebox.showinfo("Success", f"Annotation completed!\nFile saved: {output_file}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
