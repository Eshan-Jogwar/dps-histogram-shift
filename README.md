# Reversible Data Hiding (RDH) in Images Using Histogram Shifting

**Course:** B.Tech 3rd Year Term Project  
**Team Members:** 
* Eshan Jogwar (BT24CSD012)
* Tushar Sign (BT24CSD001)
* Rudravignesh (BT24CSD019)  
**Base Research Paper:** *Secure Reversible Data Hiding Using Block-Wise Histogram Shifting*, MDPI Electronics (March 2023) / Foundational IEEE T-CSVT (2006).

---

## ⚡ Quick Start (How to Run Tomorrow for the Professor)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```
*(For complete setup instructions across Linux, Windows, and Mac, see [HOW_TO_RUN.md](HOW_TO_RUN.md))*

### 2. Launch the Desktop GUI
Run the launcher script:
```bash
.venv/bin/python run_gui.py
```
*(Or activate your virtual environment: `source .venv/bin/activate` and run `python run_gui.py`)*

### 3. Run the Terminal Validation Suite
To show raw terminal benchmarks and mathematical proofs:
```bash
.venv/bin/python test_rdh.py
```

---

## 👨‍🏫 60-Second Demo Script for the Professor

When presenting to your professor, follow these 3 effortless steps on the **"⭐ 1-Click Professor Demo"** screen:

1. **Step 1: Select a Preset Scan**
   * Click **`🧠 Brain MRI`**, **`🫁 Chest X-Ray`**, or **`🦵 Knee Joint`**.
   * The scan and sample patient diagnosis record will immediately load.
2. **Step 2: Click the Green Run Button**
   * Click **`▶ RUN FULL DEMO (Embed & Lossless Extract)`**.
3. **Step 3: Point to the Results on Screen:**
   * **Side-by-Side Images:** Show that the Stego image looks identical to the Original image ($\text{PSNR} > 50\text{ dB}$, $\text{SSIM} > 0.999$).
   * **Big Green Banner:** Point out:
     > `✓ 100% LOSSLESS RECOVERY CONFIRMED: MSE = 0.000000 | Restored PSNR = ∞`
   * **Extracted Record:** Show that the extracted patient record matches the original text bit-for-bit.
   * **Stored Output:** Point out that the stego image is automatically saved in [`encoded/`](encoded/).
   * *(Bonus if asked how it works)*: Switch to the **`📊 Histogram Analysis`** tab to show the green **Peak Bin ($P$)** and red **Zero Bin ($Z$)** and explain that intermediate pixels are shifted by $+1$ to make room for the secret data, and shifted back by $-1$ on recovery.

---

## 📁 Project Architecture

```
dps/
├── implementation/
│   ├── rdh_core.py          # Core Histogram Shifting algorithm (Ni et al. & Block-wise)
│   ├── crypto_utils.py      # Secret key / password stream encryption (AES-GCM / PBKDF2)
│   ├── metrics.py           # Fidelity calculations: MSE (=0), PSNR, SSIM, and exact match
│   ├── generate_samples.py  # Script generating synthetic realistic medical scans
│   └── app_gui.py           # Tkinter Graphical User Interface
├── sample_images/           # Test medical scans (brain_mri.png, chest_xray.png, knee_scan.png)
├── encoded/                 # Destination folder storing stego objects (.png) & metadata (.json)
├── run_gui.py               # Main launcher script for the Tkinter desktop app
├── test_rdh.py              # Automated test suite proving 100% losslessness
├── synopsis.tex             # 1-page LaTeX synopsis source
└── synopsis.pdf             # Compiled 1-page PDF synopsis
```
