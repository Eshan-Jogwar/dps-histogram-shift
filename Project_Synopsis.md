# PROJECT SYNOPSIS
## Implementation of Reversible Data Hiding in Images Using Histogram Shifting

* **Team Members:** Eshan Jogwar (BT24CSD012), Tushar Sign (BT24CSD001), Rudravignesh (BT24CSD019)
* **Course / Degree:** B.Tech (3rd Year, Semester VI)
* **Project Type:** Algorithm Implementation / Software Project
* **Language & Environment:** Python 3.14 (`.venv`)

---

### 1. Project Overview
The objective of this project is to develop a software implementation in Python for **Reversible Data Hiding (RDH)** using the **Histogram Shifting** technique. 

In standard steganography (such as LSB substitution), embedding a secret message permanently alters the pixels of the host image. However, in sensitive applications like medical scans (X-rays, MRIs) and legal evidence, permanent modification of pixel values is unacceptable. Reversible data hiding solves this practical problem: it allows secret text (such as patient IDs or diagnostic notes) to be embedded directly into an image, and after extraction at the receiving end, the original host image is **completely restored bit-for-bit** with zero permanent distortion (MSE = 0).

---

### 2. Base Paper Reference
This project implements the method described in the following published literature:
* **Reference Paper:** S. K. Khudhair, M. Sahu, R. K. R., and A. K. Sahu, *"Secure Reversible Data Hiding Using Block-Wise Histogram Shifting,"* MDPI Electronics, vol. 12, no. 5, art. 1222, March 2023.
* **Foundational Algorithm:** Z. Ni, Y.-Q. Shi, N. Ansari, and W. Su, *"Reversible Data Hiding,"* IEEE Transactions on Circuits and Systems for Video Technology, vol. 16, no. 3, 2006.

---

### 3. Algorithm & Working Principle
The implementation divides the image into localized blocks (e.g., $8 \times 8$ or $16 \times 16$) to exploit local pixel correlation, following the standard four-step procedure:
1. **Histogram Calculation:** Read the grayscale image and compute the local histogram for each block to identify the **peak pixel value** $P$ (most frequent value) and the **zero/minimum value** $Z$.
2. **Histogram Shifting:** Assuming $P < Z$, all pixel values strictly between $P$ and $Z$ are shifted by $+1$ ($I'(x,y) = I(x,y) + 1$), opening up an empty bin immediately adjacent to $P$.
3. **Data Embedding:** Iterate over the image pixels. When a pixel with value $P$ is encountered, embed a secret bit $b \in \{0, 1\}$: if $b = 1$, the pixel value becomes $P+1$; if $b = 0$, it remains $P$.
4. **Extraction & Image Restoration:** The receiver inspects pixels with values $P$ and $P+1$ to extract the binary message. Then, pixels in the range $(P, Z]$ are shifted backwards by $-1$, returning every pixel to its exact original value.

---

### 4. Software Modules to be Implemented
1. **Module 1 (Payload Encoder):** Converts input text into a bitstream, with an optional password-based XOR scrambling key for basic payload privacy.
2. **Module 2 (Image Preprocessing & Blocking):** Loads grayscale images (PNG/BMP/TIFF) and segments them into configurable $N \times N$ spatial blocks using NumPy.
3. **Module 3 (Embedding & Extraction Engine):** Executes the block-wise histogram shifting and reversible extraction routines.
4. **Module 4 (Verification & Quality Metrics):** Automatically computes Peak Signal-to-Noise Ratio (PSNR), Structural Similarity (SSIM), and Mean Squared Error (MSE) between the original and restored image to verify 100% lossless recovery (MSE = 0).
5. **Module 5 (User Interface):** A lightweight interactive web dashboard (built with Streamlit) where a user can upload an image, type a secret note, download the stego image, and test one-click extraction and recovery.

---

### 5. Tools & Technologies
* **Programming Language:** Python 3.14 (Virtual Environment `.venv`)
* **Core Libraries:** NumPy (matrix operations and histogram calculation), OpenCV / Pillow (image I/O)
* **Visualization & UI:** Matplotlib (histogram distribution plots), Streamlit (web-based GUI)

---

### 6. Expected Project Deliverables
1. A complete, working Python implementation of block-wise histogram shifting data hiding.
2. Test script demonstrating that the recovered image is 100% identical to the original image ($\text{MSE} = 0$).
3. A user-friendly web interface for live project demonstration during lab/viva evaluation.