# How to Run the Project

This guide provides step-by-step instructions to set up and run the **Reversible Data Hiding (RDH)** project on any system.

---

## 1. Quick Launch (Current Environment)

If you are already in the project folder with the `.venv` installed:

### To launch the Tkinter GUI:
```bash
.venv/bin/python run_gui.py
```
*(Or if your virtual environment is active: `python run_gui.py`)*

### To run the automated verification suite:
```bash
.venv/bin/python test_rdh.py
```

---

## 2. Setup on a New Machine (Fresh Clone / Other Computer)

### Step 1: Create and Activate a Virtual Environment
```bash
# Linux / macOS:
python3 -m venv .venv
source .venv/bin/activate

# Windows (PowerShell):
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### Step 2: Install Required Dependencies
```bash
pip install -r requirements.txt
```

> **Note for Linux Users:**  
> On some Linux distributions (Ubuntu/Debian), Tkinter is packaged separately by the OS. If `import tkinter` is missing, install it using:
> ```bash
> sudo apt-get update && sudo apt-get install -y python3-tk
> ```
> *(On Windows and macOS, Tkinter is bundled with Python by default).*

### Step 3: (Optional) Generate Sample Medical Images
If you want to regenerate fresh 512x512 clinical test scans (`brain_mri.png`, `chest_xray.png`, `knee_scan.png`):
```bash
python implementation/generate_samples.py
```

---

## 3. How to Present to the Professor (60-Second Demo)

1. Run the GUI:
   ```bash
   python run_gui.py
   ```
2. On the **"1-Click Professor Demo"** tab:
   * Click **`Brain MRI`** (or **`Chest X-Ray`**).
   * Click **`RUN FULL DEMO (Embed & Lossless Extract)`**.
3. Point out the 3 key results:
   * **Side-by-side view:** Original vs Stego vs Restored scan (PSNR > 50 dB, SSIM > 0.999).
   * **Verification Banner:** `100% LOSSLESS RECOVERY CONFIRMED: MSE = 0.000000 | Restored PSNR = infinity`.
   * **Extracted Record:** Shows the exact confidential medical record restored without error.
4. *(Optional)* Switch to the **`Histogram Analysis`** tab to show the green Peak bin and red Zero bin shift.

---

## 4. Output Storage

* All stego images and their parameter files are stored in the [`encoded/`](encoded/) directory as:
  * `encoded/stego_<image_name>.png` (Lossless PNG format)
  * `encoded/stego_<image_name>_meta.json` (Companion parameters for blind extraction)
