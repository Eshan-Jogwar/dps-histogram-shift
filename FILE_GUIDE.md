# Project File Guide

This document provides a detailed breakdown of every directory and file in the codebase, explaining their purpose, key functions, and role in the Reversible Data Hiding (RDH) pipeline.

---

## Directory Overview

```
dps/
├── implementation/             # Core algorithmic modules, cryptography, metrics, and GUI
├── sample_images/              # Clinical test scans (Brain MRI, Chest X-ray, Knee Joint)
├── encoded/                    # Output directory storing generated stego images and metadata
├── run_gui.py                  # Primary entry point to launch the Tkinter desktop application
├── test_rdh.py                 # Automated test suite validating 100% lossless restoration
├── requirements.txt            # Python package dependencies
├── .gitignore                  # Git ignore rules for caches, builds, and virtual environments
├── README.md                   # Project overview, presentation guide, and quick start
├── HOW_TO_RUN.md               # Detailed installation and execution instructions across operating systems
├── HOW_IT_WORKS.md             # Plain-language algorithmic explanation and cryptographic details
├── FILE_GUIDE.md               # This document: architectural breakdown of all codebase components
├── synopsis.tex                # 1-page academic LaTeX project synopsis source
├── synopsis.pdf                # Compiled 1-page PDF synopsis
├── generate_synopsis.py        # Python utility script used to generate DOCX, PDF, and MD synopses
├── Project_Synopsis.docx       # Word document version of the project synopsis
├── Project_Synopsis.md         # Markdown version of the project synopsis
└── Project_Synopsis.pdf        # Standalone ReportLab PDF generated during early planning
```

---

## Implementation Package (`implementation/`)

### 1. `implementation/rdh_core.py`
The core engine implementing Reversible Data Hiding via Histogram Shifting.
* **Purpose:** Performs pixel histogram analysis, intermediate bin shifting, secret bit modulation, extraction, and exact inverse unshifting.
* **Key Functions:**
  * `find_peak_and_zero_bins(image_array)`: Calculates the 256-bin pixel histogram to determine the Peak bin (most frequent pixel value) and the Zero/minimum bin (closest empty or least populated bin).
  * `embed_global_histogram_shifting(cover_image, secret_bits)`: Shifts pixels between Peak and Zero by +1 (or -1) and embeds binary data into the Peak pixels. Returns the stego image and metadata.
  * `extract_and_restore_global(stego_image, meta)`: Reads the hidden bits from the modified pixels and shifts the remaining pixels backwards by -1 (or +1) to restore the exact original image array.
  * `bytes_to_bits(data)` and `bits_to_bytes(bits)`: Helper utilities converting raw byte arrays to lists of binary bits (0 and 1) and vice versa.
  * `save_stego_object(stego_array, meta, output_path)`: Writes the stego image as a lossless PNG and writes companion parameters to a JSON file in `encoded/`.
  * `load_stego_object(stego_path)`: Loads a stego PNG image and automatically parses its companion metadata JSON.

### 2. `implementation/crypto_utils.py`
The cryptographic security module providing secondary confidentiality for embedded payloads.
* **Purpose:** Ensures patient records are protected against unauthorized inspection if the steganographic hiding is reversed.
* **Key Functions:**
  * `encrypt_payload(plaintext, password)`: If a password is provided, derives a 256-bit key using PBKDF2-HMAC-SHA256 (10,000 iterations and a 16-byte random salt) and encrypts the plaintext with AES-GCM (authenticated encryption). If no password is provided, returns UTF-8 encoded bytes.
  * `decrypt_payload(payload_bytes, password)`: Identifies encrypted headers, reconstructs the key from the salt and password, and decrypts the ciphertext. Raises a descriptive error if the password is incorrect or if the ciphertext is tampered with.

### 3. `implementation/metrics.py`
The numerical quality and verification module.
* **Purpose:** Measures visual fidelity between images and provides mathematical proof of reversibility.
* **Key Functions:**
  * `calculate_mse(img1, img2)`: Computes the Mean Squared Error between two image arrays.
  * `calculate_psnr(img1, img2)`: Computes Peak Signal-to-Noise Ratio in decibels (dB). Returns infinity (`inf`) when MSE is 0.0.
  * `calculate_ssim(img1, img2)`: Implements the Structural Similarity Index metric (Wang et al.), returning a score between 0.0 and 1.0 (where 1.0 indicates identical structural correlation).
  * `verify_losslessness(original, restored)`: Validates that `np.array_equal(original, restored)` is strictly True, confirming bit-for-bit losslessness.

