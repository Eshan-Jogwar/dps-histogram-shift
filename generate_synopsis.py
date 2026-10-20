"""
Script to generate a professional, humanized College Project Synopsis
in both DOCX and Markdown formats.
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_background(cell, hex_color):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    tc_pr.append(shd)

def create_markdown_synopsis(filepath):
    content = """# PROJECT SYNOPSIS

## 1. Project Title
**Secure Reversible Data Hiding in Medical Images Using Block-Wise Histogram Shifting**

---

## 2. Base Paper Details
* **Title:** *Secure Reversible Data Hiding Using Block-Wise Histogram Shifting*
* **Authors:** Samar Kamil Khudhair, Monalisa Sahu, Raghunandan K. R., Aditya Kumar Sahu
* **Journal:** *MDPI Electronics*, Volume 12, Issue 5, Article 1222 (March 2023)
* **DOI:** [10.3390/electronics12051222](https://doi.org/10.3390/electronics12051222)
* **Foundational Reference:** *Reversible Data Hiding*, Z. Ni et al., IEEE Transactions on Circuits and Systems for Video Technology (2006).

---

## 3. Introduction & Background
In digital healthcare and telemedicine, medical scans such as X-rays, CT scans, and MRIs are constantly transmitted across public networks and stored on cloud servers. Alongside these scans, hospitals must transfer confidential patient data—including patient identity, diagnostic notes, and case history.

Standard information-hiding methods (like classic Least Significant Bit / LSB steganography) modify pixel values permanently. In regular photography, small pixel shifts are imperceptible. However, in medical diagnostics, altering pixel values can introduce visual artifacts, obscure tiny lesions, or mimic pathological conditions, which carries severe clinical and legal risks.

Reversible Data Hiding (RDH) addresses this dilemma: it embeds secret patient information inside the medical image, but upon extraction at the destination clinic or hospital, it completely restores the image back to its exact, bit-for-bit original state with zero permanent distortion.

---

## 4. Problem Statement
1. **Diagnostic Risk from Irreversible Embedding:** Conventional steganography permanently changes image pixels. Medical ethics and regulatory standards prohibit permanent alterations to diagnostic scans.
2. **Global Histogram Limitations:** Earlier reversible methods calculate a single histogram for the entire image. This approach often results in limited embedding capacity and uneven distortion across complex areas of the scan.
3. **Lack of Layered Security:** Embedding plaintext data leaves information exposed if an eavesdropper manages to intercept and reverse the embedding process.

---

## 5. Proposed Solution
To overcome these limitations, this project implements a localized, **block-wise histogram shifting** technique derived from recent 2023 research, coupled with payload security:

1. **Spatial Image Blocking:** The grayscale medical scan is divided into small, non-overlapping blocks (e.g., $8 \\times 8$ or $16 \\times 16$). Dividing into localized regions takes advantage of high local pixel correlation.
2. **Block-Level Histogram Shifting:** In each block, the algorithm identifies the peak (most frequent) pixel value and a zero/minimum bin. Intermediate pixels are shifted by $\\pm 1$ to create space, and secret data bits are embedded into the peak pixels.
3. **Payload Encryption:** The patient records are encrypted with a user-defined secret key prior to embedding, ensuring secondary confidentiality.
4. **Lossless Recovery:** The receiving system extracts the secret records, decrypts the text, and reverses the pixel shifts, returning the scan to its exact original state (Mean Squared Error $\\text{MSE} = 0$, $\\text{PSNR} = \\infty$).

---

## 6. System Architecture & Workflow

```
[Patient Data] ---> [Key-based Encryption] ---> [Encrypted Bitstream]
                                                        |
                                                        v
[Original Scan] ---> [Split into N x N Blocks] ---> [Block Histogram Shifting & Embedding]
                                                        |
                                                        v
                                                 [Stego Medical Scan]
                                                        |
                                       (Transmission / Cloud Storage)
                                                        |
                                                        v
                                             [Extraction & Reversal]
                                             /                     \\
                                            v                       v
                         [Decrypted Patient Record]     [Restored Original Scan]
                                                       (Bit-for-bit exact match)
```

---

## 7. Objectives
* Implement block-wise histogram shifting for grayscale medical imagery in Python.
* Guarantee 100% mathematical reversibility (lossless recovery where original and recovered images are identical).
* Integrate password-protected payload encryption.
* Measure and benchmark performance using quantitative metrics:
  * **PSNR (Peak Signal-to-Noise Ratio)** - verifying visual quality of the stego image (>52 dB).
  * **SSIM (Structural Similarity Index)** - verifying structural preservation (>0.99).
  * **MSE (Mean Squared Error)** - proving $\\text{MSE} = 0$ between original and recovered scans.
  * **Embedding Capacity (bits per pixel / bpp)** across different block sizes.
* Build an intuitive interface (Streamlit) for uploading scans, embedding patient notes, and verifying image restoration.

---

## 8. Hardware & Software Requirements

### Software Environment:
* **Operating System:** Linux / Windows / macOS
* **Language:** Python 3.10+ (tested on Python 3.14)
* **Key Libraries:** 
  * `NumPy`: Matrix calculations, block partitioning, and histogram shifting.
  * `OpenCV` / `Pillow`: Image reading, grayscale conversion, and saving.
  * `Matplotlib`: Visualizing pixel histograms before and after embedding.
  * `Cryptography`: Encrypting confidential patient records.
  * `Streamlit`: Web dashboard for interactive demonstrations.

### Hardware Environment:
* Standard personal computer (Dual-core CPU or higher, 4 GB RAM, no GPU required).

---

## 9. Expected Outcomes
* A fully working Python implementation of block-wise reversible data hiding.
* Experimental proof that patient records can be hidden without leaving any permanent mark on the medical scan.
* An interactive demonstration app suitable for project presentation and viva evaluation.
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"Markdown synopsis written to {filepath}")

