# MARK2DE

**Merging and Annotation of RNA for Quantification to Differential Expression**

MARK2DE is a user-friendly graphical tool designed to integrate multiple steps of RNA-seq analysis, consolidating annotation, quantification, and gene count data for downstream differential expression (DE) analysis.

---

## 🎯 Objective

   MARK2DE was developed to automate and standardize the preparation of genome-guided RNA-seq data for differential gene expression analysis, following well-established workflows used in interspecies or treatment comparison studies.

---

## 🧬 Methodology

   The tool supports the following genome-guided RNA-seq pipeline:

   1. **Genome-guided transcriptome alignment using HISAT2**
      RNA-seq reads, pre-processed with tools like Trimmomatic, are aligned to the reference genome using **HISAT2** (Kim et al., 2015).

   2. **Transcript assembly and quantification with StringTie**
      Using the alignments, **StringTie** (Pertea et al., 2015) assembles transcripts and provides TPM abundance estimates.

   3. **Similarity-based annotation using BLASTn**
      Transcripts are identified with local **BLASTn** (Cock et al., 2015) against a NCBI GeneBank database.

   4. **Gene count quantification using FeatureCounts**
      Raw read counts are obtained with **FeatureCounts** (Liao et al., 2014) for DE analysis.

   > MARK2DE integrates the outputs from these tools, and the NCBI GeneBank database gene list, to generate annotated tables with TPM and raw counts, ready for downstream analysis with packages like DESeq2 or EdgeR.

   > Its is strongly advised that these tools (1-4) are used within Galaxy (The Galaxy Community, 2024; https://usegalaxy.org/).

---

## 🧰 Features

   The interface includes three main tabs:

   ### 1. Annotation and Quantification

      * Imports gene list (.tabular), BLAST output, StringTie and FeatureCounts files;
      * Integrates and annotates transcripts, generating final tables with TPM and counts;
      * Exports a consolidated `.tabular` file.

   ### 2. Combine Files to Triplicates

      * Combines three annotated files (e.g., replicates of the same condition);
      * Allows sample naming;
      * Generates a matrix with sample-specific columns.

   ### 3. Combine Triplicates to DE

      * Combines two triplicate datasets (e.g., different conditions) for DE analysis;
      * Allows group naming (e.g., WT vs MT);
      * Outputs a final table with GeneID and six sample columns ready for downstream DE analysis.

---

## 🖥️ Requirements

   * Python 3.8+
   * Dependencies:

     * `tkinter`
     * `pandas`
     * `Pillow`

   Install via `pip`:

      ```bash
      pip install pandas pillow
      ```

---

## ▶️ How to Run

   ```bash
   python main.py
   ```

---

## 📜 Citation

   > Rocha, D. (2025). *MARK2DE: Merging and Annotation of RNA for Quantification and Differential Expression Analysis* (v1.0) \[Computer software]. Zenodo. [https://doi.org/10.5281/zenodo.xxxxxxxx](https://doi.org/10.5281/zenodo.xxxxxxxx)

---

## 📚 References

   * Kim, D., et al. (2015). HISAT: a fast spliced aligner with low memory requirements. *Nature Methods*, 12(4), 357–360.
   * Pertea, M., et al. (2015). StringTie enables improved reconstruction of a transcriptome from RNA-seq reads. *Nature Biotechnology*, 33(3), 290–295.
   * Cock, P. J. A., et al. (2015). BLAST+: architecture and applications. *BMC Bioinformatics*, 16, 1–9.
   * Liao, Y., et al. (2014). FeatureCounts: an efficient general-purpose program for assigning sequence reads to genomic features. *Bioinformatics*, 30(7), 923–930.
   * The Galaxy Community. (2024). The Galaxy platform for accessible, reproducible, and collaborative data analyses: 2024 update. *Nucleic Acids Research*, p. gkae410, 2024. https://doi.org/10.1093/nar/gkae410

---

## 👨‍💻 Author

   Prof. Danilo Massuia Rocha
   ORCID https://orcid.org/0000-0003-0059-7962
   danilo.rocha@unesp.br

   Department of Biology / Departamento de Biologia 
   School of Agricultural and Veterinary Sciences / Faculdade de Ciências Agrárias e Veterinárias – FCAV
   São Paulo State University "Júlio de Mesquita Filho" / Universidade Estadual Paulista "Julio Mesquita Filho" - UNESP Jaboticabal
   Jaboticabal, Sao Paulo, Brazil.