### 4. `implementation/generate_samples.py`
Synthetic clinical image generation tool.
* **Purpose:** Generates realistic, standardized 512x512 8-bit grayscale medical images with natural tissue gradients for offline demonstration.
* **Key Functions:**
  * `generate_brain_mri(size)`: Synthesizes an axial brain MRI slice featuring skull bone contours, soft tissue parenchyma, ventricles, and scanner noise.
  * `generate_chest_xray(size)`: Synthesizes an anterior-posterior chest radiograph with thoracic cage, lung cavities, cardiac silhouette, spine, and rib shadows.
  * `generate_knee_scan(size)`: Synthesizes a joint radiograph with femur, tibia, patella, and cartilage joint space.
  * `main()`: Generates and saves all three scans to the `sample_images/` folder.

### 5. `implementation/app_gui.py`
The graphical user interface built with Python's standard `tkinter` and `ttk` library.
* **Purpose:** Provides an interactive demonstration tool for evaluation and viva reviews.
* **Key Components:**
  * **1-Click Professor Demo Tab:** Displays Original, Stego, and Restored images side by side on a single screen with quick preset buttons, an instant run button, and a prominent lossless verification banner.
  * **Step 1: Embed Tab:** Independent interface allowing custom image selection, arbitrary secret message input, optional password entry, and saving to `encoded/`.
  * **Step 2: Extract & Restore Tab:** Independent interface for loading stego images from `encoded/`, entering decryption keys, extracting plaintext, and verifying against the original.
  * **Histogram Analysis Tab:** Embedded Matplotlib canvas plotting the Original and Stego histograms, highlighting the Peak bin and Zero bin to visually demonstrate the shift operation.

---

## Root Scripts and Execution Entry Points

### 1. `run_gui.py`
* **Purpose:** Main launcher script for the desktop graphical user interface.
* **Usage:** `python run_gui.py` or `.venv/bin/python run_gui.py`.

### 2. `test_rdh.py`
* **Purpose:** Standalone automated terminal validation suite.
* **Behavior:** Automatically iterates over all three sample scans, embeds encrypted and plaintext payloads, saves stego objects to `encoded/`, extracts the payloads, unshifts the pixels, and prints an evaluation table proving `MSE = 0.000000` and `Restored PSNR = inf`.
* **Usage:** `python test_rdh.py` or `.venv/bin/python test_rdh.py`.

---

## Data and Storage Folders

### 1. `sample_images/`
* Stores the baseline cover scans:
  * `brain_mri.png`: 512x512 grayscale axial brain MRI.
  * `chest_xray.png`: 512x512 grayscale chest radiograph.
  * `knee_scan.png`: 512x512 grayscale knee radiograph.
  * `.gitkeep`: Ensures the directory structure is maintained in version control.

### 2. `encoded/`
* Stores generated stego images and companion parameter files:
  * `stego_<name>.png`: The carrier image containing the embedded payload.
  * `stego_<name>_meta.json`: Parameter file containing Peak bin, Zero bin, shift direction, and bit count required for extraction.
  * `.gitkeep`: Ensures the output directory is tracked in Git.

---

## Documentation and Academic Deliverables

### 1. `README.md`
Project landing page containing team details, research citations, quick-start commands, presentation steps for evaluators, and project architecture.

### 2. `HOW_TO_RUN.md`
Detailed operational guide covering virtual environment setup, pip dependencies, system prerequisites (such as `python3-tk` on Linux), and execution commands.

### 3. `HOW_IT_WORKS.md`
Plain-language technical explanation of the histogram shifting algorithm using the bookshelf analogy, ASCII histogram plots, Mermaid process flowcharts, and the PBKDF2/AES-GCM encryption architecture.

### 4. `FILE_GUIDE.md`
This reference guide describing the functional purpose and responsibilities of every file in the repository.

### 5. `synopsis.tex` & `synopsis.pdf`
The official 1-page academic project synopsis written in LaTeX and compiled via Tectonic. Formatted for third-year undergraduate project review.

### 6. `requirements.txt`
Package specification pinning core dependencies: `numpy`, `pillow`, `matplotlib`, and `cryptography`.

### 7. `.gitignore`
Excludes virtual environment folders (`.venv`), Python cache directories (`__pycache__`), intermediate build artifacts, and operating system metadata.