def create_docx_synopsis(filepath):
    doc = Document()

    # Set page margins (1 inch)
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Styles helper
    def add_title(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(18)
        run.font.name = 'Calibri'
        run.font.color.rgb = RGBColor(26, 54, 93) # Dark Navy
        p.paragraph_format.space_after = Pt(4)
        return p

    def add_subtitle(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(text)
        run.font.size = Pt(13)
        run.font.name = 'Calibri'
        run.italic = True
        run.font.color.rgb = RGBColor(74, 85, 104)
        p.paragraph_format.space_after = Pt(18)
        return p

    def add_heading1(text):
        p = doc.add_paragraph()
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(14)
        run.font.name = 'Calibri'
        run.font.color.rgb = RGBColor(26, 54, 93)
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        return p

    def add_body(text, bold_prefix=None, italic=False):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            run_b = p.add_run(bold_prefix)
            run_b.bold = True
            run_b.font.size = Pt(11)
            run_b.font.name = 'Calibri'
        run = p.add_run(text)
        run.italic = italic
        run.font.size = Pt(11)
        run.font.name = 'Calibri'
        run.font.color.rgb = RGBColor(45, 55, 72)
        return p

    def add_bullet(text, bold_prefix=None):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            run_b = p.add_run(bold_prefix)
            run_b.bold = True
            run_b.font.size = Pt(11)
            run_b.font.name = 'Calibri'
        run = p.add_run(text)
        run.font.size = Pt(11)
        run.font.name = 'Calibri'
        run.font.color.rgb = RGBColor(45, 55, 72)
        return p

    # --- Title Section ---
    add_title("PROJECT SYNOPSIS")
    add_subtitle("A 3rd-Year Undergraduate Project Proposal")

    # --- 1. Project Title ---
    add_heading1("1. Project Title")
    add_body("Secure Reversible Data Hiding in Medical Images Using Block-Wise Histogram Shifting")

    # --- 2. Base Research Reference ---
    add_heading1("2. Base Research Literature")
    table = doc.add_table(rows=4, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = True
    
    headers = [
        ("Base Paper Title", "Secure Reversible Data Hiding Using Block-Wise Histogram Shifting"),
        ("Authors", "Samar Kamil Khudhair, Monalisa Sahu, Raghunandan K. R., Aditya Kumar Sahu"),
        ("Journal & Year", "MDPI Electronics, Vol. 12, Issue 5, Article 1222 (March 2023)"),
        ("Foundational Work", "Reversible Data Hiding by Z. Ni, Y. Shi, N. Ansari, W. Su (IEEE T-CSVT, 2006)")
    ]

    for idx, (label, val) in enumerate(headers):
        cell_lbl = table.cell(idx, 0)
        cell_val = table.cell(idx, 1)
        set_cell_background(cell_lbl, "E2E8F0")
        
        p_l = cell_lbl.paragraphs[0]
        r_l = p_l.add_run(label)
        r_l.bold = True
        r_l.font.size = Pt(10)
        r_l.font.name = 'Calibri'

        p_v = cell_val.paragraphs[0]
        r_v = p_v.add_run(val)
        r_v.font.size = Pt(10)
        r_v.font.name = 'Calibri'

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # --- 3. Introduction & Background ---
    add_heading1("3. Introduction & Context")
    add_body(
        "Modern healthcare facilities and telemedicine platforms routinely exchange digital medical images "
        "such as X-rays, MRI scans, and ultrasound files over internet channels and cloud archives. Alongside the "
        "imaging data, confidential patient records (such as patient names, identification numbers, and diagnostic notes) "
        "must be securely conveyed to attending physicians."
    )
    add_body(
        "Standard steganography techniques embed data by permanently altering pixel values. While minor alterations "
        "remain imperceptible in ordinary photography, modifying pixels in diagnostic scans introduces unacceptable hazards: "
        "even small pixel variations can be mistaken for lesions, obscure real fractures, or invalidate forensic evidence. "
        "Reversible Data Hiding (RDH) addresses this challenge by ensuring that once the secret data is extracted, the host scan "
        "is restored to its exact, untouched original state with zero permanent distortion (MSE = 0)."
    )

    # --- 4. Problem Statement ---
    add_heading1("4. Problem Statement")
    add_bullet(" Diagnostic scans require strict pixel fidelity. Standard steganographic methods cause irreversible distortion, violating healthcare guidelines and diagnostic trust.", bold_prefix="Irreversible Image Degradation:")
    add_bullet(" Traditional global histogram shifting treats the entire image as one unit, which limits embedding capacity and creates uneven visual distortion across textured regions.", bold_prefix="Capacity Constraints in Global Methods:")
    add_bullet(" Hiding plaintext patient records without an independent encryption key creates a privacy vulnerability if an eavesdropper reverses the embedding algorithm.", bold_prefix="Single-Layer Security Risk:")

    # --- 5. Proposed Solution & Methodology ---
    add_heading1("5. Proposed Methodology")
    add_body(
        "This project implements a localized block-wise histogram shifting technique based on recent research, enhanced "
        "with key-based payload encryption to ensure both visual reversibility and data confidentiality:"
    )
    add_bullet(" The grayscale medical image is divided into small, non-overlapping blocks (e.g., 8×8 or 16×16). Utilizing localized blocks takes advantage of high spatial pixel correlation in neighboring regions.", bold_prefix="1. Block Partitioning:")
    add_bullet(" In each block, a local histogram is generated to identify the peak bin (most frequent pixel value) and the minimum/zero bin. Intermediate pixel values are shifted by ±1 to create vacant space.", bold_prefix="2. Histogram Shifting:")
    add_bullet(" Secret patient records are encrypted using a secret key and embedded into the peak pixels of the shifted blocks.", bold_prefix="3. Payload Encryption & Embedding:")
    add_bullet(" The recipient extracts the secret bits, decrypts the message using the secret key, and reverses the pixel shifts (shifting by ∓1). The original medical scan is restored bit-for-bit with 100% fidelity.", bold_prefix="4. Lossless Restoration:")

    # --- 6. Objectives ---
    add_heading1("6. Key Project Objectives")
    add_bullet("Develop a modular Python implementation of block-wise reversible data hiding.")
    add_bullet("Guarantee mathematically proven lossless recovery (Mean Squared Error = 0, PSNR = ∞ between original and restored images).")
    add_bullet("Incorporate password-protected payload encryption before embedding.")
    add_bullet("Evaluate visual fidelity using standard benchmarks: PSNR (>52 dB) and SSIM (>0.99) for the stego image.")
    add_bullet("Create an interactive user interface (Streamlit) for straightforward demonstration during project viva and reviews.")

    # --- 7. Tools & Implementation Stack ---
    add_heading1("7. Tools & Technologies")
    table2 = doc.add_table(rows=5, cols=2)
    table2.alignment = WD_TABLE_ALIGNMENT.CENTER
    table2.autofit = True
    
    tech_stack = [
        ("Language & Environment", "Python 3.14 (Virtual Environment)"),
        ("Core Computing", "NumPy (array operations, block partitioning, histogram shifts)"),
        ("Image Processing", "OpenCV / Pillow (grayscale conversion, image I/O)"),
        ("Security & Cryptography", "Cryptography / hashlib (AES / password key derivation)"),
        ("Evaluation & UI", "Matplotlib (histogram visualizer) & Streamlit (interactive web UI)")
    ]

    for idx, (label, val) in enumerate(tech_stack):
        c_lbl = table2.cell(idx, 0)
        c_val = table2.cell(idx, 1)
        set_cell_background(c_lbl, "EDF2F7")
        
        p_l = c_lbl.paragraphs[0]
        r_l = p_l.add_run(label)
        r_l.bold = True
        r_l.font.size = Pt(10)
        r_l.font.name = 'Calibri'

        p_v = c_val.paragraphs[0]
        r_v = p_v.add_run(val)
        r_v.font.size = Pt(10)
        r_v.font.name = 'Calibri'

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # --- 8. Expected Outcomes ---
    add_heading1("8. Expected Outcomes & Deliverables")
    add_bullet("A working software application that successfully embeds patient notes into medical scans and extracts them with 100% image restoration.")
    add_bullet("Comprehensive test scripts verifying that original and reconstructed arrays are identical (np.array_equal == True).")
    add_bullet("Demonstration dashboard displaying before-and-after histograms, PSNR/SSIM metrics, and extracted plaintext.")

    doc.save(filepath)
    print(f"Word document synopsis saved to {filepath}")

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def create_pdf_synopsis(filepath):
    doc = SimpleDocTemplate(filepath, pagesize=letter, rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54)
    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#1A365D'),
        alignment=1, # Center
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#4A5568'),
        alignment=1,
        spaceAfter=15
    )
    h1_style = ParagraphStyle(
        'DocH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#1A365D'),
        spaceBefore=10,
        spaceAfter=4
    )
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#2D3748'),
        spaceAfter=6
    )
    bullet_style = ParagraphStyle(
        'DocBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#2D3748'),
        leftIndent=15,
        spaceAfter=4
    )

    story.append(Paragraph("PROJECT SYNOPSIS", title_style))
    story.append(Paragraph("A 3rd-Year Undergraduate Project Proposal", subtitle_style))

    story.append(Paragraph("1. Project Title", h1_style))
    story.append(Paragraph("<b>Secure Reversible Data Hiding in Medical Images Using Block-Wise Histogram Shifting</b>", body_style))

    story.append(Paragraph("2. Base Research Literature", h1_style))
    ref_data = [
        [Paragraph("<b>Base Paper Title</b>", body_style), Paragraph("Secure Reversible Data Hiding Using Block-Wise Histogram Shifting", body_style)],
        [Paragraph("<b>Authors</b>", body_style), Paragraph("Samar Kamil Khudhair, Monalisa Sahu, Raghunandan K. R., Aditya Kumar Sahu", body_style)],
        [Paragraph("<b>Journal & Year</b>", body_style), Paragraph("MDPI Electronics, Vol. 12, Issue 5, Article 1222 (March 2023)", body_style)],
        [Paragraph("<b>Foundational Work</b>", body_style), Paragraph("Reversible Data Hiding by Z. Ni et al. (IEEE T-CSVT, 2006)", body_style)]
    ]
    t = Table(ref_data, colWidths=[150, 350])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#E2E8F0')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))

    story.append(Paragraph("3. Introduction & Context", h1_style))
    story.append(Paragraph("Modern telemedicine platforms frequently transmit digital medical images (X-rays, MRIs, CT scans) across public networks and cloud servers. Alongside these scans, confidential patient records (identity, diagnostic notes, case history) must be securely sent to attending physicians.", body_style))
    story.append(Paragraph("Standard steganography methods permanently change pixel values. In medical diagnostics, even slight pixel modifications can be mistaken for lesions or obscure fractures, introducing legal and health risks. Reversible Data Hiding (RDH) solves this: it embeds confidential patient records inside the scan and, upon extraction, restores the scan back to its exact, untouched original state with zero permanent distortion (MSE = 0).", body_style))

    story.append(Paragraph("4. Problem Statement", h1_style))
    story.append(Paragraph("• <b>Irreversible Image Degradation:</b> Standard methods permanently alter pixels, violating medical guidelines and diagnostic trust.", bullet_style))
    story.append(Paragraph("• <b>Capacity Constraints in Global Methods:</b> Traditional global histogram shifting treats the whole image as one unit, limiting embedding capacity.", bullet_style))
    story.append(Paragraph("• <b>Single-Layer Security Risk:</b> Hiding plaintext data without encryption leaves information vulnerable if the embedding is reversed.", bullet_style))

    story.append(Paragraph("5. Proposed Methodology", h1_style))
    story.append(Paragraph("• <b>1. Block Partitioning:</b> The grayscale medical scan is divided into small, non-overlapping blocks (8×8 or 16×16) to leverage localized pixel correlation.", bullet_style))
    story.append(Paragraph("• <b>2. Histogram Shifting:</b> In each block, the algorithm identifies the peak bin and shifts intermediate pixels by ±1 to create space.", bullet_style))
    story.append(Paragraph("• <b>3. Payload Encryption & Embedding:</b> Patient notes are encrypted with a secret key and embedded into the peak pixels.", bullet_style))
    story.append(Paragraph("• <b>4. Lossless Restoration:</b> The recipient extracts the secret bits, decrypts the message, and reverses the pixel shifts (∓1), restoring the original image bit-for-bit.", bullet_style))

    story.append(Paragraph("6. Key Project Objectives", h1_style))
    story.append(Paragraph("• Develop a modular Python implementation of block-wise reversible data hiding.", bullet_style))
    story.append(Paragraph("• Guarantee mathematically proven lossless recovery (MSE = 0, PSNR = ∞ between original and restored images).", bullet_style))
    story.append(Paragraph("• Evaluate visual fidelity using standard benchmarks: PSNR (>52 dB) and SSIM (>0.99) for the stego image.", bullet_style))
    story.append(Paragraph("• Provide an interactive demonstration interface (Streamlit) for straightforward viva presentation.", bullet_style))

    story.append(Paragraph("7. Expected Deliverables", h1_style))
    story.append(Paragraph("• Working Python program for block-wise embedding and extraction.", bullet_style))
    story.append(Paragraph("• Automated test script confirming 100% identical image restoration (np.array_equal == True).", bullet_style))
    story.append(Paragraph("• Demonstration dashboard displaying before/after histograms and evaluation metrics.", bullet_style))

    doc.build(story)
    print(f"PDF synopsis saved to {filepath}")

if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    md_path = os.path.join(out_dir, "Project_Synopsis.md")
    docx_path = os.path.join(out_dir, "Project_Synopsis.docx")
    pdf_path = os.path.join(out_dir, "Project_Synopsis.pdf")
    create_markdown_synopsis(md_path)
    create_docx_synopsis(docx_path)
    create_pdf_synopsis(pdf_path)

